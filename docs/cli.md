# cli

convert an image to shaded ascii from the command line.

## usage

```
honiipy convert IMAGE [--pixel-size N] [--gradient N] [--one-to-one]
honiipy version
honiipy --help
```

`honiipy convert` writes the ascii to stdout. with no arguments, `honiipy`
prints help. in this repo the command runs as `ish honiipy ...` or
`uv run honiipy ...`.

## options

- `IMAGE` — path to the image to convert.
- `--pixel-size N` — pixels per character column (default 12); rows use `N * 2`
  to correct the character aspect ratio.
- `--gradient N` — dark→light ramp, `0` (finest, 17 steps) to `3` (coarsest, 2
  steps); default `0`. values outside `0–3` are rejected.
- `--one-to-one` — map intensity across the full 0–255 range. the default is
  relative, which stretches contrast across the image's own min/max.

see [shading](shading.md) for how the conversion works.

## examples

```
honiipy convert photo.png
honiipy convert photo.png --pixel-size 6 --gradient 2
honiipy convert photo.png --one-to-one
```

## errors

- a missing or unreadable image prints `error: cannot read image: PATH` and
  exits non-zero.
- a flat image (one intensity) has no relative range: the default relative
  style exits non-zero with a clear error; pass `--one-to-one` to render it as
  a solid block.
