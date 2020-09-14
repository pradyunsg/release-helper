import subprocess
import sys

import click


@click.command()
@click.argument("name")
@click.option("--exists/--does-not-exist", required=True)
def cmd(name, exists):
    """Check that given tag (does not) exist."""
    result = subprocess.run(
        ["git", "show-ref", "--tags", "--quiet", "--verify", "--", f"refs/tags/{name}"],
        capture_output=True,
        encoding="utf-8",
    )

    if exists and result.returncode:
        click.echo(f"Expected tag {name!r} to exist.", err=True)
        sys.exit(1)
    elif not exists and not result.returncode:
        click.echo(f"Expected tag {name!r} to not exist.", err=True)
        sys.exit(1)
