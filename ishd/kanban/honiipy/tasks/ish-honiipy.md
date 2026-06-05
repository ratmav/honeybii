# ish honiipy consumer wrapper

feat. add the local ish package that passes the repo root straight through to
the honiipy typer cli. consumer half of the former ish-honiipy-wrapper task —
the dev verbs live under `ish python` (see ish-python).

## precondition

scaffold-honiipy-cli done. `ish honiipy` is a pure pass-through to `uv run
honiipy`, so a `honiipy` script (registered via `[project.scripts]`) must exist
for it to hit. hence this task sits after the scaffold.

## reference (osai)

`~/Source/osai/ishd/packages/ish-osai/source/osai/laconic.sh` (and `sophist.sh`)
— check uv, map a leading `help` to `--help`, then `cd python/<pkg> && uv run
<pkg> "$@"`. nothing but a forward to the typer cli.

## what changes

- `ishd/packages/ish-honiipy/source/honiipy.sh` — `ish_honiipy_route`: check uv;
  if `$1` is `help`, swap to `--help`; `cd python/honiipy && uv run honiipy
  "$@"`. pure pass-through, no sub-verbs.
- `.ishrc` — add `ish-honiipy` to `ish_packages_local` (beside `ish-python`).
- `ishd/packages/ish-honiipy/.shellcheckrc` — `disable=SC1090,SC1091,SC2034`.
- `ishd/packages/ish-honiipy/test/` — bats: `ish honiipy help` / no-args show the
  typer help (cf. osai's `ish osai laconic` tests).

## deliverable

`ish honiipy <image> [opts]` runs the cli; `ish honiipy help` shows its help.
dev tooling stays under `ish python`.
