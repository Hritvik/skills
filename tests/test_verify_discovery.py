import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / 'scripts/install-skills.sh'
VERIFY = ROOT / 'scripts/verify-discovery.py'


def authored_skill_count():
    count = 0
    for pattern in ('skills/*/SKILL.md', 'plugins/*/skills/*/SKILL.md'):
        count += len(list(ROOT.glob(pattern)))
    return count


class VerifyDiscoveryTests(unittest.TestCase):
    def run_with_home(self, home, script, *args):
        command = (['bash', str(script)] if script.suffix == '.sh'
                   else [sys.executable, str(script)])
        return subprocess.run([*command, *args],
                              env={**os.environ, 'HOME': str(home)},
                              text=True, capture_output=True)

    def test_reports_missing_skills_before_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = self.run_with_home(Path(temporary), VERIFY, '--json', '--skip-opencode')
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(authored_skill_count(), report['expected'])
            self.assertFalse(report['ok'])
            for destination in report['destinations']:
                self.assertEqual(report['expected'], len(destination['missing']))

    def test_passes_after_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            install = self.run_with_home(home, INSTALL)
            self.assertEqual(install.returncode, 0, install.stderr)
            result = self.run_with_home(home, VERIFY, '--json', '--skip-opencode')
            self.assertEqual(result.returncode, 0, result.stdout)
            report = json.loads(result.stdout)
            self.assertTrue(report['ok'])
            for destination in report['destinations']:
                self.assertEqual(0, len(destination['missing']))
                self.assertEqual(0, len(destination['blocked']))


if __name__ == '__main__':
    unittest.main()
