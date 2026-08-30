import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_validator():
    path = ROOT / "skills/trip-site-publisher/scripts/validate_trip_artifact.py"
    spec = importlib.util.spec_from_file_location("trip_artifact_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TripArtifactValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.report = json.loads((ROOT / "examples/coorg-road-trip.json").read_text())

    def test_accepts_complete_fixture(self):
        self.assertEqual(self.validator.validate(self.report), [])

    def test_rejects_dangling_recommendation(self):
        changed = {**self.report, "recommendedItineraryId": "missing"}
        self.assertIn(
            "recommendedItineraryId must reference an itinerary",
            self.validator.validate(changed),
        )

    def test_rejects_unknown_evidence_reference(self):
        itinerary = {**self.report["itineraries"][0], "evidenceIds": ["missing"]}
        changed = {**self.report, "itineraries": [itinerary]}
        errors = self.validator.validate(changed)
        self.assertTrue(any("unknown evidence IDs" in error for error in errors))

    def test_rejects_invalid_mode_and_feasibility(self):
        itinerary = {**self.report["itineraries"][0], "feasibility": "cheap"}
        changed = {**self.report, "mode": "surprise-me", "itineraries": [itinerary]}
        errors = self.validator.validate(changed)
        self.assertIn("mode is invalid", errors)
        self.assertIn("itinerary 0 feasibility is invalid", errors)


if __name__ == "__main__":
    unittest.main()
