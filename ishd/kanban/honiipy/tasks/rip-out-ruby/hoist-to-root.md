# hoist to root

feat. `python/` existed only to keep the package out of ruby's way. with ruby
gone, honiipy becomes the repo: single-package root, `src/` layout.

## precondition

`delete-ruby` is done — the repo root holds nothing but honiipy and its tooling.

## context

two forces land in the same move, so they are done together rather than in
sequence — each one rewrites the same set of path references, and doing them
apart means touching `python.sh`, `honiipy.sh`, `.ishrc`, `pyproject.toml`, and
`docs/conventions.md` twice.

first, the nesting. `python/` is a uv workspace root with exactly one member.
the workspace only ever bought separation from the ruby tree at the root. one
package needs no workspace — collapse to a single-package root, the shape the
other python packages in this toolchain use.

second, `src/`. laconic's structure check resolves the test mirror with
`mirror_dir`, which raises unless the source directory's parent is named `src`:

```
structure checks need <root>/src/<pkg>; got: .../source/honiipy
```

so `source/honiipy` cannot be structure-checked at all today, and `ish python
audit` exits non-zero on it. renaming to `src/honiipy` puts the mirror check
back in service, with `tests/` at the root where `mirror_dir` expects it.

## what changes

moves, with `git mv` so history follows:

- `python/honiipy/source/honiipy/` -> `src/honiipy/`
- `python/honiipy/tests/` -> `tests/` (fixtures, images, `.gitattributes`)
- `python/honiipy/pyproject.toml` + `python/pyproject.toml` -> one root
  `pyproject.toml`; `python/uv.lock` -> `uv.lock`; delete `python/`

root `pyproject.toml` — merge the two manifests:

- keep `[project]`, `[project.scripts]`, `[build-system]` from the member.
- `[tool.hatch.build.targets.wheel]` — `packages = ["src/honiipy"]`.
- keep `[dependency-groups] dev` and `[tool.pytest.ini_options]` from the
  workspace root.
- drop `[tool.uv.workspace]` entirely.
- `[tool.uv.sources]` — the laconic path loses one level:
  `{ path = "../laconic", editable = true }`. it is `../../laconic` today only
  because the manifest sits under `python/`. verify the depth against
  `~/Source/laconic` rather than trusting this line — laconic is developed
  alongside honiipy and has already moved its package root once.

path references, all of which currently name `python/honiipy` or
`source/honiipy`:

- `ishd/packages/ish-python/source/python.sh` — `_ish_python_root` becomes
  `"${ISH_PROJECT_ROOT}"`, `_ish_python_source` becomes `"src/honiipy"`.
- `ishd/packages/ish-honiipy/source/honiipy.sh` — `_ish_honiipy_root` becomes
  `"${ISH_PROJECT_ROOT}"`. its header comment says the package is reached "via
  --project" as a "workspace member"; there is no workspace after this.
- `.ishrc` — `ish_kanban_context_source="src/honiipy/"` and
  `ish_kanban_context_tests="tests/"`. these are what `/ish-kanban-onboard`
  reads to study the project, so a stale value misdirects every later session.
- `docs/conventions.md` — the two `source/honiipy` references under `size
  discipline`. the `layout` section names no paths by design; leave it alone.
- `ishd/kanban/honiipy/roadmap/honiipy.md` — describes building "under
  `python/honiipy/`" with a `source/honiipy` layout.
- `ishd/packages/ish-bash/test/integration/honiipy.bats` — the relative-path
  test names `python/honiipy/tests/images/snake.jpg`, which becomes
  `tests/images/snake.jpg`.
the three bash edits above are known-temporary. `adopt-poe-tasks` deletes
`ish-python`, `ish-bash`, and `ish-honiipy` outright once the gates move to
poe. repoint them so the repo stays working through the hoist; do not invest
in them beyond that.

laconic gate:

- `ish_python_laconic` keeps running laconic unmodified with every check
  enabled — no `--size`, no flags narrowing what it inspects. `src/honiipy`
  satisfies `mirror_dir`, so the structure pass finally runs here.
- the mirror check exempts only `__init__.py`; `_`-prefixed modules are
  mirrored like anything else. add `tests/test__banner.py` and
  `tests/test__gradients.py`. both modules are already exercised —
  `test_banner_matches_snake_conversion` pins `ART`, and the gradients are
  covered through `test_shading.py` — so these are thin mirrors asserting the
  modules' own surface, not new test design.
- laconic is developed alongside honiipy and its rules move. if the gate fails
  on a rule not described here, laconic changed: adapt honiipy to it. do not
  pin a version, pass a narrowing flag, or fork the checker. see the laconic
  paragraph under `size discipline` in `docs/conventions.md`.

## what stays

- every module, test, and fixture byte for byte. this is a move, not an edit —
  no behavior changes and no fixture regenerates.
- the `__init__.py` façade. `from honiipy import shade` is documented, tested,
  and public.
- the package name `honiipy` and the `honiipy` console script.

## test

- `ish python audit` passes from the repo root. the bash edits are deliberately
  not gated on `ish bash audit`: the wrappers retire wholesale in
  `adopt-poe-tasks` and get no further investment. the `ish honiipy convert`
  check below is what exercises them.
- `ish honiipy convert <some image>` renders, with a relative path resolving
  from the caller's cwd.
- `uv run laconic check --source=src/honiipy` passes with no flags at all —
  size rules and test mirror both.
- `grep -rn "python/honiipy\|source/honiipy" . --exclude-dir=.git
  --exclude-dir=.venv --exclude-dir=kanban` returns nothing. the kanban is
  excluded because task prose quotes the old paths to describe the move.

## deliverable

honiipy is the repo root: `src/honiipy/`, `tests/`, one `pyproject.toml`, no
workspace, no `python/`. laconic's full gate runs against `src/honiipy`.
