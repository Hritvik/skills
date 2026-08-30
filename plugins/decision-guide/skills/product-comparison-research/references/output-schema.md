# Website report contract

Use this contract when producing a reusable comparison artifact. JSON is the canonical content source; the website should render it without embedding research claims in components.

## Root fields

- `schemaVersion`: currently `1`
- `status`: `prototype` or `verified`
- `reportId`: stable lowercase slug
- `title`, `category`, `market`, `currency`
- `updatedAt`: ISO 8601 timestamp
- `brief`: constraints, priorities, accepted offer conditions, and assumptions
- `methodology`: disclosed score weights totaling 100 and hard disqualifiers
- `winnerId`: ID of a product in `products`
- `products`: normalized candidates
- `rejected`: important excluded candidates with reasons
- `sources`: evidence records referenced by products
- `limitations`: missing evidence, location limits, and uncertainty

## Product fields

Each product requires:

- `id`, `brand`, `name`, `modelNumber`, `segment`, `capacity`
- `availability`: `available`, `unavailable`, `location-dependent`, or `unknown`
- `price`: `current`, `historicalLow`, `typical`, `currency`, `condition`, `feesKnown`, `observedAt`
- `score`: overall 0–100, dimension scores, and `confidence` (`high`, `medium`, or `low`)
- `reviews`: displayed rating, displayed count, number analyzed when known, positive themes, negative themes, and manipulation warnings
- `warranty`: comprehensive, component-specific, exclusions, and evidence source IDs
- `strengths`, `caveats`, `verdict`, `priceVerdict`
- `sourceIds`: references into root `sources`

Use `null` for genuinely unknown values. Do not use zero as unknown.

## Source fields

Each source requires `id`, `url`, `publisher`, `type`, `collectedAt`, `supports`, and `quality` (`primary`, `strong-secondary`, or `supporting`).

## Stability rules

- IDs and field names are presentation-independent.
- Add optional fields without changing existing meanings; increment `schemaVersion` for breaking changes.
- Preserve raw observations when deriving an adjusted score.
- Keep seller offers separate when prices or conditions differ.
- Never overwrite `verified` evidence with prototype values.
