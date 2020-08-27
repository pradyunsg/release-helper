from pathlib import Path

from release_helper.commands.directory_check_empty import cmd


def test_with_does_not_exist(runner):
    result = runner.invoke(cmd, ["folder"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_with_file(runner):
    Path("file").write_text("I exist.\n")

    result = runner.invoke(cmd, ["file"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "file is not a directory.\n"


def test_with_empty(runner):
    Path("folder").mkdir()

    result = runner.invoke(cmd, ["folder"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_with_non_empty_with_one_file(runner):
    Path("folder").mkdir()
    Path("folder/file.txt").write_text("I exist.\n")

    result = runner.invoke(cmd, ["folder"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "folder is not empty.\n"


def test_with_non_empty_with_one_file_and_delete(runner):
    Path("folder").mkdir()
    Path("folder/file.txt").write_text("I exist.\n")

    result = runner.invoke(cmd, ["folder", "--delete"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert not Path("folder/file.txt").exists()


def test_with_non_empty_with_many_files(runner):
    Path("folder").mkdir()
    Path("folder/file.txt").write_text("I exist.\n")
    Path("folder/file2.txt").write_text("And me too.\n")

    result = runner.invoke(cmd, ["folder"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "folder is not empty.\n"


def test_with_two_empty_directories(runner):
    Path("folder-1").mkdir()
    Path("folder-2").mkdir()

    result = runner.invoke(cmd, ["folder-1", "folder-2"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_with_four_directories_with_two_non_empty(runner):
    Path("folder-1").mkdir()
    Path("folder-2").mkdir()
    Path("folder-3").mkdir()
    Path("folder-1/file.txt").write_text("I exist.\n")
    Path("folder-3/file.txt").write_text("I exist.\n")

    result = runner.invoke(cmd, ["folder-1", "folder-2", "folder-3", "folder-4"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == ("folder-1 is not empty.\n" "folder-3 is not empty.\n")
