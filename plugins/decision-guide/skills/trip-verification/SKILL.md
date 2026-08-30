---
name: trip-verification
description: Refresh only stale, volatile vacation facts such as fares, availability, entry rules, closures, exchange rates, and weather without rebuilding the trip.
---

# Trip Verification

Load the saved plan immediately. Identify volatile fields whose `staleAfter` has passed or whose downstream decision depends on a fresh check. Refresh only those fields.

Prioritize primary transport, accommodation inventory and all-in price, official visa/entry rules, attraction closures, exchange rate, and near-term weather. Preserve earlier observations as history; do not silently overwrite contradictions. Treat sister platforms as correlated sources.

Return a verification patch containing status, observed time, stale threshold, source IDs, changed values, and affected itinerary IDs. If a change invalidates a hard gate, invoke the smallest necessary replanning path. Never book, contact, reserve, or pay.
