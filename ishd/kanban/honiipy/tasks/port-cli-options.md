# port cli options

feat. wire the cli to the ported core with parity options. ergonomics may drift
from the ruby; behavior must match.

## reference (ruby cli)

`bin/honeybii`:
- positional image path (png|gif|jpg).
- `-p/--pixel-size` (default 12).
- `-g/--gradient N` (0-3, default 0).
- `-o/--one-to-one` (default style is relative).
- plain `honeybii` with no args prints help.

## what changes

- `source/honiipy/cli.py` — the options above, calling the ported core,
  idiomatic for the chosen framework (e.g. `--pixel-size` typer option).
- validate gradient in range; clear error on bad/missing image.
- `tests/test_cli.py` — cover each option and the error paths.

## deliverable

`honiipy IMAGE [-p N] [-g N] [-o]` produces the same ascii as the ruby cli.
