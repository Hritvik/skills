#!/usr/bin/env python3
import json
import pathlib
import sys


REQUIRED_TRIP = {"destination", "checkIn", "checkOut", "adults", "children", "currency", "totalBudget"}
REQUIRED_CANDIDATE = {
    "id", "name", "status", "propertyType", "location", "roomPlan",
    "sleepingCapacity", "bathrooms", "price", "bookingTerms",
    "reviewEvidence", "photoEvidence", "preferenceFit", "risks",
    "confidence", "sourceIds",
}
REQUIRED_TOP = {"generatedAt", "trip", "assumptions", "recommendationId", "candidates", "sources"}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["report must be an object"]
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if data.get("kind") != "hotel-comparison":
        errors.append("kind must be hotel-comparison")
    missing_top = REQUIRED_TOP - set(data)
    if missing_top:
        errors.append(f"report missing: {', '.join(sorted(missing_top))}")
    missing_trip = REQUIRED_TRIP - set(data.get("trip", {}))
    if missing_trip:
        errors.append(f"trip missing: {', '.join(sorted(missing_trip))}")
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            errors.append(f"candidate {index} must be an object")
            continue
        missing = REQUIRED_CANDIDATE - set(candidate)
        if missing:
            errors.append(f"candidate {index} missing: {', '.join(sorted(missing))}")
    recommendation = data.get("recommendationId")
    ids = {candidate.get("id") for candidate in candidates if isinstance(candidate, dict)}
    if recommendation is not None and recommendation not in ids:
        errors.append("recommendationId must reference a candidate")
    if not isinstance(data.get("sources"), list):
        errors.append("sources must be a list")
    return errors


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_report.py REPORT.json")
    path = pathlib.Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"valid hotel comparison report: {path}")


if __name__ == "__main__":
    main()
