# Artifact contract

Use stable lowercase hyphenated IDs. Store independently refreshable artifacts:

```text
data/trips/{trip-id}/
├── exploration.json
├── evidence.json
├── verification.json
└── itineraries/{itinerary-id}.json
```

The exploration owns the canonical brief, assumptions, screened and rejected options, shortlist summaries, comparison dimensions, and recommended itinerary ID. Individual itineraries own bases, route, days, transport, stays, experiences, budget items, compromise, risks, and evidence IDs. Evidence is deduplicated. Verification tracks volatile facts without regenerating itinerary prose.

Never duplicate calculated totals in prose. Store monetary line items and allow deterministic code to derive totals, per-person cost, headroom, and feasibility.
