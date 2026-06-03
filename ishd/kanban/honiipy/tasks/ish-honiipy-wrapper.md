# ish honiipy wrapper

feat. add the ish package that wraps `uv run` so the repo root drives the python
package from the outside. mirrors `ish-osai`.

## reference

`~/Source/osai/ishd/packages/ish-osai/source/osai/` — router + per-verb shell
that cd into the package and call uv.

## what changes

- `ishd/packages/ish-honiipy/source/honiipy/honiipy.sh` + verb files — router
  for `run`, `test`, `lint`, `fmt`, `audit`. `audit` = ruff + pytest (+ laconic
  later).
- each verb cds `python/honiipy` and calls `uv run ...` (keep repo-root cwd for
  relative paths, per osai).
- `.ishrc` — add `ish_packages_local=(ish-honiipy)`.
- bats tests under `ishd/packages/ish-honiipy/test/` if following ish-osai.

## deliverable

`ish honiipy run <image>`, `ish honiipy test`, `ish honiipy audit` work. the
`ish_kanban_check_agent_audit="ish honiipy audit"` gate is now real.
