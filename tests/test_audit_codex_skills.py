import importlib.util
import json
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/audit-codex-skills.py'


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def write(self, path, text):
        target = self.home / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def skill(self, path, name='example'):
        return self.write(path + '/SKILL.md', f'---\nname: {name}\n---\nBody\n')

    def audit(self):
        spec = importlib.util.spec_from_file_location('audit', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.audit(self.home)

    def test_symlink_system_disabled_duplicates_and_lock(self):
        original = self.skill('.agents/skills/demo')
        link = self.home / '.codex/skills/demo'
        link.parent.mkdir(parents=True)
        link.symlink_to(original.parent, target_is_directory=True)
        self.skill('.codex/skills/.system/system', 'system')
        (link.parent / 'loop').symlink_to(link.parent, target_is_directory=True)
        self.write('.agents/.skill-lock.json', json.dumps({'skills': {'demo': {'source': 'org/repo'}}}))
        self.write('.codex/config.toml', f'[[skills.config]]\npath = "{link / "SKILL.md"}"\nenabled = false\n')
        report = self.audit()
        self.assertEqual(report['raw_entries'], 3)
        self.assertEqual(report['distinct_names'], 2)
        self.assertEqual(report['active_duplicates'], {})
        self.assertEqual(sum(item['active'] for item in report['entries']), 2)
        self.assertEqual(report['entries'][0]['source'], 'org/repo')
        self.assertEqual(len(report['entries'][0]['sha256']), 64)

    def test_manifest_excludes_undeclared_and_disabled_plugins(self):
        self.write('.codex/config.toml', '[plugins."bundle@market"]\nenabled = true\n[plugins."off@market"]\nenabled = false\n')
        root = '.codex/plugins/cache/market/bundle/1.0'
        self.write(root + '/.codex-plugin/plugin.json', json.dumps({'skills': ['./skills/included']}))
        self.skill(root + '/skills/included', 'included')
        self.skill(root + '/skills/omitted', 'omitted')
        self.skill(root + '/docs/hidden', 'hidden')
        self.write('.codex/plugins/cache/market/off/1/.claude-plugin/plugin.json', '{"skills":"./skills"}')
        self.skill('.codex/plugins/cache/market/off/1/skills/off', 'off')
        report = self.audit()
        self.assertEqual([entry['name'] for entry in report['entries']], ['included'])
        self.assertEqual(report['entries'][0]['plugin'], 'bundle@market')
        self.assertIn('estimate', report['entries'][0]['version_selection'])

    def test_portable_default_and_claude_fallback(self):
        self.write('.codex/config.toml', '[plugins."bundle@market"]\nenabled = true\n')
        root = '.codex/plugins/cache/market/bundle/1'
        self.write(root + '/.claude-plugin/plugin.json', '{}')
        self.skill(root + '/skills/demo')
        self.assertEqual(self.audit()['raw_entries'], 1)

    def test_missing_declared_path_warns(self):
        self.write('.codex/config.toml', '[plugins."missing@market"]\nenabled = true\n')
        report = self.audit()
        self.assertEqual(report['raw_entries'], 0)
        self.assertTrue(report['warnings'])

    def test_active_duplicates_are_counted_and_content_preserved(self):
        one = self.skill('.agents/skills/one', 'same')
        two = self.skill('.codex/skills/two', 'same')
        before = (one.read_bytes(), two.read_bytes())
        report = self.audit()
        self.assertEqual(report['active_duplicates'], {'same': 2})
        self.assertEqual(report['distinct_names'], 1)
        self.assertEqual(before, (one.read_bytes(), two.read_bytes()))

    def test_missing_manifest_path_warns(self):
        self.write('.codex/config.toml', '[plugins."bundle@market"]\nenabled = true\n')
        self.write('.codex/plugins/cache/market/bundle/1/.codex-plugin/plugin.json',
                   '{"skills":"./absent"}')
        report = self.audit()
        self.assertEqual(report['raw_entries'], 0)
        self.assertIn('Missing declared skill path', report['warnings'][0])

    def test_portable_root_manifest(self):
        self.write('.codex/config.toml', '[plugins."bundle@market"]\nenabled = true\n')
        root = '.codex/plugins/cache/market/bundle/1'
        self.write(root + '/plugin.json', '{"skills":"./declared"}')
        self.skill(root + '/declared/demo')
        self.skill(root + '/skills/hidden', 'hidden')
        report = self.audit()
        self.assertEqual([entry['name'] for entry in report['entries']], ['example'])

    def test_external_declared_paths_rejected(self):
        self.write('.codex/config.toml', '[plugins."bundle@market"]\nenabled = true\n')
        root = '.codex/plugins/cache/market/bundle/1'
        manifest = root + '/plugin.json'
        for declaration in ('../outside', str(self.home / 'outside')):
            self.write(manifest, json.dumps({'skills': declaration}))
            with self.subTest(declaration=declaration), self.assertRaises(ValueError):
                self.audit()
        outside = self.skill('outside')
        link = self.home / root / 'linked'
        link.symlink_to(outside.parent, target_is_directory=True)
        self.write(manifest, '{"skills":"./linked"}')
        with self.assertRaises(ValueError):
            self.audit()

    def test_tool_only_plugin_has_no_missing_skill_warning(self):
        self.write('.codex/config.toml', '[plugins."tool@market"]\nenabled = true\n')
        self.write('.codex/plugins/cache/market/tool/1/plugin.json', '{}')
        report = self.audit()
        self.assertEqual(report['raw_entries'], 0)
        self.assertEqual(report['warnings'], [])

    def test_wrong_config_type_fails_safely_without_leaking(self):
        self.write('.codex/config.toml', 'skills = "private-value"\n')
        result = subprocess.run([sys.executable, str(SCRIPT), '--home', str(self.home)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Inventory failed', result.stderr)
        self.assertNotIn('private-value', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_malformed_config_fails(self):
        self.write('.codex/config.toml', 'invalid = [')
        with self.assertRaises(ValueError):
            self.audit()


if __name__ == '__main__':
    unittest.main()
