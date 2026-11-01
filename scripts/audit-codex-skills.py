#!/usr/bin/env python3
"""Read-only disk inventory; cached plugins are estimates, not runtime availability."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tomllib


def read_json(path):
    return json.loads(path.read_text())


def skill_files(root):
    """Follow an explicitly selected root, but never nested directory symlinks."""
    if root.is_file():
        return [root] if root.name == 'SKILL.md' else []
    found = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(directory) / d).is_symlink())
        if 'SKILL.md' in files:
            found.append(Path(directory) / 'SKILL.md')
    return sorted(found)


def name_of(text, path):
    frontmatter = text.split('---', 2)
    if len(frontmatter) == 3 and not frontmatter[0].strip():
        match = re.search(r'^name:\s*(.+?)\s*$', frontmatter[1], re.MULTILINE)
        if match:
            return match.group(1).strip('\"\'')
    return path.parent.name


def audit(home):
    config_path = home / '.codex/config.toml'
    config = tomllib.loads(config_path.read_text()) if config_path.exists() else {}
    disabled = {
        os.path.abspath(item['path'])
        for item in config.get('skills', {}).get('config', [])
        if item.get('enabled') is False and Path(item.get('path', '')).is_absolute()
    }
    lock_path = home / '.agents/.skill-lock.json'
    locks = read_json(lock_path).get('skills', {}) if lock_path.exists() else {}
    entries, warnings = [], []

    def add(path, kind, **metadata):
        content = path.read_bytes()
        entries.append({
            'name': name_of(content.decode(), path), 'path': str(path),
            'kind': kind, 'active': os.path.abspath(path) not in disabled,
            'sha256': hashlib.sha256(content).hexdigest(), **metadata,
        })

    for relative in ('.agents/skills', '.codex/skills'):
        root = home / relative
        if not root.exists():
            continue
        for folder in sorted(root.iterdir()):
            if folder.name == '.system':
                for path in skill_files(folder):
                    add(path, 'system')
            elif folder.is_dir():
                path = folder / 'SKILL.md'
                if path.is_file():
                    source = locks.get(folder.name, {})
                    add(path, 'local', source=source.get('source'),
                        source_url=source.get('sourceUrl'),
                        source_skill_path=source.get('skillPath'))
                elif folder.is_symlink() and not folder.exists():
                    warnings.append(f'Missing symlink target: {folder}')
            elif folder.is_symlink() and not folder.exists():
                warnings.append(f'Missing symlink target: {folder}')

    cache = home / '.codex/plugins/cache'
    for identity, settings in sorted(config.get('plugins', {}).items()):
        if settings.get('enabled') is not True:
            continue
        plugin, separator, marketplace = identity.partition('@')
        if not separator:
            warnings.append(f'Unrecognized plugin identity: {identity}')
            continue
        candidates = [cache / marketplace / plugin]
        if marketplace == 'openai-curated':
            candidates.append(cache / 'openai-curated-remote' / plugin)
        versions = [v for base in candidates if base.is_dir()
                    for v in base.iterdir() if v.is_dir()]
        if not versions:
            warnings.append(f'No cached version found for enabled plugin: {identity}')
            continue
        version = max(versions, key=lambda p: (p.stat().st_mtime_ns, str(p)))
        manifests = [version / '.codex-plugin/plugin.json',
                     version / '.claude-plugin/plugin.json', version / 'plugin.json']
        manifest_path = next((p for p in manifests if p.is_file()), None)
        if manifest_path is None:
            warnings.append(f'No plugin manifest: {identity} ({version.name})')
            continue
        manifest = read_json(manifest_path)
        roots = manifest.get('skills', './skills')
        roots = [roots] if isinstance(roots, str) else roots
        if not isinstance(roots, list) or not all(isinstance(p, str) for p in roots):
            raise ValueError(f'Invalid skills declaration: {manifest_path}')
        seen = set()
        for relative in roots:
            root = version / relative
            if Path(relative).is_absolute() or not root.resolve().is_relative_to(version.resolve()):
                raise ValueError(f'Skill path escapes plugin root: {identity}')
            if not root.exists():
                if 'skills' in manifest:
                    warnings.append(f'Missing declared skill path: {identity}: {relative}')
                continue
            for path in skill_files(root):
                if not path.resolve().is_relative_to(version.resolve()):
                    raise ValueError(f'Skill file escapes plugin root: {identity}')
                if path in seen:
                    continue
                seen.add(path)
                add(path, 'plugin', plugin=identity, marketplace=marketplace,
                    cached_version=version.name, manifest_version=manifest.get('version'),
                    manifest=str(manifest_path),
                    source=manifest.get('repository'),
                    version_selection='latest cache mtime estimate; runtime availability unverified')
    counts = Counter(item['name'] for item in entries if item['active'])
    return {
        'scope': 'User skill directories and enabled plugin disk caches; runtime availability unverified',
        'raw_entries': len(entries), 'distinct_names': len({e['name'] for e in entries}),
        'active_entries': sum(e['active'] for e in entries),
        'active_distinct_names': len(counts),
        'active_duplicates': {name: count for name, count in sorted(counts.items()) if count > 1},
        'entries': entries, 'warnings': warnings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--json', action='store_true', help='Print full inventory as JSON')
    args = parser.parse_args()
    try:
        report = audit(args.home.expanduser().absolute())
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        # Configuration contents may contain credentials: never print parser context.
        print(f'Inventory failed ({type(error).__name__}); check config, manifests, and file access.', file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report['scope'])
        print(f"{report['raw_entries']} entries; {report['distinct_names']} distinct names; "
              f"{report['active_entries']} active entries")
        for entry in report['entries']:
            status = 'active' if entry['active'] else 'disabled'
            print(f"{status:8} {entry['name']} [{entry['kind']}] {entry['path']}")
        print('Active duplicate names: ' + json.dumps(report['active_duplicates'], sort_keys=True))
        for warning in report['warnings']:
            print('Warning: ' + warning)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
