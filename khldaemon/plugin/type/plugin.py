import importlib

from .meta import Meta


async def _func(interface):
    ...


class Plugin:

    def __init__(self, path: str) -> None:
        self.module = importlib.import_module(path)
        self.meta = Meta(self.module)

        try:
            self.on_load = self.module.on_load
        except AttributeError:
            self.on_load = lambda interface: ...
        try:
            self.on_unload = self.module.on_unload
        except AttributeError:
            self.on_unload = lambda interface: ...
        try:
            self.on_message = self.module.on_message
        except AttributeError:
            self.on_unload = _func
        try:
            self.on_event = self.module.on_event
        except AttributeError:
            self.on_event = _func

    def __str__(self) -> str:
        return self.meta.name

    @property
    def name(self):
        return self.meta.name

    @property
    def id(self):
        return self.meta.id

    @property
    def link(self):
        return self.meta.link

    @property
    def author(self):
        return self.meta.author

    @property
    def version(self):
        return self.meta.version

    @property
    def description(self):
        return self.meta.description
