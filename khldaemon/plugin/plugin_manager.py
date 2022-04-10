import os
from typing import Dict

from colorama import Fore, Style
from khl import Message, MessageTypes

from .interface import PluginInterface, MessageInterface
from .type.plugin import Plugin
from ..utils.logger import ColoredLogger


class PluginManager:
    plugins: Dict

    def __init__(self, config, bot) -> None:
        self.plugins = {}
        self.help_messages = {}
        self.config = config
        self.logger = ColoredLogger(level=self.config.log_level)
        self.bot = bot
        self.bot.client.register(MessageTypes.TEXT, self.on_message)

    def search_all_plugin(self):
        self.plugins.clear()
        plugin = Plugin('khldaemon.plugin.builtin.khl_plugin')
        self.plugins[plugin.meta.id] = plugin
        for DIR in self.config.plugin_directories:
            file_list = os.listdir(DIR)
            for file in file_list:
                if file.endswith('.py'):
                    plugin = Plugin(f'{DIR}.{file.replace(".py", "")}')
                    if plugin.meta.id in self.plugins:
                        self.logger.error(f'插件 {plugin.meta.name}@{plugin.meta.id} V{plugin.meta.version} 加载失败')
                        continue
                    self.plugins[plugin.meta.id] = plugin

    def load_plugins(self):
        self.search_all_plugin()
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            self.logger.info(f'插件 {plugin.meta.name}{Fore.GREEN}@{Style.RESET_ALL}{plugin.meta.id} {Fore.GREEN}V{plugin.meta.version}{Style.RESET_ALL} 已加载')
            plugin.on_load(PluginInterface(self, plugin.meta.id))

    def unload_plugins(self):
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            plugin.on_unload(PluginInterface(self, plugin.meta.id))

    async def on_message(self, msg: Message):
        self.logger.info(f'接收到消息: <{msg.author.nickname}> {msg.content}')
        for plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            await plugin.on_message(MessageInterface(self, plugin.meta.id, msg))
