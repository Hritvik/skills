# Hritvik's Agent Skills

A growing collection of reusable skills, plugins, custom agents, and hooks for Codex, T3 Code using Codex, and Claude Code.

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

Preview, then install standalone skills and personal agents as symlinks:

```bash
./scripts/install-codex.sh --dry-run
./scripts/install-codex.sh
```

Skills link into `~/.agents/skills`; personal Codex agents link into
`~/.codex/agents`. The installer checks all destination conflicts before writing,
leaves matching links alone, and refuses to replace directories or unrelated
symlinks (including broken links). Resolve a reported conflict deliberately, then
rerun the preview. It does not install plugins or change client configuration.

Register this repository's local plugin marketplace once:

```bash
codex plugin marketplace add "$(pwd)/.agents/plugins"
```

Install the Decision Guide plugin:

```bash
codex plugin add decision-guide@hritvik-skills
```

Start a new Codex task after installing or updating skills and plugins. Review and trust plugin hooks with `/hooks` before expecting them to run.

## Use with T3 Alpha / T3 Code

Use the same installation when the T3 thread uses the **Codex provider**. T3
asks Codex's app-server for `skills/list` with the thread's working directory;
it does not need another copy of each skill or a T3-specific skill adapter.
Project workflows belong in the project's `.agents/skills/<name>/SKILL.md`;
commit them when they must travel into worktrees or another machine.

This was verified against the locally installed T3 Code (Beta) 0.1.3, build
commit `d2c440312e5f`, on 2026-10-29. Its bundled server calls `skills/list`
with `cwds: [input.cwd]`. This establishes provider delegation, not a guarantee
that every installed plugin, hook, custom agent, or UI command works identically
in both apps.

T3 can use a different provider home (`homePath` / `shadowHomePath`). Shared
user skills require the same machine/user home; plugins and configuration also
depend on the provider's selected Codex home. Remote environments need their own
installation. With the Claude provider, use the Claude instructions below;
Codex plugin installation does not install a Claude plugin.

After installation, start a fresh thread in each app and ask it to locate and
read a known skill, for example `capability-steward`. Confirm that its discovered
path resolves back to this repository. In T3, confirm the thread uses Codex and
the intended checkout. A disk inventory alone does not prove runtime discovery.

## Use with T3 OpenCode, CLIProxyAPI, and Free Pool

OpenCode v2 reads personal `~/.agents/skills` and project `.agents/skills`
directories, including the repository links installed above. T3's OpenCode
provider asks that runtime for its skill inventory. The configured `cliproxy`,
`freellmpool`, and `fp2` model providers use the same inventory; changing between
those models does not require another skills installation.

Codex plugin caches and legacy `~/.codex/skills` are separate. To expose their
skill instructions to OpenCode, preview and apply the bridge:

```bash
python3 scripts/sync-opencode-skills.py
python3 scripts/sync-opencode-skills.py --apply
```

The bridge reads the Codex disk audit and links eligible skill folders into
OpenCode's native user skills directory. Existing shared skills keep their
OpenCode definition; unrelated destinations and ambiguous names are preserved.
This transfers instructions and supporting files, not Codex plugins, hooks,
custom agents, tool connections, or credentials. Cache inventories are estimates;
verify the result in the live runtime. Rerun after adding or updating Codex-only
collections. The bridge never deletes stale links; review removed or renamed
upstream skills explicitly.

Verify the exact workspace without a model request:

```bash
opencode api GET /api/skill \
  --header "x-opencode-directory:$PWD" > /tmp/opencode-skills.json
python3 -c 'import json; s=json.load(open("/tmp/opencode-skills.json")); print(s["location"]); print([(x["id"], x["path"]) for x in s["data"]])'
```

Wait for initial scanning and repeat if the inventory is initially empty. Use a
regular output file because OpenCode v2.1.4 can truncate large CLI output through
a pipe. In T3, select OpenCode and mention a skill with `@skill-id`. The selected
agent's permissions and the model/proxy's support for tool calls still apply;
registration does not prove every workflow's external tools are available.

Verified locally on 2026-10-29 with OpenCode v2.1.4 and T3 Code (Beta) 0.1.3.
The exact portfolio workspace inventory increased from 115 to 188 skills after
73 instruction-folder links were added. All 73 IDs registered with the intended
source and nonempty content. Its 15 `cliproxy`, 14 `freellmpool`, and 2 `fp2`
models advertise tool support; no inference request was made to test individual
model behavior. These counts describe the verification snapshot, not a fixed
requirement for future installations.
T3's bundled server calls `skill.list` with the working directory and passes
explicit skill mentions into its prompt. See the
[OpenCode V2 skills documentation](https://opencode.ai/v2/docs/skills) for discovery,
ID precedence, and permissions. Remote hosts or customized provider environments
need verification against their own runtime.

## Maintenance ownership

This repository owns authored workflow content and its installation script.
`agent-sync` owns optional cross-client projection and MCP configuration; it is
not required for Codex and T3 using the same Codex provider. Avoid having both
tools manage the same destination. Keep third-party plugins with their existing
installation owner, as described below. Verify provider behavior again after
major client upgrades before adding another adapter or copying skills.

## Use with Claude Code

Add this checkout as a local Claude marketplace:

```text
/plugin marketplace add ~/repositories/skills
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

## Managing installed skills

Use one installation owner per collection. Keep authored skills in this repository
and symlink them into the agent's discovery folder. Prefer a maintained plugin for
third-party collections that publish one. Keep individually installed skills when
they have a distinct purpose or local changes; a matching name alone does not make
two skills interchangeable.

| Collection | Installation owner | Maintenance |
| --- | --- | --- |
| Personal workflows | This repository | Edit the source; keep installed symlinks |
| Matt Pocock | `mattpocock-skills@mattpocock` | Refresh the marketplace and installed plugin |
| Han | Existing Han plugins | Refresh the marketplace and installed plugins |
| OpenAI and connected-service plugins | Codex plugin management | Use the plugin's supported update path; do not edit its cache |
| UI Skills | Existing local router plus live MCP catalog | Fetch only the relevant skills from the registry; the local router is a separate file |
| Other standalone skills | Their recorded upstream source, when known | Review a source diff and back up before applying a targeted update |

### Audit before changing installations

Run the read-only inventory from this checkout:

```bash
python3 scripts/audit-codex-skills.py
python3 scripts/audit-codex-skills.py --json
```

The helper follows direct skill-folder symlinks, reports disabled skills and source
metadata when available, and counts only manifest-declared plugin skill paths.
It labels plugin cache versions as estimates: cached files and enabled config
entries do not prove a client loaded them. Remote plugins, project-scoped skills,
and the live UI Skills registry are outside this disk inventory. The standalone
skills lock file records only some installations, so do not use it as the full
inventory. For runtime verification, Codex's app-server `skills/list` response
reports loaded skill paths, enabled state, and discovery errors.

Before a change, back up the affected files, config, and skill lock file outside
the discovery directories. Compare complete skill folders, including scripts and
references. Disable an exact standalone duplicate in Codex rather than deleting
shared files used by another agent:

```toml
[[skills.config]]
path = "/absolute/path/to/duplicate/SKILL.md"
enabled = false
```

Restart Codex after changing these settings. To restore a disabled skill, remove
its entry or set `enabled = true`. Verify its replacement is enabled before
disabling a standalone copy.

### Refresh a collection

For Matt Pocock's collection:

```bash
codex plugin marketplace upgrade mattpocock
codex plugin add mattpocock-skills@mattpocock --json
```

The first command refreshes the catalog; the second ensures the plugin is
installed from that catalog and reports its version. Recheck new versions for
added or retired skills and duplicate installations. Newly bundled skills can
arrive through the plugin, but unrelated new plugins are not installed by this
routine. Matt Pocock documents startup updates; explicit refresh and version
verification provide a way to check the actual installed state.

For standalone skills, use a targeted install/update only after reviewing the
recorded source and local differences. Do not treat `npx skills check` as a
read-only operation: the inspected **skills CLI 1.7.4** maps `check`, `update`, and
`upgrade` to the same update handler, despite its README describing a check-only
command. Avoid blanket updates because shared skill folders may serve several
agents or contain a different workflow than the lock file suggests.

### Verified cleanup on 24 October 2026

The Matt Pocock plugin declared 27 skills. Its checkout also contained 11 other
skill files that were not declared by its manifest; those were not treated as
installed plugin skills. Disabled 26 exact standalone copies with Codex config,
preserving the files. Kept the standalone `prototype` workflow because it differs
from Matt Pocock's version and is tracked to Emil Kowalski's source.

A fresh Codex app-server reported 200 discovered entries, 174 enabled entries,
26 disabled standalone copies, all 27 Matt Pocock plugin skills enabled, and no
discovery errors. These counts describe that local runtime, not the full desktop
remote-plugin catalog. The earlier recursive-file inventory was not reliable.

During research, the `skills check` command applied source-tracked updates to
`prototype`, `apple-design`, `animation-vocabulary`, `tailwind-design-system`,
`agent-browser`, and `frontend-design` before it was stopped. The cleanup backup
under `~/.codex/backups/skill-management/` contains the resulting standalone files,
lock file, and the config from before disabling duplicates; it does not undo those
six upstream updates. No automatic update schedule was added.

Sources: [OpenAI skill discovery and disabling](https://learn.chatgpt.com/docs/build-skills),
[OpenAI marketplace management](https://developers.openai.com/plugins/build/plugins),
[OpenAI guidance on skill context](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra),
[Matt Pocock installation guidance](https://github.com/mattpocock/skills),
[UI Skills live catalog](https://www.ui-skills.com/cli), and
[standalone skills CLI](https://github.com/vercel-labs/skills).
