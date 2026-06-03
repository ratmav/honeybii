# rip out ruby

feat. honiipy stands alone; remove the ruby implementation.

## precondition

parity verified (see parity-verification). do not start until honiipy matches.

## what changes

- remove `lib/`, `bin/honeybii`, `Gemfile`, `honeybii.gemspec`, `Rakefile`,
  `test/` (ruby), `.ruby-version`.
- the ruby `Dockerfile` / `Makefile` — repurpose for python or remove.
- `.gitignore` — drop ruby entries (`.bundle/`, `*.gem`).

## what stays

- the python package, ish shell, kanban, docs.

## deliverable

the repo is python-only. nothing references rmagick or the gem.
