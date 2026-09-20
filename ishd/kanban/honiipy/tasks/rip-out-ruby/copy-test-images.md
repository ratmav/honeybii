# copy test images

feat. the python suite reads its input images out of the ruby test tree. copy
them under the python tests so the ruby tree can be deleted without breaking it.

## context

`python/honiipy/tests/test_shading.py` resolves inputs from the repo root:

```python
_IMAGES = Path(__file__).parents[3] / "test" / "images"
```

`parents[3]` is the repo root, so `_IMAGES` is `<root>/test/images` — the ruby
directory `delete-ruby` removes. six tests read it: the five parametrized
`test_shade_matches_fixture` cases (`flower_bee`, `gradient`, `honeybees`,
`mona_lisa`, `starry_night`) and `test_banner_matches_snake_conversion`
(`snake.jpg`). `source/honiipy/_banner.py` names the same path in its docstring.

parity is not at risk here. `tests/fixtures/*.txt` pin honiipy's own output as
the regression guard, and the measured agreement with the ruby implementation
is already written up in the parity section of `docs/conventions.md`. only the
`.jpg` inputs are load-bearing.

copy rather than move: the ruby suite stays runnable until `delete-ruby`
removes it wholesale, so no commit boundary leaves either suite red.

## what changes

- copy all seven `test/images/*.jpg` to `python/honiipy/tests/images/` —
  `flower_bee`, `gradient`, `gradient_2`, `honeybees`, `mona_lisa`, `snake`,
  `starry_night`. `gradient_2.jpg` has no python test today; carry it so the
  ruby deletion loses no asset.
- `test_shading.py` — `_IMAGES = Path(__file__).parent / "images"`.
- `source/honiipy/_banner.py` docstring — `test/images/snake.jpg` becomes
  `tests/images/snake.jpg`.

## what stays

- `test/images/` and the whole ruby tree, untouched until `delete-ruby`.
- every byte of `tests/fixtures/*.txt`. the images are copied unmodified, so
  pinned output must not move. a fixture diff here means the copy corrupted
  something — `.gitattributes` marks the fixtures exact-byte.

## test

- `ish python test` passes: five fixture cases plus the banner test, all
  reading from `python/honiipy/tests/images/`.
- `grep -rn "test/images" python/honiipy ishd docs` returns nothing.

## deliverable

the python suite has no path dependency on the ruby test tree.
