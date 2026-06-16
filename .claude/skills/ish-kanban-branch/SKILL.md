---
name: ish-kanban-branch
description: Create and switch to the correct task branch.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Follow these steps exactly, in order.

> **Do not invoke during an audit.** Audits run on `main` with no task branch and commit directly to `main`. Onboard and next-task already skip branch creation when `ish kanban audit cadence` recommends an audit; if you reach this skill directly mid-audit, stop and stay on `main`.

## Step 1: Identify next task

Run `ish kanban boards list` to list available boards. If there is one board, use it. If multiple, ask the user which board to work on.

Run `ish kanban tasks next --board=<board>` to get the next task. Read the task with `ish kanban tasks show --name=<task> --board=<board>`.

## Step 2: Compute branch name and ensure hierarchy

Read the branch algorithm below, then execute it.

### Branch algorithm

**Format:** `{name}/{board}/{type}/{path}`

1. **name:** `git config user.email`, strip `@` and domain.
2. **board:** the kanban board name (from `ish kanban boards list` or task context).
3. **type:** `task` for standalone tasks and parent directories. `subtask1` for first nesting level.
4. **path:** task path within `tasks/`, with `.md` stripped.

**Examples:**
- `kanban/<board>/tasks/foo.md` → `ratmav/<board>/task/foo`
- `kanban/<board>/tasks/foo/bar.md` → `ratmav/<board>/subtask1/foo/bar`

**Hierarchy:**
- Standalone tasks and parent directories branch from `main`.
- Subtasks branch from their parent directory branch.
- Merges go back: subtask → parent, parent → main.

**Ownership check:**
- If a remote branch exists for this task, check the name prefix.
- Matches your email prefix → yours, check it out.
- Different name → warn the user, let them decide.

**Execution:**
1. Compute the branch name from the task path.
2. If subtask: ensure the parent branch exists (create from main if needed).
3. If the branch already exists locally, run `ish kanban branches check --branch=<branch>`. If warnings are reported, surface them to the user and let them decide how to proceed (recreate the branch, continue as-is, or abort).
4. Create or switch to the task branch.
5. Report: branch name, base branch, whether newly created or checked out.

## Step 3: Report

Tell the user which branch they're on and what task they're working on.
