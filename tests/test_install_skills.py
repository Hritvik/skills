import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/install-skills.sh'
DESTINATIONS = (Path('.agents') / 'skills', Path('.claude') / 'skills')


def authored_skills():
    found = []
    for pattern in ('skills/*/SKILL.md', 'plugins/*/skills/*/SKILL.md'):
        found.extend(entry.parent for entry in sorted(ROOT.glob(pattern)))
    return found


class InstallTests(unittest.TestCase):
    def run_install(self, home, *args):
        return subprocess.run(['bash', str(SCRIPT), *args],
                              env={**os.environ, 'HOME': str(home)},
                              text=True, capture_output=True)

    def test_links_every_skill_into_every_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            for _ in range(2):
                result = self.run_install(home)
                self.assertEqual(result.returncode, 0, result.stderr)
            for source in authored_skills():
                for destination in DESTINATIONS:
                    target = home / destination / source.name
                    self.assertTrue(target.is_symlink(), target)
                    self.assertEqual(target.resolve(), source.resolve())

    def test_dry_run_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            result = self.run_install(home, '--dry-run')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / '.agents').exists())
            self.assertFalse((home / '.claude').exists())
            self.assertFalse((home / '.codex').exists())

    def test_blocked_path_is_preserved_while_the_rest_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            blocked_source, other_source = authored_skills()[0], authored_skills()[-1]
            blocked = home / DESTINATIONS[0] / blocked_source.name
            blocked.mkdir(parents=True)
            result = self.run_install(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(blocked.is_dir())
            self.assertFalse(blocked.is_symlink())
            linked = home / DESTINATIONS[0] / other_source.name
            self.assertTrue(linked.is_symlink())
            self.assertTrue((home / DESTINATIONS[1] / blocked_source.name).is_symlink())

    def test_prune_removes_only_links_into_this_repo(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(self.run_install(home).returncode, 0)
            source = authored_skills()[0]
            stale = home / DESTINATIONS[0] / 'zzz-stale'
            stale.symlink_to(source)
            foreign = home / DESTINATIONS[0] / 'zzz-foreign'
            other = home / 'elsewhere'
            other.mkdir()
            foreign.symlink_to(other)
            result = self.run_install(home, '--prune')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale.is_symlink())
            self.assertTrue(foreign.is_symlink())

    def test_duplicate_names_fail_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / 'checkout'
            (checkout / 'scripts').mkdir(parents=True)
            shutil.copy2(SCRIPT, checkout / 'scripts/install-skills.sh')
            (checkout / 'skills/duplicate').mkdir(parents=True)
            (checkout / 'skills/duplicate/SKILL.md').write_text('first')
            (checkout / 'plugins/alpha').mkdir(parents=True)
            (checkout / 'plugins/alpha/skills/duplicate').mkdir(parents=True)
            (checkout / 'plugins/alpha/skills/duplicate/SKILL.md').write_text('second')
            home = root / 'home'
            result = subprocess.run(
                ['bash', str(checkout / 'scripts/install-skills.sh')],
                env={**os.environ, 'HOME': str(home)}, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Duplicate skill name', result.stderr)
            self.assertFalse((home / '.agents').exists())

    def test_parent_conflict_is_detected_for_that_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / 'checkout'
            (checkout / 'scripts').mkdir(parents=True)
            shutil.copy2(SCRIPT, checkout / 'scripts/install-skills.sh')
            (checkout / 'skills/example').mkdir(parents=True)
            (checkout / 'skills/example/SKILL.md').write_text('example')
            (checkout / 'agents/codex').mkdir(parents=True)
            (checkout / 'agents/codex/example.toml').write_text('example')
            home = root / 'home'
            (home / '.codex').mkdir(parents=True)
            (home / '.codex/agents').write_text('preserve')
            result = subprocess.run(
                ['bash', str(checkout / 'scripts/install-skills.sh')],
                env={**os.environ, 'HOME': str(home)}, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((home / '.codex/agents').read_text(), 'preserve')
            self.assertTrue((home / '.agents/skills/example').is_symlink())

    def test_unknown_option_fails_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = self.run_install(Path(temporary), '--invalid')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(temporary).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
