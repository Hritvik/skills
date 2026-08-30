# Website output contract

The renderer exposes:

- `/` trip library;
- `/trips/{trip-id}` exploration and itinerary comparison;
- `/trips/{trip-id}/{itinerary-id}` detailed shareable itinerary.

The comparison view shows expected cost and range, duration, transport effort, entry difficulty, season fit, trip character, confidence, and principal compromise. The detail view shows route, day plan, transport, stays, budget, experiences, food, weather, entry rules, risks, verification status, and sources.

Components must remain destination-independent. New content normally requires only a validated artifact. Print and compact share views derive from the same data.
