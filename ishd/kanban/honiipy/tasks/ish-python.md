# ish python dev tooling

feat. add the local ish package that runs honiipy's python dev verbs from the
repo root. this is the dev half of the former ish-honiipy-wrapper task, split
out because — per osai — the dev verbs live under a `python` dispatcher,
separate from the cli pass-through (see ish-honiipy).

## reference (osai)

- `~/Source/osai/ishd/packages/ish-osai/source/osai/python.sh` — the dispatcher:
  help + `case` route to each verb.
- `.../osai/python/{test,lint,fmt,fix}.sh`, `.../osai/python/laconic.sh` — the
  per-verb bodies. each cds the package and runs `uv run ruff` / `uv run
  pytest`; `audit` = lint + test + laconic-against-source.
- osai buries these under `ish osai python`; honeybii has one package and no
  umbrella, so it's a top-level `ish python`.

## what changes

- `ishd/packages/ish-python/source/python.sh` — router (`ish_python_route`,
  `ish_python_help`) mirroring `osai.sh`: help, `case` dispatch, `help|""` and
  unknown-command arms.
- `ishd/packages/ish-python/source/python/<verb>.sh` — one per verb. each checks
  uv, cds `python/honiipy`, runs:
  - lint  -> `uv run ruff check source/honiipy`
  - fmt   -> `uv run ruff format source/honiipy`
  - fix   -> `uv run ruff check --fix source/honiipy`
  - test  -> `uv run pytest` (cov on honiipy, like osai)
  - audit -> lint + test (laconic-against-source later, once laconic is wired
    for honiipy)
- `.ishrc` — add `ish_packages_local=(ish-python)`; fix the gate to
  `ish_kanban_check_agent_audit="ish python audit"` (was `ish honiipy audit`,
  off-pattern: audit is a dev verb, cf. osai's `ish osai python audit`).
- `ishd/packages/ish-python/.shellcheckrc` — `disable=SC1090,SC1091,SC2034`.
- `ishd/packages/ish-python/test/` — bats integration mirroring osai's (no args
  -> help; help lists verbs). vendor osai's bats-support/bats-assert +
  common-setup.

## note

no python tests exist yet — scaffold-honiipy-cli adds the first. so `ish python
test` reports "no tests ran" and `ish python audit` is red until the scaffold
lands. the tooling is real now; the gate goes green with the first test.

## deliverable

`ish python lint|fmt|fix|test|audit` run against `python/honiipy`; the
`ish_kanban_check_agent_audit` gate points at a real command.
