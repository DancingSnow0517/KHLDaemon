import json
import os.path
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

from khl import Message, Event

from ..command.builder.nodes.basic import Literal
from ..utils.logger import ColoredLogger
from ..utils.serializer import Serializable

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer

SerializableType = TypeVar('SerializableType')


class Interface:
    def __init__(self, khld_server: 'KHLDaemonServer', plugin_id: str) -> None:
        self.khld_server = khld_server
        self.plugin_manager = self.khld_server.plugin_manager
        self.command_manger = self.khld_server.command_manager
        self.plugin_id = plugin_id
        self.config = self.plugin_manager.config
        self.logger = ColoredLogger(level=self.config.log_level, plugin_id=self.plugin_id)


class PluginInterface(Interface):

    def registry_help_messages(self, prefix: str, desc: str):
        self.plugin_manager.help_messages[prefix] = desc

    def register_command(self, literal: Literal):
        self.command_manger.register_command(literal)

    def load_config_simple(
            self, file_name='config.json', default_config: Optional = None, *, in_data_folder: bool = True,
            echo_in_console: bool = True, target_class: Optional[Type[SerializableType]] = None,
            encoding: str = 'utf8'
    ) -> Union[dict, SerializableType]:
        def log(msg):
            if echo_in_console:
                self.logger.info(msg)

        if target_class is not None:
            target_class: Serializable
            if default_config is None:
                default_config = target_class.get_default().serialize()
        config_file_path = os.path.join(self.get_data_folder(), file_name) if in_data_folder else file_name
        needs_save = False
        try:
            with open(config_file_path, encoding=encoding) as file_handle:
                read_data: dict = json.load(file_handle)
        except Exception as e:
            if default_config is not None:
                result_config = default_config.copy()
            else:
                raise e
            needs_save = True
            log('读取配置文件失败，使用默认值: {}'.format(e))
        else:
            result_config = read_data
            if default_config is not None:
                for key, value in default_config.items():
                    if key in read_data:
                        result_config[key] = read_data[key]
                    else:
                        result_config[key] = value
                        log(f'发现缺失的键 "{key}"，使用默认值"{value}"')
                        needs_save = True
            log('配置文件已加载')
        if target_class is not None:
            try:
                result_config = target_class.deserialize(result_config)
            except Exception as e:
                result_config = target_class.get_default()
                needs_save = True
                log('读取配置文件失败，使用默认值: {}'.format(e))
        else:
            if default_config is not None:
                for key in list(result_config.keys()):
                    if key not in default_config:
                        result_config.pop(key)
        if needs_save:
            self.save_config_simple(result_config, file_name=file_name, in_data_folder=in_data_folder)
        return result_config

    def get_data_folder(self) -> str:
        plugin_data_folder = os.path.join('config', self.plugin_id)
        if not os.path.isdir(plugin_data_folder):
            os.makedirs(plugin_data_folder)
        return plugin_data_folder

    def save_config_simple(
            self, config: Union[dict, Serializable], file_name: str = 'config.json', *, in_data_folder: bool = True,
            encoding: str = 'utf8'
    ) -> None:
        config_file_path = os.path.join(self.get_data_folder(), file_name) if in_data_folder else file_name
        if isinstance(config, Serializable):
            data = config.serialize()
        else:
            data = config
        target_folder = os.path.dirname(config_file_path)
        if len(target_folder) > 0 and not os.path.isdir(target_folder):
            os.makedirs(target_folder)
        with open(config_file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class MessageInterface(Interface):

    def __init__(self, khld_server: 'KHLDaemonServer', plugin_id: str, msg: Message) -> None:
        super().__init__(khld_server, plugin_id)
        self.message = msg


class EventInterface(Interface):

    def __init__(self, khld_server: 'KHLDaemonServer', plugin_id: str, event: Event) -> None:
        super().__init__(khld_server, plugin_id)
        self.event = event
