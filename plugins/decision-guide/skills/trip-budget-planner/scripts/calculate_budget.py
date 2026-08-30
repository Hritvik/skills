"""Deterministic vacation budget arithmetic."""


def _money(value, field):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative number")
    return value


def classify(expected, limit, minimum=None, maximum=None):
    expected = _money(expected, "expected")
    limit = _money(limit, "limit")
    minimum = expected if minimum is None else _money(minimum, "minimum")
    maximum = expected if maximum is None else _money(maximum, "maximum")
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")
    if expected > limit:
        return "ineligible"
    if maximum > limit:
        return "stretch"
    if expected > limit * 0.9:
        return "tight"
    return "comfortable"


def calculate(travellers, limit_per_person, items):
    if not isinstance(travellers, int) or isinstance(travellers, bool) or travellers <= 0:
        raise ValueError("travellers must be a positive integer")
    limit_per_person = _money(limit_per_person, "limit_per_person")
    if not isinstance(items, list):
        raise ValueError("items must be a list")

    expected_total = 0
    minimum_total = 0
    maximum_total = 0
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"item {index} must be an object")
        amount = _money(item.get("amount"), f"item {index} amount")
        item_range = item.get("range") or {}
        minimum = _money(item_range.get("min", amount), f"item {index} minimum")
        maximum = _money(item_range.get("max", amount), f"item {index} maximum")
        if minimum > maximum:
            raise ValueError(f"item {index} minimum cannot exceed maximum")
        expected_total += amount
        minimum_total += minimum
        maximum_total += maximum

    expected_per_person = expected_total / travellers
    minimum_per_person = minimum_total / travellers
    maximum_per_person = maximum_total / travellers
    return {
        "expectedTotal": expected_total,
        "rangeTotal": {"min": minimum_total, "max": maximum_total},
        "expectedPerPerson": expected_per_person,
        "rangePerPerson": {"min": minimum_per_person, "max": maximum_per_person},
        "limitPerPerson": limit_per_person,
        "headroomPerPerson": limit_per_person - expected_per_person,
        "classification": classify(
            expected_per_person,
            limit_per_person,
            minimum_per_person,
            maximum_per_person,
        ),
    }
