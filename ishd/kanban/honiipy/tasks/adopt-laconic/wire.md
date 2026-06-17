# adopt laconic — wire

feat. wire laconic's size + structure checks into the python toolchain, per
the spike. laconic already passes honiipy's current source (baseline green),
so no source fixes are needed.

## install

add laconic as an editable uv path dependency in `python/pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=7.1.0",
    "ruff>=0.15.9",
    "laconic",
]

[tool.uv.sources]
laconic = { path = "../../laconic", editable = true }
```

local until laconic lands on pypi — then drop the `[tool.uv.sources]` entry.
run `uv sync` and confirm `uv run laconic` resolves the cli.

## ish python laconic

add a `laconic` verb to `ishd/packages/ish-python/` that runs both checks
against honiipy's source:

```
uv run laconic check --source=source/honiipy
```

run it from the python workspace like the other verbs. laconic runs size +
structure by default and exits non-zero on any violation.

## ish python audit

add laconic as a gating step in the `audit` verb, beside ruff lint/format and
pytest — audit fails if lint, format, test, OR laconic fail. mirror osai's
`ishd/packages/ish-osai/source/osai/python/audit.sh` pattern.

## tests + docs

- bats tests for the `laconic` verb and the audit wiring, under the ish-python
  package's test dir (the user runs `ish bash audit`).
- `docs/conventions.md`: state that the size discipline (files <= 100,
  functions <= 15, one test per module; `__init__`/`_`-prefixed exempt) is now
  ENFORCED by laconic via `ish python laconic` and `ish python audit`, not just
  a guideline.

## reference (spike findings)

- laconic cli: `laconic check --source=<dir> [--size] [--structure]`; limits
  hardcoded at 100 / 15; exemptions match our conventions exactly.
- prior art in osai: `.../ish-osai/source/osai/python/laconic.sh` (invocation),
  `.../python/audit.sh` (audit wiring).
- baseline: `laconic check --source=source/honiipy` passed clean during the
  spike — re-verify after wiring.
