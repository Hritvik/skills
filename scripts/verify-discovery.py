#!/usr/bin/env python3
"""Verify that every authored skill is discoverable in every client.

Reads the repository as the source of truth, then checks each client's actual
skill location. OpenCode is checked through its runtime API, not the disk, so a
link that exists but is not loaded still fails.

Exit codes: 0 all discoverable, 1 anything missing, blocked, shadowed, or stale.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()

SKILL_DESTINATIONS = (
    ("codex+opencode", HOME / ".agents" / "skills"),
    ("claude", HOME / ".claude" / "skills"),
)
CODEX_CONFIG = HOME / ".codex" / "config.toml"
PAYLOAD_MARKERS = ("hooks", "commands", "agents", ".mcp.json")


def authored_skills():
    """Return {name: source} for every skill in the repository."""
    found = {}
    duplicates = []
    for pattern in ("skills/*/SKILL.md", "plugins/*/skills/*/SKILL.md"):
        for entry in sorted(REPO_ROOT.glob(pattern)):
            source = entry.parent
            name = source.name
            if name in found:
                duplicates.append((name, str(found[name]), str(source)))
            else:
                found[name] = source
    return found, duplicates


def check_destination(root, expected):
    """Classify each expected skill at one destination."""
    report = {"root": str(root), "linked": [], "missing": [], "blocked": [], "stale": []}
    if not root.is_dir():
        report["missing"] = sorted(expected)
        return report

    for name, source in sorted(expected.items()):
        path = root / name
        if path.is_symlink():
            target = os.readlink(path)
            if target == str(source):
                report["linked"].append(name)
            elif target.startswith(str(REPO_ROOT) + os.sep):
                report["stale"].append(f"{name} -> {target}")
            else:
                report["blocked"].append(f"{name} (link to {target})")
        elif path.exists():
            kind = "directory" if path.is_dir() else "file"
            report["blocked"].append(f"{name} (real {kind})")
        else:
            report["missing"].append(name)

    for entry in sorted(root.iterdir()):
        if not entry.is_symlink():
            continue
        target = os.readlink(entry)
        if target.startswith(str(REPO_ROOT) + os.sep) and entry.name not in expected:
            report["stale"].append(f"{entry.name} -> {target}")
    return report


def check_codex_disabled(expected):
    """Codex can disable a skill by exact path; that defeats 'everything everywhere'."""
    disabled = []
    if not CODEX_CONFIG.is_file():
        return disabled
    try:
        data = tomllib.loads(CODEX_CONFIG.read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return disabled
    for entry in (data.get("skills") or {}).get("config") or []:
        path = Path(str(entry.get("path", "")))
        if entry.get("enabled", True) is False and path.parent.name in expected:
            disabled.append(f"{path.parent.name} ({path})")
    return disabled


def check_opencode(expected, attempts=4, delay=2.0):
    """Ask the OpenCode runtime what it loaded; retry while its scan warms up."""
    command = [
        "opencode",
        "api",
        "GET",
        "/api/skill",
        "--header",
        f"x-opencode-directory:{REPO_ROOT}",
    ]
    last_error = None
    payload = None
    for attempt in range(attempts):
        try:
            # OpenCode truncates large output through a pipe; capture to a file.
            with tempfile.TemporaryFile("w+", suffix=".json") as handle:
                result = subprocess.run(
                    command, stdout=handle, stderr=subprocess.PIPE, text=True, timeout=90
                )
                handle.seek(0)
                raw = handle.read()
        except (OSError, subprocess.SubprocessError) as error:
            last_error = str(error)
            break
        if result.returncode == 0 and raw.strip():
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as error:
                last_error = f"invalid JSON: {error}"
            else:
                if payload.get("data"):
                    break
        else:
            last_error = (result.stderr or raw).strip()[:200]
        if attempt + 1 < attempts:
            time.sleep(delay)

    if payload is None:
        return {"available": False, "error": last_error, "missing": sorted(expected), "shadowed": [], "total": 0}

    loaded = {}
    for item in payload.get("data") or []:
        path = item.get("path")
        if path:
            loaded[item.get("id")] = Path(path)

    missing, shadowed = [], []
    for name in sorted(expected):
        if name not in loaded:
            missing.append(name)
        elif not str(loaded[name].resolve()).startswith(str(REPO_ROOT) + os.sep):
            shadowed.append(f"{name} -> {loaded[name]}")
    return {
        "available": True,
        "error": None,
        "missing": missing,
        "shadowed": shadowed,
        "total": len(loaded),
    }


def plugin_payloads():
    """Plugins whose non-skill parts cannot be delivered by linking folders."""
    carriers = []
    for plugin in sorted((REPO_ROOT / "plugins").glob("*")):
        if not plugin.is_dir():
            continue
        if any((plugin / marker).exists() for marker in PAYLOAD_MARKERS):
            carriers.append(plugin.name)
    return carriers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    parser.add_argument("--skip-opencode", action="store_true", help="Skip the live runtime check")
    args = parser.parse_args()

    expected, duplicates = authored_skills()
    destinations = [(label, check_destination(root, expected)) for label, root in SKILL_DESTINATIONS]
    disabled = check_codex_disabled(expected)
    opencode = {"available": False, "skipped": True, "missing": [], "shadowed": [], "total": 0}
    if not args.skip_opencode:
        opencode = check_opencode(expected)
    payload = plugin_payloads()

    problems = []
    if duplicates:
        problems.append(f"{len(duplicates)} duplicate skill name(s) inside the repository")
    for label, report in destinations:
        for key in ("missing", "blocked", "stale"):
            if report[key]:
                problems.append(f"{label}: {len(report[key])} {key}")
    if disabled:
        problems.append(f"codex: {len(disabled)} authored skill(s) disabled in config")
    if not opencode.get("skipped"):
        if not opencode.get("available"):
            problems.append("opencode: runtime inventory unavailable")
        else:
            if opencode["missing"]:
                problems.append(f"opencode: {len(opencode['missing'])} missing")
            if opencode["shadowed"]:
                problems.append(f"opencode: {len(opencode['shadowed'])} shadowed")

    if args.json:
        print(json.dumps({
            "repo": str(REPO_ROOT),
            "expected": len(expected),
            "duplicates": duplicates,
            "destinations": [{"label": label, **report} for label, report in destinations],
            "codex_disabled": disabled,
            "opencode": opencode,
            "plugin_payloads": payload,
            "ok": not problems,
            "problems": problems,
        }, indent=2))
        return 0 if not problems else 1

    standalone = sum(1 for source in expected.values() if source.parent == REPO_ROOT / "skills")
    print(f"Repository: {REPO_ROOT}")
    print(f"Expected skills: {len(expected)} ({standalone} standalone, {len(expected) - standalone} in plugins)")
    if duplicates:
        print("\nDuplicate names inside the repository:")
        for name, first, second in duplicates:
            print(f"  {name}: {first} / {second}")

    for label, report in destinations:
        print(f"\n{label}: {report['root']}")
        print(f"  linked {len(report['linked'])}, missing {len(report['missing'])}, "
              f"blocked {len(report['blocked'])}, stale {len(report['stale'])}")
        for key, heading in (("missing", "missing"), ("blocked", "blocked"), ("stale", "stale")):
            for item in report[key]:
                print(f"  {heading}: {item}")

    print("\nopencode (runtime):")
    if opencode.get("skipped"):
        print("  skipped")
    elif not opencode.get("available"):
        print(f"  unavailable: {opencode.get('error')}")
    else:
        loaded = opencode["total"]
        print(f"  {len(expected) - len(opencode['missing'])}/{len(expected)} authored skills loaded "
              f"of {loaded} total")
        for item in opencode["missing"]:
            print(f"  missing: {item}")
        for item in opencode["shadowed"]:
            print(f"  shadowed: {item}")

    if disabled:
        print("\ncodex config disables authored skills:")
        for item in disabled:
            print(f"  {item}")

    if payload:
        print(f"\nnote: {len(payload)} plugin(s) also carry hooks, commands, agents, or MCP config.")
        print("      Linking delivers skills only; those parts need the native plugin install.")

    print("\n" + ("OK: every authored skill is discoverable." if not problems else "FAIL: " + "; ".join(problems)))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
