from click.testing import CliRunner
from pytest import fixture


@fixture(scope="function")
def runner():
    value = CliRunner(mix_stderr=False)
    with value.isolated_filesystem():
        yield value
