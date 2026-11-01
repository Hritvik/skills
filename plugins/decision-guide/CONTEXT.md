# Decision Guide domain language

## Vacation planning

**Trip Collection** — The complete logical saved trip presented to a traveller.

**Trip Manifest** — The part of a Trip Collection that holds its brief, assumptions, shortlist, recommendation, comparison dimensions, and index of related records.

**Itinerary** — One continuing trip concept with a stable identity across revisions.

**Evidence** — An immutable observation from a source that supports one or more trip claims.

**Verification** — The current assessment of whether a volatile claim remains usable for a decision.

**Published Revision** — One immutable, internally consistent state of a Trip Collection.

**Current Revision** — The Published Revision resolved by the ordinary link for a Trip Collection.

**Snapshot** — A generated portable single-file representation of a Published Revision; never the canonical source.

**Projection** — A derived database, search, or presentation representation that can be rebuilt from canonical records.

**Migration** — An explicit deterministic transformation that creates a new revision while preserving its source.
