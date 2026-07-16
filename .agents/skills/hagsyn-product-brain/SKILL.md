---
name: hagsyn-product-brain
description: Use when handling product development work in Hagsyn-Graph that needs central control over task routing, execution order, product boundary decisions, standards lookup, UI consistency, Knowledge restraint, project-local skill governance, or session-end stop behavior.
---

# Hagsyn Product Brain

## Overview

This skill is the control center for Hagsyn-Graph product development.
It classifies work, selects the right governing materials, routes to lower-level project skills, and applies session-end stop control.

## When to Use

Use this skill when the task involves:

- product evolution, module planning, or feature expansion
- frontend changes that affect shell, layout, tool flow, or module structure
- deciding whether work belongs to `Tools` or `Knowledge`
- changes that should align with `docs/product`, `docs/standards`, or `docs/ux`
- project-local skill creation, update, or review
- any multi-step Hagsyn development task that needs centralized control

Do not use this skill for:

- isolated backend bugfixes with no product or module impact
- one-off shell commands unrelated to Hagsyn product work
- non-Hagsyn repositories

## Required Reading Order

When relevant, read in this order:

1. `docs/product/**`
2. `docs/standards/**`
3. `docs/ux/**`
4. project-local skills under `.agents/skills/**`

## Lower-Level Skill Routing

Use lower-level skills when their domain applies:

- `hagsyn-product-guard` for product direction and demo-drift risk
- `hagsyn-product-council` for high-level product judgment before implementation scope is fixed
- `hagsyn-workflow-harness` for governed execution workflows across feature development, bug fixing, UI adjustment, and skill governance
- `hagsyn-ui-workspace-pattern` for frontend shell, workspace layout, tool views, or empty states
- `hagsyn-testing-council` for testing strategy, regression expectations, and report requirements when the task reaches verification scope
- `hagsyn-review-council` for full-surface review before completion or for early lightweight review on high-risk tasks
- `hagsyn-skill-review` whenever a project-local skill is created or materially updated
- `hagsyn-knowledge-shell` for `Nodes / Graph / Roadmaps`

## Scenario Index

Read the relevant scenario document before acting:

- **Product task routing and execution order**
  - `references/product-task-routing.md`
- **Project-local skill governance and post-write review**
  - `references/skill-governance.md`
- **Session-end stop hook and confirmation behavior**
  - `references/session-stop-hook.md`

## Global Constraints

- Keep `Tools` as the current center of gravity for real value
- Do not push `Knowledge` beyond shell stage without real scenarios
- Do not allow demo data or fake completeness to drive product decisions
- Do not stop a turn without a real reason
