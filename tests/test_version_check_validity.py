from release_helper.commands.version_check_validity import cmd


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
