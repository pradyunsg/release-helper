from release_helper.commands.version_bump import cmd


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


def test_with_python_file_custom_var(runner):
    with open("foo.py", "w") as f:
        f.writelines(['"""String!"""\n', 'fun_version = "1.0.0"\n'])
    result = runner.invoke(cmd, ["foo.py", "1.1.0", "--variable-name", "fun_version"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""

    with open("foo.py") as f:
        lines = f.readlines()

    assert lines == [
        '"""String!"""\n',
        'fun_version = "1.1.0"\n',
    ]


def test_with_python_file_no_change(runner):
    with open("foo.py", "w") as f:
        f.writelines(['"""String!"""\n', '__version__ = "1.0.0"\n'])
    result = runner.invoke(cmd, ["foo.py", "1.0.0"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Did not make any changes to the file.\n"

    with open("foo.py") as f:
        lines = f.readlines()

    assert lines == [
        '"""String!"""\n',
        '__version__ = "1.0.0"\n',
    ]


def test_with_unknown_file(runner):
    with open("README.rst", "w") as f:
        f.write("This project is foobar 1.0.0")

    result = runner.invoke(cmd, ["README.rst", "1.1.0"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Don't know what to do for .rst files\n"
