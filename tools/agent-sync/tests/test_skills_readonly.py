"""The skills store is read-only for agent-sync: the skills repo owns installation."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from agent_sync.cli import app
from agent_sync.skills import (
    SkillValidationError,
    discover_skills,
    parse_skill_frontmatter,
    validate_all_skills,
    validate_skill_frontmatter,
)


def write_skill(root: Path, name: str = "example", description: str = "Example") -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\nBody.\n",
        encoding="utf-8",
    )
    return directory


class SkillReadOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        patcher = patch("pathlib.Path.home", return_value=self.home)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = self.home / ".agents" / "skills"
        self.store.mkdir(parents=True)

    def test_skill_adapters_package_is_gone(self):
        self.assertIsNone(importlib.util.find_spec("agent_sync.skill_adapters"))

    def test_skill_commands_are_read_only(self):
        result = CliRunner().invoke(app, ["skills", "--help"])
        self.assertEqual(0, result.exit_code, result.output)
        for writer in ("apply", "remove", "diff", "import"):
            self.assertNotIn(writer, result.output)
        for reader in ("list", "validate", "show", "doctor"):
            self.assertIn(reader, result.output)

    def test_read_commands_never_create_the_canonical_store(self):
        absent_home = self.home / "absent"
        with patch("pathlib.Path.home", return_value=absent_home):
            for command in ("list", "validate", "doctor"):
                result = CliRunner().invoke(app, ["skills", command])
                self.assertEqual(0, result.exit_code, result.output)
            self.assertFalse((absent_home / ".agents").exists())

    def test_list_reports_discovered_skills(self):
        write_skill(self.store, "alpha")
        write_skill(self.store, "beta")
        result = CliRunner().invoke(app, ["skills", "list"])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIn("alpha", result.output)
        self.assertIn("beta", result.output)

    def test_show_rejects_unknown_skill(self):
        result = CliRunner().invoke(app, ["skills", "show", "missing"])
        self.assertEqual(1, result.exit_code)


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Path(self.temp.name)

    def test_valid_skill_passes(self):
        write_skill(self.store)
        results = validate_all_skills(self.store)
        self.assertEqual(1, len(results))
        self.assertIsNone(results[0][1])

    def test_missing_description_fails(self):
        directory = self.store / "example"
        directory.mkdir()
        skill_md = directory / "SKILL.md"
        skill_md.write_text("---\nname: example\n---\n", encoding="utf-8")
        frontmatter = parse_skill_frontmatter(skill_md)
        with self.assertRaises(SkillValidationError) as caught:
            validate_skill_frontmatter(frontmatter, skill_md)
        self.assertEqual("description", caught.exception.field)

    def test_non_skill_directories_are_ignored(self):
        (self.store / "notes").mkdir()
        (self.store / "notes" / "readme.md").write_text("not a skill")
        write_skill(self.store)
        self.assertEqual(["example"], [path.name for path in discover_skills(self.store)])

    def test_missing_store_is_empty_not_an_error(self):
        self.assertEqual([], discover_skills(self.store / "absent"))
        self.assertEqual([], validate_all_skills(self.store / "absent"))


if __name__ == "__main__":
    unittest.main()
