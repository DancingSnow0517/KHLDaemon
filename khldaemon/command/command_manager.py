import collections
from enum import auto, Enum
from typing import TYPE_CHECKING, List, Dict

import khldaemon.command.builder.command_builder_util as utils
from .builder.exception import CommandError
from .builder.nodes.basic import Literal, CommandSuggestion, CommandSuggestions
from .command_source import CommandSource

if TYPE_CHECKING:
    from ..khld_server import KHLDaemonServer


class TraversePurpose(Enum):
    EXECUTE = auto()
    SUGGEST = auto()


class CommandManager:
    def __init__(self, khld_server: 'KHLDaemonServer') -> None:
        self.khld_server = khld_server
        self.config = self.khld_server.config
        self.logger = self.khld_server.logger
        self.bot = self.khld_server.bot

        self.root_nodes = collections.defaultdict(list)  # type: Dict[str, List[Literal]]

    def clear(self):
        self.root_nodes.clear()

    def register_command(self, node: Literal):
        for literal in node.literals:
            self.root_nodes[literal].append(node)

    def _traverse(self, command: str, source: CommandSource, purpose: TraversePurpose) -> None or List[CommandSuggestion]:

        first_literal_element = utils.get_element(command)
        plugin_root_nodes = self.root_nodes.get(first_literal_element, [])
        suggestions = CommandSuggestions()

        if purpose == TraversePurpose.SUGGEST and len(plugin_root_nodes) == 0:
            return CommandSuggestions([CommandSuggestion('', literal) for literal in self.root_nodes.keys()])

        for plugin_root_node in plugin_root_nodes:
            node = plugin_root_node
            try:
                if purpose == TraversePurpose.EXECUTE:
                    node.execute(source, command)
                elif purpose == TraversePurpose.SUGGEST:
                    suggestions.extend(node.generate_suggestions(source, command))

            except CommandError as error:
                if not error.is_handled():
                    error.set_message(f'{type(error).__name__}: {error.get_error_data()}')
                    source.reply(error)
            except:
                self.logger.exception(
                    'Error when executing command "{}" with command source "{}" on {}'.format(command, source, node, ))

        if purpose == TraversePurpose.SUGGEST:
            return suggestions

    def execute_command(self, command: str, source: CommandSource):
        self._traverse(command, source, TraversePurpose.EXECUTE)
