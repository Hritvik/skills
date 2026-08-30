import json
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_report_validator():
    path = ROOT / "skills/hotel-comparison/scripts/validate_report.py"
    spec = importlib.util.spec_from_file_location("hotel_report_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_trip_validator():
    path = ROOT / "skills/trip-site-publisher/scripts/validate_trip_artifact.py"
    spec = importlib.util.spec_from_file_location("trip_artifact_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PluginContractTests(unittest.TestCase):
    def test_manifest_exposes_all_research_skills(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "decision-guide")
        self.assertEqual(manifest["skills"], "./skills/")

        expected = {
            "destination-area-planner",
            "hotel-comparison",
            "itinerary-builder",
            "movie-ticket-finder",
            "product-comparison-research",
            "shopping-price-finder",
            "transport-comparison",
            "trip-budget-planner",
            "trip-feasibility-checker",
            "trip-opportunity-finder",
            "trip-site-publisher",
            "trip-verification",
            "vacation-planner",
        }
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)

    def test_manifest_starter_prompts_fit_plugin_ui_contract(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in prompts))
        self.assertTrue(any("vacation" in prompt.lower() for prompt in prompts))

    def test_vacation_orchestrator_composes_required_specialists(self):
        skill = (ROOT / "skills/vacation-planner/SKILL.md").read_text()
        for required in (
            "grilling",
            "trip-opportunity-finder",
            "trip-feasibility-checker",
            "transport-comparison",
            "destination-area-planner",
            "itinerary-builder",
            "trip-budget-planner",
            "trip-verification",
            "trip-site-publisher",
            "hotel-comparison",
        ):
            self.assertIn(required, skill)

    def test_vacation_orchestrator_supports_both_planning_modes(self):
        skill = (ROOT / "skills/vacation-planner/SKILL.md").read_text()
        self.assertIn("fixed-destination", skill)
        self.assertIn("open-ended discovery", skill)
        self.assertIn("10%", skill)

    def test_trip_site_contract_is_versioned_and_data_driven(self):
        schema = json.loads(
            (ROOT / "skills/trip-site-publisher/references/trip-artifact.schema.json").read_text()
        )
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("schemaVersion", schema["required"])
        self.assertIn("kind", schema["required"])
        self.assertIn("evidence", schema["properties"])

    def test_example_artifacts_cover_fixed_and_exploratory_trips(self):
        fixed = json.loads((ROOT / "examples/coorg-road-trip.json").read_text())
        exploratory = json.loads(
            (ROOT / "examples/international-under-50000.json").read_text()
        )
        self.assertEqual(fixed["mode"], "fixed-destination")
        self.assertEqual(exploratory["mode"], "open-ended-discovery")
        self.assertGreaterEqual(len(exploratory["itineraries"]), 3)

    def test_trip_artifact_validator_accepts_examples(self):
        validator = load_trip_validator()
        for filename in ("coorg-road-trip.json", "international-under-50000.json"):
            artifact = json.loads((ROOT / "examples" / filename).read_text())
            self.assertEqual(validator.validate(artifact), [])

    def test_trip_artifact_validator_rejects_unsafe_references(self):
        validator = load_trip_validator()
        artifact = json.loads((ROOT / "examples/coorg-road-trip.json").read_text())
        artifact["itineraries"][0]["budgetItems"][0]["sourceIds"] = ["missing-source"]
        artifact["verification"][0]["sourceIds"] = ["missing-source"]
        errors = validator.validate(artifact)
        self.assertIn("itinerary 0 budget item 0 has unknown source IDs: ['missing-source']", errors)
        self.assertIn("verification 0 has unknown source IDs: ['missing-source']", errors)

    def test_trip_artifact_validator_rejects_missing_user_presentation_fields(self):
        validator = load_trip_validator()
        artifact = json.loads((ROOT / "examples/coorg-road-trip.json").read_text())
        del artifact["generatedAt"]
        del artifact["itineraries"][0]["mainCompromise"]
        errors = validator.validate(artifact)
        self.assertIn("missing required field: generatedAt", errors)
        self.assertIn("itinerary 0 missing required field: mainCompromise", errors)

    def test_hotel_skill_routes_policy_profile_and_output_schema(self):
        skill = (ROOT / "skills/hotel-comparison/SKILL.md").read_text()
        for required in (
            "references/evaluation-policy.md",
            "references/review-analysis.md",
            "references/output-schema.md",
            "profiles/default.yaml",
            "profiles/hritvik.yaml",
        ):
            self.assertIn(required, skill)

    def test_hotel_defaults_preserve_core_quality_gates(self):
        policy = (ROOT / "skills/hotel-comparison/references/evaluation-policy.md").read_text()
        for requirement in (
            "exact dates",
            "mandatory charges",
            "bedroom",
            "bathroom",
            "recent reviews",
            "cross-platform",
            "Hard rejection",
        ):
            self.assertIn(requirement, policy)

    def test_personal_preferences_are_not_universal_policy(self):
        default_profile = (ROOT / "skills/hotel-comparison/profiles/default.yaml").read_text()
        personal_profile = (ROOT / "skills/hotel-comparison/profiles/hritvik.yaml").read_text()
        self.assertNotIn("coffee_plantation", default_profile)
        self.assertIn("coffee_plantation", personal_profile)

    def test_movie_skill_uses_shared_invocation_conventions(self):
        movie = (ROOT / "skills/movie-ticket-finder/SKILL.md").read_text()
        self.assertIn("Ask only for missing", movie)
        self.assertIn("durable profile", movie)
        self.assertIn("exact date", movie)
        self.assertIn("Never select, hold, reserve, book, or purchase", movie)

    def test_hotel_report_validator_accepts_complete_report(self):
        validator = load_report_validator()
        candidate = {
            "id": "stay-1", "name": "Estate Stay", "status": "available",
            "propertyType": "homestay", "location": {}, "roomPlan": [],
            "sleepingCapacity": 5, "bathrooms": 2, "price": {},
            "bookingTerms": {}, "reviewEvidence": {}, "photoEvidence": {},
            "preferenceFit": {}, "risks": [], "confidence": "high",
            "sourceIds": ["source-1"],
        }
        report = {
            "schemaVersion": 1, "kind": "hotel-comparison",
            "generatedAt": "2026-08-30T12:00:00+05:30", "assumptions": [],
            "trip": {
                "destination": "Coorg", "checkIn": "2026-09-05",
                "checkOut": "2026-09-07", "adults": 5, "children": 0,
                "currency": "INR", "totalBudget": 20000,
            },
            "recommendationId": "stay-1", "candidates": [candidate],
            "sources": [],
        }
        self.assertEqual(validator.validate(report), [])

    def test_hotel_report_validator_rejects_dangling_recommendation(self):
        validator = load_report_validator()
        report = {
            "schemaVersion": 1, "kind": "hotel-comparison",
            "generatedAt": "2026-08-30T12:00:00+05:30", "assumptions": [],
            "trip": {
                "destination": "Coorg", "checkIn": "2026-09-05",
                "checkOut": "2026-09-07", "adults": 5, "children": 0,
                "currency": "INR", "totalBudget": 20000,
            },
            "recommendationId": "missing", "candidates": [], "sources": [],
        }
        self.assertIn("recommendationId must reference a candidate", validator.validate(report))

    def test_hotel_report_validator_handles_malformed_candidate(self):
        validator = load_report_validator()
        report = {
            "schemaVersion": 1, "kind": "hotel-comparison",
            "generatedAt": "2026-08-30T12:00:00+05:30", "assumptions": [],
            "trip": {
                "destination": "Coorg", "checkIn": "2026-09-05",
                "checkOut": "2026-09-07", "adults": 5, "children": 0,
                "currency": "INR", "totalBudget": 20000,
            },
            "recommendationId": None, "candidates": ["invalid"], "sources": [],
        }
        self.assertIn("candidate 0 must be an object", validator.validate(report))


if __name__ == "__main__":
    unittest.main()
