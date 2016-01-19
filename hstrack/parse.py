#
# Copyright 2016 Kimmo Parviainen-Jalanko
#
# Release to public under MIT License, see LICENSE for details.
#
import logging

import click

LOG_PATH = '/Applications/Hearthstone/Logs/Power.log'

logger = logging.getLogger(__name__)


@click.command()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    logging.basicConfig(level=50 - (10 * verbose))
    with open(LOG_PATH) as f:
        for line in f:
            logger.debug(line.split(' - ', 1)[-1].rstrip())


if __name__ == '__main__':
    main()
