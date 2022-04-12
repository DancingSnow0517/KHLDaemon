import sys

import nest_asyncio

from .cli.cli_entry import entry_point


def main():
    nest_asyncio.apply()
    entry_point()


if __name__ == '__main__':
    sys.exit(main())
