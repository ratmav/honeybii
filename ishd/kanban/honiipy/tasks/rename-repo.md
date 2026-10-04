# rename repo

feat. the port is done — make the repo honiipy.

## what changes

- rename the working dir `~/Source/honeybii` -> `~/Source/honiipy`.
- rename the github repo and update the git remote.
- update any lingering `honeybii` references to honiipy. the readme's `install`
  section hardcodes the github url twice, and `docs/conventions.md` names the
  old repo in its `ish wrappers` section; check `.ishrc` and the roadmap too.
  the readme's `lineage` section is not one of these — it credits jamey
  deorio's honeybii and stays.

## what stays

- the package name `honiipy` and the `honiipy` console script. the rename is
  the repo and its directory, not the package.
- the version in `pyproject.toml`, an alpha placeholder. that manifest is the
  only place it is written: `honiipy version` reads installed metadata, and the
  test asserts against the same, so neither restates the number.

## out of scope

packaging for an index. honiipy installs from git and that is enough for now;
publishing needs a version policy, a release path, and credentials, none of
which this task decides.

## note

the board, the ish packages, and the `ish_kanban_*` variables are already named
honiipy, so this is directory and remote plumbing.

## deliverable

`~/Source/honiipy`, a github repo named honiipy, and a readme that tells someone
how to install it.
