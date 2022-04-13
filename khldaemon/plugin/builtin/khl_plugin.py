from khl import Message

from khldaemon.plugin.interface import PluginInterface, MessageInterface

PLUGIN_METADATA = {
    'id': 'khl_plugin',
    'version': '1.0.0',
    'name': 'KHLDaemon',
    'description': 'A khl.py builtin plugin',
    'author': 'DancingSnow',
    'link': 'https://github.com/DancingSnow0517/KHLDaemon'
}


def on_load(interface: PluginInterface):
    interface.registry_help_messages('!!help', '显示帮助信息')
    interface.registry_help_messages('!!KHLD', '显示机器人信息')






def on_unload(interface: PluginInterface):
    pass


async def on_message(interface: MessageInterface):
    pass
