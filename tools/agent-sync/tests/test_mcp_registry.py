"""Canonical MCP registry: loading, filtering, and secret references."""

import tempfile
import unittest
from pathlib import Path

import yaml

from agent_sync.exceptions import ConfigNotFoundError
from agent_sync.redaction import extract_env_references
from agent_sync.registry import (
    filter_servers_by_client,
    filter_servers_by_profile,
    load_profiles,
    load_registry,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class RegistryLoadingTests(unittest.TestCase):
    def test_examples_registry_loads(self):
        registry = load_registry(EXAMPLES / "servers.yaml")
        self.assertEqual(1, registry.version)
        self.assertEqual(
            {"context7", "playwright", "github", "postgres", "filesystem"},
            set(registry.servers),
        )

    def test_missing_registry_raises(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ConfigNotFoundError):
                load_registry(Path(temp) / "absent.yaml")

    def test_unsupported_version_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "servers.yaml"
            path.write_text(yaml.safe_dump({"version": 2, "servers": {}}), encoding="utf-8")
            with self.assertRaises(Exception):
                load_registry(path)

    def test_examples_profiles_load(self):
        profiles = load_profiles(EXAMPLES / "profiles.yaml")
        self.assertTrue(profiles.profiles)


class RegistryFilteringTests(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry(EXAMPLES / "servers.yaml")

    def test_client_include_list_is_respected(self):
        codex_servers = filter_servers_by_client(self.registry, "codex")
        self.assertIn("context7", codex_servers.servers)
        self.assertIn("postgres", codex_servers.servers)

        zoom_servers = filter_servers_by_client(self.registry, "zoom")
        self.assertNotIn("context7", zoom_servers.servers)
        self.assertIn("playwright", zoom_servers.servers)

    def test_profile_selection_returns_named_servers(self):
        profiles = load_profiles(EXAMPLES / "profiles.yaml")
        name = next(iter(profiles.profiles))
        selected = filter_servers_by_profile(self.registry, profiles, name)
        self.assertTrue(set(selected.servers) <= set(self.registry.servers))

    def test_unknown_profile_raises(self):
        profiles = load_profiles(EXAMPLES / "profiles.yaml")
        with self.assertRaises(ValueError):
            filter_servers_by_profile(self.registry, profiles, "does-not-exist")


class SecretReferenceTests(unittest.TestCase):
    def test_env_references_are_extracted_not_resolved(self):
        data = yaml.safe_load((EXAMPLES / "servers.yaml").read_text(encoding="utf-8"))
        references = extract_env_references(data)
        self.assertIn("CONTEXT7_TOKEN", references)
        self.assertIn("GITHUB_PERSONAL_ACCESS_TOKEN", references)


if __name__ == "__main__":
    unittest.main()
