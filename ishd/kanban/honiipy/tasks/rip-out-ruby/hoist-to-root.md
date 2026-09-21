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
  `{ path = "../laconic/laconic", editable = true }`. it is
  `../../laconic/laconic` today only because the manifest sits under `python/`.

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
- `docs/conventions.md` — the layout tree in the `layout` section, and the two
  `source/honiipy` references under `size discipline`.
- `ishd/kanban/honiipy/roadmap/honiipy.md` — describes building "under
  `python/honiipy/`" with a `source/honiipy` layout.
the three bash edits above are known-temporary. `adopt-poe-tasks` deletes
`ish-python`, `ish-bash`, and `ish-honiipy` outright once the gates move to
poe. repoint them so the repo stays working through the hoist; do not invest
in them beyond that.

laconic gate:

- `ish_python_laconic` runs `laconic check --source=... --size` for now.
  laconic's structure pass is all-or-nothing: `_run_structure` runs the test
  mirror check *and* `check_init_empty`, which fails on any non-empty
  `__init__.py`. honiipy is a library with a cli over the top, and
  `src/honiipy/__init__.py` is its public surface — it re-exports `shade` and
  defines `__version__`, consumed by `cli.py`, the tests, and the first code
  block in `docs/shading.md`. satisfying that check means deleting shipped api,
  so the size rules stay gated and the mirror rule reverts to convention until
  laconic offers an escape.
- `docs/conventions.md` `size discipline` — say plainly that the mirror rule is
  convention, not gated, and why. an ungated rule documented as gated is worse
  than an ungated rule.

## what stays

- every module, test, and fixture byte for byte. this is a move, not an edit —
  no behavior changes and no fixture regenerates.
- the `__init__.py` façade. `from honiipy import shade` is documented, tested,
  and public.
- the package name `honiipy` and the `honiipy` console script.

## test

- `ish python audit` passes from the repo root. there is no bash gate —
  shellcheck is not installed and `ish bash audit` retires with the wrappers,
  so the `ish honiipy convert` check below is what exercises the bash edits.
- `ish honiipy convert <some image>` renders, with a relative path resolving
  from the caller's cwd.
- `uv run laconic check --source=src/honiipy --size` passes; without `--size`
  it reports the `__init__.py` violation, as expected.
- `grep -rn "python/honiipy\|source/honiipy" . --exclude-dir=.git
  --exclude-dir=.venv` returns nothing.

## deliverable

honiipy is the repo root: `src/honiipy/`, `tests/`, one `pyproject.toml`, no
workspace, no `python/`. laconic's size gate runs against `src/honiipy`.
