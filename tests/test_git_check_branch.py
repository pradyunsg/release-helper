from release_helper.commands.git_check_branch import cmd


def test_fails_on_no_repo(runner):
    result = runner.invoke(cmd, ["main"])

    assert result.exit_code == 3
    assert result.stdout == ""
    assert result.stderr == "FATAL: git did not exit cleanly.\n"


def test_fails_when_not_given_branch_name(runner):
    result = runner.invoke(cmd, [])

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr != ""  # make sure click said something.


def test_fails_when_branch_has_no_commits(runner, git):
    git("checkout", "-b", "main")

    result = runner.invoke(cmd, ["main"])

    assert result.exit_code == 3
    assert result.stdout == ""
    assert result.stderr == "FATAL: git did not exit cleanly.\n"


def test_fails_when_branch_does_not_match(runner, git):
    git("checkout", "-b", "somethingelse")
    git("commit", "--allow-empty", "-m", "root commit")

    result = runner.invoke(cmd, ["main"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Branch name check failed: 'main' != 'somethingelse'\n"


def test_succeeds_when_branch_matches(runner, git):
    git("checkout", "-b", "main")
    git("commit", "--allow-empty", "-m", "root commit")

    result = runner.invoke(cmd, ["main"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""
