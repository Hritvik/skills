import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_codex_marketplace_plugins_resolve_to_valid_manifests(self):
        marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
        marketplace = json.loads(marketplace_path.read_text())

        self.assertEqual("hritvik-skills", marketplace["name"])
        self.assertTrue(marketplace["plugins"])

        for entry in marketplace["plugins"]:
            source = entry["source"]
            self.assertEqual("local", source["source"])
            plugin_root = (marketplace_path.parent / source["path"]).resolve()
            manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
            self.assertTrue(manifest_path.is_file(), manifest_path)
            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(entry["name"], manifest["name"])

    def test_claude_marketplace_plugins_resolve_to_valid_manifests(self):
        marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
        marketplace = json.loads(marketplace_path.read_text())

        self.assertEqual("hritvik-skills", marketplace["name"])
        self.assertTrue(marketplace["plugins"])

        for entry in marketplace["plugins"]:
            plugin_root = (ROOT / entry["source"]).resolve()
            manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
            self.assertTrue(manifest_path.is_file(), manifest_path)
            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(entry["name"], manifest["name"])

    def test_marketplaces_describe_the_same_plugins(self):
        codex_marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )
        claude_marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text()
        )

        codex_names = {entry["name"] for entry in codex_marketplace["plugins"]}
        claude_names = {entry["name"] for entry in claude_marketplace["plugins"]}
        self.assertEqual(codex_names, claude_names)

    def test_standalone_skills_have_valid_entrypoints(self):
        skills_root = ROOT / "skills"
        if not skills_root.exists():
            return

        skill_directories = (path for path in skills_root.iterdir() if path.is_dir())
        for skill_root in skill_directories:
            skill_file = skill_root / "SKILL.md"
            self.assertTrue(skill_file.is_file(), skill_file)
            contents = skill_file.read_text()
            self.assertTrue(contents.startswith("---\n"), skill_file)
            self.assertIn("\nname:", contents, skill_file)
            self.assertIn("\ndescription:", contents, skill_file)


class ToolOwnershipContractTests(unittest.TestCase):
    """One writer per destination: the installer owns skills, the tool owns MCP config."""

    def setUp(self):
        self.tool = ROOT / "tools" / "agent-sync"

    def test_agent_sync_is_a_self_contained_tool(self):
        pyproject = (self.tool / "pyproject.toml").read_text()
        self.assertIn('agent-sync = "agent_sync.cli:app"', pyproject)
        self.assertTrue((self.tool / "src" / "agent_sync" / "cli.py").is_file())
        self.assertTrue((self.tool / "tests").is_dir())
        self.assertFalse((ROOT / "pyproject.toml").exists())

    def test_installer_is_the_only_writer_of_the_skill_store(self):
        writers = []
        for script in (ROOT / "scripts").iterdir():
            if not script.is_file():
                continue
            text = script.read_text(errors="ignore")
            if "skill_targets=" in text:
                writers.append(script.name)
        self.assertEqual(["install-skills.sh"], writers)

    def test_installer_covers_every_skill_destination(self):
        installer = (ROOT / "scripts" / "install-skills.sh").read_text()
        for destination in (".agents/skills", ".claude/skills", ".codex/agents"):
            self.assertIn(destination, installer)

    def test_authored_skill_names_are_unique(self):
        seen = {}
        for pattern in ("skills/*/SKILL.md", "plugins/*/skills/*/SKILL.md"):
            for entry in ROOT.glob(pattern):
                self.assertNotIn(
                    entry.parent.name,
                    seen,
                    f"{entry.parent} duplicates {seen.get(entry.parent.name)}",
                )
                seen[entry.parent.name] = entry.parent

    def test_agent_sync_does_not_write_skills(self):
        self.assertFalse((self.tool / "src" / "agent_sync" / "skill_adapters").exists())
        skills_module = (self.tool / "src" / "agent_sync" / "skills.py").read_text()
        self.assertNotIn("def import_skills_from_codex", skills_module)
        self.assertNotIn("def save_skill_registry", skills_module)

    def test_agent_sync_skills_commands_are_read_only(self):
        cli = (self.tool / "src" / "agent_sync" / "cli.py").read_text()
        skills_section = cli.split("# Skills Commands", 1)[1]
        skills_commands = skills_section.split("@app.callback()", 1)[0]
        for writer in ("def apply(", "def remove(", "def diff(", "def import_skills("):
            self.assertNotIn(writer, skills_commands)
        for reader in ("def list_skills(", "def validate_skills(", "def show(", "def doctor("):
            self.assertIn(reader, skills_commands)


if __name__ == "__main__":
    unittest.main()