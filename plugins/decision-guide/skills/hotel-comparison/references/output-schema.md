# Hotel comparison report schema

Produce one UTF-8 JSON object so the comparison website can render new trips without component edits.

Required top-level fields:

```json
{
  "schemaVersion": 1,
  "kind": "hotel-comparison",
  "generatedAt": "2026-08-30T12:00:00+05:30",
  "trip": {
    "destination": "Coorg",
    "checkIn": "2026-09-05",
    "checkOut": "2026-09-07",
    "adults": 5,
    "children": 0,
    "roomsRequested": 2,
    "currency": "INR",
    "totalBudget": 20000
  },
  "assumptions": [],
  "recommendationId": "property-id",
  "candidates": [],
  "rejected": [],
  "sources": []
}
```

Each candidate must contain `id`, `name`, `status`, `propertyType`, `location`, `roomPlan`, `sleepingCapacity`, `bathrooms`, `price`, `bookingTerms`, `reviewEvidence`, `photoEvidence`, `preferenceFit`, `risks`, `confidence`, and `sourceIds`. Price contains `base`, `displayedTaxes`, `mandatoryFeesKnown`, `total`, `currency`, `conditions`, and `observedAt`. Use `null` for unknown values and explain the gap in `risks`; never invent values.

Each source contains `id`, `url`, `publisher`, `observedAt`, and `supports`. Rejected candidates contain `id`, `name`, and explicit `reasons`.
