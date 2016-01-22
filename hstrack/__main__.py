#!/usr/bin/env python3.5
#
# Copyright 2016 Kimmo Parviainen-Jalanko
#
# Release to public under MIT License, see LICENSE for details.
#
import asyncio
import logging
import os

import click

from hstrack.parse import Parser

LOG_PATH = '/Applications/Hearthstone/Logs/Power.log'


@click.command()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    logging.basicConfig(level=50 - (10 * verbose))
    logger = logging.getLogger(__name__)
    fd = os.open(LOG_PATH, os.O_RDONLY)
    lines = list()   # XXX: We only have a single partial line, not a list.
    logger.info("Seeked to {}".format(os.lseek(fd, 0, os.SEEK_END)))

    parser = Parser()

    def reader():
        while True:
            buf = os.read(fd, 1024).decode('utf-8')
            logger.debug(buf)
            if not buf:
                logger.debug(os.fstat(fd))
                break
            else:
                x = buf.splitlines()
                if lines and not lines[-1].endswith('\n'):
                    x[0] = lines.pop(-1) + x[0]
                for line in x:
                    if not line.endswith('\n'):
                        lines.append(line)
                    else:
                        parser.process(line)

    loop = asyncio.get_event_loop()
    loop.add_reader(fd, reader)
    loop.run_forever()
    os.close(fd)


if __name__ == '__main__':
    main()
