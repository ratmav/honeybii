"""honiipy CLI: image-to-ascii converter."""

import typer
from typer.core import TyperGroup

from honiipy import __version__
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


@app.command()
def version() -> None:
    """Print the honiipy version."""
    typer.echo(__version__)


def main() -> None:
    """Entry point for `uv run honiipy`."""
    app()
