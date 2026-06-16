# shading

turn an image into shaded ascii text.

## api

```python
from honiipy import shade

art = shade("photo.png", point_size=12, gradient=0, style="relative")
print(art)
```

- `path` — image file.
- `point_size` — pixels per character column; rows use `point_size * 2` to
  correct the character aspect ratio (terminal cells are ~twice as tall as wide).
- `gradient` — index into four dark→light ramps (0 = 17 steps, 3 = 2 steps).
- `style` — `relative` stretches contrast across the image's own min/max;
  `one_to_one` maps intensity across the full 0–255 range.

the pipeline stages — `load_gray`, `pixelate`, `intensity_range`,
`relative_index`, `one_to_one_index`, `to_ascii` — are public for reuse.

## pipeline

1. `load_gray` — open and convert to 8-bit grayscale (pillow `L`, 0–255).
2. `pixelate` — resize to `cols = w // point_size`,
   `rows = h // (point_size * 2)`, Lanczos resampling.
3. map each pixel to a gradient char by `style`, joined row-major.

## behavior

- a flat image (every pixel one intensity) has no relative range: `relative`
  raises `ValueError`; `one_to_one` renders a solid block (its divisor is the
  constant 255).
- intensities round half away from zero, not python's banker's `round()`.
