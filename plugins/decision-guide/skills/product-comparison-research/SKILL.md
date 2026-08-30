---
name: product-comparison-research
description: Research and compare consumer products within a category, budget, and buyer context using current prices, price history, quality signals, owner reviews, warranty, and service evidence. Use for evidence-backed purchase recommendations and website-ready comparison reports; stop before cart or purchase actions.
---

# Product Comparison Research

Produce a defensible buying decision, not a catalog or a ranking based only on star ratings.

## Establish the brief

Before live research, restate known constraints and ask one compact batch only for missing inputs that could change the recommendation:

- market and delivery area; request a precise PIN code only when availability requires it
- product subtype and acceptable substitutes
- hard budget based on unconditional final price
- usage, capacity, space, compatibility, or installation constraints
- priority order such as reliability, performance, service, features, or lowest cost
- whether card, exchange, membership, coupon, refurbished, or open-box offers are acceptable

Treat a PIN code as sensitive location data. Obtain explicit confirmation before entering it on a retailer site. If the user asks only for methodology or a reusable artifact, proceed with clearly stated assumptions without forcing shopping questions.

## Research workflow

1. Define one comparable segment. Do not rank materially different subtypes together.
2. Discover broadly enough to avoid retailer or brand bias, then normalize exact model numbers and variants.
3. Apply hard eligibility gates: budget, availability, required specifications, seller credibility, warranty clarity, and model identity.
4. Verify surviving candidates using current direct sources. Prefer manufacturer specifications and warranty terms, authorized retailers, credible testing, large owner-review collections, and established price-history sources.
5. Capture unconditional effective price separately from conditional offers, mandatory fees, installation, accessories, and delivery costs. Never call a price delivered when fees are unknown.
6. Analyze reviews by themes and time horizon. Look for repeated defects, service patterns, variant mixing, promotional language, and differences between recent and lifetime ratings.
7. Score only comparable products. Use category-relevant dimensions, disclose weights, and keep hard disqualifiers outside the weighted score.
8. Adjust the recommendation for evidence confidence, source agreement, recency, exact-model matching, sample size, and long-term evidence.
9. Run contradiction checks: high rating versus repeated failures, long component warranty versus short comprehensive warranty, inflated discounts, discontinued models, weak local service, and suspiciously low sellers.
10. Recommend a best match, meaningful alternatives, rejected finalists, price timing, risks, and confidence. Separate verified fact, inference, and recommendation.

For washing machines, read [references/washing-machines.md](references/washing-machines.md). For another category, identify its comparison boundaries, failure modes, ownership costs, and hard gates before scoring.

## Research limits

- Use current web or browser evidence because prices, stock, warranties, and ratings change.
- Put a collection date and direct URL on every material source.
- Label unavailable, stale, conflicting, inferred, or low-confidence data instead of filling gaps.
- Do not fabricate review counts, historical lows, specifications, sellers, or scores.
- Do not let one retailer, affiliate list, search snippet, or isolated review determine the recommendation.
- Stop before adding to cart, applying coupons, starting subscriptions, logging in, or purchasing.

## Output

Lead in chat with the decision, two alternatives at most, material caveats, buy-now/wait guidance, confidence, and direct source links.

When a website-ready artifact is requested, follow [references/output-schema.md](references/output-schema.md), write one JSON report, and validate it with:

```bash
python3 scripts/validate_report.py path/to/report.json
```

The report must retain evidence references and distinguish prototype data from verified research. Do not modify presentation components when the existing renderer supports the schema.

## Quality gate

Before delivery confirm:

- candidates are exact, normalized models in one comparison class
- every important number and claim has evidence or is explicitly marked unknown/inferred
- prices state conditions, fees, availability, location scope, and observation time
- scoring weights reflect the buyer brief and sum to 100
- the winner remains defensible after checking recurring complaints and contrary evidence
- recommendation confidence is no higher than the underlying evidence confidence
- rejected finalists and reasons are visible
