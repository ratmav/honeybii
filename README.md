# honiipy

an image-to-ascii converter.

```shell
                   $@@@%V~
                    8@@@@@:
                    .*#@@@%-
                       .+%@%-
                         =@@$
       -:=**=+:~-       ~$@@V
     =#%@@@@@@@@@@%8###%@@@$.         .+x$#88#V*-
   .$@@@@#VxxYV$8%%@@@%8$*~         +$@@@@%%%%@@@$:
   8@@@%:          ...            :#@@%$V$YVY$V$%@@x
  =@@@@+                         Y@@@$VVx:- .:VVY%@@*
  *@@@@=                       :8@@@VVx-      .$x8@@8
  .%@@@@=                    -Y@@@@VV+        -x#@@@8
   ~8@@@@8Y+~.            .:V%@@@%Y=.      .~*$%@@@@=
     x%@@@@@@%8##$$$$$$$$8%@@@@%$*Y$V$$$#8%%@@@@@@%+
       +V8@@@@@@@@@@@@@@@@@@%#YxY8@@@@@@@@@@@@@@8*.
          .~*$#888888888%%8#$$8@@@@@@@@@@%%8$Y=~
          .*#%%88%%%%8#$Yx*===+:~~~~~~---.
        .Y@@@@@@@%V*:-.
       ~8@@@@@8x~
      -%@@@@%=
      =@@@@%-                   :x$#8#$x:
      x@@@@*        ~=*x*+~  .*8@@@@@@@@@8+
      *%@@@=     .Y@@8$#8@@$x8@@@@8Y++x%@@@*
      =$@@@#     #@Y.    .Y8@@%#x~     -8@@%
      -Y$@@@V.   %@     :$@@8#Yx=      -8@@#
       ~Y$8@@%x~ :8#~-x8@@#$Y+*@@%V**Y#@@@#-
        .*Y$#%@@%8##8#8#$VY+.  :V%@@@@@8V+
          -=xYV$#88$VV#$$:        -~~~.
             .~:+====:.~$x
                         Vx
                          $.
                          ++
                          ~+
                          ~.
                          .
```

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

honiipy is a python port of honeybii by jamey deorio — the original ruby
image-to-ascii gem ([rubygems](https://rubygems.org/gems/honeybii),
[source](https://github.com/jameydeorio/honeybii)).

## license

mit — see [LICENSE](LICENSE).
