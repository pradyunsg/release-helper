import subprocess
import sys

import click


def _is_clean():
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, encoding="utf-8",
    )
    return result.stdout.strip() == ""


@click.command()
def cmd():
    """Check that the repository is in a clean state."""
    if not _is_clean():
        click.echo("git working directory/index is not clean.", err=True)
        sys.exit(1)
