# I Know Kung Fu

A source repository for portable, reusable Agent Skills. Canonical skill sources live under [`skills/`](skills/) and follow the open Agent Skills format: each skill is a self-contained directory with a required `SKILL.md` and optional references, scripts, assets, and evaluations.

## Quick Installation

Copy and paste the prompt below into your AI coding agent (e.g. Claude, Gemini, Antigravity, Cursor, Windsurf):

```text
Install Agent Skills from this repository:
https://github.com/ivanseibel/i-know-kung-fu

Instructions for agent:
1. Discover available skills in `skills/` (directories containing `SKILL.md`).
2. List available skills and confirm with me which ones to install and the target scope (project `.agents/skills` or user-global), unless specified below.
3. Copy selected skill folders completely into the target skills directory without executing scripts or silently overwriting existing files.

[Extra instructions: e.g., target location, specific skills to install]
```

## Available skills

### `goal-to-action`

Turns an uncertain goal into an evidence-aware strategic path, validates critical assumptions, and produces a traceable execution-ready plan—or an explicit feasibility diagnosis.

Source: [`skills/goal-to-action/`](skills/goal-to-action/)

## Local development

Validate the portable skill metadata:

```bash
python3 /path/to/quick_validate.py skills/goal-to-action
```

Validate the bundled Strategic Graph template:

```bash
python3 skills/goal-to-action/scripts/validate_graph.py \
  skills/goal-to-action/assets/graph-template.json
```

The repository stores source packages only. Developing a skill here does not install it into any agent host.
