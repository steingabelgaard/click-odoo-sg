#!/usr/bin/env python
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

import click
import click_odoo

_logger = logging.getLogger(__name__)


def uninstall(env, module_names):
    modules = env["ir.module.module"].search([("name", "in", module_names), ('state', 'in', ['installed','to upgrade'])])
    _logger.info("uninstalling %s", modules.mapped("name"))
    for module in modules:
        if module.state == 'to upgrade':
            module.button_upgrade_cancel()
    modules.button_immediate_uninstall()
    env.cr.commit()


@click.command()
@click_odoo.env_options(with_rollback=False)
@click.option(
    "--modules",
    "-m",
    required=True,
    help="Comma-separated list of modules to uninstall",
)
def main(env, modules):
    module_names = [m.strip() for m in modules.split(",")]
    uninstall(env, module_names)


if __name__ == "__main__":  # pragma: no cover
    main()