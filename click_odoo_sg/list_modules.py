#!/usr/bin/env python
# Copyright 2021 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

import click
import click_odoo

_logger = logging.getLogger(__name__)


def list_modules(env, states):
    modules = env["ir.module.module"].search([('state', 'in', states)])
    for module in modules:
        _logger.info("%s: %s %s", module.name, module.state, module.installed_version)

@click.command()
@click_odoo.env_options(with_rollback=False)
@click.option(
    "--states",
    "-s",
    default='installed',
    help="Comma-separated list of modulestates to list",
)
def main(env, states):
    module_names = [m.strip() for m in modules.split(",")]
    uninstall(env, module_names)


if __name__ == "__main__":  # pragma: no cover
    main()