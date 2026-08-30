# Hritvik's Agent Skills

A growing collection of reusable skills, plugins, custom agents, and hooks for Codex and Claude Code.

## Repository model

```text
skills/                       Standalone, agent-compatible skills
plugins/                      Installable Codex plugin packages
  <plugin>/.codex-plugin/     Codex plugin metadata
  <plugin>/.claude-plugin/    Claude Code plugin metadata
agents/codex/                 Personal Codex custom-agent TOML files
hooks/                        Opt-in hook examples and shared hook scripts
.agents/plugins/              Local Codex marketplace metadata
.claude-plugin/               Claude Code marketplace metadata
scripts/                      Installation and validation helpers
tests/                        Repository contract tests
```

Keep a workflow as a standalone skill while it is small and evolving. Promote related, stable skills into a plugin when they should be installed together, include hooks, or depend on an MCP server.

## Use with Codex

Install standalone skills and personal agents as symlinks:

```bash
./scripts/install-codex.sh
```

Register this repository's local plugin marketplace once:

```bash
codex plugin marketplace add "$(pwd)/.agents/plugins"
```

Install the Decision Guide plugin:

```bash
codex plugin add decision-guide@hritvik-skills
```

Start a new Codex task after installing or updating skills and plugins. Review and trust plugin hooks with `/hooks` before expecting them to run.

## Use with Claude Code

Add this checkout as a local Claude marketplace:

```text
/plugin marketplace add /Users/hritvikdinkar/repositories/skills
```

Install the Decision Guide plugin:

```text
/plugin install decision-guide@hritvik-skills
```

After the repository is published to GitHub, replace the local path with
`<github-owner>/skills` in the marketplace command. Claude copies installed
plugins into its cache, so reinstall or update the plugin after changing its
source.

## Cross-harness packaging

Each plugin keeps Codex and Claude metadata side by side. Its `skills/`, hooks,
scripts, and other implementation files remain shared:

```text
plugins/decision-guide/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
└── skills/
```

Harness-specific agents and hooks may be added only when their schemas differ;
the underlying workflow guidance should stay in the shared skill directories.

## Development

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

The repository is the canonical source. Installed Codex skills and agents should normally be symlinks back to it so edits are picked up without copying files.
