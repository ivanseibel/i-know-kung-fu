# I Know Kung Fu

A source repository for portable, reusable Agent Skills. Canonical skill sources live under [`skills/`](skills/) and follow the open Agent Skills format: each skill is a self-contained directory with a required `SKILL.md` and optional references, scripts, assets, and evaluations.

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

## Agent-driven installation

[`INSTALL_PROMPT.md`](INSTALL_PROMPT.md) contains a copy-and-paste installation prompt. It makes the executing agent inventory all skills, ask whether to install selected skills or all of them, ask for project or user-global scope, detect the active host's current discovery location, and install non-destructively.

Before publishing, replace `{{REPOSITORY_URL}}` in the prompt with this repository's final public URL.
