import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/sync-opencode-skills.py'


def load_module():
    spec = importlib.util.spec_from_file_location('sync_opencode', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.target = self.home / '.config/opencode/skills'

    def tearDown(self):
        self.temp.cleanup()

    def skill(self, relative, name='example'):
        folder = self.home / relative
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Example workflow\n---\nContent\n')
        return folder

    def run_cli(self, *args):
        env = {**os.environ}
        env.pop('XDG_CONFIG_HOME', None)
        return subprocess.run(['python3', str(SCRIPT), '--home', str(self.home), *args],
                              env=env, capture_output=True, text=True)

    def test_cli_defaults_to_dry_run_then_apply_is_idempotent(self):
        source = self.skill('.codex/skills/example')
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())
        for _ in range(2):
            result = self.run_cli('--apply')
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / 'example').resolve(), source.resolve())

    def test_shared_skills_need_no_projection(self):
        self.skill('.agents/skills/example')
        self.skill('.codex/skills/example')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())

    def test_claude_shared_skills_are_preserved(self):
        self.skill('.claude/skills/example')
        self.skill('.codex/skills/example')
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertFalse(self.target.exists())

    def test_disabled_and_system_skills_are_excluded(self):
        disabled = self.skill('.codex/skills/example') / 'SKILL.md'
        self.skill('.codex/skills/.system/internal', 'internal')
        (self.home / '.codex/config.toml').write_text(
            f'[[skills.config]]\npath = {json.dumps(str(disabled))}\nenabled = false\n')
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertFalse(self.target.exists())

    def test_collision_prevents_all_writes(self):
        self.skill('.codex/skills/a', 'a')
        self.skill('.codex/skills/z', 'z')
        (self.target / 'z').mkdir(parents=True)
        self.assertNotEqual(self.run_cli('--apply').returncode, 0)
        self.assertFalse((self.target / 'a').exists())
        self.assertTrue((self.target / 'z').is_dir())

    def test_broken_and_unrelated_symlinks_preserved(self):
        self.skill('.codex/skills/example')
        self.target.mkdir(parents=True)
        destination = self.target / 'example'
        destination.symlink_to(self.home / 'missing')
        self.assertNotEqual(self.run_cli('--apply').returncode, 0)
        self.assertEqual(destination.readlink(), self.home / 'missing')

    def test_parent_file_prevents_all_writes(self):
        self.skill('.codex/skills/example')
        (self.home / '.config').write_text('keep')
        self.assertNotEqual(self.run_cli('--apply').returncode, 0)
        self.assertEqual((self.home / '.config').read_text(), 'keep')

    def test_plan_rejects_unsafe_name_and_missing_source(self):
        module = load_module()
        for name, path in [('Display Name', self.skill('unsafe id')), ('example', self.home / 'missing')]:
            with self.subTest(name=name):
                plan = module.plan_links(self.home, self.target, [
                    {'name': name, 'path': str(path / 'SKILL.md'), 'kind': 'local', 'active': True}])
                self.assertTrue(plan['conflicts'])
                self.assertEqual(plan['links'], [])

    def test_duplicate_sources_conflict_but_identical_sources_deduplicate(self):
        module = load_module()
        a, b = self.skill('a/example'), self.skill('b/example')
        def entry(source):
            return {'name': 'example', 'path': str(source / 'SKILL.md'), 'kind': 'plugin', 'active': True}
        self.assertTrue(module.plan_links(self.home, self.target, [entry(a), entry(b)])['conflicts'])
        self.assertEqual(len(module.plan_links(self.home, self.target, [entry(a), entry(a)])['links']), 1)

    def test_enabled_plugin_manifest_projects_instruction_folder(self):
        source = self.skill('.codex/plugins/cache/test/collection/1/skills/example')
        manifest = source.parents[1] / '.codex-plugin/plugin.json'
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({'name': 'collection', 'skills': './skills'}))
        (self.home / '.codex/config.toml').write_text('[plugins."collection@test"]\nenabled = true\n')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / 'example').resolve(), source.resolve())

    def test_folder_id_is_used_instead_of_frontmatter_display_name(self):
        source = self.skill('.codex/skills/release', 'Release Workflow')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / 'release').resolve(), source.resolve())
        self.assertFalse((self.target / 'Release Workflow').exists())

    def test_shared_folder_id_prevents_display_name_projection(self):
        self.skill('.agents/skills/release', 'Shared Release Workflow')
        self.skill('.codex/skills/release', 'Release Workflow')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())

    def test_source_link_alias_id_is_preserved_before_resolving(self):
        module = load_module()
        source = self.skill('canonical/release', 'Release Workflow')
        alias = self.home / 'release-alias'
        alias.symlink_to(source)
        plan = module.plan_links(self.home, self.target, [
            {'name': 'Release Workflow', 'path': str(alias / 'SKILL.md'),
             'active': True, 'kind': 'local'}])
        self.assertEqual(plan['conflicts'], [])
        self.assertEqual(plan['links'], [(source.resolve(), self.target / 'release-alias')])

    def test_xdg_target(self):
        self.skill('.codex/skills/example')
        destination = self.home / 'xdg'
        result = subprocess.run(['python3', str(SCRIPT), '--home', str(self.home), '--apply'],
                                env={**os.environ, 'XDG_CONFIG_HOME': str(destination)},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((destination / 'opencode/skills/example').is_symlink())

    def test_main_in_process_covers_dry_run_apply_and_errors(self):
        module = load_module()
        self.skill('.codex/skills/example')
        env = {**os.environ}
        env.pop('XDG_CONFIG_HOME', None)
        def invoke(*extra):
            with patch.dict(os.environ, env, clear=True), patch('sys.argv', [str(SCRIPT), '--home', str(self.home), *extra]), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return module.main()
        self.assertEqual(invoke(), 0)
        self.assertEqual(invoke('--apply'), 0)
        self.assertEqual(invoke('--apply'), 0)
        (self.target / 'example').unlink()
        (self.target / 'example').mkdir()
        self.assertEqual(invoke('--apply'), 1)
        with patch.object(module, 'inventory', side_effect=ValueError('private')):
            self.assertEqual(invoke(), 1)
        with patch.object(module, 'inventory', return_value={'entries': [], 'warnings': ['fixture warning']}):
            self.assertEqual(invoke(), 0)
        with patch.dict(os.environ, {'XDG_CONFIG_HOME': 'relative'}), patch('sys.argv', [str(SCRIPT), '--home', str(self.home)]), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(module.main(), 1)

    def test_shared_discovery_ignores_hidden_and_finds_flat_and_links(self):
        module = load_module()
        root = self.home / '.agents/skills'
        root.mkdir(parents=True)
        (root / 'flat.md').write_text('description')
        (root / '.hidden.md').write_text('hidden')
        source = self.skill('external')
        (root / 'linked').symlink_to(source)
        self.skill('.agents/skills/group/nested', 'nested')
        self.skill('.agents/skills/.hidden/secret', 'secret')
        self.assertEqual(module.shared_ids(self.home), {'flat', 'linked', 'nested'})

    def test_apply_rejects_conflicted_plan_and_exclude_avoids_links(self):
        module = load_module()
        with self.assertRaises(ValueError):
            module.apply_plan({'links': [], 'conflicts': ['conflict']})
        source = self.skill('external/example')
        plan = module.plan_links(self.home, self.target, [
            {'name': 'example', 'path': str(source / 'SKILL.md'), 'active': True, 'kind': 'local'}], ['example'])
        self.assertEqual(plan['links'], [])
        self.assertEqual(plan['skipped'], ['example'])


if __name__ == '__main__':
    unittest.main()
