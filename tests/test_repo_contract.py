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


if __name__ == "__main__":
    unittest.main()
