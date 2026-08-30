#!/usr/bin/env python3
"""Small semantic validator for vacation artifacts; JSON Schema remains canonical."""

import json
import pathlib
import re
import sys


ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MODES = {"fixed-destination", "open-ended-discovery"}
FEASIBILITY = {"comfortable", "tight", "stretch", "ineligible"}
EVIDENCE_STATUS = {
    "verified", "estimated", "conditional", "unknown", "stale",
    "unavailable", "direct-confirmation-required",
}


def _as_list(value):
    return value if isinstance(value, list) else []


def _unknown_ids(values, known_ids):
    return sorted(set(_as_list(values)) - known_ids)


def validate(report):
    errors = []
    if not isinstance(report, dict):
        return ["artifact must be an object"]
    for field in (
        "schemaVersion",
        "kind",
        "id",
        "mode",
        "title",
        "generatedAt",
        "brief",
        "itineraries",
        "evidence",
        "verification",
    ):
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if report.get("kind") != "vacation-exploration":
        errors.append("kind must be vacation-exploration")
    if not isinstance(report.get("id"), str) or not ID.fullmatch(report.get("id", "")):
        errors.append("id must be lowercase hyphenated")
    if report.get("mode") not in MODES:
        errors.append("mode is invalid")
    itineraries = report.get("itineraries", [])
    if not isinstance(itineraries, list):
        errors.append("itineraries must be an array")
        itineraries = []
    itinerary_ids = {item.get("id") for item in itineraries if isinstance(item, dict)}
    recommended = report.get("recommendedItineraryId")
    if recommended is not None and recommended not in itinerary_ids:
        errors.append("recommendedItineraryId must reference an itinerary")
    evidence = report.get("evidence", [])
    if not isinstance(evidence, list):
        errors.append("evidence must be an array")
        evidence = []
    evidence_ids = {item.get("id") for item in evidence if isinstance(item, dict)}
    for index, itinerary in enumerate(itineraries):
        if not isinstance(itinerary, dict):
            errors.append(f"itinerary {index} must be an object")
            continue
        for field in (
            "id",
            "title",
            "feasibility",
            "mainCompromise",
            "budgetItems",
            "days",
            "evidenceIds",
        ):
            if field not in itinerary:
                errors.append(f"itinerary {index} missing required field: {field}")
        if itinerary.get("feasibility") not in FEASIBILITY:
            errors.append(f"itinerary {index} feasibility is invalid")
        missing = _unknown_ids(itinerary.get("evidenceIds", []), evidence_ids)
        if missing:
            errors.append(f"itinerary {index} has unknown evidence IDs: {missing}")
        for item_index, item in enumerate(_as_list(itinerary.get("budgetItems"))):
            if not isinstance(item, dict):
                errors.append(f"itinerary {index} budget item {item_index} must be an object")
                continue
            missing_sources = _unknown_ids(item.get("sourceIds", []), evidence_ids)
            if missing_sources:
                errors.append(
                    f"itinerary {index} budget item {item_index} has unknown source IDs: {missing_sources}"
                )
    for index, source in enumerate(evidence):
        if not isinstance(source, dict):
            errors.append(f"evidence {index} must be an object")
            continue
        if source.get("status") not in EVIDENCE_STATUS:
            errors.append(f"evidence {index} status is invalid")
        if source.get("status") == "verified" and not source.get("observedAt"):
            errors.append(f"evidence {index} verified status requires observedAt")
    verification = report.get("verification", [])
    if not isinstance(verification, list):
        errors.append("verification must be an array")
        verification = []
    for index, item in enumerate(verification):
        if not isinstance(item, dict):
            errors.append(f"verification {index} must be an object")
            continue
        missing_sources = _unknown_ids(item.get("sourceIds", []), evidence_ids)
        if missing_sources:
            errors.append(f"verification {index} has unknown source IDs: {missing_sources}")
    return errors


def main(path):
    report = json.loads(pathlib.Path(path).read_text())
    errors = validate(report)
    if errors:
        print("\n".join(errors))
        return 1
    print("Trip artifact is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
