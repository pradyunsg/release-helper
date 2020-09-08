from release_helper.commands.git_check_tag import cmd


def test_exists_with_required_tag(runner, git):
    git("commit", "--allow-empty", "-m", "Root Commit")
    git("tag", "root")

    result = runner.invoke(cmd, ["root", "--exists"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_exists_with_missing_tag(runner, git):
    git("commit", "--allow-empty", "-m", "Root Commit")

    result = runner.invoke(cmd, ["root", "--exists"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Expected tag 'root' to exist.\n"


def test_does_not_exist_with_required_tag(runner, git):
    git("commit", "--allow-empty", "-m", "Root Commit")
    git("tag", "root")

    result = runner.invoke(cmd, ["root", "--does-not-exist"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Expected tag 'root' to not exist.\n"


def test_does_not_exist_with_missing_tag(runner, git):
    git("commit", "--allow-empty", "-m", "Root Commit")

    result = runner.invoke(cmd, ["root", "--does-not-exist"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""
