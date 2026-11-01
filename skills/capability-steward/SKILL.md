---
name: capability-steward
description: Capture, reconcile, and centrally track capability expectations and provider commitments across independently built services or products. Use during early portfolio, platform, or service coordination before exact API and event contracts should be finalized.
---

# Capability Steward

Maintain lightweight capability artifacts that let consumers state desired outcomes and providers state what they plan to honor. Keep these artifacts about responsibilities, observable properties, and boundaries; do not prematurely turn them into endpoint, payload, transport, or implementation specifications.

## Resolve the central home first

Before reading or writing capability artifacts, locate exactly one directory containing `capability-home.yaml` with `kind: capability-steward-home`. Treat that directory and its `registry.yaml` as the only authoritative home for the coordinated portfolio.

- Search the accessible workspace roots, not only the active repository.
- If exactly one valid home is available, use it for every artifact mutation.
- If none is available, ask the user to identify or establish the central home. Do not initialize capability artifacts in the active product repository.
- If multiple homes are available, stop and ask which one is authoritative. Never merge or select silently.
- Product repositories may be linked as evidence or technical-contract sources, but must not contain authoritative copies of capability maps, contracts, expectations, commitments, or decisions.
- Update `registry.yaml` in the same change whenever an artifact is added, moved, superseded, or removed.

Read [references/central-home.md](references/central-home.md) before establishing a home, registering an artifact, or migrating a repo-local artifact.

## Choose the operation

- **Map a service:** Record what it provides, consumes, owns, and excludes.
- **Propose a capability:** Capture a cross-effort need before a provider is committed.
- **Add an expectation:** Preserve a consumer-authored outcome, importance, rationale, and observable acceptance scenario.
- **Respond to an expectation:** Record the provider's disposition without rewriting the consumer's statement.
- **Consolidate a commitment:** Combine compatible accepted expectations into one coherent provider promise.
- **Assess impact:** Identify consumers affected by a proposed commitment change or withdrawal.
- **Validate:** Check lifecycle, ownership, references, rationale, and evidence.
- **Summarize:** Present unresolved expectations, planned commitments, conflicts, and validation state by service or portfolio.

For creating or editing an artifact, read [references/artifact-model.md](references/artifact-model.md). For lifecycle transitions, negotiation, conflict handling, or validation, also read [references/stewardship-rules.md](references/stewardship-rules.md). Start new contracts from [assets/capability-contract.yaml](assets/capability-contract.yaml) when the central home has no more specific template.

## Working method

1. Resolve the central home and inspect its registry, existing artifacts, ownership conventions, and identifiers before creating anything.
2. Identify the acting party for every requested change: consumer, provider, or steward. Never infer authority to speak for another party.
3. Make the smallest update that captures the new information. Preserve unresolved questions and intentional ambiguity.
4. Show consequential qualifications and conflicts explicitly. A provider response that weakens a required consumer property needs consumer acknowledgement; it is not silent acceptance.
5. Keep technical contracts linked but separate. Introduce OpenAPI, AsyncAPI, MCP schemas, or payload details only when the user is ready to design them.
6. Report changed records, newly affected parties, unresolved decisions, and the next required owner action.

## Non-negotiable guards

- Consumer expectations are consumer-owned; providers may respond but not rewrite them.
- Provider commitments are provider-owned; consumers may challenge them but not declare them accepted on the provider's behalf.
- An expectation is not a promise. Only an explicit provider commitment describes planned service behavior.
- `partially-honor`, `defer`, `decline`, `change`, and `withdraw` decisions require rationale.
- A commitment change or withdrawal must retain history and identify affected consumers.
- A commitment cannot be `validated` without observable evidence.
- Keep stable IDs across edits. Supersede records instead of repurposing IDs.
- Do not treat target dates, releases, or service levels as commitments unless the provider explicitly accepts them.
- Never invent owners, acceptance, evidence, deadlines, or technical decisions.
- Never create an authoritative capability artifact outside the resolved central home.
- Never leave an unregistered authoritative artifact or two authoritative files with the same ID.

## Output style

Prefer a concise change summary plus the updated artifact. When only advising, distinguish clearly among:

- **Expectation:** what a consumer needs.
- **Disposition:** how the provider responds.
- **Commitment:** what the provider plans to guarantee.
- **Evidence:** what demonstrates the capability works.
