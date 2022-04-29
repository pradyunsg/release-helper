import sys
from unittest import mock

import pytest
from release_helper import __main__, commands


@pytest.mark.parametrize("command", commands.commands)
def test_all_declared_commands_can_be_imported(command: str) -> None:
    __import__(f"release_helper.commands.{command.replace('-', '_')}")


def test_main_exposes_all_commands(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        with mock.patch("sys.argv", [sys.argv[0]]):
            commands.main()

    result = capsys.readouterr()
    for command in commands.commands:
        assert command in result.out


def test_main_from_dunder_main_is_commands_main():
    assert __main__.main is commands.main
