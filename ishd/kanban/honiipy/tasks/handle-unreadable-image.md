# handle unreadable image

fix. cli convert reports a clean error for only some unreadable-image
failures; broaden it to cover the rest.

## context

`cli.py`'s `_render` catches `FileNotFoundError` and `UnidentifiedImageError`.
other read failures — a corrupt or truncated image, a permission error, a
directory path — raise other `OSError` subclasses that escape as an uncaught
traceback instead of the documented `error: cannot read image: PATH`.

## what changes

- broaden `_render`'s except from `(FileNotFoundError, UnidentifiedImageError)`
  to `OSError` (it subsumes both — `UnidentifiedImageError` is an `OSError` in
  pillow), so every unreadable-image case prints `error: cannot read image:
  PATH` and exits 1.

## what stays

- the separate `ValueError` branch (flat-image / bad-args messages) and its
  wording.

## test

- a cli convert on a currently-uncaught case (e.g. a directory path) exits 1
  with the clean error, not a traceback.

## deliverable

every unreadable image fails gracefully (clean error, exit 1), with a test.
