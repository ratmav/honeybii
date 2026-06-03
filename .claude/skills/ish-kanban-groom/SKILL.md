---
name: ish-kanban-groom
description: Audit docs and kanban for stale references after completing a task.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order.

## Step 1: Identify what changed

Read the diff (`git diff` or `git diff HEAD~1`) to identify renames, removals, and semantic shifts. Build an old → new mapping. For example: type renamed, function moved, concept redefined. Confirm the mapping with the user if anything is ambiguous.

## Step 2: Scan docs for stale references

Grep for old terms across all files under `ish_kanban_context_*` paths. Report any stale references found. Fix them.

## Step 3: Scan kanban and skills

Grep for old terms in `ishd/kanban/` task files and `.claude/skills/`. Report stale references. Fix them.

## Step 4: Verify completeness

For each old term in the mapping, confirm zero remaining references (except git history). If any survive, fix or flag.

## Step 5: Workflow self-check

Did anything about this task expose workflow friction? Unclear instructions? Missing conventions? Steps that should be automated? Note findings for the next audit.

## Step 6: Capture lessons and close task

Move useful content out of the task file:
- Design decisions → docs
- Implementation details for follow-on work → other kanban tasks

Extract the board name from the current git branch (second segment: `name/board/type/path`). Then run `ish kanban tasks close --name=<task> --board=<board>` to remove from plan.yaml and delete the task file.
