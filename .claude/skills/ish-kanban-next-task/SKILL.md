---
name: ish-kanban-next-task
description: Transition to next task within an existing session.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Use this for mid-session transitions. For fresh sessions, use `/ish-kanban-onboard`.

Follow these steps exactly, in order.

## Step 1: Review the board

Run `ish kanban boards list` to list available boards. If there is one board, use it. If multiple, ask the user which board to work on.

Run `ish kanban tasks next --board=<board>` to find the next task. Run `ish kanban tasks show --name=<task> --board=<board>` to read it.

## Step 2: Check audit cadence

Run `ish kanban audit cadence`. If it recommends an audit, report it to the user. If the user chooses to audit, stay on main — audits have no task branch. Skip step 3 and proceed to step 4.

## Step 3: Ensure task branch

Read `.claude/skills/ish-kanban-branch/SKILL.md` and follow its steps to create or switch to the correct branch.

## Step 4: Evaluate context

Assess whether the current session has enough context to continue:

- **Task scope:** How many files will this touch? How complex?
- **Remaining context:** Is this session running long?
- **Area relevance:** Is the next task in the same area as the last, or a different part of the codebase?

Recommend one of:
- **Go** — enough context, same area, proceed.
- **Study then go** — different area, read all `ish_kanban_context_*` paths first, then proceed.
- **Fresh session** — low context or major area switch. Recommend `/clear` then `/ish-kanban-onboard`.

## Step 5: Wait for test confirmation

Ask the user to run each `ish_kanban_check_user_*` command from the project configuration to confirm known good state.

Do not start implementation until the user confirms tests pass.
