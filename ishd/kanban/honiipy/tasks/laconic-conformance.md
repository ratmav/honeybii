# laconic conformance

feat. honiipy predates most of laconic's rules. make the gate pass.

## precondition

`rip-out-ruby/hoist-to-root` is done — the package is at `src/honiipy` and
laconic's full gate runs against it.

## context

laconic is the authority. run it, read the rule doc it names, fix, run again,
until it is silent. nothing about its rules or its findings is restated here:
`~/Source/laconic/docs/rules/` is the reference, and `~/Source/laconic` itself
is the worked example, since it passes its own gate.

expect a package restructure, not a tidy-up.

## decisions

two calls laconic cannot make for honiipy:

- **adapt, never work around.** where a rule conflicts with an existing choice,
  the rule wins. the façade rule retires `from honiipy import shade` in favour
  of `honiipy.shading.shade` — update `docs/shading.md`, `README.md`, and the
  tests rather than reshaping the package to keep the old surface alive.
- **the banner is data, not api.** the cli cannot import past the public
  surface, and publishing the banner through the façade to satisfy that would
  put an implementation detail in the public api. make it a resource file read
  with `importlib.resources`, as laconic does with its own, and make sure the
  wheel ships it.

## what stays

- every algorithm. `shade` and the pipeline behave identically and no fixture
  regenerates — a diff in `tests/fixtures/*.txt` means something broke.
- the `honiipy` console script name and its cli flags.

## test

- `uv run laconic check --source=src/honiipy` reports nothing, no flags.
- `ish python audit` passes.
- `ish honiipy convert <image>` renders, and `honiipy --help` still shows the
  banner.

## deliverable

laconic runs and passes.
