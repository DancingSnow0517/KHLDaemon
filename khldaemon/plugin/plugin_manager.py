import os
from typing import Dict, TYPE_CHECKING

from colorama import Fore, Style
from khl import Message, MessageTypes, Event

from .interface import PluginInterface, MessageInterface, EventInterface
from .type.plugin import Plugin
from ..command.command_source import UserCommandSource

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer


class PluginManager:
    plugins: Dict

    def __init__(self, khld_server: 'KHLDaemonServer') -> None:
        self.khld_server = khld_server
        self.plugins = {}
        self.help_messages = {}
        self.config = self.khld_server.config
        self.logger = self.khld_server.logger
        self.bot = self.khld_server.bot
        self.bot.client.register(MessageTypes.TEXT, self.on_message)
        self.bot.client.register(MessageTypes.SYS, self.on_event)

    def search_all_plugin(self):
        self.plugins.clear()
        plugin = Plugin('khldaemon.plugin.builtin.khl_plugin')
        self.plugins[plugin.id] = plugin
        for DIR in self.config.plugin_directories:
            file_list = os.listdir(DIR)
            for file in file_list:
                if file.endswith('.py'):
                    plugin = Plugin(f'{DIR}.{file.replace(".py", "")}')
                    if plugin.id in self.plugins:
                        self.logger.error(f'插件 {plugin.name}@{plugin.id} V{plugin.version} 加载失败')
                        continue
                    self.plugins[plugin.id] = plugin

    def load_plugins(self):
        self.search_all_plugin()
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            self.logger.info(
                f'插件 {plugin.meta.name}{Fore.GREEN}@{Style.RESET_ALL}{plugin.meta.id} {Fore.GREEN}V{plugin.meta.version}{Style.RESET_ALL} 已加载')
            plugin.on_load(PluginInterface(self.khld_server, plugin.id))

    def unload_plugins(self):
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            plugin.on_unload(PluginInterface(self.khld_server, plugin.id))

    async def on_message(self, msg: Message):
        self.logger.info(f'接收到消息: <{msg.author.nickname}> {msg.content}')
        self._execute_command(msg)
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            await plugin.on_message(MessageInterface(self.khld_server, plugin.id, msg))

    async def on_event(self, event: Event):
        self.logger.info(f'接收到事件: {event.event_type.value}')
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            await plugin.on_event(EventInterface(self.khld_server, plugin.id, event))

    def _execute_command(self, msg: Message):
        content = msg.content
        pos = content.find(' ')
        if pos == -1:
            root = content
        else:
            root = content[:pos]

        if root in self.khld_server.command_manager.root_nodes:
            self.khld_server.command_manager.execute_command(content, UserCommandSource(self.khld_server, msg))
