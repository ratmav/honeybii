# cli relative paths

fix. `ish honiipy convert <relative-path>` fails — the wrapper resolves the
path from the wrong directory.

## context

`ish honiipy` runs `uv run honiipy` from the python workspace dir, so a relative
image path resolves there, not the caller's cwd. a valid repo-root-relative
path (e.g. `test/images/snake.jpg`) errors with `cannot read image`. honiipy
itself can't fix this — it can't know the intended base dir; the wrapper must.

## what changes

- the `ish-honiipy` wrapper resolves relative path arguments against the
  caller's cwd before invoking uv — or invokes uv without changing cwd (e.g.
  `uv run --project python honiipy …`) — so relative paths work from any cwd.

## test

- a bats check in the ish-bash suite: from the repo root,
  `ish honiipy convert test/images/<img>.jpg` succeeds (non-empty ascii,
  exit 0), matching the absolute-path output.

## deliverable

`ish honiipy convert <relative path>` works from any directory.
