import sys

import click
from packaging.version import InvalidVersion, Version


@click.command()
@click.argument("version", required=True)
def cmd(version):
    """Ensure a version is a valid PEP 440 version."""
    try:
        Version(version)
    except InvalidVersion:
        click.echo(f"{version!r} is not a valid PEP 440 version.", err=True)
        sys.exit(1)
