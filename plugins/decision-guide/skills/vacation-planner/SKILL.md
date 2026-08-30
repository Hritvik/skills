---
name: vacation-planner
description: Discover feasible destinations or build complete fixed-destination vacations, then compare, verify, and emit reusable itinerary artifacts. Use for recommendation-only trip planning; it does not book, reserve, message, or pay.
---

# Vacation Planner

Build a complete, defensible trip rather than a list of attractions.

## Establish the brief

Use facts already present in the conversation and durable profile. Compose `grilling` adaptively: ask the whole current decision frontier in one compact round, but do not interrogate the user about facts that can be researched. Minimum inputs are origin, approximate dates or window, traveller composition, budget and whether domestic, international, or both. Proceed with visible assumptions when they do not change eligibility.

Treat budget as all-in by default: primary transport, visa, insurance, stay, local transport, food, activities, connectivity, mandatory fees, and contingency. Keep optional shopping separate. Reserve 10% headroom when judging comfortable feasibility.

## Choose a mode

- **fixed-destination:** skip broad opportunity discovery. Use `destination-area-planner`, `transport-comparison`, `hotel-comparison`, `itinerary-builder`, and `trip-budget-planner`.
- **open-ended discovery:** use `trip-opportunity-finder`, then `trip-feasibility-checker`. Construct meaningfully different finalist itineraries and deeply verify only the strongest options.

Use `movie-ticket-finder`, `shopping-price-finder`, and `product-comparison-research` only when the trip actually needs those specialist decisions.

## Orchestrate artifacts

Maintain one canonical brief. Specialists return bounded structured patches; they must not rewrite the entire trip. Store one exploration record, one file per itinerary, deduplicated evidence, and independently refreshable verification status. Read [references/composition-map.md](references/composition-map.md) for sequencing and [references/artifact-contract.md](references/artifact-contract.md) before writing artifacts.

Apply hard feasibility gates before preference scoring. Produce at most five diverse concepts, normally representing best overall, value, comfort/ease, strongest experience match, and a clearly labelled stretch option. Do not invent a category when no credible option exists.

Run `trip-verification` for volatile finalist facts. Facts must be labelled `verified`, `estimated`, `conditional`, `unknown`, `stale`, `unavailable`, or `direct-confirmation-required` with observation times where applicable.

Use `trip-site-publisher` to emit validated website-ready JSON. Reopening a saved trip must load stored artifacts immediately and refresh only stale fields rather than recreating the plan.

## Result and boundary

Lead with the best-fit itinerary and the decisive trade-off, followed by meaningful alternatives. Include all-in expected cost and range, feasibility class, transport effort, route/bases, day plan, stay plan, visa/entry implications, season fit, risks, confidence, and direct sources.

Never select inventory, hold, reserve, book, contact a provider, log in, or enter payment or identity documents. Public research may be published, but exclude private booking references, credentials, passport data, full home addresses, and personal contact details if they appear later.
