---
name: hotel-comparison
description: Compare live hotels, homestays, villas, resorts, and estate stays for exact dates, occupancy, total budget, room quality, recent reviews, and booking terms. Use for recommendation-only accommodation research; stop before reserving or paying.
---

# Hotel Comparison

Find the best stay for the actual trip, not the highest lifetime rating or lowest headline price.

## Build the trip brief

Start with facts already supplied in the conversation. The minimum useful brief is destination, check-in and checkout dates, guest composition, and maximum total stay budget. Capture vehicle access when distance or local transport could materially change the candidate pool. Ask one compact batch only for missing facts that could change eligibility or ranking, such as children’s ages, accessibility, required room count, an entire-property requirement, vehicle access, or a hard location boundary.

Load [profiles/default.yaml](profiles/default.yaml) for ordinary assumptions. When the request is for Hritvik, merge [profiles/hritvik.yaml](profiles/hritvik.yaml) over those defaults. Explicit trip instructions override both. Never ask the user to repeat a value already known from the conversation or profile. State consequential assumptions before research and allow correction without blocking useful work.

## Research and decide

Read [references/evaluation-policy.md](references/evaluation-policy.md) before researching candidates. Read [references/review-analysis.md](references/review-analysis.md) when finalists have enough review evidence to analyse or when cleanliness, maintenance, service, safety, or seasonal conditions could change the recommendation.

Use current web or browser evidence. Verify exact dates, occupancy, room allocation, sleeping capacity, total displayed price, taxes, mandatory charges, and booking conditions on direct listing pages. Inspect actual bedroom, bathroom, common-area, and exterior photographs for finalists. A property remains “available” only while the live page retains the requested dates and occupancy.

When the first inventory sources produce few eligible options, run the source-coverage and availability-recovery workflow in the evaluation policy before weakening hard requirements or declaring the market exhausted. Treat sister brands and syndicated listings as correlated evidence rather than independent confirmation.

Discover broadly, then deeply inspect no more than five eligible finalists. Cross-check the strongest options on another credible, preferably independent platform when possible. Separate verified facts, inferences, and judgement. Do not fill gaps with assumptions.

Hard rejections are not offset by weighted scoring. Among eligible properties, adapt weights to the trip brief; use the default weights in the evaluation policy when the user has not expressed priorities.

## Result and boundaries

Lead with one recommendation and up to two meaningful alternatives. Include exact room configuration, tax-inclusive total or clearly unknown fees, recent-review verdict, visual-quality verdict, location/access trade-off, cancellation and payment terms, availability observation time, confidence, and direct date-specific links. Include rejected finalists when the reason prevents an attractive-looking mistake.

If a website-ready artifact is requested, follow [references/output-schema.md](references/output-schema.md) and validate it with:

```bash
python3 scripts/validate_report.py path/to/report.json
```

Never select a room, reserve, hold inventory, log in, message a host, or enter payment details. Stop at verified recommendations.

## Improvement discipline

Classify feedback before changing durable behavior:

- personal taste updates a named profile;
- a broadly applicable failure updates the evaluation policy;
- a seasonal or regional issue updates destination-specific evidence in the report;
- one property’s failure remains candidate evidence, not a universal rule.

Add a regression scenario for material workflow failures. Do not silently generalize from one stay or one review.
