"""Plug together the various commands with ``click``."""

import importlib

import click

commands = [
    "directory-check-empty",
    # Git
    "git-check-branch",
    "git-check-working-directory",
    "git-check-not-a-tag",
    "git-check-remote",
    "git-generate-authors",
    # The most important thing.
    "version-check-validity",
    "version-bump",
    # Related-files' content handling
    "file-add-heading",
    "file-change-heading",
]
# TODO: add a test to check that all these commands actually exist.


class SubpackageMultiCommand(click.MultiCommand):
    def list_commands(self, ctx):
        # This is the ordered list of the commands.
        return commands

    def get_command(self, ctx, name):
        assert name in commands
        identifier = name.replace("-", "_")

        module = importlib.import_module(f"release_helper.commands.{identifier}")
        return module.cmd


def main():
    cli = SubpackageMultiCommand(name="release=helper", no_args_is_help=True)
    cli()
