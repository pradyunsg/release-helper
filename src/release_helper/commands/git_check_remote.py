import subprocess
import sys

import click


@click.command()
@click.argument("name")
@click.argument("urls", nargs=-1)
def cmd(name, urls):
    """Check remote includes given URL(s)."""
    if not urls:
        click.echo("FATAL: Got no URLs.", err=True)
        sys.exit(2)

    result = subprocess.run(
        ["git", "remote", "get-url", "--push", name],
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode:
        click.echo(result.stdout, nl=False)
        click.echo(result.stderr, nl=False, err=True)
        click.echo("FATAL: git did not exit cleanly.", err=True)
        sys.exit(3)

    got_urls = result.stdout.rstrip().splitlines()

    if not (set(got_urls) & set(urls)):
        formatted_urls = "\n- " + "\n- ".join(urls)
        click.echo(
            f"git remote {name!r} does not include any URL from:{formatted_urls}",
            err=True,
        )
        sys.exit(1)
