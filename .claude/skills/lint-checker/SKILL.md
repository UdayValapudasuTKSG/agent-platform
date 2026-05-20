---
name: lint-checker
description: Check a Python project for import errors, lint violations, type issues, and formatting problems. Use when the user asks to lint, check imports, find unused code, or validate a Python codebase before commit/deploy/PR.
---

# Lint Checker

When invoked, run the checks below on the current Python project and report findings grouped by file. Do not auto-fix unless the user asks.

## Steps

1. **Detect what's available.** Check which tools are installed:
   ```bash
   ruff --version; mypy --version; pylint --version; flake8 --version; isort --version
   ```
   Prefer `ruff` if present — it replaces flake8/isort/pylint for most checks and is ~100x faster.

2. **Detect project config.** Look for `pyproject.toml`, `ruff.toml`, `.flake8`, `mypy.ini`, `setup.cfg`. Respect existing config; don't override rules.

3. **Run checks** in this order, stopping to report after each if findings are substantial:
   - **Lint + imports:** `ruff check .` (fallback: `flake8 .` and `isort --check-only .`)
   - **Format:** `ruff format --check .` (fallback: `black --check .`)
   - **Types:** `mypy .` — only if mypy config exists or user asked for type checks
   - **Deep lint:** `pylint <package>` — only if user explicitly asks; it's slow and noisy

4. **Report** as a grouped summary:
   - One section per file, listing `path:line — code — message`
   - Separate "errors" (syntax, undefined names, import failures) from "style" (formatting, unused vars)
   - End with a one-line total: `N errors, M warnings across K files`

## Fixing

Only fix when the user asks ("fix them", "apply fixes", etc.). Then:
- `ruff check --fix .` for auto-fixable lint
- `ruff format .` for formatting
- For anything ruff can't fix, edit the file directly — don't suggest sed/awk one-liners.

After fixing, re-run the check and confirm zero findings before declaring done.

## When to skip

- If the project has no Python files, say so and stop.
- If no lint tools are installed, suggest `pip install ruff` (single tool covers most cases) rather than running anything.
