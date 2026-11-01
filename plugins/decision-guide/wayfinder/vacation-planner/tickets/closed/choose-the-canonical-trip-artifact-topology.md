---
title: Choose the canonical trip artifact topology
label: wayfinder:grilling
type: grilling
mode: HITL
status: closed
assignee: codex
---

## Question

Should the canonical persisted result remain one portable exploration artifact, or split into an exploration manifest, one itinerary file per option, deduplicated evidence, and independently refreshable verification records? Decide the source of truth, atomic update boundary, schema-versioning promise, and migration expectations without choosing implementation mechanisms.

## Resolution

The canonical saved unit is a **Trip Collection**. Users experience it as one trip, while its Trip Manifest, Itineraries, Evidence, and Verification are independently owned records.

Changes are prepared and validated as a complete candidate revision, then published as one internally consistent **Published Revision**. Published revisions are immutable and remain addressable; ordinary trip links resolve to the **Current Revision**. An Itinerary keeps a stable concept ID across revisions rather than using positional IDs.

Every independently persisted record declares its own schema version, and the Trip Manifest declares the collection-contract version governing valid combinations. Older formats migrate only through explicit deterministic migrations that create a new revision and preserve the source. The current monolithic fixtures are prototypes to migrate, not a permanent compatibility promise.

A complete collection may be exported as a generated single-file **Snapshot**, but snapshots are never an equal source of truth. A future database or search engine may hold a rebuildable **Projection**; versioned files remain canonical until collaborative editing or another demonstrated requirement justifies reopening ownership.

Evidence and Verification remain distinct. Evidence is an immutable observed source-backed fact. Verification is the current assessment of whether a volatile claim remains usable.
