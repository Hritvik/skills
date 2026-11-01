import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/install-codex.sh'


class InstallTests(unittest.TestCase):
    def run_install(self, home, *args):
        return subprocess.run(['bash', str(SCRIPT), *args],
                              env={**os.environ, 'HOME': str(home)},
                              text=True, capture_output=True)

    def test_installs_shared_skills_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            for _ in range(2):
                result = self.run_install(home)
                self.assertEqual(result.returncode, 0, result.stderr)
            for source in (ROOT / 'skills').iterdir():
                if (source / 'SKILL.md').is_file():
                    target = home / '.agents/skills' / source.name
                    self.assertTrue(target.is_symlink())
                    self.assertEqual(target.resolve(), source.resolve())

    def test_dry_run_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            result = self.run_install(home, '--dry-run')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / '.agents').exists())
            self.assertFalse((home / '.codex').exists())

    def test_conflicts_leave_all_existing_paths_untouched(self):
        for kind in ('directory', 'symlink', 'broken-symlink'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                source = next(p for p in (ROOT / 'skills').iterdir()
                              if (p / 'SKILL.md').is_file())
                target = home / '.agents/skills' / source.name
                target.parent.mkdir(parents=True)
                other = home / 'other'
                if kind == 'directory':
                    target.mkdir()
                else:
                    if kind == 'symlink':
                        other.mkdir()
                    target.symlink_to(other)
                result = self.run_install(home)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(target.is_dir() if kind == 'directory' else target.is_symlink())
                if kind != 'directory':
                    self.assertEqual(target.readlink(), other)
                self.assertFalse((home / '.codex').exists())

    def test_parent_conflict_is_detected_before_any_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / 'checkout'
            (checkout / 'scripts').mkdir(parents=True)
            shutil.copy2(SCRIPT, checkout / 'scripts/install-codex.sh')
            (checkout / 'skills/example').mkdir(parents=True)
            (checkout / 'skills/example/SKILL.md').write_text('example')
            (checkout / 'agents/codex').mkdir(parents=True)
            (checkout / 'agents/codex/example.toml').write_text('example')
            home = root / 'home'
            (home / '.codex').mkdir(parents=True)
            (home / '.codex/agents').write_text('preserve')
            result = subprocess.run(
                ['bash', str(checkout / 'scripts/install-codex.sh')],
                env={**os.environ, 'HOME': str(home)}, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((home / '.agents').exists())
            self.assertEqual((home / '.codex/agents').read_text(), 'preserve')

    def test_unknown_option_fails_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = self.run_install(Path(temporary), '--invalid')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(temporary).iterdir()), [])
