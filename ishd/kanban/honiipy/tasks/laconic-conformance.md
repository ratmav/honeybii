# laconic conformance

feat. honiipy predates most of laconic's rules. bring the package to the shape
the gate demands.

## precondition

`rip-out-ruby/hoist-to-root` is done — the package is at `src/honiipy` and
laconic's full gate runs against it.

## context

laconic grew from size + structure into an architectural linter with eleven
numbered rules, documented one file each under `~/Source/laconic/docs/rules/`.
honiipy runs it unmodified with every check enabled, so the whole rule set
applies. the gate currently reports 29 findings in seven categories:

| rule | finding | count |
|------|---------|-------|
| laconic-4 | `MISSING` — module without a test mirror | 2 |
| laconic-6 | `UNIMPORTED` — `__all__` lists a name the file does not import | 1 |
| laconic-7 | `EXPOSED` — module the façade never touches, outside `_internal/` | 3 |
| laconic-8 | `ORDER` — public name defined after a private one | 7 |
| laconic-9 | `REACH` — cli imports past the package's public surface | 1 |
| laconic-10 | `UNLISTED` — public module lacks its own `__all__` entry | 15 |
| laconic-11 | `LEAF EXPORT` — façade binds a name, not a module | 1 |

read the rule docs before starting; the checker is the authority and each doc
quotes its literal output. `~/Source/laconic` is also the worked example — it
passes its own gate, so its package is the target shape rather than a guess.

### the api changes

laconic-11 is the consequential one: a façade may only do
`from . import <module>`. `from honiipy import shade` becomes
`honiipy.shading.shade(...)`. this reverses the top-level import surface the
project chose earlier, and it is the price of running laconic unmodified.
callers to update: `docs/shading.md`'s opening example, `tests/test_cli.py`,
and the cli itself.

### the banner

laconic-9 stops the cli importing anything the package's `__all__` does not
offer, so `from honiipy._banner import ART` has to go. laconic hit the same
problem and answered it by storing its banner as a `.txt` data file read
through `importlib.resources`, not as a module — a resource is not an import,
so the rule does not apply. follow that: `ART` becomes
`src/honiipy/_internal/banner.txt`.

the alternative — publishing the banner through the façade — would put an
implementation detail in the public api to satisfy a lint. do not.

## what changes

package shape, mirroring `~/Source/laconic/src/laconic`:

- `src/honiipy/_internal/` — new, with `__init__.py`.
- `cli.py` and `_gradients.py` move into it. inside `_internal/` the folder is
  the marking, so the underscore prefix goes: `_gradients.py` becomes
  `_internal/gradients.py`.
- `_banner.py` becomes `_internal/banner.txt`, holding the art alone. the cli
  reads it with `importlib.resources`. ensure hatch ships it.
- `shading.py` stays at the top level — the façade draws from it.
- `src/honiipy/__init__.py` — docstring, `from . import shading`,
  `__all__ = ["shading"]`. nothing else.
- `__version__` leaves the façade; laconic-6 permits only imported names.
  `importlib.metadata.version("honiipy")` in the cli replaces it.
- `[project.scripts]` — `honiipy = "honiipy._internal.cli:main"`.

per-module:

- `shading.py` — add `__all__` naming its public surface, and move
  `_round_half_up`, `_indexer`, and `_join_rows` below every public function
  (laconic-8, laconic-10).
- `_internal/cli.py` — import `from honiipy import shading` and nothing
  first-party beyond it. re-check `ORDER` after the move.

tests, mirroring `~/Source/laconic/tests`:

- `tests/__init__.py` and `tests/_internal/__init__.py`.
- `tests/test_shading.py` stays.
- `tests/_internal/test_cli.py` — `test_cli.py` moves here.
- `tests/_internal/test_gradients.py` — new.
- the banner is a resource, not a module, so it needs no mirror. keep the
  existing assertion that the shipped art equals a live conversion of
  `tests/images/snake.jpg`; it is the only thing pinning the two together.

docs:

- `docs/shading.md` — the opening example and any `from honiipy import shade`.
- `README.md` — check the usage block for the same.

## what stays

- every algorithm. this is a packaging and surface change; `shade` and the
  pipeline behave identically and no fixture regenerates.
- `tests/fixtures/*.txt` byte for byte. a fixture diff means something changed
  that should not have.
- the `honiipy` console script name and its cli flags.

## test

- `uv run laconic check --source=src/honiipy` reports nothing, no flags.
- `ish python audit` passes.
- `ish honiipy convert <image>` renders, and `honiipy --help` still shows the
  banner.
- `python -c "import honiipy; honiipy.shading.shade"` resolves; the old
  `from honiipy import shade` is expected to fail.

## deliverable

honiipy passes laconic's full rule set with no flags and no suppressions.
