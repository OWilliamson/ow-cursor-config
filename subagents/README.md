# Subagents (`subagents/`)

**What this is:** In Cursor, **subagents** (often exposed as **Task** runs: explore, shell, codex, etc.) are **child agent sessions** with their own context and tool budget. Project folders such as `~/.cursor/subagents/` or `.cursor/subagents/` can hold **definitions, prompts, or pointers** your team uses to standardize those child runs. Cursor’s exact file formats evolve; treat this directory as the **place to version** anything you want checked into git alongside other Cursor config.

**This package:** This tree intentionally ships **no** bundled subagent definition files yet—only this README. Add markdown or other supported artifacts here when you define reusable subagent prompts or manifests for your workflow.

## Contents

| Item | What it does |
|------|----------------|
| *(no definition files yet)* | This folder is reserved for **subagent prompts, manifests, or references** you want versioned next to commands/rules/skills. |

When you add files, add one table row per file (or per logical bundle) and a short description of when that subagent should be used.
