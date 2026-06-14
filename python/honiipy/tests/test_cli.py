import pytest
from typer.testing import CliRunner

from honiipy._banner import ART
from honiipy.cli import app, main

runner = CliRunner()


def test_main_invokes_app() -> None:
    """main() is the console_scripts entry — typer parses sys.argv and exits."""
    with pytest.raises(SystemExit):
        main()


def test_no_args_shows_help() -> None:
    result = runner.invoke(app, [])
    assert "Usage" in result.output
    assert ART.strip() in result.output


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "honiipy" in result.stdout


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.0.0" in result.stdout
