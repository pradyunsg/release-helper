"""Plug together the various commands with ``click``."""

import importlib

import click

commands = [
    # File system
    "directory-check-empty",
    # Git
    "git-check-branch",
    "git-check-clean",
    "git-check-remote",
    "git-check-tag",
    # Version handling
    "version-check-validity",
    "version-bump",
]


class _SubpackageMultiCommand(click.MultiCommand):
    def list_commands(self, ctx):
        # This is the ordered list of the commands.
        return commands

    def get_command(self, ctx, name):
        assert name in commands
        identifier = name.replace("-", "_")

        module = importlib.import_module(f"release_helper.commands.{identifier}")
        return module.cmd


def main():
    """Primary entry point from the command line."""
    cli = _SubpackageMultiCommand(name="release=helper", no_args_is_help=True)
    cli()
