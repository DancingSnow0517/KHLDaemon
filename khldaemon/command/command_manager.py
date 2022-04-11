import collections
from enum import Enum, auto
from typing import TYPE_CHECKING, Dict, List

import khldaemon.command.builder.command_builder_util as utils
from .builder.exception import CommandError
from .builder.nodes.basic import CommandSuggestion, CommandSuggestions
from .command_source import CommandSource

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer


class TraversePurpose(Enum):
    EXECUTE = auto()
    SUGGEST = auto()


class CommandManager:
    def __init__(self, khld_server: 'KHLDaemonServer') -> None:
        super().__init__()
        self.khld_server = khld_server
        self.logger = self.khld_server.logger
        self.root_nodes = collections.defaultdict(list)  # type: Dict[str, List[PluginCommandNode]]

        self.__preserve_command_error_display_flag = False

    def clear_command(self):
        self.root_nodes.clear()

    def register_command(self, plugin_node: PluginCommandNode):
        for literal in plugin_node.node.literals:
            self.root_nodes[literal].append(plugin_node)

    def _traverse(self, command: str, source: CommandSource, purpose: TraversePurpose) -> None or List[CommandSuggestion]:

        first_literal_element = utils.get_element(command)
        plugin_root_nodes = self.root_nodes.get(first_literal_element, [])
        suggestions = CommandSuggestions()

        if purpose == TraversePurpose.SUGGEST and len(plugin_root_nodes) == 0:
            return CommandSuggestions([CommandSuggestion('', literal) for literal in self.root_nodes.keys()])

        for plugin_root_node in plugin_root_nodes:
            plugin = plugin_root_node.plugin
            node = plugin_root_node.node
            try:
                with self.khld_server.plugin_manager.with_plugin_context(plugin):
                    if purpose == TraversePurpose.EXECUTE:
                        node.execute(source, command)
                    elif purpose == TraversePurpose.SUGGEST:
                        suggestions.extend(node.generate_suggestions(source, command))

            except CommandError as error:
                if not error.is_handled():
                    try:
                        error.set_message(type(error).__name__)
                    except KeyError:
                        self.logger.debug(f'Fail to translated command error with key {type(error).__name__}')
                    source.reply(error)
            except:
                self.logger.exception(
                    'Error when executing command "{}" with command source "{}" on {} registered by {}'.format(command,
                                                                                                               source,
                                                                                                               node,
                                                                                                               plugin))

        if purpose == TraversePurpose.SUGGEST:
            return suggestions

    def execute_command(self, command: str, source: CommandSource):
        self._traverse(command, source, TraversePurpose.EXECUTE)

    def suggest_command(self, command: str, source: CommandSource) -> CommandSuggestions:
        return self._traverse(command, source, TraversePurpose.SUGGEST)
