# Stewardship Rules

Read this reference when changing lifecycle state, reconciling competing expectations, assessing impact, or validating artifacts.

## Lifecycles

Capability contracts normally progress through:

`identified → exploring → aligned → committed → realized → validated`

Do not force linear progress when information is missing. Record the blocking owner action instead.

Provider commitments normally progress through:

`proposed → planned → in-progress → available → validated`

`changed`, `withdrawn`, and `superseded` are explicit historical outcomes, not deletion instructions.

## Reconciliation

When expectations overlap:

1. Compare outcomes and observable properties, not proposed implementations.
2. Consolidate only when one provider promise genuinely satisfies each linked expectation.
3. Preserve consumer-specific constraints that do not belong in the shared promise alongside their expectation.
4. Surface incompatibilities such as mutually exclusive ordering, availability, isolation, or lifecycle needs.
5. Identify who must decide; do not resolve product or ownership conflicts by assumption.

## Impact assessment

Before changing or withdrawing a commitment:

1. Follow `derived_from`, `affected_consumers`, and supersession references.
2. List consumer workflows and acceptance scenarios that may no longer hold.
3. Record the provider rationale.
4. Capture migration, replacement, or unresolved follow-up when supplied.
5. Leave the prior promise inspectable.

## Validation checklist

Check that:

- IDs are stable and unique within the artifact set.
- Every expectation has a consumer and owner or an explicit ownership gap.
- Every commitment has a provider and owner or an explicit ownership gap.
- Provider dispositions do not alter consumer-authored statements.
- Honored expectations reference a commitment.
- Partial, deferred, declined, changed, or withdrawn decisions include rationale.
- Consolidated commitments reference all source expectations.
- Boundaries and qualifications are explicit.
- Validated commitments contain observable evidence.
- Unresolved questions identify the party expected to answer.
- Technical details are linked rather than duplicated when canonical contracts exist.

Report errors separately from unresolved collaboration questions. Missing agreement is not a schema error; invented agreement is worse than an honest unresolved state.

