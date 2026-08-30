---
name: trip-feasibility-checker
description: Apply hard budget, visa, season, safety, transport, and duration gates to proposed trips before they are scored or deeply researched.
---

# Trip Feasibility Checker

Reject or flag a trip before preference scoring when primary transport, visa eligibility or lead time, transit rules, minimum useful duration, seasonal closure, official safety constraint, accessibility need, or all-in budget makes it impractical.

Use authoritative current sources for entry rules and advisories. Never infer passport eligibility. Treat correlated travel listings as one evidence family. Separate verified facts from estimates and record observation time plus expiry/stale threshold for volatile facts.

Return `eligible`, `conditional`, `stretch`, or `ineligible` with explicit failed gates and evidence IDs. A high preference score cannot override a failed hard gate.
