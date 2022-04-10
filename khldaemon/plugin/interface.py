from typing import TYPE_CHECKING

from khl import Message

from ..utils.logger import ColoredLogger

if TYPE_CHECKING:
    from .plugin_manager import PluginManager


class Interface:
    def __init__(self, plg_manager: 'PluginManager', plugin_id: str) -> None:
        self.plugin_manager = plg_manager
        self.plugin_id = plugin_id
        self.config = self.plugin_manager.config
        self.bot = self.plugin_manager.bot
        self.logger = ColoredLogger(level=self.config.log_level, plugin_id=self.plugin_id)


class PluginInterface(Interface):

    def registry_help_messages(self, prefix: str, desc: str):
        self.plugin_manager.help_messages[prefix] = desc


class MessageInterface(Interface):

    def __init__(self, plg_manager: 'PluginManager', plugin_id: str, msg: Message) -> None:
        super().__init__(plg_manager, plugin_id)
        self.message = msg
