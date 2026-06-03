---
name: ish-kanban-commit
description: Stage and commit task changes with message drafted from diff.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order. Refer to `ish kanban workflow` for commit message format and branch conventions.

## Step 1: Check branch matches task

Parse the current branch name (`git branch --show-current`) to identify the task. The branch name encodes the task path: `{name}/{board}/{type}/{path}`. Extract the board name (second segment) for `--board=` flags. If on `main`, note it — this is expected for audit commits but unusual otherwise. If the branch doesn't encode a task and this isn't an audit, warn the user.

## Step 2: Survey working tree

Run `ish kanban survey` to see git state (status, staged diff, unstaged diff, recent commits).

Report findings to the user.

## Step 3: Stage changes

Stage all task-related changes. Use specific file paths, not `git add -A`.

Do not stage files that likely contain secrets (.env, credentials, tokens). Warn if any are present.

Force-add skill files in `.claude/` if they're gitignored but part of the task.

## Step 4: Draft commit message

Draft the message from the staged diff, not from memory.

Format:
```
<type>: <title>

<what and why, hemingway style>

- <non-exhaustive list of changes>
```

Types: `feat`, `fix`, `docs`, `plan`, `spike`, `audit`. Lowercase title, 50 chars max. Body wraps at 72 chars.

Show the draft to the user for approval.

## Step 5: Commit

After user approves, commit using HEREDOC for the message. No `--no-verify`, no `Co-Authored-By`.

## Step 6: Verify

Run `git status` to confirm the tree is clean (or only has intentionally unstaged changes).

## Step 7: Audit cadence

Run `ish kanban audit cadence`. If this is an `audit` type commit, run `ish kanban audit tag`.

## Step 8: Offer merge

Ask the user if they want to merge this branch. If yes, suggest running `/ish-kanban-merge`.
