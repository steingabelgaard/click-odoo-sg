#!/usr/bin/env python
# Copyright 2020 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

import click
import click_odoo

_logger = logging.getLogger(__name__)


def loadtrans(env, lang, overwrite, websites):
    wizard = env['base.language.install'].create({'lang': lang,
                                                  'overwrite': overwrite})
    if websites:
        wizard.website_ids = env['website'].search([])
    _logger.info("Loading translations")
    wizard.lang_install()
    env.cr.commit()


@click.command()
@click_odoo.env_options(with_rollback=False)
@click.option('--lang', '-l', default='da_DK')
@click.option('--overwrite/--no-overwrite', default=True)
@click.option('--websites/--no-websites', default=True)
def main(env, lang, overwrite, websites):
    """ Pull translations from translations server """
    loadtrans(env, lang, overwrite, websites)
    

if __name__ == "__main__":  # pragma: no cover
    main()