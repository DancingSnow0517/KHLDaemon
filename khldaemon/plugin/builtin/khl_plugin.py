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
    bot = interface.bot

    interface.registry_help_messages('!!help', '显示帮助信息')
    interface.registry_help_messages('!!khl', '显示机器人信息')

    @bot.command(name='help', prefixes=['!!'])
    async def help_msg(msg: Message):
        help_messages = ''
        for i in interface.plugin_manager.help_messages:
            help_messages += f'[{i}] {interface.plugin_manager.help_messages[i]}\n'
        await msg.reply(help_messages)

    @bot.command(name='khl', prefixes=['!!'])
    async def khl(msg: Message):
        rt = f'当前已加载 {len(interface.plugin_manager.plugins)} 个插件'
        await msg.reply(rt)


def on_unload(interface: PluginInterface):
    pass


async def on_message(interface: MessageInterface):
    pass
