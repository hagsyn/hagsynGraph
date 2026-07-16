---
name: hagsyn-testing-council
description: Use when finishing or reviewing feature work in Hagsyn-Graph and test strategy, regression coverage, visual verification, or test-report generation needs centralized guidance before the work is treated as complete.
---

# Hagsyn Testing Council

## Overview

This skill governs testing expectations for Hagsyn-Graph feature work.
It ensures each completed feature has matching regression coverage, visual or interaction checks when needed, and a written test report under `docs/testing/reports/`.

## When to Use

Use this skill when:

- a tool feature is newly implemented or significantly changed
- frontend behavior changes in a user-visible way
- backend routes or output semantics change
- a bug was fixed and should gain regression coverage
- a testing report should be written after a development round

## Scenario Index

Read the relevant scenario SOP before acting:

1. 功能完成后的测试策略
   - `references/feature-test-strategy.md`
2. 回归修复后的测试与报告
   - `references/bugfix-regression-and-report.md`

## Global Rules

1. 每个功能完成后都要补对应测试，不依赖手测收口。
2. 用户可见 UI 变化至少要做前端结构检查，必要时再做交互验证。
3. bug 修复后必须补回归测试，避免同类问题再次复现。
4. 每轮功能完成后应在 `docs/testing/reports/` 下沉淀测试报告。
