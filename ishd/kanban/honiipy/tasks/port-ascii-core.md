# port ascii core

feat. port the shading engine from ruby/rmagick to python/pillow. library only,
no cli. structured, tested, laconic-clean (files <=100 lines, functions <=15).

## reference (ruby source to port)

- `lib/honeybii/ascii_image.rb` — base: load image, hold ascii, to_s.
- `lib/honeybii/shaded_ascii.rb` — the engine:
  - gradients (4 ramps) and styles (relative default, one_to_one).
  - `grayscale!` — quantize to gray.
  - `pixelate!` — resize to columns = w / point_size,
    rows = h / (point_size * 2). the *2 corrects character aspect ratio.
  - `get_intensity_range` — min/max pixel intensity.
  - relative: index = gradient_size * (intensity - min) / (max - min).
  - one_to_one: index = gradient_size * intensity / max_intensity.

## pillow notes

- grayscale via `Image.convert("L")`; intensity is the 0-255 L value (ruby used
  0-65535 — scale the one_to_one divisor accordingly).
- resize with the same column/row math.
- guard the relative divide-by-zero on a flat image (max == min). the ruby has
  this bug; do not port it.

## what changes

- `source/honiipy/` — the core modules (split per laconic size limits).
- `tests/` — mirror each module; cover grayscale, pixelate dims, both styles,
  all gradients, the flat-image guard.

## deliverable

a python api that turns an image path into shaded ascii, matching the ruby
algorithm. tested.
