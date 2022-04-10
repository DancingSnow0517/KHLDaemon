import asyncio

from khl import Bot
from ruamel import yaml

from khldaemon.config import Config
from khldaemon.plugin.plugin_manager import PluginManager
from khldaemon.utils.logger import ColoredLogger


def get_config():
    with open('config.yml', 'r', encoding='utf-8') as f:
        return Config(**yaml.round_trip_load(f))


class KHLDaemonServer:

    def __init__(self) -> None:
        self.config = get_config()
        self.logger = ColoredLogger(level=self.config.log_level)
        self.bot = Bot(self.config.token)
        self.plugin_manager = PluginManager(self.config, self.bot)

        self.bot.task.add_interval(seconds=30, timezone='Asia/Shanghai')(lambda: print('task'))

    def start(self):
        self.plugin_manager.load_plugins()
        if not self.bot.loop:
            self.bot.loop = asyncio.get_event_loop()
        try:
            self.bot.loop.run_until_complete(self.bot.start())
        except KeyboardInterrupt:
            self.plugin_manager.unload_plugins()
            self.logger.info('KHLDamon stopped')
