# Portable Agent Skills installation prompt

Replace `{{REPOSITORY_URL}}` with the published repository URL, then copy everything inside the block into a compatible coding agent.

```text
Install one or more Agent Skills from this source repository:

{{REPOSITORY_URL}}

Treat this as an installation task, not as permission to execute the skills. Follow these rules:

1. Obtain a read-only view or temporary checkout of the repository using the safest available capability. Do not run scripts from the repository during discovery or installation.
2. Discover skills by inspecting every direct child of `skills/` that contains a valid `SKILL.md`. Read only each file's `name` and `description` first. Do not rely on a hardcoded catalog.
3. Show the discovered skills as a concise numbered list with name and description.
4. Ask me these two decisions before changing files:
   - Which skills should be installed: selected names/numbers, or all discovered skills?
   - Should they be installed for this project only, or in the current tool's user-global skills location?
5. Detect the agent/tool currently executing this prompt. Resolve its current supported Agent Skills discovery locations from available official documentation, built-in help, or local configuration. Prefer the interoperable `.agents/skills` project directory or `~/.agents/skills` user directory when the current host officially supports it; otherwise use that host's documented project or user skills directory. Do not guess an unsupported path.
6. Before copying, report the resolved host, scope, and exact destination. If host or destination cannot be determined reliably, stop and ask me rather than guessing.
7. Validate every selected source before installation:
   - the directory contains `SKILL.md`;
   - frontmatter has a valid `name` and `description`;
   - the directory name matches `name`;
   - referenced relative files exist;
   - no source path escapes the skill directory.
   Use an installed Agent Skills validator if available; otherwise perform these checks directly.
8. Install each complete selected skill directory into `<resolved-skills-root>/<skill-name>`. Copy references, scripts, assets, evaluations, and optional host metadata with it. Do not copy repository-level files into the skills root.
9. Be non-destructive:
   - never overwrite or delete an existing destination silently;
   - if a destination exists, compare it with the source and ask whether to skip, replace it after a recoverable backup, or abort;
   - never modify unrelated skills or configuration;
   - do not create compatibility duplicates or symlinks unless the detected host requires them and I approve the exact adapter.
10. After installation, validate the installed `SKILL.md` and its relative references. Do not execute bundled scripts merely to prove installation. Tell me whether the host needs a reload/restart based on current documentation.
11. Finish with a concise report containing installed skill names, exact paths, skipped/conflicting items, validation results, and a natural-language example that should trigger each skill.

Project scope means the current project only. User-global scope means the personal skills directory used by the tool executing this prompt, not a system-wide administrator directory.
```
