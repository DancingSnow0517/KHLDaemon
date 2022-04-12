import asyncio

from khl import Bot, Message
from ruamel import yaml

from .command.command_source import UserCommandSource
from .command.command_manager import CommandManager
from .config import Config
from .plugin.plugin_manager import PluginManager
from .utils.logger import ColoredLogger


def get_config():
    with open('config.yml', 'r', encoding='utf-8') as f:
        return Config(**yaml.round_trip_load(f))


class KHLDaemonServer:

    def __init__(self) -> None:
        self.config = get_config()
        self.logger = ColoredLogger(level=self.config.log_level)
        self.bot = Bot(self.config.token)
        self.plugin_manager = PluginManager(self)
        self.command_manager = CommandManager(self)

    def start(self):
        self.plugin_manager.load_plugins()
        if not self.bot.loop:
            self.bot.loop = asyncio.get_event_loop()
        try:
            self.bot.loop.run_until_complete(self.bot.start())
        except KeyboardInterrupt:
            self.plugin_manager.unload_plugins()
            self.logger.info('KHLDamon stopped')
