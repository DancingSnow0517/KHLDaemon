import os.path
import pkgutil
import sys
from argparse import ArgumentParser

import colorama

from khldaemon.constants import core_constant
from ..khld_server import KHLDaemonServer
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
    print('{} {} is starting up'.format(core_constant.NAME, core_constant.VERSION))
    print('{} is open source, you can find it here: {}'.format(core_constant.NAME, core_constant.GITHUB_URL))
    if not environment_check():
        print('Use "python -m khldaemon init" to initialize KHLDaemon first')
        return

    colorama.init(autoreset=True)
    khldaemon_server = KHLDaemonServer()

    logger = ColoredLogger(name='khl.py', level=khldaemon_server.config.log_level)
    patch(logger)

    khldaemon_server.start()


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
