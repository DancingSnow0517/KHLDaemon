import asyncio

from khl import Bot
from ruamel import yaml

from .command.command_manager import CommandManager
from .config import Config
from .plugin.plugin_manager import PluginManager
from .utils.logger import ColoredLogger


class KHLDaemonServer:

    def __init__(self) -> None:
        self.config = self.get_config()
        self.bot = Bot(self.config.token)
        self.logger = ColoredLogger(level=self.config.log_level)
        self.plugin_manager = PluginManager(self)
        self.command_manager = CommandManager(self)
        self.status = False

    @staticmethod
    def get_config():
        with open('config.yml', 'r', encoding='utf-8') as f:
            return Config(**yaml.round_trip_load(f))

    def start_server(self):
        self.plugin_manager.load_plugins()
        if not self.bot.loop:
            self.bot.loop = asyncio.get_event_loop()
        try:
            self.status = True
            self.bot.loop.run_until_complete(self.bot.start())
        except KeyboardInterrupt:
            self.plugin_manager.unload_plugins()
            self.logger.info('KHLDamon stopped')

    @property
    def plugin_count(self):
        return len(self.plugin_manager.plugins)

    @property
    def command_count(self):
        return len(self.command_manager.root_nodes)
