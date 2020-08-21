import re
import sys
from pathlib import Path

import click


@click.command()
@click.argument(
    "file",
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
)
@click.argument("version_string", required=True)
def cmd(file, version_string):
    """Bump version in given file.

    If this is a `.py` file, replace the version in a __version__ = "..." assignment.
    If this is a `.txt` file, write the version with a newline into the file.
    Errors out otherwise.
    """
    path = Path(file)
    if path.suffix == ".py":
        # Find and replace the __version__ = "..." line.
        contents = path.read_text()
        new_contents = re.sub(
            '__version__ = "(.+)"', f'__version__ = "{version_string}"', contents
        )
        path.write_text(new_contents)
    elif path.suffix == ".txt":
        path.write_text(version_string + "\n")
    else:
        click.echo(f"Don't know what to do for {path.suffix} files")
        sys.exit(1)
