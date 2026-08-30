# Repository instructions

- Treat this repository as the canonical source for authored skills, plugins, agents, and hooks.
- Keep standalone skills under `skills/<skill-name>/SKILL.md`.
- Keep installable plugins under `plugins/<plugin-name>/` with both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` present.
- Keep the Codex and Claude marketplace entries aligned on plugin name, version, source directory, and description.
- Put shared skills at the plugin root under `skills/`; do not duplicate skill content per harness.
- Keep personal Codex custom agents under `agents/codex/*.toml`.
- Bundle plugin-specific hooks inside that plugin. Keep root `hooks/` content opt-in.
- Do not hardcode credentials, tokens, home-directory paths, or machine-specific secrets.
- Add or update repository contract tests when changing packaging or installation behavior.
- Validate changes before committing.
