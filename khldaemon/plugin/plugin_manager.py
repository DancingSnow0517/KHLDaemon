import os
from typing import List
from colorama import Fore, Style

from khl import Message, MessageTypes, Bot

from .interface import PluginInterface, MessageInterface
from .type.plugin import Plugin
from ..utils.logger import ColoredLogger


class PluginManager:
    plugins: List[Plugin]

    def __init__(self, config) -> None:
        self.plugins = []
        self.help_messages = {}
        self.config = config
        self.logger = ColoredLogger(level=self.config.log_level)
        self.bot = Bot(self.config.token)
        self.bot.client.register(MessageTypes.TEXT, self.on_message)

    def search_all_plugin(self):
        self.plugins.clear()
        self.plugins.append(Plugin('khldaemon.plugin.builtin.khl_plugin'))
        for DIR in self.config.plugin_directories:
            file_list = os.listdir(DIR)
            for file in file_list:
                if file.endswith('.py'):
                    self.plugins.append(Plugin(f'{DIR}.{file.replace(".py", "")}'))

    def load_plugins(self):
        self.search_all_plugin()
        for plugin in self.plugins:
            self.logger.info(f'插件 {plugin.meta.name}{Fore.GREEN}@{Style.RESET_ALL}{plugin.meta.id} {Fore.GREEN}V{plugin.meta.version}{Style.RESET_ALL} 已加载')
            plugin.on_load(PluginInterface(self, plugin.meta.id))

    def unload_plugins(self):
        for plugin in self.plugins:
            plugin.on_unload(PluginInterface(self, plugin.meta.id))

    async def on_message(self, msg: Message):
        self.logger.info(f'接收到消息: <{msg.author.nickname}> {msg.content}')
        for plugin in self.plugins:
            await plugin.on_message(MessageInterface(self, plugin.meta.id, msg))
