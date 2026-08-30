import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_budget_module():
    path = ROOT / "skills/trip-budget-planner/scripts/calculate_budget.py"
    spec = importlib.util.spec_from_file_location("trip_budget", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TripBudgetTests(unittest.TestCase):
    def test_all_in_total_and_per_person(self):
        budget = load_budget_module()
        result = budget.calculate(
            travellers=5,
            limit_per_person=10000,
            items=[
                {"category": "transport", "amount": 10000},
                {"category": "stay", "amount": 20000},
                {"category": "food", "amount": 10000},
            ],
        )
        self.assertEqual(result["expectedTotal"], 40000)
        self.assertEqual(result["expectedPerPerson"], 8000)
        self.assertEqual(result["classification"], "comfortable")

    def test_tight_stretch_and_ineligible_boundaries(self):
        budget = load_budget_module()
        self.assertEqual(budget.classify(46000, 50000, 48000, 49000), "tight")
        self.assertEqual(budget.classify(49000, 50000, 47000, 52000), "stretch")
        self.assertEqual(budget.classify(51000, 50000, 49000, 53000), "ineligible")

    def test_rejects_invalid_inputs(self):
        budget = load_budget_module()
        with self.assertRaises(ValueError):
            budget.calculate(travellers=0, limit_per_person=50000, items=[])
        with self.assertRaises(ValueError):
            budget.calculate(
                travellers=2,
                limit_per_person=50000,
                items=[{"category": "stay", "amount": -1}],
            )


if __name__ == "__main__":
    unittest.main()
