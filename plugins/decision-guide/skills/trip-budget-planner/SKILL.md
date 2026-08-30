---
name: trip-budget-planner
description: Calculate complete group and per-person vacation costs, ranges, contingency headroom, confidence, and budget feasibility from structured line items.
---

# Trip Budget Planner

Treat the budget as all-in unless explicitly scoped otherwise. Include primary transport, visa, insurance, accommodation, local transport, food, activities, connectivity, mandatory fees, and contingency. Keep optional shopping separate.

Every line item must state category, group amount, currency, confidence (`verified`, `estimated`, `conditional`, or `unknown`), range when uncertain, and source IDs where verified. Normalize currencies using a dated rate and preserve the original amount.

Use [scripts/calculate_budget.py](scripts/calculate_budget.py) for arithmetic. Classify against the per-person limit:

- comfortable: expected cost at or below 90% of budget and upper range within budget;
- tight: expected cost within budget but above 90%, with upper range within budget;
- stretch: expected cost within budget but plausible upper range crosses it;
- ineligible: expected cost exceeds budget.

Never imply precision higher than the inputs.
