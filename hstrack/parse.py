#
# Copyright 2016 Kimmo Parviainen-Jalanko
#
# Release to public under MIT License, see LICENSE for details.
#
import logging
import re
from collections import defaultdict
from pprint import pprint

import click

LOG_PATH = '/Applications/Hearthstone/Logs/Power.log'

logger = logging.getLogger(__name__)

DEBUG_LINE_RE = re.compile(
        r'^D (?P<ts>[^ ]+) (?P<module>[\w]+\.[\w]+)\(\) - (?P<msg>.+)')

TAG_CHANGE_RE = re.compile(r'\W+ TAG_CHANGE Entity=(?P<entity>.+) tag=(?P<tag>.+) value=(?P<value>.+)')

SHOW_ENTITY_RE = re.compile(r'\W+ SHOW_ENTITY Entity - Updating Entity=(?P<entity>.+) CardID=(?P<card_id>.+)')


def chunks(l, n=2):
    """Yield successive n-sized chunks from l.
    :param l: iterable to be chunked
    :param n: chunk size
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Game(object):
    def __init__(self):
        self.entities = defaultdict(dict)


class Parser:
    def __init__(self):
        self.current_game = None
        self.games = list()

    def process(self, line):
        m = DEBUG_LINE_RE.match(line)
        if m is None:
            return
        module = m.group('module')
        if module != 'PowerTaskList.DebugPrintPower':
            return
        msg = m.group('msg')
        logger.debug(msg)
        if msg.strip() == 'CREATE_GAME':
            self.new_game()
        elif msg.lstrip().startswith('TAG_CHANGE'):
            self.tag_change(msg)
        elif msg.lstrip().startswith('SHOW_ENTITY'):
            self.show_entity(msg)
        else:
            print(line)

    def new_game(self):
        game = Game()
        logger.info("new game")
        if self.current_game is not None:
            self.games.append(self.current_game)
        self.current_game = game

    def tag_change(self, msg):
        m = TAG_CHANGE_RE.match(msg)
        if m is None:
            logger.error("Could not parse tag change: {}".format(msg))
            return
        entity, tag, value = self.get_entity(m)

    def get_entity(self, m):
        d = m.groupdict()
        # logger.info(d)
        entity = d['entity']
        if entity.startswith('['):
            entity = self.parse_entity(entity)
        tag = d['tag']
        value = d['value']
        logger.info("{} {}={}".format(entity, tag, value))
        return entity, tag, value

    def parse_entity(self, entity):
        return dict(chunks(re.split(' ?([\w]+)=', entity[1:-1])[1:]))

    def show_entity(self, msg):
        m = SHOW_ENTITY_RE.match(msg)
        if m is None:
            logger.error("Could not parse show entity: {}".format(msg))
            return
        entity, tag, value = self.get_entity(m)


@click.command()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    logging.basicConfig(level=50 - (10 * verbose))
    parser = Parser()
    with open(LOG_PATH) as f:
        for line in f:
            parser.process(line)
    pprint(parser.games)


if __name__ == '__main__':
    main()
