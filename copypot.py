# Copyright 2023 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64
import os
import re
import subprocess

import click
import click_odoo

from . import gitutils, manifest

LINE_PATTERNS_TO_REMOVE = [
    r'"POT-Creation-Date:.*?"[\n\r]',
    r'"PO-Revision-Date:.*?"[\n\r]',
]

PO_FILE_EXT = ".po"
POT_FILE_EXT = ".pot"


def copy_pot(
    env,
    module,
    addons_dir,
    commit,
    msgmerge_if_new_pot,
    commit_message,
    pot_branch,
):
    addon_name = module.name
    addon_dir = os.path.join(addons_dir, addon_name)
    i18n_path = os.path.join(addon_dir, "i18n")
    pot_filepath = os.path.join(i18n_path, addon_name + POT_FILE_EXT)
    po_filepath = os.path.join(i18n_path, 'da' + PO_FILE_EXT)

    if not os.path.isdir(i18n_path):
        os.makedirs(i18n_path)

    subprocess.call(['git', 'checkout', 'origin/' + pot_branch, '--', pot_filepath])
    subprocess.call(['git', 'checkout', 'origin/' + pot_branch, '--', po_filepath])
    files_to_commit = set()
    files_to_commit.add(pot_filepath)
    files_to_commit.add(po_filepath)
    
    if commit:
        gitutils.commit_if_needed(
            list(files_to_commit),
            commit_message.format(addon_name=addon_name),
            cwd=addons_dir,
        )


@click.command()
@click_odoo.env_options(with_rollback=False, default_log_level="error")
@click.option("--addons-dir", default=".", show_default=True)
@click.option(
    "--modules",
    "-m",
    help="Comma separated list of addons to export translation.",
)
@click.option(
    "--commit / --no-commit",
    show_default=True,
    help="Git commit copied .pot/.po files if needed.",
)
@click.option(
    "--commit-message", show_default=True, default="[UPD] Update {addon_name}.pot"
)
@click.option(
    "--pot-branch", show_default=True, default="15.0-beta", help="Source branch to copy .pot/.po files from"
)
def main(
    env,
    addons_dir,
    modules,
    commit,
    commit_message,
    pot_branch,
):
    """Export translation (.pot) files of addons
    installed in the database and present in addons_dir.
    Check that existing .po file are syntactically correct.
    Optionally, run msgmerge on the existing .po files to keep
    them up to date. Commit changes to git, if any.
    """
    addon_names = [addon_name for addon_name, _, _ in manifest.find_addons(addons_dir)]
    if modules:
        modules = {m.strip() for m in modules.split(",")}
        not_existing_modules = modules - set(addon_names)
        if not_existing_modules:
            raise click.ClickException(
                "Module(s) was not found: " + ", ".join(not_existing_modules)
            )
        addon_names = [
            addon_name for addon_name in addon_names if addon_name in modules
        ]
    if addon_names:
        modules = env["ir.module.module"].search(
            [("state", "=", "installed"), ("name", "in", addon_names)]
        )
        for module in modules:
            copy_pot(
                env,
                module,
                addons_dir,
                commit,
                commit_message,
                pot_branch,
            )


if __name__ == "__main__":
    main()