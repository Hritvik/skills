---
name: plan-to-work
description: Convert one approved request or decision into an immutable Loom execution package — pinned source revision, named outcome owner, bounded result, observable acceptance evidence, repository and write scope — and handle a mid-flight source change as an explicit continue, repackage or cancel. Use when something has been decided and now needs to become claimable work, or when a running package's source or scope has changed underneath it. NOT for deciding what happens to a request (that is request-triage), NOT for scheduling, claiming or choosing a worker (that is Loom), NOT for accepting the outcome (that is the named owner), and NOT for project milestones or sequencing (that is Throughline).
---

# Plan to Work

A decision is not executable until someone can say exactly what bounded result is wanted, against which revision, accepted how, and inside which paths. This skill performs that handoff and nothing beyond it.

## Stay on the near side of the boundary

Loom receives an executable package, never a project plan. This skill prepares the package and records it through Loom. Loom then owns execution dependencies, claimability, claims and leases, review, integration and the package-level result.

Do not schedule, do not choose the worker, do not estimate, do not track progress afterwards, and do not accept the outcome. Those belong to Loom and to the accountable owner.

## The handoff gate

Four fields are mandatory. A package cannot be created without all of them.

1. **Source** — the request, decision, or artifact this came from, pinned to an exact revision. A path alone is not a pin; a revision without a record is not a source.
2. **Outcome owner** — a named human accountable for accepting the result. Never an agent, never "the team".
3. **Bounded result and observable acceptance** — what changes, and the check the owner will run to confirm it. "Works properly" fails the gate; "the export finishes under two minutes on the 40k-row fixture" passes.
4. **Repository and write scope** — the exact paths this package may touch, minimal and non-overlapping with anything else claimable.

A direct-to-Loom ask carries the same fields even with no Throughline reference: its provenance line stands in for the source, and the owner and acceptance intent are already recorded on it by `request-triage`.

Read [references/handoff-record.md](references/handoff-record.md) before composing a package by hand, and for the staleness decision record.

## Derive, do not copy

Everything else is derived or omitted — the handoff is deliberately narrow, and a copied plan is a second editable authority.

- **Execution dependencies are derived** from write paths and from prerequisites that must be integrated first. Project or milestone sequencing never becomes a Loom edge; if the same editable edge exists in both systems, it is wrong in one of them.
- **Scope comes from the decision artifact**, not from the requester's enthusiasm. A package that needs two unrelated repositories is two packages.
- **Acceptance evidence comes from what the requester said**, not from what is convenient to test.
- **Everything else is left out.** No rationale, no design narrative, no history, no estimate of effort, no copy of the request body. The package points at the source; it does not restate it.

## Compose the package

- **Title** is the bounded result, in the imperative and specific.
- **Goal** is a pointer: the source id and its pinned revision, plus one sentence of intent that would still be true if the implementation changed.
- **Acceptance** is the observable checks, listed so a reviewer can fail them.
- **Write paths** are the smallest set that completes the result, declared precisely enough that another package cannot claim an overlapping path.
- **Owner and acceptance intent** travel with the package so a later reader does not have to reconstruct who asked and what they expected.

Create it through Loom, and record the package id back on the source request as a link. The ask stays in one place; the package is a link.

## If the source changes

The source revision is pinned at creation. A material change to the request, the specification, or the acceptance criteria makes the package **stale for handoff purposes** — it does not update itself, and a running task never silently acquires new intent.

The accountable owner chooses one of three, explicitly and on the record:

- **continue** against the pinned revision, accepting that the newer change is out of scope for this package;
- **repackage**, creating new work against the new revision and retiring this package;
- **cancel** the package.

Never choose on the owner's behalf, and never let a stale package keep running because cancelling looks wasteful. If the change is immaterial — a typo, a comment — say so and record why it does not affect intent.

## Return only decisions

What goes back to the request level, and nothing more: package created, blocked on owner input, stale source or scope mismatch, review rejected, integration with evidence, package accepted, cancellation.

Claims, renewals, retries, attempts and ordinary transitions stay in Loom's audit log. Do not mirror them upward: a request-level record that duplicates the execution log becomes a stale second authority within a day.

## Stop instead of guessing

- No named human owner, or no observable acceptance → do not create the package; return it to `request-triage` as `clarify`.
- The source revision has already moved and nobody has decided → record `stale source` and ask the owner.
- The same edge or the same plan body exists in Throughline and Loom → stop and report the duplicate authority.
- The bounded result cannot be stated in one sentence → it is not bounded yet; split it or go back to shaping.
- Someone asks for a package to be created so that work already underway can be "covered" — that is an orphan package. Refuse it; start from the request.

## Output

- **Package** — the Loom id, or `refused` with the gate field that failed.
- **Source** — the record and its pinned revision.
- **Owner** — who accepts.
- **Acceptance** — the observable checks, verbatim as recorded.
- **Scope** — the write paths.
- **Derived dependencies** — what was added and why; empty is a fine answer.
- **Left out** — what was deliberately not carried, when a reader might expect it.
