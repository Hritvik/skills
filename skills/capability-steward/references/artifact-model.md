# Capability Artifact Model

Use this model when creating or materially restructuring capability artifacts. Adapt field names to an established repository format rather than creating a parallel convention.

## Capability contract

A contract describes one capability boundary between a provider and one or more consumers. It may contain:

- `id`, `title`, `status`, and `owners`
- capability outcome and scope
- provider identity
- known consumers
- consumer expectations
- provider commitments
- open questions and decisions
- linked technical contracts, when they exist
- change history or supersession references

Keep exact endpoints, payloads, token claims, broker choices, and implementation libraries out unless they are already decided and materially constrain the capability.

## Consumer expectation

Record:

- Stable expectation ID
- Consumer and owner
- Desired outcome
- Importance: `required`, `preferred`, or `optional`
- Rationale or affected workflow
- Required observable properties
- Acceptance scenario
- Real dependency or target, if supplied
- Provider response and referenced commitment, when available

An acceptance scenario should describe externally observable behavior without prescribing implementation. For example, prefer “a reconnecting consumer can resume without permanent event loss” over “the provider uses Kafka offsets.”

## Provider disposition

Use one of:

- `honor`: accepted and covered by a commitment
- `partially-honor`: accepted with explicit limitations
- `explore`: more discovery is required
- `defer`: valid but not currently planned
- `decline`: outside the provider's intended boundary
- `superseded`: replaced by a referenced expectation or decision

Record rationale for every disposition except an unqualified `honor`. A material qualification should be acknowledged by the affected consumer before the expectation is considered aligned.

## Provider commitment

Record:

- Stable commitment ID
- Provider and owner
- Source expectation IDs
- Promise stated as an outcome and observable guarantees
- Explicit boundaries and exclusions
- Status and target only when provider-approved
- Affected consumers
- Validation scenarios and evidence
- Superseded commitment, if applicable

Consolidate compatible expectations when one promise can serve several consumers. Do not broaden a commitment beyond what the provider accepted.

## Service capability map

Use a compact map with:

- `provides`: capabilities the service intends to own
- `consumes`: capabilities expected from other services
- `owns`: data, policy, or lifecycle authority
- `excludes`: responsibilities intentionally outside the boundary
- links to relevant capability contracts

The map is a discovery index, not a replacement for the contracts.

