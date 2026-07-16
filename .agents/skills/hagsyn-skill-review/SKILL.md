---
name: hagsyn-skill-review
description: Use when creating or updating project-local skills in Hagsyn-Graph and a post-write review is needed to enforce progressive disclosure, scenario-first references, SOP completeness, Python-only scripts, and kwargs-style script interfaces.
---

# Hagsyn Skill Review

## Overview

This skill reviews newly created or updated project-local skills before they are treated as complete.
It enforces Hagsyn's local skill structure and prevents oversized SKILL.md files, missing scenario SOPs, or mixed script conventions.

## When to Use

Use this skill when:

- a new skill is added under `.agents/skills/**`
- an existing project-local skill is significantly updated
- a skill gains references or scripts
- a skill is being finalized after drafting

Do not skip review just because the frontmatter looks valid.

## Review Standard

Check the skill against these rules:

1. `SKILL.md` should keep only:
   - triggering conditions
   - scenario index
   - routing guidance
   - top-level constraints
2. Detailed execution should move into `references/` by scenario.
3. Each scenario should have its own SOP.
4. Each SOP should include self-check steps.
5. Scripts should live in `scripts/`, not inline in `SKILL.md`.
6. Scripts should be Python-only.
7. Script interfaces should use kwargs-style parameters.

## Failure Signals

The skill should be revised if:

- `SKILL.md` reads like a giant all-in-one manual
- references are organized by script or helper instead of by scenario
- a scenario has steps but no self-check
- scripts are Bash or JavaScript instead of Python
- script usage is positional and brittle instead of kwargs-oriented

## Output Format

The review result should clearly say:

1. what passed
2. what failed
3. what must be moved into `references/`
4. what must be moved into `scripts/`
5. whether the skill is ready or needs revision
