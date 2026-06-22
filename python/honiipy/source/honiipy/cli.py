"""honiipy CLI: image-to-ascii converter."""

from pathlib import Path

import typer
from typer.core import TyperGroup

from honiipy import __version__, shade
from honiipy._banner import ART


class BannerGroup(TyperGroup):
    def format_help(self, ctx, formatter) -> None:
        typer.echo(ART)
        super().format_help(ctx, formatter)


app = typer.Typer(
    cls=BannerGroup,
    name="honiipy",
    no_args_is_help=True,
    help="image-to-ascii converter.",
)


@app.callback()
def _main() -> None:
    """image-to-ascii converter."""


def _render(image: Path, pixel_size: int, gradient: int, one_to_one: bool) -> None:
    """Convert an image and echo the ascii, or a clear error and exit 1."""
    style = "one_to_one" if one_to_one else "relative"
    try:
        art = shade(image, point_size=pixel_size, gradient=gradient, style=style)
    except OSError:  # missing, corrupt, truncated, permission, directory, ...
        typer.echo(f"error: cannot read image: {image}", err=True)
        raise typer.Exit(1)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(art)


@app.command()
def convert(
    image: Path = typer.Argument(..., help="image to convert."),
    pixel_size: int = typer.Option(12, "--pixel-size", help="pixels per column."),
    gradient: int = typer.Option(0, "--gradient", min=0, max=3, help="ramp 0-3."),
    one_to_one: bool = typer.Option(False, "--one-to-one", help="full 0-255 range."),
) -> None:
    """Convert an image to shaded ascii."""
    _render(image, pixel_size, gradient, one_to_one)


@app.command()
def version() -> None:
    """Print the honiipy version."""
    typer.echo(__version__)


def main() -> None:
    """Entry point for `uv run honiipy`."""
    app()
