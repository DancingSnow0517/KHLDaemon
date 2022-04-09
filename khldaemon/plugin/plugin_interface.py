from typing import TYPE_CHECKING

from ..utils.logger import ColoredLogger

if TYPE_CHECKING:
    from .plugin_manager import PluginManager


class PluginInterface:
    def __init__(self, plg_manager: 'PluginManager', plugin_id: str) -> None:
        self.plugin_manager = plg_manager
        self.plugin_id = plugin_id
        self.config = self.plugin_manager.config
        self.bot = self.plugin_manager.bot
        self.help_messages = {}
        self.logger = ColoredLogger(level=self.config.log_level, plugin_id=self.plugin_id)

    def registry_help_messages(self, prefix: str, desc: str):
        self.help_messages[prefix] = desc

