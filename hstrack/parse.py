#
# Copyright 2016 Kimmo Parviainen-Jalanko
#
# Release to public under MIT License, see LICENSE for details.
#
import logging
from pprint import pprint

import click

LOG_PATH = '/Applications/Hearthstone/Logs/Power.log'

logger = logging.getLogger(__name__)


class Game(object):
    def __init__(self):
        pass


class Parser:
    def __init__(self):
        self.current_game = None
        self.games = list()

    def process(self, line):
        if line.strip() == 'CREATE_GAME':
            self.new_game()

    def new_game(self):
        game = Game()
        logger.info("new game")
        if self.current_game is not None:
            self.games.append(self.current_game)
        self.current_game = game

    def parse(self):
        with open(LOG_PATH) as f:
            for line in f:
                if 'PowerTaskList.DebugPrintPower()' not in line:
                    continue
                beef = line.split(' - ', 1)[-1].rstrip()
                logger.debug(beef)
                self.process(beef)


@click.command()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    logging.basicConfig(level=50 - (10 * verbose))
    parser = Parser()
    parser.parse()
    pprint(parser.games)


if __name__ == '__main__':
    main()
