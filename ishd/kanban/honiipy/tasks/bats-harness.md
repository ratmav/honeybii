# bats test harness

feat. stand up the shared bats harness so ish packages have shell tests. split
out of ish-python, which shipped verified by smoke test only — its bats test is
backfilled here.

## why its own task

bats is shared infra: ish-python, ish-honiipy, and any future ish package use
it. no system bats exists, and osai vendors it via git submodules + an
`ish osai bash test` runner — bigger than any single package.

## decide

- layout: per-package (osai puts bats-core + bats-support + bats-assert under
  each package's `test/`) duplicates across ish-python + ish-honiipy; a shared
  repo-level harness vendors once. pick one.
- runner: an `ish bash test`-style verb, or a documented `test/bats/bin/bats`
  invocation.

## reference (osai)

- `~/Source/osai/.gitmodules` — bats-core (`test/bats`), bats-support,
  bats-assert (`test/test_helper/`) as submodules.
- `.../ish-osai/test/test_helper/common-setup.bash` — sets `ISH_BIN`, loads
  bats-support/assert.
- `.../ish-osai/test/integration/osai.bats` — test style: no args → help, help
  lists verbs.

## what changes

- add bats-core + bats-support + bats-assert as submodules (layout per decision).
- a `common-setup` helper and a runner.
- backfill ish-python's bats: `ish python help` lists the verbs; no args → help;
  unknown command → error.

## deliverable

ish-python's router is covered by bats, runnable via a documented command, with
the harness reusable by every ish package. ish-honiipy's bats lands with its own
task.
