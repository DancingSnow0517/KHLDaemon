import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union, List

from khl import Message, User, MessageTypes

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer





class CommandSource(ABC):

    @abstractmethod
    def get_server(self) -> 'KHLDaemonServer':
        ...


class UserCommandSource(CommandSource):

    def __init__(self, khld_server: 'KHLDaemonServer', message: Message) -> None:
        super().__init__()
        self.khld_server = khld_server
        self.message = message
        self._loop = asyncio.get_event_loop()

    def get_server(self) -> 'KHLDaemonServer':
        return self.khld_server

    def add_reaction(self, emoji: str):
        self._loop.run_until_complete(self.message.add_reaction(emoji))

    def delete_reaction(self, emoji: str, user: User):
        self._loop.run_until_complete(self.message.delete_reaction(emoji, user))

    def reply(self, content: Union[str, List] = '', use_quote: bool = True, *, type: MessageTypes = None,
                    **kwargs):
        self._loop.run_until_complete(self.message.reply(content=content, use_quote=use_quote, type=type, **kwargs))

    def delete(self):
        self._loop.run_until_complete(self.message.delete())

