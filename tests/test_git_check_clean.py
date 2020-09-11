from pathlib import Path

import pytest

from release_helper.commands.git_check_clean import cmd


@pytest.mark.parametrize("staged", [True, False])
@pytest.mark.parametrize("unstaged", [True, False])
def test_command(runner, git, *, staged, unstaged):
    git("commit", "--allow-empty", "-m", "Root Commit")
    if staged:
        Path("staged.txt").write_text("")
        git("add", "staged.txt")

    if unstaged:
        Path("unstaged.txt").write_text("")

    result = runner.invoke(cmd)

    print("stdout:", repr(result.stdout))
    print("stderr:", repr(result.stderr))

    if staged or unstaged:
        assert result.exit_code == 1
        assert result.stdout == ""
        assert result.stderr == "git working directory/index is not clean.\n"
    else:
        assert result.exit_code == 0
        assert result.stdout == ""
        assert result.stderr == ""
