# delete ruby

feat. honiipy stands alone; remove the ruby implementation and its docker
harness.

## precondition

- `copy-test-images` is done — nothing under `python/` reads `test/images/`.
- parity verified in `fe5c193`: honiipy matches the ruby implementation
  algorithmically, the residuals are documented in the parity section of
  `docs/conventions.md`, and `tests/fixtures/*.txt` pin honiipy's own output.
  exact byte parity is impossible across imaging libraries and is not the bar.

## context

the ruby gem is the reference implementation the port was measured against.
that job is finished — the measurement is recorded in prose and the regression
guard is python-native, so the reference itself is no longer load-bearing.

the `Dockerfile` and `Makefile` go with it rather than being repurposed. both
are ruby end to end — `FROM ruby:3.3`, `libmagickwand-dev`, `bundle install`,
`ENTRYPOINT ["bundle", "exec"]`, and make targets shelling into `rake test` and
`ruby bin/honeybii`. a python equivalent shares no line with them, and honiipy
already has two front doors: `ish honiipy` for development and, once
`rename-repo` publishes, `uv tool install honiipy` for consumers. a container
would be a third with no distinct job.

## what changes

remove, all tracked:

- `lib/honeybii.rb`, `lib/honeybii/{ascii_image,line_ascii,shaded_ascii}.rb`
- `bin/honeybii`
- `test/` entire — the three `*.rb` files and the seven `images/*.jpg` now
  carried under `python/honiipy/tests/images/`
- `Gemfile`, `honeybii.gemspec`, `Rakefile`, `.ruby-version`
- `README.markdown` — the ruby readme, superseded by `README.md`
- `Dockerfile`, `Makefile`

then:

- `.gitignore` — drop the ruby entries `.bundle/` and `*.gem`. keep `.DS_Store`,
  `tmp_scripts/`, and the python block.
- `docs/conventions.md` opening paragraph — it currently says honiipy "is built
  in place inside the honeybii repo and will replace the ruby gem once it
  reaches parity" and to "keep it runnable until parity". both are false once
  this lands. restate it as what honiipy is, not what it is becoming.

## what stays

- `LICENSE` — mit carried forward, crediting jamey deorio. a license obligation,
  not a choice.
- the `lineage and license` section of `docs/conventions.md` and the readme
  credit. the name is a homage and the license requires attribution.
- the `parity` section of `docs/conventions.md`. it is the rationale for
  pillow-native grayscale, lanczos resampling, and half-away-from-zero
  rounding — durable engineering reasoning, not an origin story. restate it in
  the past tense: parity was verified, these are the residuals, this is why the
  pipeline is pinned where it is.
- the python package, ish shell, kanban, docs, and `.gitmodules` (bats lives
  under `ishd/packages/ish-bash/test/`, unrelated to the ruby `test/`).

## test

- `ish python audit` and `ish bash audit` pass.
- `grep -rni "rmagick\|bundle\|gemspec\|rake" . --exclude-dir=.git` returns
  nothing outside `LICENSE`, the kanban, and docs prose.

## deliverable

the repo is python-only. nothing references rmagick or the gem, and no
documentation describes the port as in progress.
