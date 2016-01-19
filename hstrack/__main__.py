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

LOG_PATH = '/Applications/Hearthstone/Logs/Power.log'


@click.command()
def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    fd = os.open(LOG_PATH, os.O_RDONLY)
    lines = list()
    logger.info("Seeked to {}".format(os.lseek(fd, 0, os.SEEK_END)))

    def reader():
        while True:
            buf = os.read(fd, 1024)
            logger.info(buf)
            if not buf:
                break
            else:
                x = buf.splitlines()
                if lines and not lines[-1].endswith(b'\n'):
                    x[0] = lines.pop(-1) + x[0]

    loop = asyncio.get_event_loop()
    loop.add_reader(fd, reader)
    loop.run_forever()
    os.close(fd)


if __name__ == '__main__':
    main()
