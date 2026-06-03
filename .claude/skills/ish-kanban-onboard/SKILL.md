---
name: ish-kanban-onboard
description: Onboard to the project. Run at the start of every session.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order. Do not skip steps.

## Step 1: Read the workflow

Run `ish kanban workflow` to read the project workflow. This is the authority on how work gets done. Every subsequent step must be consistent with what it says. If any step below contradicts the workflow, follow the workflow.

## Step 2: Check git state

Run `ish kanban survey` to see git state (status, staged diff, unstaged diff, recent commits).

Report the current branch, whether the tree is clean, and summarize any uncommitted state. If there are uncommitted changes, surface them before proceeding.

## Step 3: Review the board

Run `ish kanban boards list` to list available boards. If there is one board, use it. If multiple, ask the user which board to work on.

Run `ish kanban tasks next --board=<board>` to find the next task. Run `ish kanban tasks show --name=<task> --board=<board>` to read it.

Report which task is next.

## Step 4: Check audit cadence

Run `ish kanban audit cadence`. If it recommends an audit, report it to the user. If the user chooses to audit, stay on main — audits have no task branch. Skip step 5 and proceed to step 6.

## Step 5: Ensure task branch

Read `.claude/skills/ish-kanban-branch/SKILL.md` and follow its steps to create or switch to the correct task branch. Do not proceed until on the correct branch.

## Step 6: Study the project

Read all files under each `ish_kanban_context_*` path from the project configuration above. Read all of them — the goal is to become an expert on the project, not to skim for relevance.

## Step 7: Review the task

Evaluate the task against quality standards:

- Is it explicit enough to execute without guessing?
- Does it state what changes, what stays, and why?
- Is there any ambiguity?

If ambiguous, report the specific ambiguities. Do not proceed until resolved.

If clear, tell the user the task is ready. Ask the user to run each `ish_kanban_check_user_*` command from the project configuration to confirm known good state.

## Step 8: Wait for test confirmation

The user runs tests. If tests fail, diagnose together. If tests pass, confirm ready to begin.

Do not start implementation until the user confirms tests pass.
