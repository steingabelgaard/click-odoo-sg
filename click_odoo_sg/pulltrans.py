#!/usr/bin/env python
# Copyright 2020 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

import click
import click_odoo

_logger = logging.getLogger(__name__)


def pulltrans(env):
    server = env['translation.server'].search([])
    if server:
        _logger.info("Pulling translations")
        server[0].pull_from_server()
        env.cr.commit()


@click.command()
@click_odoo.env_options(with_rollback=False)
def main(env):
    """ Pull translations from translations server """
    pulltrans(env)
    

if __name__ == "__main__":  # pragma: no cover
    main()