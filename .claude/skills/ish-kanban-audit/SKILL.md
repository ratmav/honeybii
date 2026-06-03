---
name: ish-kanban-audit
description: Full-project adversarial QA. Finds contradictions, gaps, ambiguities, and drift.
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## Project configuration

!`cat .ishrc`

Adversarial audit. Find problems, not confirmations. Assume every claim is wrong until you verify it in source AND tests. Report findings as you go — do not wait until the end.

## Step 0: Context check

Ask the user to run `/context` and report usage. Audit reads broadly. If context is too low, tell the user to run `/clear` then `/ish-kanban-onboard` then `/ish-kanban-audit`. Do not proceed with insufficient context.

## Step 1: Scope

The audit scope includes all `ish_kanban_context_*` paths from the project configuration above, plus `.claude/skills/` and `ishd/kanban/`.

Ask what to audit:

- **full** — everything: docs, source, tests, kanban, skills
- **area** — a specific area (e.g., "task commands", "workflow")
- **file** — a specific file or set of files

If the user already specified scope, use that.

## Step 2: Run automated checks

Ask the user to run each `ish_kanban_check_user_*` command. Then run each `ish_kanban_check_agent_*` command directly.

Fold any failures into your findings — do not duplicate manual searching for things the automated checks already cover.

## Step 3: Find contradictions

Two sources of truth that disagree. One of them is wrong.

Identify every contract in the scoped area — function signatures, type definitions, data structures, enum values, file paths, module names. Search for every reference across docs, source, tests, kanban, and skills.

For each reference:

- Verify the reference matches the actual definition. Check parameter names, types, defaults, return types. A doc that says 3 args when source shows 4 is a contradiction.
- Verify the referenced file exists. A task that says "modify foo.sh" when foo.sh is deleted is a contradiction.
- Verify two docs that describe the same thing agree. If one doc says "no X" but source emits X, determine which is wrong.
- Verify parallel implementations agree. If the same operation exists in two places, confirm they produce the same results for the same inputs.

## Step 4: Find gaps

Something stated but not enforced. Something enforced but not stated. Something that should exist but doesn't.

Search for stated invariants, assumptions, and constraints across docs and kanban. For each one:

- Find the source that enforces it. No enforcement means the invariant is a wish, not a fact.
- Find the test that verifies it. An invariant enforced in source but not tested is one refactor away from disappearing. A claim without a test is an opinion.
- Find every untested code path. For each branch, conditional, error handler, and match arm in the scoped source — find the test that exercises it. Pay special attention to error paths, edge cases, and degenerate inputs.
- Find undocumented behavior. Source that implements behavior no doc describes is invisible to future sessions.
- Find untested design claims. If the architecture docs claim "X works because Y" — find the test that proves Y. Design claims without tests are the most dangerous gaps because they look validated.

## Step 5: Find ambiguities

Something that could be read two ways. Ambiguity causes different implementations to make different assumptions.

- Read each kanban task in the scoped area. Determine whether a fresh session with no context could execute it without guessing. If a task says "update the module" without saying what to change, flag it.
- Search for overloaded terms. The same word used for different concepts. If context is needed to disambiguate, flag it.
- Search for implicit ordering assumptions. Code that assumes a specific ordering without documenting or enforcing it. If the assumption is implicit, flag it.
- Identify unclear ownership. A concept described in multiple docs without a clear authority.
- Flag passive voice in docs, tasks, and skills. Passive voice hides the actor — "the invariant is checked" obscures who checks it. Passive voice in task instructions is ambiguity.

## Step 6: Find circular dependencies

A needs B, B needs A. These must be broken.

- Check module imports/sources for cycles.
- Check task dependencies for cycles.
- Check doc definitions for cycles (doc A defines X in terms of Y, doc B defines Y in terms of X).

## Step 7: Find drift

Something technically correct but misleading given how the project evolved.

- Search for redefined terms. A word that meant one thing in an early doc and now means something different. The old meaning lingers and confuses.
- Search for orphaned concepts. Terms in docs or tasks that no longer exist in source. The code moved on but the docs didn't.
- Search for stale examples. Doc examples that use old APIs, deleted functions, or patterns that no longer work.

## Step 8: Workflow and skill consistency

Verify the workflow and skills match each other, match actual practice, and match project docs.

- Verify each skill implements what `kanban/workflow.md` describes. Find steps in the workflow that no skill covers, or skill behaviors the workflow doesn't describe.
- Verify skills that reference each other agree on shared concepts (branch naming, merge targets, commit types).
- Verify skills reference current architecture concepts from project docs. Stale names, wrong property lists, or outdated invariants in skills are contradictions.
- Check git log for evidence of workflow friction — steps skipped, wrong actions taken, manual corrections needed.

## Step 9: Report

Present findings organized by severity:

1. **contradictions** — two sources of truth disagree. must fix.
2. **circular dependencies** — A needs B, B needs A. must fix.
3. **gaps** — stated but not enforced, or enforced but not stated. should fix.
4. **ambiguities** — could be read two ways. clarify.
5. **drift** — technically correct but misleading. nice to fix.

For each finding, name specific files and lines. Propose a fix or flag for discussion.

**One at a time.** Present a single finding, wait for the user to review and decide, then present the next.

## Step 10: Create spikes

For each confirmed finding, create a spike task on the kanban board using `ish kanban tasks new --name=<finding> --board=<board>`.

Slot all audit findings at the top of `plan.yaml`, before other work. Unresolved findings are debt — they go first.

After all findings are reviewed, update `plan.yaml` and tell the user to run `/ish-kanban-commit`. The commit skill moves the `audit` tag.
