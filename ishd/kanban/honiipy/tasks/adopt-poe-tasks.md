# adopt poe tasks

spike. decided in direction: honiipy adopts a poethepoet task setup modelled on
`~/Source/laconic`. open question is how poe and the ish wrappers compose.

## precondition

`rip-out-ruby/hoist-to-root` is done. poe tasks are declared in the root
`pyproject.toml`, which only exists as a single merged manifest after the hoist.

## context

honiipy's dev gate today is bash. `ishd/packages/ish-python/source/python.sh`
defines `lint`, `fmt`, `fix`, `test`, `laconic`, and an `audit` that runs three
of them and ors a `failed` flag. `.ishrc` names `ish python audit` and
`ish bash audit` as the agent checks, and `docs/conventions.md` documents the
`ish python <verb>` surface as the dev interface.

laconic puts the same orchestration in `pyproject.toml` under poe. worth reading
before deciding anything — its root manifest is the reference:

- namespaced per-package tasks (`laconic:dev:lint`, `laconic:dev:test`, ...)
  with an explicit per-task `cwd`, chosen because an explicit cwd survives poe's
  ref chains where an include's cwd does not.
- an aggregate `dev:check` built from plain refs with
  `ignore_fail = "return_non_zero"`, so every gate runs and all failures report
  rather than stopping at the first. this is the behavior `ish python audit`
  hand-rolls with its `failed` flag.
- gates that do not belong to a package (its supply-chain audit, its reference
  tooling test) sitting at the workspace root alongside the member gates.

honiipy is a single package, so the namespacing and cwd machinery are laconic's
answer to a problem honiipy does not have. what carries over is the task table
and the aggregate-gate semantics, not the layout.

## questions

one at a time, per the spike workflow.

1. does poe replace the `ish python` verbs, or sit under them? three shapes:
   poe as the gate with `ish python <verb>` as thin pass-throughs; poe replacing
   `ish python` outright, with `.ishrc` agent checks pointing at
   `uv run poe dev:check`; or no poe, keeping bash. each changes what
   `docs/conventions.md` documents as the dev interface.
2. which gates does honiipy want that it does not have? laconic runs `bandit`
   for sast and `uv audit` for supply chain; honiipy runs neither.
3. what happens to `ish bash audit`? the ish sources are bash and poe is python
   tooling. if poe takes the python gate, bash keeps its own, and the project
   has two gate systems — acceptable or not is the call.

## interaction

`python-wrapper-relative-paths` fixes cwd handling in `ish python test` and
`ish python laconic`. if question 1 resolves toward poe replacing those verbs,
that task is moot and should be closed rather than executed — poe's per-task
`cwd` is the same mechanism, declared instead of scripted. resolve this spike
before starting it. it is slotted after this task for that reason.

`rip-out-ruby/hoist-to-root` pins `ish_python_laconic` to `--size` because
laconic's structure pass fails on honiipy's non-empty `__init__.py`. whatever
runs the gate inherits that constraint until laconic offers an escape.

## deliverable

the composition question is answered and written into `docs/conventions.md`, the
follow-on implementation tasks are on the board, and this file is deleted.
