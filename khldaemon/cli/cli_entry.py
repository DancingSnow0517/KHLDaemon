import asyncio
import os.path
import pkgutil
import sys
from argparse import ArgumentParser

from ruamel import yaml

from ..config import Config
from ..plugin.plugin_manager import PluginManager
from ..utils.logger import ColoredLogger


def entry_point():
    if len(sys.argv) == 1:
        run_bot()
        return

    parser = ArgumentParser(
        prog='khldaemon',
        description='KHLDaemon CLI'
    )
    subparsers = parser.add_subparsers(title='Command', help='Available commands', dest='subparser_name')
    subparsers.add_parser('start', help='start KHLDaemon')
    subparsers.add_parser('init', help='Prepare the working environment of KHLDaemon.')

    result = parser.parse_args()
    if result.subparser_name == 'start':
        run_bot()
    elif result.subparser_name == 'init':
        init_bot()


def environment_check():
    if not os.path.exists('config'):
        return False
    if not os.path.exists('plugin'):
        return False
    if not os.path.exists('config.yml'):
        return False
    return True


def run_bot():
    if not environment_check():
        raise Exception('Use "python -m khldaemon init" to initialize KHLDaemon first')

    with open('config.yml', 'r', encoding='utf-8') as f:
        config = Config(**yaml.round_trip_load(f))

    logger = ColoredLogger(level=config.log_level)
    patch(logger)

    plugin_manager = PluginManager(config, logger)
    plugin_manager.load_plugins()

    if not plugin_manager.interface.bot.loop:
        plugin_manager.interface.bot.loop = asyncio.get_event_loop()
    try:
        plugin_manager.interface.bot.loop.run_until_complete(plugin_manager.interface.bot.start())
    except KeyboardInterrupt:
        plugin_manager.unload_plugins()
        logger.info('KHLDamon stopped')


def initialize_environment():
    if not os.path.exists('config'):
        os.mkdir('config')
    if not os.path.exists('plugin'):
        os.mkdir('plugin')
    if not os.path.exists('config.yml'):
        data = pkgutil.get_data('khldaemon', 'resources/default_config.yml')
        with open('config.yml', 'wb') as f:
            f.write(data)


def init_bot():
    initialize_environment()


def patch(logger):
    import khl.command
    import khl.bot
    khl.receiver.log = logger
    khl.client.log = logger
    khl.requester.log = logger
    khl.command.command.log = logger
    khl.command.parser.log = logger
    khl.command.manager.log = logger
    khl.command.lexer.log = logger
    khl.bot.log = logger
