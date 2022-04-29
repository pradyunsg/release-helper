import sys

import click
from packaging.utils import canonicalize_version
from packaging.version import InvalidVersion, Version


@click.command()
@click.argument("version", required=True)
@click.option("--require-canonical", is_flag=True)
def cmd(version, require_canonical):
    """Ensure a version is a valid PEP 440 version."""
    try:
        parsed_version = Version(version)
    except InvalidVersion:
        click.echo(f"{version!r} is not a valid PEP 440 version.", err=True)
        sys.exit(1)

    if require_canonical:
        canonical_version = canonicalize_version(parsed_version)
        if version != canonical_version:
            click.echo(
                f"{version!r} is not a canonical PEP 440 version "
                f"(should be {canonical_version!r}).",
                err=True,
            )
            sys.exit(1)
