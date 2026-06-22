# honiipy

an image-to-ascii converter — turn an image into shaded ascii text, right in
your terminal. honiipy even renders its own help banner: an ascii python,
dogfooded from `test/images/snake.jpg`.

## install

not yet on pypi. for now, run it from source in this repo through the ish
wrapper or uv (see [docs/cli.md](docs/cli.md) for details):

    ish honiipy convert path/to/image.jpg

## usage

    honiipy convert IMAGE [--pixel-size N] [--gradient N] [--one-to-one]
    honiipy version

- `--pixel-size N` — pixels per character column (default 12); rows use `N * 2`
  to correct the character aspect ratio.
- `--gradient N` — dark→light ramp, `0` (finest, 17 steps) to `3` (coarsest);
  default `0`.
- `--one-to-one` — map intensity across the full 0–255 range; the default,
  relative, stretches contrast across the image's own min/max.

full reference: [docs/cli.md](docs/cli.md), [docs/shading.md](docs/shading.md).

## lineage

honiipy is a python port of [honeybii](http://honeybii.com) by jamey deorio —
the original ruby image-to-ascii gem
([rubygems](https://rubygems.org/gems/honeybii),
[source](https://github.com/jameydeorio/honeybii)). it carries honeybii's mit
license forward and credits jamey as the original author.

the name is a homage: honeybii -> honiipy (bee -> python).

## license

mit — see [LICENSE](LICENSE), crediting jamey deorio (the original honeybii
author) and the honiipy maintainer.
