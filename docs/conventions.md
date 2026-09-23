# conventions

## stack

- python >=3.12, managed with `uv`.
- build backend: hatchling.
- image handling: pillow.
- lint/format: ruff. no black, no mypy.
- tests: pytest, mirroring source one-to-one.

## layout

build inside out: honiipy is a self-contained python package, and ish, kanban,
and the wrappers sit outside it and consume it like any other caller.

docs do not restate directory trees, file listings, or code. the repo already
says that, and a second copy only drifts out of sync. document intent and the
reasoning behind it; let the source answer the rest.

## ish wrappers

three local ish packages drive the package from the repo root, split by concern:

- `ish python <lint|fmt|fix|test|laconic|audit>` — python dev verbs: ruff /
  pytest / laconic against `python/honiipy`. backs the agent audit gate
  (`ish python audit`).
- `ish bash <lint|fmt|fix|test|audit>` — bash dev verbs: shellcheck / shfmt /
  bats against the ish wrapper sources. backs the agent audit gate
  (`ish bash audit`); bats vendored under `ishd/packages/ish-bash/test/` as
  git submodules.
- `ish honiipy [args]` — consumer pass-through: forwards to the honiipy typer
  cli (`uv run honiipy`).

## size discipline (from laconic)

- files <= 100 lines.
- functions <= 15 lines.
- one `tests/test_X.py` per `source/honiipy/X.py`. only `__init__.py` is
  exempt; `_`-prefixed modules are mirrored like anything else, so marking a
  module internal cannot quietly drop its test requirement.

`ish python laconic` enforces these against `source/honiipy` (size +
structure), and `ish python audit` runs it alongside ruff and pytest — so the
rules above are gated, not just guidance.

laconic runs unmodified, with every check it offers enabled: no flags narrowing
what it inspects, no pinned version, no local fork. it is developed alongside
honiipy, so its rules move. when they do, the gate fails here and honiipy
adapts — the rules above describe laconic's current behavior, not a contract
with it.
