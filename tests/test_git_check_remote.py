from release_helper.commands.git_check_remote import cmd


def test_fails_on_no_urls(runner, git):
    result = runner.invoke(cmd, ["upstream"])

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == "FATAL: Got no URLs.\n"


def test_fails_on_missing_remote(runner, git):
    result = runner.invoke(cmd, ["upstream", "https://pradyunsg.me/repo.git"])

    assert result.exit_code == 3
    assert result.stdout == ""
    assert result.stderr.endswith("FATAL: git did not exit cleanly.\n")


def test_fails_on_single_url_that_does_not_match(runner, git):
    git("remote", "add", "upstream", "https://pradyunsg.me/not-repo.git")

    result = runner.invoke(cmd, ["upstream", "https://pradyunsg.me/repo.git"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "git remote 'upstream' does not include any URL from:\n"
        "- https://pradyunsg.me/repo.git\n"
    )


def test_fails_on_multiple_url_that_do_not_match(runner, git):
    git("remote", "add", "upstream", "https://pradyunsg.me/not-repo.git")

    result = runner.invoke(
        cmd,
        [
            "upstream",
            "https://pradyunsg.me/repo.git",
            "https://pradyunsg.me/repo-alt.git",
        ],
    )

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "git remote 'upstream' does not include any URL from:\n"
        "- https://pradyunsg.me/repo.git\n"
        "- https://pradyunsg.me/repo-alt.git\n"
    )


def test_succeeds_on_multiple_urls_match(runner, git):
    git("remote", "add", "upstream", "https://pradyunsg.me/repo.git")

    result = runner.invoke(
        cmd,
        [
            "upstream",
            "https://pradyunsg.me/repo.git",
            "https://pradyunsg.me/repo-alt.git",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_succeeds_on_single_url_match(runner, git):
    git("remote", "add", "upstream", "https://pradyunsg.me/repo.git")

    result = runner.invoke(cmd, ["upstream", "https://pradyunsg.me/repo.git"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_succeeds_on_single_url_match_from_multiple(runner, git):
    git("remote", "add", "upstream", "https://pradyunsg.me/repo.git")
    git("remote", "set-url", "--add", "upstream", "https://pradyunsg.me/another.git")

    result = runner.invoke(cmd, ["upstream", "https://pradyunsg.me/repo.git"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""
