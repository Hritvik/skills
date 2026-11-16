---
name: request-triage
description: Turn one raw ask into exactly one explicit disposition — clarify, merge as a duplicate, defer, reject, investigate, execute direct through Loom, or open/link a Throughline request — with provenance, a named outcome owner, and acceptance intent recorded. Use when a new request arrives pasted, swept from a source, or raised in conversation and someone must decide what happens to it before any work starts. NOT for sweeping sources into the inbox (that is desk:intake), NOT for challenging scope, dates or commitments (that is coach), NOT for operational symptoms and outages (that is service-incident-triage), and NOT for the versioned handoff once a request already exists (that is plan-to-work).
---

# Request Triage

A raw ask is not a task. It becomes work only through a disposition that someone can see, argue with, and reverse. This skill produces that disposition and hands it to the engine that owns it.

## Own no state

Triage is a decision, not a queue. Keep no request list, no cursor, no state file, and no second copy of an ask that already lives in Throughline or Loom. Read the engines, decide, write through the owning engine, and leave the record there. If a disposition needs remembering, it belongs to Throughline, not to this skill.

## Read the ask before choosing anything

- **Separate the ask from its proposed solution.** What outcome does the requester want, and what did they assume about how to get it? Triage decides the first; the second is an input, not an instruction.
- **Restate it in one sentence.** If you cannot, the disposition is `clarify` — the ask is not understood yet, not small.
- **Capture provenance**: how it arrived (pasted, a swept item's id, a thread link), who asked, and when. An ask with no provenance cannot go direct to Loom.
- **Pin what it references.** A named spec, design, contract or file is pinned at an exact revision, not "the current one". A stable path does not establish the same approved revision.
- **Notice the size the ask is dressed as.** A one-line message can carry a milestone; a long description can be a typo. Size is decided by consequence, not by length.

## Find the duplicate before you disposition

Search before you create, always:

- Throughline for the same outcome — live efforts, parked items, the inbox, and the requesting person's outstanding items.
- Loom for the same executable ask — planned and in-progress packages, including any whose title differs but whose write path or goal matches.

If the ask already exists, the disposition is `merge as a duplicate` naming that id and the reason. The same ask arriving from a second source — a pasted message after a sweep already filed it — is still one ask. Filing it twice is the failure this step exists to prevent, and it is invisible until two packages collide on one write path.

## The seven dispositions

Exactly one applies. Never a combination, never "looks fine, proceed".

| Disposition | When it is right | Authority | What it writes |
|---|---|---|---|
| **clarify** | The outcome, the requester, or the acceptance is not yet knowable. Ask the smallest set of questions that changes the disposition. | Triage decides; nothing is created | Nothing until answered |
| **merge as a duplicate** | The ask already exists in Throughline or Loom. | Recommend; the request owner confirms | A link or note on the existing record, never a new one |
| **defer** | The ask is valid but not now. | Request owner | A Throughline parked item with the reason and the trigger that would unpark it |
| **reject** | Out of scope, harmful, impossible, or already refused. | Request owner | The reason recorded where the ask came from; no work begins |
| **investigate** | Feasibility is genuinely unknown and one bounded probe answers it. | Request owner, because it spends time | A timeboxed Loom package with a question as its acceptance, or a Throughline item naming the owner |
| **direct to Loom** | It passes all four tests below. | Triage proposes; the named owner is accountable | A Loom package carrying provenance and acceptance intent |
| **Throughline request** | It carries durable context: a promise, decision history, milestone, product outcome, or follow-up. | Request owner | The request as an item or a new effort, linked to its source |

`defer`, `reject` and `merge as a duplicate` change what the requester gets, so they never proceed on triage's own authority. Present the recommendation with its reason and let the owner accept it.

## The direct-to-Loom test

Direct execution is the cheap path and the one that fails quietly. All four must hold:

1. **Bounded** — one repository, one package, one review, one integration.
2. **Reversible** — reverting is a single integration, with no data, promise or published contract to unwind.
3. **Self-contained** — the ask carries everything needed. No stakeholder promise, milestone, decision history, or product outcome has to survive past the package.
4. **Owned** — a named outcome owner exists, and the package records the provenance line and the acceptance intent from [references/direct-to-loom.md](references/direct-to-loom.md).

Fail any one and the disposition is a Throughline request. A bug that arrived from a tracked effort or a promise is not self-contained even when the fix is one line: the durable context already exists, so link to it instead of copying it onto the package.

## Hand off, do not absorb

- **Direct to Loom:** create the package through Loom, with the pinned write paths, the provenance line and the acceptance intent. Loom owns claimability, the lease, review, integration and the receipt. Triage does not schedule it and does not choose the worker.
- **Throughline request:** record the outcome, the constraint, the owner and the source link. Throughline owns the continuity. When the outcome is ready to execute, `plan-to-work` performs the handoff — not this skill.
- **Investigation:** the probe is ordinary work with a question as its acceptance; it goes through the same path as anything else, not around it.

Whichever path is taken, the ask appears in exactly one place as a record. Everywhere else is a link.

## Acceptance is never inferred

Triage names who accepts the outcome and what evidence would show it. It never treats a closed child package, a merged pull request, or a green test run as the user having got what they asked for. If nobody can be named as the accepting owner, the disposition is `clarify`.

## Output

Keep it to one block, in this order:

- **Ask** — one sentence, the outcome not the proposal.
- **Disposition** — one of the seven, with the reason in a line.
- **Provenance** — how it arrived, who asked, what was pinned.
- **Owner** — who accepts, or who must decide this disposition.
- **Record** — the Throughline or Loom id created or linked, or `nothing yet`.
- **Next action** — the single next step, and whose it is.

## Stop and hand over

- An outage, a page, or a live customer impact is `service-incident-triage`, not a request.
- A scope, date or commitment challenge is `coach`.
- An ask about a person's day, queue or what to work on is `desk`.
- Capacity, priority, spend, credentials, legal exposure, or a change to an existing commitment belongs to the owner. State the conflict and stop; do not resolve it by choosing a disposition that hides it.
- If two records already describe one ask, stop and report the collision rather than picking a winner.
