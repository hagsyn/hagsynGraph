---
name: hagsyn-ui-workspace-pattern
description: Use when working on Hagsyn-Graph frontend pages, workspace shells, tool views, right-side detail panels, or empty states that could drift away from the project workspace pattern.
---

# Hagsyn UI Workspace Pattern

## Trigger Conditions

Use this skill when work touches:

- `frontend/index.html` layout, navigation, panel structure, or module framing
- tool workspace states such as input, running, result, history, or download flow
- right-side contextual detail areas
- empty states, placeholder copy, or no-data handling

Do not use this skill for backend-only, database-only, auth-only, or docs-only changes with no frontend workspace impact.

## Scenario Index

Choose the closest scenario and read that SOP before implementation:

1. Workspace shell or page framing changes:
   - `references/workspace-shell-sop.md`
2. Tool workspace or result-flow changes:
   - `references/tool-workspace-sop.md`
3. Empty state or right-panel context changes:
   - `references/empty-state-and-detail-panel-sop.md`

If a task spans more than one scenario, read all matching SOPs and apply the stricter rule where they overlap.

## Top-Level Rules

1. Keep the product in a workspace shell, not a marketing page or showcase dashboard.
2. Make the real tool path primary: enter tool, configure, run, inspect result, download.
3. Preserve meaningful context on the right side; do not leave the panel decorative or blank without intent.
4. Use honest empty states; do not fabricate graph data, business metrics, files, or analytics.
5. Reuse the existing dark developer-tool direction and avoid introducing a separate page language for each tool.
