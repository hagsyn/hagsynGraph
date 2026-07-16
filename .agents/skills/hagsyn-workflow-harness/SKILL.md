---
name: hagsyn-workflow-harness
description: Use when Hagsyn-Graph work needs a governed execution workflow for feature development, bug fixing, UI adjustment, or project-local skill changes, especially when docs lookup, downstream skill routing, testing evidence, and stop-hook continuation rules must be applied consistently.
---

# Hagsyn Workflow Harness

## When to Use

Use this skill when work in Hagsyn-Graph needs a repeatable execution workflow instead of ad hoc implementation, including:

- new feature or tool development
- bug reproduction and repair
- UI or workspace interaction adjustment
- project-local skill creation or update

Do not use this skill for one-off shell commands or isolated repo tasks that do not need workflow governance.

## Workflow Index

Read the relevant workflow SOP before acting:

- **Feature development**
  - `references/feature-development-workflow.md`
- **Bug fix**
  - `references/bugfix-workflow.md`
- **UI adjustment**
  - `references/ui-adjustment-workflow.md`
- **Skill governance**
  - `references/skill-governance-workflow.md`

## Global Rules

- Read relevant materials in `docs/product/**`, `docs/standards/**`, and `docs/ux/**` before implementation when the workflow calls for product, engineering, or UI decisions.
- Route to lower-level project skills when their domain applies:
  - `hagsyn-product-council` for product-shaping decisions before scope is stable
  - `hagsyn-product-guard` for scope drift, fake completeness, or `Tools` vs `Knowledge` boundary checks
  - `hagsyn-ui-workspace-pattern` for workspace shell, tool view, right-panel, and empty-state UI changes
  - `hagsyn-testing-council` for test strategy, regression coverage, visual verification, and testing report expectations
  - `hagsyn-review-council` for full-surface review before completion and for early lightweight review when a task becomes high-risk
  - `hagsyn-skill-review` for any project-local skill creation or material update
- Frontend-visible work is not complete without appropriate structure checks and real interaction verification.
- Behavior-changing work is not complete without tests or regression evidence that matches the changed surface.
- Important changes are not complete until review evidence matches the changed surface, including a final `hagsyn-review-council` pass when the workflow reaches release-gate scope.
- Record testing evidence in a report or task-facing verification summary before treating the workflow as complete.
- Apply the session stop hook at the end of the workflow: do not stop at a midpoint when meaningful next actions still exist inside the current workflow.
