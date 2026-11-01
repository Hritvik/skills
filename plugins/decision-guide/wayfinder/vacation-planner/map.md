---
title: Find the way to a reusable vacation-planning system
label: wayfinder:map
status: open
tracker: local-markdown
---

## Destination

Reach a decision-complete, implementable specification for a persistent vacation-planning capability and reusable public website renderer, validated against both the Bengaluru-to-Coorg fixed trip and an open-ended international trip under ₹50,000 per person.

The map is complete when no product, workflow, evidence, artifact, evaluation, or distribution decision remains for an implementation effort to invent.

## Notes

- Domain: exploratory and fixed-destination vacation planning.
- Authoring skills: use `brainstorm`, `grilling`, `domain-modeling`, `prototype`, and `research` when available. Use `skill-creator` and `plugin-creator` only after this map reaches its destination.
- `wayfinder` is an authoring workflow, not a runtime dependency of the finished vacation planner.
- Runtime requirements discovery composes `grilling`; existing hotel, movie, shopping, and product-comparison skills remain bounded specialists.
- Planning is the default. Existing code and schemas are prototypes/evidence, not automatically final decisions.
- Recommendation-only boundary: no booking, reservation, provider messaging, login, or payment.
- Public-domain trip research may be published publicly; private booking or identity details remain excluded if introduced later.
- Refer to the map and tickets by title, not merely their local identifiers.

## Decisions so far

- [Support fixed and exploratory planning](tickets/closed/support-fixed-and-exploratory-planning.md) — one orchestrator supports known destinations and budget-first destination discovery.
- [Use adaptive grilling for requirements](tickets/closed/use-adaptive-grilling-for-requirements.md) — question depth scales with ambiguity and never repeats known facts.
- [Treat stated budgets as all-in](tickets/closed/treat-stated-budgets-as-all-in.md) — include essential trip costs and use 10% headroom for comfortable feasibility.
- [Publish through a reusable data-driven website](tickets/closed/publish-through-a-reusable-data-driven-website.md) — comparison and itinerary pages consume structured data rather than trip-specific components.
- [Keep the first website read-only](tickets/closed/keep-the-first-website-read-only.md) — trip changes occur through the skill; the website filters, compares, shares, and prints.
- [Keep external actions recommendation-only](tickets/closed/keep-external-actions-recommendation-only.md) — live research stops before inventory selection, contact, reservation, or payment.
- [Choose the canonical trip artifact topology](tickets/closed/choose-the-canonical-trip-artifact-topology.md) — persist each trip as immutable, versioned collection revisions with independently owned records and generated snapshots.

## Not yet specified

- The renderer's final component vocabulary and visual hierarchy depend on the website prototype and user reaction.
- Exact source-provider strategy may change after the Coorg and international behavioural evaluations expose coverage gaps.
- The final installation and distribution route depends on whether the current `decision-guide` boundary remains the right product surface.
- Detailed freshness intervals may need to vary by evidence type after targeted-refresh behaviour is tested.

## Out of scope

- Booking, payment, provider messaging, credential handling, and passport-data storage.
- A CMS, collaborative editor, database-backed trip builder, or user authentication in the first version.
- Live turn-by-turn navigation or a mandatory embedded mapping provider in the first version.
- Treating the existing prototype implementation as approved merely because it has passing tests.
