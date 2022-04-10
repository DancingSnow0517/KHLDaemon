import importlib

from .meta import Meta


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
            self.on_unload = lambda interface: ...

    def __str__(self) -> str:
        return self.meta.name
