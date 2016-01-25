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

parser = Parser()
remainder = str()


@click.command()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    logging.basicConfig(level=50 - (10 * verbose))
    logger = logging.getLogger(__name__)
    fd = os.open(LOG_PATH, os.O_RDONLY)
    logger.info("Seeked to {}".format(os.lseek(fd, 0, os.SEEK_END)))

    def reader():
        while True:
            buf = os.read(fd, 1024).decode('utf-8')
            logger.debug(buf)
            if not buf:
                # logger.debug(os.fstat(fd))
                break
            else:
                lines = buf.splitlines()
                if remainder:
                    lines.insert(0, remainder + lines.pop(0))
                for line in lines:
                    if not line.endswith('\n'):
                        logger.debug("Incomplete line: {}".format(line))
                        remainder = line
                    else:
                        parser.process(line)

    loop = asyncio.get_event_loop()
    loop.add_reader(fd, reader)
    loop.run_forever()
    os.close(fd)


if __name__ == '__main__':
    main()
