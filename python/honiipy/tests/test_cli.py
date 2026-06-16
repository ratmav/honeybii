import pytest
from PIL import Image
from typer.testing import CliRunner

from honiipy import shade
from honiipy._banner import ART
from honiipy.cli import app, main

runner = CliRunner()


def _gradient_image(path) -> None:
    """write a 60x120 left-to-right grayscale ramp (a non-flat image)."""
    img = Image.new("L", (60, 120))
    img.putdata([(x * 255) // 59 for _ in range(120) for x in range(60)])
    img.save(path)


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


def test_convert_matches_core(tmp_path) -> None:
    path = tmp_path / "grad.png"
    _gradient_image(path)
    result = runner.invoke(app, ["convert", str(path)])
    assert result.exit_code == 0
    assert result.stdout == shade(str(path)) + "\n"


def test_convert_pixel_size(tmp_path) -> None:
    path = tmp_path / "grad.png"
    _gradient_image(path)
    result = runner.invoke(app, ["convert", str(path), "--pixel-size", "6"])
    assert result.exit_code == 0
    assert result.stdout == shade(str(path), point_size=6) + "\n"


def test_convert_gradient(tmp_path) -> None:
    path = tmp_path / "grad.png"
    _gradient_image(path)
    result = runner.invoke(app, ["convert", str(path), "--gradient", "2"])
    assert result.exit_code == 0
    assert result.stdout == shade(str(path), gradient=2) + "\n"


def test_convert_one_to_one(tmp_path) -> None:
    path = tmp_path / "grad.png"
    _gradient_image(path)
    result = runner.invoke(app, ["convert", str(path), "--one-to-one"])
    assert result.exit_code == 0
    assert result.stdout == shade(str(path), style="one_to_one") + "\n"


def test_convert_rejects_out_of_range_gradient(tmp_path) -> None:
    path = tmp_path / "grad.png"
    _gradient_image(path)
    result = runner.invoke(app, ["convert", str(path), "--gradient", "5"])
    assert result.exit_code == 2  # typer min/max usage error


def test_convert_missing_image(tmp_path) -> None:
    result = runner.invoke(app, ["convert", str(tmp_path / "nope.png")])
    assert result.exit_code == 1


def test_convert_not_an_image(tmp_path) -> None:
    path = tmp_path / "notimg.png"
    path.write_text("not an image")
    result = runner.invoke(app, ["convert", str(path)])
    assert result.exit_code == 1


def test_convert_flat_relative_errors(tmp_path) -> None:
    path = tmp_path / "flat.png"
    Image.new("L", (48, 48), 128).save(path)
    result = runner.invoke(app, ["convert", str(path)])
    assert result.exit_code == 1  # flat image has no relative range
