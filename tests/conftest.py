import inspect
import subprocess

from click.testing import CliRunner
from pytest import fixture


@fixture(scope="function")
def runner():
    options = (
        {"mix_stderr": False}
        if "mix_stderr" in inspect.signature(CliRunner).parameters
        else {}
    )
    value = CliRunner(**options)
    with value.isolated_filesystem():
        yield value


@fixture(scope="function")
def git():
    def git_run(*args, **kwargs):
        cmd = ["git"] + list(args)
        return subprocess.run(cmd, check=True)

    git_run("init")
    return git_run
