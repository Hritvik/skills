# Decomposition

How to turn one accepted source into packages that are safe to run in parallel, and how to defend the boundary of each one.

## The unit

A **vertical slice**: a narrow but complete path through the layers it touches, demoable or verifiable on its own. Schema, API, UI, tests belong to one slice, not one slice each. A horizontal layer, a stub, a "phase", or a refactor with no observable result is not a package.

Two tests, both cheap to apply:

- **One context window.** An agent should be able to finish and verify it without running out of room halfway. When in doubt, split.
- **Claimable alone.** If it cannot be worked without a sibling landing first, the dependency is real and gets an edge — or the two are one package.

## Ordering

1. **Prefactor first.** Anything that makes the change easy goes before the change, as its own package.
2. **Contracts before consumers.** See contract pinning in [work-items-body.md](work-items-body.md). The introducing package lands first and every consumer depends on it.
3. **Expand–contract for a wide refactor.** One mechanical change whose blast radius fans across the codebase — a renamed column, a retyped shared symbol — cannot land green as a slice. Sequence it: expand (add the new form beside the old, nothing breaks), migrate in batches sized by blast radius (each batch its own package, each blocked by the expand), contract (delete the old form once no caller remains, blocked by every migrate batch). When even batches cannot stay green alone, keep the order and let them share an integration package that everything blocks.
4. **Integration last.** One package owns shared wiring and the parent-level scenario. It is the only package allowed to touch files that siblings would otherwise collide on.
5. **Review where it counts.** A separate review package only when independent acceptance is required — security-sensitive, correctness-critical, or a contract others will consume. Ordinary review is part of the package's own lifecycle in Loom, not a package.

## Ownership of paths

- Each package owns an explicit, minimal set of write paths.
- Packages that can be claimable at the same time must have **disjoint** paths. Two packages owning one file is how parallel work corrupts itself.
- Shared or generated files — lockfiles, an index, a schema registry, a build manifest — belong to exactly one named package, normally the integration package. Say which, in the body, or say "none".
- Generated artifacts are not owned by whoever regenerates them; they are owned by the package whose change regenerates them.

## AFK or HITL

Mark a package **HITL** only when a human must decide something before it can be built: an architectural call, a design choice, a product trade-off. Before marking HITL, check two things — can this be settled by reading the code, and if the assumption is wrong does something actually break? An assumption the code settles is AFK. An assumption that falls back safely is AFK. Reserve HITL for real calls, because every HITL package is a stall.

## Justification and the cut list

Every package names what it descends from: the source line it implements, the artifact it exists for, or the work it is a necessity of. A candidate that cannot name one goes in the **cut list** with what it would have done in plain language and why it was cut.

Two rules keep the cut list honest:

- **Never justify a cut item by searching outward** to a sibling, a linked plan, or a closed item. If the justification is not in the source, it is not justified.
- **Silence is not exclusion.** A package that does not enumerate its own necessities has not excluded them. Cut subsystems, integrations and artifacts the source never asks for — never the behavior required to deliver what it does ask for.

## What never becomes a package

- A restatement of the source, or a "plan" package that produces no observable change.
- Documentation of process: decision logs, review summaries, facilitation notes, gap analyses.
- A workstream named after a person or a goal with no bounded result.
- Anything whose acceptance is standard operating procedure rather than an outcome.

## When the source is too vague to slice

That is not a decomposition problem. If the outcome, the owner or the acceptance cannot be pinned, the package would be a guess dressed as work — send it back as `clarify` instead of inventing the missing parts.
