---
name: trip-site-publisher
description: Emit and validate versioned vacation exploration and itinerary JSON for a reusable public website renderer; use when trip results need persistent comparison pages.
---

# Trip Site Publisher

Render content through data, not trip-specific components. Read [references/output-contract.md](references/output-contract.md) and validate the artifact against [references/trip-artifact.schema.json](references/trip-artifact.schema.json).

Use stable IDs and one independent itinerary record per option. Deduplicate evidence. Preserve fact status, observation time, source correlation group, uncertainty, and verification freshness. Do not reproduce calculated budget totals in free text.

The reusable site should automatically discover trip artifacts and expose a trip library, exploration comparison page, and shareable itinerary pages. A new trip normally changes only JSON. Structural site changes belong to the website-building workflow, not ordinary publication.

Validate with:

```bash
python3 scripts/validate_trip_artifact.py path/to/trip.json
```

Publishing or deploying externally requires the user's explicit approval at that time.
