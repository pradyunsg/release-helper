import subprocess
import sys

import click


@click.command()
@click.argument("name")
def cmd(name):
    """Check current branch's name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode:
        click.echo(result.stdout, nl=False)
        click.echo(result.stderr, nl=False, err=True)
        click.echo("FATAL: git did not exit cleanly.", err=True)
        sys.exit(3)

    got = result.stdout.rstrip()
    if name != got:
        click.echo(f"Branch name check failed: {name!r} != {got!r}", err=True)
        sys.exit(1)
