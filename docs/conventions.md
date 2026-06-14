# conventions

honiipy is a python port of [honeybii](http://honeybii.com) by jamey deorio — an
image-to-ascii converter. it is built in place inside the honeybii repo and will
replace the ruby gem once it reaches parity. the ruby source under
`lib/honeybii/` is the reference implementation; keep it runnable until parity.

## stack

- python >=3.12, managed with `uv`.
- build backend: hatchling.
- image handling: pillow.
- lint/format: ruff. no black, no mypy.
- tests: pytest, mirroring source one-to-one.

## layout

```
python/                       uv workspace root
  pyproject.toml              workspace + shared dev deps
  honiipy/
    pyproject.toml            package manifest
    source/honiipy/           package code
    tests/                    mirrors source
```

ish, kanban, and the ish wrappers live at the repo root and consume the package
from the outside — build inside out.

## ish wrappers

two local ish packages drive the package from the repo root, split by concern
(osai's consumer-vs-dev pattern, minus the `ish osai` umbrella — honeybii has
one package):

- `ish python <lint|fmt|fix|test|audit>` — dev verbs: ruff / pytest against
  `python/honiipy`. backs the agent audit gate (`ish python audit`).
- `ish honiipy [args]` — consumer pass-through: forwards to the honiipy typer
  cli (`uv run honiipy`).

## reference repos

- `~/Source/osai` — uv workspace + typer CLI + ruff + laconic size checks.
- `~/Source/sylvan` — uv package + conventions doc + argparse CLI.

these are the template. follow them for packaging, cli, and test layout. cli
framework: typer (osai), not argparse (sylvan) — osai's `BannerGroup` gives
banner-on-help, its `CliRunner` tests are a ready template, and typer options
make the later parity-flag validation (`-g 0-3`) trivial.

## size discipline (from laconic)

- files <= 100 lines.
- functions <= 15 lines.
- one `tests/test_X.py` per `source/honiipy/X.py`. `__init__.py` and
  `_`-prefixed modules (e.g. `_banner.py`) are exempt, covered through
  their consumer's test.

## lineage and license

honiipy carries honeybii's mit license forward and credits jamey deorio in the
readme. the name is a homage: honeybii -> honiipy (bee -> python).
