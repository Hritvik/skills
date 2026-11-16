---
name: plan-to-work
description: Decompose one accepted decision, spec or plan into Loom execution packages — vertical slices sized for one context, each with a pinned source revision, a named human outcome owner, observable acceptance and an exact write scope — and create them in the registry so agents can claim them. Use when something has been decided and now needs to become claimable work, or when a running package's source or scope has changed underneath it. NOT for deciding what happens to a request (that is request-triage), NOT for scheduling, claiming or choosing a worker (that is Loom), NOT for accepting the outcome (that is the named owner), and NOT for project milestones or sequencing (that is Throughline).
---

# Plan to Work

A decision is not executable until someone can say exactly what bounded result is wanted, against which revision, accepted how, and inside which paths — for every piece of it. This skill performs that handoff, once per package, and nothing beyond it.

## Two layers, and only two

| Layer | Holds | Lives | Never holds |
|---|---|---|---|
| **Registry** | identity, board, status, revision, claim and lease, dependencies, write paths, acceptance, event log | Loom | rationale, prose, history |
| **Body** | objective, upstream links, pinned revision, owner, exclusions, RED/GREEN, acceptance intent | one `work-items.md` beside the plan | state, claims, or a second copy of the dependency graph |

Bodies are the execution contract; the registry is the truth. This is Loom's own split, and it is why no local board, no task-state file, and no tracker shadow belongs anywhere in this skill.

Read [references/work-items-body.md](references/work-items-body.md) for the body layout, the per-package section template, and the exact registry mapping.

## The gate, per package

Every package carries all four. A package missing any of them is not created.

1. **Source** — the decision, spec or plan it came from, pinned to an exact revision. A path is not a pin.
2. **Outcome owner** — a named human accountable for acceptance. Never an agent, never "the team".
3. **Bounded result and observable acceptance** — what changes, and checks a reviewer can fail on purpose. "Works properly" fails the gate; "the export finishes under two minutes on the 40k-row fixture" passes.
4. **Write scope** — the exact paths, minimal, and disjoint from every package that could be claimable at the same time.

Direct-to-Loom work carries the same four; its provenance line from `request-triage` stands in for a Throughline source.

## Slice before you write

The unit is a **vertical slice**: a narrow but complete path through the layers it touches, demoable or verifiable on its own, and small enough for one agent to finish in a fresh context window. Not a layer, not a stub, not a phase.

- Prefactor first, when making the change easy makes the rest easy.
- An **integration** package owns the shared wiring and the parent-level scenario; a **review** package exists only where independent acceptance is required.
- A mechanical change whose blast radius fans across the codebase is not a slice. Sequence it as expand–contract: add the new form beside the old, migrate in batches, delete the old form last, each batch blocked by the expand.
- Mark each package **AFK** or **HITL**. Prefer AFK; HITL is for a genuine architectural or design call, not for an assumption you could settle by reading the code.
- Every package names what it descends from. One that cannot, goes in a **visible cut list** with what it would have done and why it was cut — the owner cannot reverse a cut they never saw.

Read [references/decomposition.md](references/decomposition.md) before splitting, for the contract-pinning rule, the shared-path policy, and the cut-list rules.

## Write the body file, then create the packages

1. One `work-items.md` beside the plan, keyed by **full namespaced ids** from the first line — `uds/W-3`, never a local `W-3` that has to be translated later.
2. Each section is written summary-first, with acceptance written before the detail, so detail that serves no check gets cut. Stay at intention and touch points: never a prescribed edit list, which goes stale against the code the implementer actually reads.
3. Create the packages in dependency order — a dependency must exist before a package can name it. Create everything as `draft`, and promote a package to `planned` or `ready` only when its frontier is real.
4. `goal` points at the body anchor instead of restating it. Write paths and acceptance go in the registry natively.
5. Record the package ids back on the source. The ask stays in one place; each package is a link.

## Dependencies are execution order, never project sequencing

An edge exists only if it means "this package is not safe to claim yet". Milestones, phases and replans stay in Throughline; if the same editable edge exists in both systems, it is wrong in one of them.

One fact to state rather than pretend around: Loom unblocks a package when its dependency is **integrated**, not accepted. So acceptance is not a prerequisite for execution unless a package's own integration includes that check. Design accordingly instead of assuming a stricter gate.

## If the source changes

The source revision is pinned at creation. A material change makes the package **stale for handoff purposes** — it does not update itself, and a running package never silently acquires new intent. The accountable owner chooses **continue**, **repackage** or **cancel**, on the record. Never choose on their behalf; never let a stale package keep running because cancelling looks wasteful.

The record to write, including the immaterial-change case, is in [references/handoff-record.md](references/handoff-record.md).

## Return only decisions

Back to the request level, and nothing more: package created, blocked on owner input, stale source or scope mismatch, review rejected, integration with evidence, package accepted, cancellation. Claims, renewals, retries and attempts stay in Loom's log — a request record that mirrors them becomes a stale second authority within a day.

## Stop instead of guessing

- No named human owner, or no observable acceptance → do not create; send it back to `request-triage` as `clarify`.
- The bounded result cannot be stated in one sentence → it is not bounded; split it or go back to shaping.
- Two packages would own an overlapping path and neither is an integration package → stop and decide the owner.
- A package is wanted so that work already underway can be "covered" → that is an orphan. Refuse it; start from the source.
- The plan body and Loom disagree about an edge or a scope → report the duplicate authority rather than picking a winner.

## Output

- **Packages** — ids created, with AFK/HITL and dependencies, or `refused` and the gate field that failed.
- **Source** — the record and its pinned revision.
- **Body file** — path, and the count of sections written.
- **Cut list** — what was cut and why, when anything was.
- **Left out** — what was deliberately not carried, where a reader might expect it.
