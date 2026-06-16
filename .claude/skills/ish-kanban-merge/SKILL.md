---
name: ish-kanban-merge
description: Merge current task branch to parent and clean up.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order.

## Step 1: Determine current branch

Run `git branch --show-current`. If on `main`, refuse — nothing to merge.

## Step 2: Determine merge target

Run `ish kanban merge` to get the merge target for the current branch. It computes the target with the same branch-base logic the rest of the system uses (`subtask1` → parent task branch, `task` → `main`). Use its output as `<target>` for the remaining steps. Do not re-derive the target by hand.

## Step 3: Check for remaining subtasks

If this is a parent branch with subtask branches still active, refuse. Check with `git branch --list '{name}/{board}/subtask1/{task}/*'`.

## Step 4: Confirm with user

Tell the user: "Merging `<current>` into `<target>`." Wait for confirmation.

## Step 5: Ensure target exists

If target branch doesn't exist locally, track from remote: `git checkout -b <target> origin/<target>`.

Switch to the target branch.

## Step 6: Merge

Run `git merge <source>`. If conflicts, stop and report. Do not force.

## Step 7: Clean up

Delete the merged branch locally: `git branch -d <source>`.

If the branch exists on remote, ask the user before deleting: `git push origin --delete <source>`.

Never delete `main`.
