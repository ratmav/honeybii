# conventions

honiipy is a python port of [honeybii](http://honeybii.com) by jamey deorio — an
image-to-ascii converter. it is built in place inside the honeybii repo and will
replace the ruby gem once it reaches parity. the ruby source under
`lib/honeybii/` is the reference implementation; keep it runnable until parity.

## stack

- python >=3.12, managed with `uv`.
- build backend: hatchling.
- image handling: pillow.
- lint/format: ruff. no black, no mypy.
- tests: pytest, mirroring source one-to-one.

## layout

build inside out: honiipy is a self-contained python package, and ish, kanban,
and the wrappers sit outside it and consume it like any other caller.

docs do not restate directory trees, file listings, or code. the repo already
says that, and a second copy only drifts out of sync. document intent and the
reasoning behind it; let the source answer the rest.

## ish wrappers

three local ish packages drive the package from the repo root, split by concern
(osai's consumer-vs-dev pattern, minus the `ish osai` umbrella — honeybii has
one python package):

- `ish python <lint|fmt|fix|test|laconic|audit>` — python dev verbs: ruff /
  pytest / laconic against `python/honiipy`. backs the agent audit gate
  (`ish python audit`).
- `ish bash <lint|fmt|fix|test|audit>` — bash dev verbs: shellcheck / shfmt /
  bats against the ish wrapper sources. backs the agent audit gate
  (`ish bash audit`); bats vendored under `ishd/packages/ish-bash/test/` as
  git submodules.
- `ish honiipy [args]` — consumer pass-through: forwards to the honiipy typer
  cli (`uv run honiipy`).

## reference repos

- `~/Source/osai` — uv workspace + typer CLI + ruff + laconic size checks.
- `~/Source/sylvan` — uv package + conventions doc + argparse CLI.

these are the template. follow them for packaging, cli, and test layout. cli
framework: typer (osai), not argparse (sylvan) — osai's `BannerGroup` gives
banner-on-help, its `CliRunner` tests are a ready template, and typer options
make the later parity-flag validation (`--gradient 0-3`) trivial.

## size discipline (from laconic)

- files <= 100 lines.
- functions <= 15 lines.
- one `tests/test_X.py` per `source/honiipy/X.py`. only `__init__.py` is
  exempt; `_`-prefixed modules are mirrored like anything else, so marking a
  module internal cannot quietly drop its test requirement.

`ish python laconic` enforces these against `source/honiipy` (size +
structure), and `ish python audit` runs it alongside ruff and pytest — so the
rules above are gated, not just guidance.

laconic runs unmodified, with every check it offers enabled: no flags narrowing
what it inspects, no pinned version, no local fork. it is developed alongside
honiipy, so its rules move. when they do, the gate fails here and honiipy
adapts — the rules above describe laconic's current behavior, not a contract
with it.

## parity

honiipy targets algorithmic parity with honeybii, not byte-identical output:
pillow and rmagick are different imaging libraries. for every bundled test
image, gradient (0–3), and style, both render the same character grid (identical
rows × columns) and share the relative min/max stretch and half-away-from-zero
rounding.

output differs only in which glyph a cell gets, where two unavoidable library
differences nudge a pixel's intensity across a gradient boundary:

- grayscale — pillow's `L` mode uses Rec. 601 luma weights; rmagick reduces via
  `GRAYColorspace` + `pixel.intensity`, a different luminance.
- resampling — honiipy downsamples with Lanczos; honeybii uses ImageMagick's
  default resize filter.

character agreement (12px point size) averages ~92%: coarse gradients and smooth
images often match exactly, while the finest 17-step gradient on photographs
falls as low as ~46%, where a one-bucket shift is most likely. on the
photographs, `one_to_one` generally tracks honeybii more closely than
`relative`, since `relative` also stretches across a min/max the two grayscale
paths compute slightly differently.

these residuals are properties of the imaging library, not defects, so honiipy
keeps pillow-native grayscale and Lanczos resampling and pins its own output in
the regression fixtures (`tests/fixtures/`) rather than asserting equality with
honeybii; regenerate the fixtures when a pipeline change is intentional.

## lineage and license

honiipy carries honeybii's mit license forward in `LICENSE` (crediting jamey
deorio and the honiipy maintainer) and credits jamey deorio in the readme. the
name is a homage: honeybii -> honiipy (bee -> python).
