import os
from typing import List

from khl import Message, MessageTypes, Bot

from .plugin_interface import PluginInterface
from .type.plugin import Plugin
from ..utils.logger import ColoredLogger


class PluginManager:

    plugins: List[Plugin]

    def __init__(self, config, logger: ColoredLogger) -> None:
        self.plugins = []
        self.config = config
        self.logger = logger
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
            self.logger.info(f'插件 {plugin.meta.name}@{plugin.meta.id} V{plugin.meta.version} 已加载')
            plugin.on_load(PluginInterface(self, plugin.meta.id))

    def unload_plugins(self):
        for plugin in self.plugins:
            plugin.on_unload(PluginInterface(self, plugin.meta.id))

    async def on_message(self, msg: Message):
        self.logger.info(f'接收到消息: <{msg.author.nickname}> {msg.content}')
        for plugin in self.plugins:
            await plugin.on_message(msg)


