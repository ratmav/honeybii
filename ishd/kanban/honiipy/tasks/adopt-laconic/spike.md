# adopt laconic — spike

spike. decide how to install laconic into this project and wire it into the
python audit toolchain. output: a recommended approach, an updated
`docs/conventions.md`, and execution subtasks on the board. no code.

## goal

laconic enforces the size discipline `docs/conventions.md` states today as
guidelines (files <= 100 lines, functions <= 15, one `tests/test_X.py` per
`source/honiipy/X.py`; `__init__` and `_`-prefixed modules exempt). adopt it
so:

- `ish python laconic` runs laconic against `python/honiipy`, and
- `ish python audit` runs laconic alongside ruff lint/format and pytest.

## context

- laconic lives at `~/Source/laconic` — its own repo and python package, not on
  pypi yet, present on local disk. it is a separate project: read it to learn
  its cli and packaging, but never modify its repo, git, or plan.
- prior art: `~/Source/osai` already uses laconic size checks (see
  `docs/conventions.md`). study how osai depends on laconic and how its
  toolchain invokes it, then adapt that here.
- the wrapper to extend is the bash package `ishd/packages/ish-python/`
  (verbs lint/fmt/fix/test/audit; bats tests under that package).
- workspace dev deps live in `python/pyproject.toml` (`[dependency-groups]`).

## questions to resolve (one at a time)

1. install: depend on a local, non-pypi package with uv — path dependency,
   `[tool.uv.sources]`, editable? what happens where laconic is absent (other
   machines, CI)? options and tradeoffs.
2. cli surface: laconic's entry point, what it checks, and how its limits are
   set. do its defaults match our conventions, or do we configure them?
3. wiring: how `ish python laconic` invokes laconic, and where it slots into
   `ish python audit` (order, and gating on failure).
4. baseline: does the current `python/honiipy` already pass laconic? if not,
   the execution subtasks must include the fixes.

## deliverables

- present findings and options; the user decides scope.
- capture the chosen rules and rationale in `docs/conventions.md`.
- create the execution subtasks under `adopt-laconic/` (e.g. dependency +
  `ish python laconic` verb + `ish python audit` wiring + bats tests; docs).
- delete this spike file once its implementation tasks are on the board.
