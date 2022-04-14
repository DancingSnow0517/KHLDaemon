import asyncio
from typing import Union, List, IO

from khl import Bot, Message, User, Guild, Channel, MessageTypes, PublicChannel
from khl.game import Game
from ruamel import yaml

from .command.command_manager import CommandManager
from .config import Config
from .plugin.plugin_manager import PluginManager
from .utils.logger import ColoredLogger


class KHLDaemonServer(Bot):

    def __init__(self) -> None:
        self.config = self.get_config()
        super().__init__(self.config.token)
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
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        try:
            self.status = True
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.plugin_manager.unload_plugins()
            self.logger.info('KHLDamon stopped')

    @property
    def plugin_count(self):
        return len(self.plugin_manager.plugins)

    @property
    def command_count(self):
        return len(self.command_manager.root_nodes)

    def fetch_me(self, force_update: bool = False) -> User:
        return self.loop.run_until_complete(super().fetch_me(force_update))

    def fetch_public_channel(self, channel_id: str) -> PublicChannel:
        return self.loop.run_until_complete(super().fetch_public_channel(channel_id))

    def delete_channel(self, channel: Union[Channel, str]):
        return self.loop.run_until_complete(super().delete_channel(channel))

    def fetch_guild(self, guild_id: str) -> Guild:
        return self.loop.run_until_complete(super().fetch_guild(guild_id))

    def list_guild(self) -> List[Guild]:
        return self.loop.run_until_complete(super().list_guild())

    def send(self, target: Channel, content: Union[str, List], *, type: MessageTypes = None, temp_target_id: str = '',
             **kwargs):
        return self.loop.run_until_complete(
            super().send(target, content, type=type, temp_target_id=temp_target_id, **kwargs))

    def upload_asset(self, file: Union[IO, str]) -> str:
        return self.loop.run_until_complete(super().upload_asset(file))

    def create_asset(self, file: Union[IO, str]) -> str:
        return self.loop.run_until_complete(super().create_asset(file))

    def kickout(self, guild: Guild, user: Union[User, str]):
        return self.loop.run_until_complete(super().kickout(guild, user))

    def leave(self, guild: Guild):
        return self.loop.run_until_complete(super().leave(guild))

    def add_reaction(self, msg: Message, emoji: str):
        return self.loop.run_until_complete(super().add_reaction(msg, emoji))

    def delete_reaction(self, msg: Message, emoji: str, user: User = None):
        return self.loop.run_until_complete(super().delete_reaction(msg, emoji, user))

    def list_game(self, *, begin_page: int = 1, end_page: int = None, page_size: int = 50, sort: str = '') -> \
            List[Game]:
        return self.loop.run_until_complete(
            super().list_game(begin_page=begin_page, end_page=end_page, page_size=page_size, sort=sort))

    def create_game(self, name: str, process_name: str = None, icon: str = None) -> Game:
        return self.loop.run_until_complete(super().create_game(name, process_name, icon))

    def update_game(self, id: int, name: str = None, icon: str = None) -> Game:
        return self.loop.run_until_complete(super().update_game(id, name, icon))

    def delete_game(self, game: Union[Game, int]):
        return self.loop.run_until_complete(super().delete_game(game))

    def update_playing_game(self, game: Union[Game, int], data_type: int = 1):
        return self.loop.run_until_complete(super().update_playing_game(game, data_type))

    def stop_playing_game(self):
        return self.loop.run_until_complete(super().stop_playing_game())
