import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union, List

from khl import Message, MessageTypes

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer


def async_command(func):
    def _sync(source: UserCommandSource, msg=None):
        spec_args = inspect.getfullargspec(func).args
        spec_args_len = len(spec_args)
        if spec_args_len == 1:
            asyncio.get_event_loop().run_until_complete(func(source))
        else:
            asyncio.get_event_loop().run_until_complete(func(source, msg))

    return _sync


class CommandSource(ABC):

    @abstractmethod
    def get_server(self) -> 'KHLDaemonServer':
        ...

    @abstractmethod
    def reply(self, content: Union[str, List] = '', use_quote: bool = True, *, type: MessageTypes = None,
              **kwargs):
        pass


class UserCommandSource(CommandSource):

    def __init__(self, khld_server: 'KHLDaemonServer', message: Message) -> None:
        super().__init__()
        self.khld_server = khld_server
        self.message = message
        self._loop = asyncio.get_event_loop()

    def get_server(self) -> 'KHLDaemonServer':
        return self.khld_server

    def reply(self, content: Union[str, List] = '', use_quote: bool = True, *, type: MessageTypes = None, **kwargs):
        print(content)
        self._loop.run_until_complete(self.message.reply(content=content, use_quote=use_quote, type=type, **kwargs))
