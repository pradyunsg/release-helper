"""Ensure a directory is empty, if it exists."""

import os
import shutil
import sys

import click


def _delete_contents(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def _handle_one(path, delete):
    if not os.path.exists(path):
        return

    if not os.path.isdir(path):
        return "is not a directory"

    contents = os.listdir(path)
    if not contents:  # nothing inside, all OK
        return

    if not delete:  # this has files, and not supposed to delete them.
        return "is not empty"

    _delete_contents(path)


@click.command()
@click.option(
    "--delete",
    is_flag=True,
    default=False,
    help="Delete the contents of given directories, if non-empty.",
)
@click.argument("directories", required=True, nargs=-1)
def cmd(directories, delete):
    """Ensure a directory is empty, if it exists."""
    issues = []
    for path in directories:
        reason = _handle_one(path, delete)
        if reason is not None:
            issues.append((path, reason))

    if issues:
        for path, reason in issues:
            click.echo(f"{path} {reason}.", err=True)
        sys.exit(1)
