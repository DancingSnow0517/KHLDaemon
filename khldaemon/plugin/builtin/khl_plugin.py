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
    interface.registry_help_messages('!!help', '显示帮助信息')
    interface.registry_help_messages('!!KHLD', '显示机器人信息')

    interface.register_command(
        Literal('!!help').runs(print_help_messages)
    )
    interface.register_command(
        Literal('!!KHLD').
            runs(lambda src: src.reply(f'KHLD 控制指令\n```\n{khld_help_messages}\n```', type=MessageTypes.KMD)).
            then(
            Literal('status').
                runs(show_khld_status)
        ).
            then(
            Literal('plugin').
                runs(lambda src: src.reply(f'插件相关命令: \n```\n{plugin_help_messages}\n```', type=MessageTypes.KMD)).
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
                Literal('reloadall').runs(reload_plugin)
            )
        ).
            then(
            Literal('reload').
                runs(lambda src: src.reply(f'重载相关命令: \n```\n{reload_help_messages}\n```', type=MessageTypes.KMD)).
                then(
                Literal('plugin').runs(reload_plugin)
            ).
                then(
                Literal('config').runs(reload_config)
            ).
                then(
                Literal('all').runs(reload_all)
            )
        )
    )


def print_help_messages(source: UserCommandSource):
    help_messages = source.khld_server.plugin_manager.help_messages
    msg = []
    enter = '\n'
    for prefix in help_messages:
        msg.append(f'[{prefix}] {help_messages[prefix]}')
    source.reply(f'KHLD 指令帮助信息列表\n```\n{enter.join(msg)}\n```', type=MessageTypes.KMD)


def show_khld_status(source: UserCommandSource):
    msg = [
        f'{core_constant.NAME_SHORT} 状态: ',
        f'{core_constant.NAME} 版本 {core_constant.VERSION}',
        f'{core_constant.NAME} 状态: {source.khld_server.status}',
        f'插件数量: {source.khld_server.plugin_count}'
    ]
    source.reply('\n'.join(msg))


def list_plugin(source: UserCommandSource):
    msg = ['插件列表: ']
    plugins = source.khld_server.plugin_manager.plugins
    for plugin_id in plugins:
        msg.append(f'{plugins[plugin_id].name}@{plugin_id}')
    source.reply('\n'.join(msg))


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


def reload_plugin(source: UserCommandSource):
    source.khld_server.plugin_manager.reload_plugins()


def reload_config(source: UserCommandSource):
    source.khld_server.config = source.khld_server.get_config()


def reload_all(source: UserCommandSource):
    reload_plugin(source)
    reload_config(source)


def on_unload(interface: PluginInterface):
    pass


async def on_message(interface: MessageInterface):
    pass
