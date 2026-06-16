---
name: ish-kanban-review
description: Review changeset after tests pass, before grooming.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order.

## Step 1: Run automated checks

Ask the user to run each `ish_kanban_check_user_*` command. Then run each `ish_kanban_check_agent_*` command directly. Fold any failures into your findings.

## Step 2: Read changeset

Run `ish kanban survey` to see git state (status, staged diff, unstaged diff, recent commits).

## Step 3: Import hygiene

Check for:
- Private cross-module imports (reaching into another module's internals)
- Unused imports
- Duplicate imports
- Indirect imports (importing through a re-export when direct is available)

## Step 4: Conventions

Read the project's conventions doc if one exists under `ish_kanban_context_*` paths.

Check:
- Source files under 100 lines (warning at 100, fail at 150)
- Functions under 15 lines (warning at 10)
- Meaningful names (no abbreviations, no single letters except loop vars)
- One concept per file
- No dead code (commented out, unreachable)

## Step 5: Consistency

Check:
- One representation per concept (no parallel data structures for the same thing)
- API patterns match neighboring modules (flags, return values, error handling)
- Module structure follows project conventions

## Step 6: Architecture alignment

Read architecture docs from `ish_kanban_context_*` paths. Verify implementation matches documented design. Flag any divergence.

## Step 7: Report

Present findings one at a time, severity-ordered. Wait for the user to address each before continuing. If no findings, report clean.

Once the review is clean (no remaining findings), tell the user to run `/ish-kanban-groom` next.
