# Copyright 2023 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import click
import click_odoo
from click_odoo_contrib.update import _save_installed_checksums


@click.command()
@click_odoo.env_options(
    with_rollback=False,
)
@click.option(
    "--ignore-addons",
    help=(
        "A comma-separated list of addons to ignore. "
        "These will not be updated if their checksum has changed. "
        "Use with care."
    ),
)
def main(
    env,
    ignore_addons,
):
    """ Save module checksums """
    _save_installed_checksums(env.cr, ignore_addons)

if __name__ == "__main__":  # pragma: no cover
    main()
