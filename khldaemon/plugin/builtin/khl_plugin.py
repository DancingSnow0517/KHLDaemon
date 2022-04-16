from khl.card import CardMessage, Card, Module, Element, Types

from khldaemon.api.all import *
from khldaemon.constants import core_constant

PLUGIN_METADATA = {
    'id': 'khl_plugin',
    'version': '1.0.0',
    'name': 'KHLDaemon',
    'description': 'A khl.py builtin plugin',
    'author': 'DancingSnow',
    'link': 'https://github.com/DancingSnow0517/KHLDaemon'
}

khld_help_messages = '''[!!KHLD status] 显示 KHLDaemon 状态
[!!KHLD plugin] 显示插件相关的帮助信息
[!!KHLD reload] 显示重载相关的帮助信息'''

plugin_help_messages = '''[!!KHLD plugin list] 列出所有的插件
[!!KHLD plugin info <plugin_id>] 显示 id 为 <plugin_id> 插件的信息
[!!KHLD plugin reloadall] 重载所有插件'''

reload_help_messages = '''[!!KHLD reload plugin] 重载所有插件
[!!KHLD reload config] 重载配置文件
[!!KHLD reload all] 重载上述所有'''


def on_load(interface: PluginInterface):
    interface.register_help_messages('!!help', '显示帮助信息')
    interface.register_help_messages('!!KHLD', '显示机器人信息')

    interface.register_command(
        Literal('!!help').runs(print_help_messages)
    )
    interface.register_command(
        Literal('!!KHLD').
            runs(lambda src: src.reply(CardMessage(Card(Module.Header('KHLD 控制指令'), Module.Section(Element.Text(f'```\n{khld_help_messages}\n```', type=Types.Text.KMD)), theme=Types.Theme.SUCCESS)))).
            then(
            Literal('status').
                runs(show_khld_status)
        ).
            then(
            Literal({'plugin', 'plg'}).
                runs(lambda src: src.reply(CardMessage(Card(Module.Header('插件相关命令'), Module.Section(Element.Text(f'```\n{plugin_help_messages}\n```', type=Types.Text.KMD)), theme=Types.Theme.SUCCESS)))).
                then(
                Literal('list').runs(list_plugin)
            ).
                then(
                Literal('info').
                    then(
                    Text('plg_id').runs(info_plugin)
                )
            ).
                then(
                Literal({'reloadall', 'ra'}).runs(reload_plugin)
            )
        ).
            then(
            Literal({'reload', 'r'}).
                runs(lambda src: src.reply(CardMessage(Card(Module.Header('重载相关命令'), Module.Section(Element.Text(f'```\n{reload_help_messages}\n```', type=Types.Text.KMD)), theme=Types.Theme.SUCCESS)))).
                then(
                Literal({'plugin', 'plg'}).runs(reload_plugin)
            ).
                then(
                Literal({'config', 'cfg'}).runs(reload_config)
            ).
                then(
                Literal('all').runs(reload_all)
            )
        )
    )


def print_help_messages(source: UserCommandSource):
    cm = CardMessage()

    help_messages = source.khld_server.plugin_manager.help_messages
    msg = []
    enter = '\n'
    for prefix in help_messages:
        msg.append(f'[{prefix}] {help_messages[prefix]}')
    cm.append(Card(
        Module.Header('KHLD 指令帮助信息列表'),
        Module.Section(Element.Text(f'```\n{enter.join(msg)}\n```', type=Types.Text.KMD)), theme=Types.Theme.SUCCESS))
    source.reply(cm)


def show_khld_status(source: UserCommandSource):
    card = Card(Module.Header(f'{core_constant.NAME_SHORT} 状态'), theme=Types.Theme.WARNING)
    card.append(Module.Section(Element.Text(f'{core_constant.NAME} 版本: {core_constant.VERSION}', type=Types.Text.KMD)))
    card.append(Module.Section(Element.Text(f'{core_constant.NAME} 状态: {source.khld_server.status}', type=Types.Text.KMD)))
    card.append(Module.Section(Element.Text(f'插件数量: {source.khld_server.plugin_count}', type=Types.Text.KMD)))
    source.reply(CardMessage(card))


def list_plugin(source: UserCommandSource):
    card = Card(Module.Header('插件列表'), Module.Divider(), theme=Types.Theme.INFO)
    plugins = source.khld_server.plugin_manager.plugins
    for plugin_id in plugins:
        card.append(Module.Section(Element.Text(f'{plugins[plugin_id].name}**@**{plugin_id}', type=Types.Text.KMD)))
    source.reply(CardMessage(card))


def info_plugin(source: UserCommandSource, msg):
    plugin_id = msg['plg_id']
    if plugin_id not in source.khld_server.plugin_manager.plugins:
        source.reply(f'插件 {plugin_id} 未找到')
    else:
        plugin = source.khld_server.plugin_manager.plugins[plugin_id]
        msg = [
            f'插件 {plugin.name} 的详细信息',
            f'插件 id: {plugin.id}',
            f'插件版本: {plugin.version}',
            f'插件介绍: {plugin.description if plugin.description != "" else "无"}',
            f'插件作者: {plugin.author if plugin.author != "" else "无"}',
            f'插件链接: {plugin.link if plugin.link != "" else "无"}'
        ]
        source.reply('\n'.join(msg))


async def reload_plugin(source: UserCommandSource):
    source.khld_server.plugin_manager.reload_plugins()
    await source.message.ctx.channel.send(f'重载成功, 当前已加载 {len(source.khld_server.plugin_manager.plugins)} 插件')


async def reload_config(source: UserCommandSource):
    source.khld_server.config = source.khld_server.get_config()
    await source.message.ctx.channel.send('配置文件重载成功')


def reload_all(source: UserCommandSource):
    reload_plugin(source)
    reload_config(source)


def on_unload(interface: PluginInterface):
    pass


async def on_message(interface: MessageInterface):
    pass
