# parity verification

feat. prove honiipy matches the ruby honeybii on the bundled test images, and
document any intentional drift.

## what changes

- compare `honiipy` output against the ruby `honeybii` for each image in
  `test/images/` (flower_bee, gradient, mona_lisa, starry_night, honeybees),
  across gradients and both styles.
- where pillow vs rmagick differ unavoidably (quantization, resampling),
  document the difference and the chosen behavior in `docs/conventions.md`.
- add a regression test that pins honiipy's output for at least one image.

## note

exact byte parity may be impossible (different image libraries). target visual
and algorithmic parity; capture deviations rather than chase them.

## deliverable

documented parity and a pinned-output regression test.
