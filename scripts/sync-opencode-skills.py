#!/usr/bin/env python3
"""Link Codex-only skill instructions into OpenCode; default is a read-only plan.

Enabled plugin caches are disk estimates, not proof of runtime availability.
This exports instructions/resources, not Codex tools, agents, hooks, or permissions.
"""
import argparse
import importlib.util
import os
from pathlib import Path
import re
import sys


def inventory(home):
    spec = importlib.util.spec_from_file_location(
        'codex_skill_audit', Path(__file__).with_name('audit-codex-skills.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit(home)


def shared_ids(home):
    """Preserve the IDs OpenCode already gets from shared compatibility roots."""
    result = set()
    for relative in ('.agents/skills', '.claude/skills'):
        root = home / relative
        if not root.is_dir():
            continue
        for directory, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [name for name in dirs if not name.startswith('.') and name != 'node_modules']
            current = Path(directory)
            if current == root:
                result.update(Path(name).stem for name in files
                              if name.endswith('.md') and not name.startswith('.'))
            if 'SKILL.md' in files:
                result.add(current.name)
                dirs[:] = []
            # os.walk does not enter linked children; inspect explicit skill links.
            for name in dirs:
                child = current / name
                if child.is_symlink() and (child / 'SKILL.md').is_file():
                    result.add(name)
    return result


def plan_links(home, target, entries, excluded=()):
    """Plan without writes; preserve shared and existing installation owners."""
    links, conflicts, skipped = [], [], []
    shared = shared_ids(home)
    candidates = {}
    for entry in entries:
        # OpenCode derives IDs from folder paths; frontmatter is only a label.
        name = Path(entry['path']).parent.name
        if not entry.get('active') or entry.get('kind') not in ('local', 'plugin'):
            continue
        if name in shared or name in excluded:
            skipped.append(name)
            continue
        if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', name) or name in ('.', '..'):
            conflicts.append(f'Unsafe skill ID: {name!r}')
            continue
        source = Path(entry['path']).parent.resolve()
        if not (source / 'SKILL.md').is_file():
            conflicts.append(f'Missing skill entrypoint: {source}')
            continue
        candidates.setdefault(name, set()).add(source)
    for name, sources in sorted(candidates.items()):
        if len(sources) != 1:
            conflicts.append(f'Multiple sources for {name}; use --exclude {name} and resolve deliberately.')
            continue
        source = next(iter(sources))
        destination = target / name
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink() and destination.resolve() == source:
                skipped.append(name)
            else:
                conflicts.append(f'Existing destination preserved: {destination}')
        else:
            links.append((source, destination))
    if links:
        parent = target
        while parent != parent.parent:
            if (parent.exists() or parent.is_symlink()) and not parent.is_dir():
                conflicts.append(f'Destination parent is not a directory: {parent}')
                break
            parent = parent.parent
    return {'links': links, 'conflicts': conflicts, 'skipped': sorted(set(skipped))}


def apply_plan(plan):
    """Apply only a conflict-free plan; never replace or delete an existing path."""
    if plan['conflicts']:
        raise ValueError('Resolve conflicts before applying the plan.')
    for source, destination in plan['links']:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source, target_is_directory=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--apply', action='store_true', help='Create the planned links')
    parser.add_argument('--exclude', action='append', default=[], help='Preserve/skip an ambiguous skill ID')
    args = parser.parse_args()
    home = args.home.expanduser().absolute()
    config_home = Path(os.environ.get('XDG_CONFIG_HOME', str(home / '.config'))).expanduser()
    if not config_home.is_absolute():
        print('XDG_CONFIG_HOME must be absolute.', file=sys.stderr)
        return 1
    try:
        report = inventory(home)
        plan = plan_links(home, config_home / 'opencode/skills', report['entries'], args.exclude)
        print('Instructions/resources only; plugin cache versions are estimates. Verify with OpenCode skill.list.')
        for warning in report['warnings']:
            print(f'Warning: {warning}')
        for source, destination in plan['links']:
            print(f'Would link: {destination} -> {source}')
        for conflict in plan['conflicts']:
            print(f'Conflict: {conflict}', file=sys.stderr)
        print(f"{len(plan['links'])} links planned; {len(plan['skipped'])} IDs already shared, linked, or excluded.")
        if plan['conflicts']:
            return 1
        if args.apply:
            apply_plan(plan)
            print('Applied. No existing files or client configuration were replaced.')
        return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        # Config parser errors can embed secret values; never print their context.
        print('Sync failed; check source manifests, configuration, and file access.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
