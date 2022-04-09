import os.path
import pkgutil
import sys
from argparse import ArgumentParser

from ..plugin.plugin_manager import PluginManager


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

    plugin_manager = PluginManager()
    plugin_manager.load_plugins()

    try:
        plugin_manager.interface.bot.run()
    except KeyboardInterrupt:
        plugin_manager.unload_plugins()


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