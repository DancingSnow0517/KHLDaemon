# KHLDaemon

一个基于 [TWT233](https://github.com/TWT233) 的 [khl.py](https://github.com/TWT233/khl.py) 的插件系统

## 安装

使用命令 ``pip install khldaemon`` 来安装

## 使用

使用命令 ``python -m khldaemon init`` 来初始化机器人

将会生成 ``plugin`` ``config`` 文件夹，以及 ``config.yml`` 配置文件

修改配置文件，填上你的开黑啦机器人的 ``token``

然后使用命令 ``python -m khldaemon start`` 启动机器人

## 样例插件

```python
from khldaemon.api.all import *
# or
# from khldaemon.api.interface import *
# from khldaemon.api.utils import *
# from khldaemon.api.command import *
# from khldaemon.api.types import  *

# plugin meta
PLUGIN_METADATA = {
    'id': 'test_plugin',
    'version': '1.0.0',
    'name': 'Test Plugin',
    'description': 'A test plugin',
    'author': 'DancingSnow',
    'link': 'https://github.com/DancingSnow0517/'
}


class Config(Serializable):
    config1: str = 'c1'
    config2: str = 'c1'
    config3: bool = False


config: Config


# run when bot start
def on_load(interface: PluginInterface):
    global config
    interface.logger.info('plugin loaded')

    interface.register_help_messages('!!hello', 'Hello World!')

    # register a command
    interface.register_command(
        Literal('!!hello').runs(lambda src: src.reply('world!'))
    )

    # config interface
    config = interface.load_config_simple(file_name='test_config.json', target_class=Config, in_data_folder=True)
    config.config1 = 't'
    interface.save_config_simple(config=config, file_name='test_config.json', in_data_folder=True)


# run when bot stop
def on_unload(interface: PluginInterface):
    interface.logger.info('plugin unloaded')


# run when a message is received
async def on_message(interface: MessageInterface):
    interface.logger.info(interface.message.content)


# run when an event is received
async def on_event(interface: EventInterface):
    interface.logger.info(interface.event.event_type)

```