# python wrapper relative paths

fix. `ish python test` and `ish python laconic` resolve forwarded path
arguments from the package dir, not the caller's cwd — the same class of bug
fixed for `ish-honiipy` in cli-relative-paths.

## context

every `ish-python` verb runs `cd "${_ish_python_root}"` (= `python/honiipy`)
before `uv run`. `test` and `laconic` forward `"$@"`, so a path passed there
resolves under the package dir: from the repo root,
`ish python test python/honiipy/tests/test_cli.py` is sought under
`python/honiipy/python/honiipy/...` and fails. `-k` selectors and the no-arg
default are unaffected; `lint`/`fmt`/`fix` forward no `"$@"`, so they have no
user-facing bug.

the wrinkle vs. ish-honiipy (a pure pass-through): ish-python also injects its
own package-relative args (`source/honiipy`, `tests`) that currently rely on
the cd, so the cd can't simply be dropped — those must keep resolving.

## what changes

- mirror the ish-honiipy fix: invoke uv with `--project "${_ish_python_root}"`
  instead of cd, and make the injected targets absolute
  (`${_ish_python_root}/source/honiipy`, `${_ish_python_root}/tests`) so they
  resolve regardless of cwd, while forwarded `"$@"` paths resolve from the
  caller's cwd. apply across the verbs that currently cd.

## what stays

- each verb's behavior, flags, and fixed source/tests targets; only cwd
  handling changes. ruff/pytest/laconic invocations are otherwise unchanged.

## test

- a bats check in the ish-bash suite: from the repo root, `ish python test`
  given a repo-relative test-file path runs that test (exit 0), matching the
  same run with a package-relative path.

## deliverable

`ish python` dev verbs resolve forwarded path arguments from the caller's cwd,
with their injected source/tests targets still resolving.
