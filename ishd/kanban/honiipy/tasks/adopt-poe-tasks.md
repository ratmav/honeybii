# adopt poe tasks

feat. retire the bash dev verbs. honiipy's gates run on python, declared in the
root `pyproject.toml` under poethepoet, modelled on `~/Source/laconic`.

## precondition

`rip-out-ruby/hoist-to-root` is done. poe tasks are declared in the root
`pyproject.toml`, which only exists as a single merged manifest after the hoist.

## context

honiipy's dev gate today is bash. `ishd/packages/ish-python/source/python.sh`
defines `lint`, `fmt`, `fix`, `test`, `laconic`, and an `audit` that runs three
of them and ors a `failed` flag. `.ishrc` names `ish python audit` and
`ish bash audit` as the agent checks. `docs/conventions.md` documents the
`ish python <verb>` surface as the dev interface.

decided: poe replaces those verbs rather than sitting under them, and the bash
packages retire with them. honiipy runs on python entirely — a bash gate needs
shellcheck and bats to police bash that will not exist.

laconic is the reference. read its root `pyproject.toml` before starting:

- an aggregate `dev:check` built from plain refs with
  `ignore_fail = "return_non_zero"`, so every gate runs and all failures report
  rather than stopping at the first. this is the behavior `ish python audit`
  hand-rolls with its `failed` flag.
- per-task `cwd`, set explicitly because an explicit cwd survives poe's ref
  chains where an include's cwd does not.
- gates beyond lint/test: `bandit` for sast, `uv audit` for supply chain.
  honiipy runs neither today; adopt both, matching the reference.

laconic namespaces its tasks (`laconic:dev:lint`) because its repo currently
hosts two packages. honiipy is one package at its own root, so the names stay
flat — `dev:lint`, not `honiipy:dev:lint`.

## what changes

- add `poethepoet` and `bandit` to the dev dependency group.
- declare in the root `pyproject.toml`: `dev:fmt`, `dev:fix`, `dev:lint`,
  `dev:test`, `dev:laconic`, `dev:sast`, `dev:dependencies`, and an aggregate
  `dev:check` over them with `ignore_fail = "return_non_zero"`.
- `dev:laconic` runs `laconic check --source src/honiipy --size`. the structure
  pass is withheld deliberately — see the laconic gate note in
  `rip-out-ruby/hoist-to-root`.
- forwarded path arguments must resolve from the caller's cwd. `dev:test` and
  `dev:laconic` take user-supplied paths, and the bash verbs they replace
  resolved those against the package dir instead — from the repo root,
  `ish python test tests/test_cli.py` looked under `tests/tests/test_cli.py`
  and failed. poe's per-task `cwd` is the declared fix for the same bug; a
  check that a repo-relative path runs the test it names belongs in this task.
- delete `ishd/packages/ish-python/`, `ishd/packages/ish-bash/`, and
  `ishd/packages/ish-honiipy/`.
- delete the bats submodules under `ishd/packages/ish-bash/test/` and their
  `.gitmodules` entries.
- `docs/conventions.md` — replace the `ish wrappers` section with the poe task
  surface. the consumer entry point becomes `uv run honiipy`, not `ish honiipy`.

## what stays

- every gate's behavior. ruff, pytest with branch coverage, and the laconic
  size checks keep their current flags and thresholds; only the declaration
  moves from bash to `pyproject.toml`.
- the `honiipy` console script and the `__init__.py` façade.

## out of scope

`.ishrc` and the kanban board tooling. `ish kanban` is retiring too, on its own
track — this task removes only the three local dev packages. whatever still
reads `.ishrc` keeps working until the board migration lands, so leave the
`ish_kanban_*` variables alone and point `ish_kanban_check_agent_python` at
`uv run poe dev:check`. drop `ish_kanban_check_agent_bash`; there is no bash
left to audit.

## test

- `uv run poe dev:check` runs every gate and reports all failures, not just the
  first.
- from the repo root, `uv run poe dev:test tests/test_cli.py` runs that file.
- `grep -rn "ish python\|ish bash\|ish honiipy" . --exclude-dir=.git` returns
  nothing outside the kanban.

## deliverable

honiipy's dev gates are python, declared in `pyproject.toml`, with no bash
package and no shellcheck or bats dependency.
