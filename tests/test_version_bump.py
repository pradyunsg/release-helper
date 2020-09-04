from release_helper.commands.version_bump import cmd


def test_with_python_file(runner):
    with open("foo.py", "w") as f:
        f.writelines(['"""String!"""\n', '__version__ = "1.0.0"\n'])
    result = runner.invoke(cmd, ["foo.py", "1.1.0"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""

    with open("foo.py") as f:
        lines = f.readlines()

    assert lines == [
        '"""String!"""\n',
        '__version__ = "1.1.0"\n',
    ]


def test_with_txt_file(runner):
    with open("version.txt", "w") as f:
        f.write("1.0.0")

    result = runner.invoke(cmd, ["version.txt", "1.1.0"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""

    with open("version.txt") as f:
        contents = f.read()

    assert contents == "1.1.0\n"
