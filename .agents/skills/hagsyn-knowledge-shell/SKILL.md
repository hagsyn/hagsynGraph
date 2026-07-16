---
name: hagsyn-knowledge-shell
description: Use when shaping the Nodes, Graph, or Roadmaps modules in Hagsyn-Graph and the work must preserve shell-first Knowledge structure, avoid demo data, and delay deeper behavior until real scenarios and real content sources exist.
---

# Hagsyn Knowledge Shell

## Overview

This skill governs the Knowledge side of Hagsyn-Graph.
It keeps `Nodes`, `Graph`, and `Roadmaps` in a shell-first, real-scenario-driven state until actual objects, relations, and route needs justify deeper implementation.

## When to Use

Use this skill when the task involves:

- `Nodes` workspace design or knowledge object structure
- `Graph` workspace design or relationship-expression structure
- `Roadmaps` workspace design or route-building structure
- deciding what should remain a shell versus what is mature enough to deepen
- empty states or workspaces in Knowledge modules that risk drifting into fake completeness

Do not use this skill for:

- real executable tool implementation inside `Tools`
- backend-only file processing or auth work
- docs-only edits with no impact on Knowledge module behavior or structure

## Scenario Index

Read the closest scenario SOP before acting:

1. **Nodes shell design**
   - `references/nodes-shell-sop.md`
2. **Graph shell design**
   - `references/graph-shell-sop.md`
3. **Roadmaps shell design**
   - `references/roadmaps-shell-sop.md`

If a task touches multiple Knowledge modules, read all relevant SOPs and keep the stricter shell-first rule where they overlap.

## Global Rules

1. Keep `Nodes`, `Graph`, and `Roadmaps` present as product modules, but do not inflate them with fake content.
2. Let real tools and real usage create the demand signal for Knowledge expansion.
3. Treat empty or light states as honest shell states, not as failures to be hidden with fabricated examples.
4. Make each Knowledge module structurally useful before it becomes data-rich.
5. Do not let Knowledge overtake `Tools` as the current value center without real evidence.
