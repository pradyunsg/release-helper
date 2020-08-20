from click.testing import CliRunner
from pytest import fixture

from release_helper.commands.version_check_validity import cmd


@fixture(scope="function")
def runner():
    value = CliRunner(mix_stderr=False)
    with value.isolated_filesystem():
        yield value


def test_with_valid(runner):
    result = runner.invoke(cmd, ["1.0"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_with_invalid(runner):
    result = runner.invoke(cmd, ["fluffy"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "'fluffy' is not a valid PEP 440 version.\n"
