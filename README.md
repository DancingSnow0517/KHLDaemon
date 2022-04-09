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
from khl import Message

from khl.plugin.plugin_interface import PluginInterface

# plugin meta
PLUGIN_METADATA = {
    'id': 'test_plugin',
    'version': '1.0.0',
    'name': 'Test Plugin',
    'description': 'A test plugin',
    'author': 'DancingSnow',
    'link': 'https://github.com/DancingSnow0517/khl.py/tree/plugin'
}


# run when bot start
def on_load(interface: PluginInterface):
    interface.logger.info('plugin loaded')
    bot = interface.bot

    @bot.command(name='test')
    async def test(msg: Message):
        await msg.reply('test')


# run when bot stop
def on_unload(interface: PluginInterface):
    interface.logger.info('plugin unloaded')


# run when a message is received
async def on_message(msg: Message):
    print(msg.content)
    
```