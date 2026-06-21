# rip out ruby

feat. honiipy stands alone; remove the ruby implementation.

## precondition

parity verified: honiipy matches honeybii algorithmically — see the parity
section in `docs/conventions.md`. exact byte parity is impossible across imaging
libraries; the deviations are documented and accepted.

## what changes

- remove `lib/`, `bin/honeybii`, `Gemfile`, `honeybii.gemspec`, `Rakefile`,
  `test/` (ruby), `.ruby-version`.
- the ruby `Dockerfile` / `Makefile` — repurpose for python or remove.
- `.gitignore` — drop ruby entries (`.bundle/`, `*.gem`).

## what stays

- the python package, ish shell, kanban, docs.

## deliverable

the repo is python-only. nothing references rmagick or the gem.
