---
name: interview-brief
description: >
  Builds the one-page brief for an interview: the JD's hardest requirement, the candidate's matching proof, the gap
  named honestly, and the questions to ask them. Use before any interview, when an interview is scheduled, or when
  asked "what should I say about X". Encodes the mapping discipline (proof chosen to answer their hardest
  requirement, not the candidate's favourite work), the guardrail list of claims that must never be made, and the
  rule that naming a gap plainly raises credibility while hiding it destroys it. Does not write application form
  free-text answers — use outreach-voice. Does not decide whether to accept an offer.
argument-hint: "[company or interview date]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(ls *)
---

## Build the brief 48 hours out, not the night before

Two interviews can land on one day, hours apart. The brief is what makes that survivable.

## Step 1 — Find the hardest requirement

Read the JD and take **the first three bullets**, not the long tail. Then ask: which single line would a hiring manager
use to reject someone? That is the requirement the interview will test.

Examples of what this looks like in practice:

| JD language | What is actually being tested |
| --- | --- |
| *"secure, multi-tenant, permissions-aware systems with appropriate auditing"* | Tenancy model and how you reason about isolation — not general backend skill |
| *"own the ingestion path at high event volumes"* | Backpressure, replay, ordering — not Kafka vocabulary |
| *"foundational compute platform spanning Kubernetes control planes"* | Cluster-plane engineering, where "services ran on Kubernetes" is not enough |
| *"deep expertise in Java and its ecosystem"* | Last substantial Java service, and whether you can go a level deeper |

## Step 2 — Choose one proof, matched to that requirement

One, not three. Three claims welded together is how a message — or an answer — starts sounding like a CV.

The proof must be:

- **True and specific.** A system, a decision, a number from the verified record.
- **Matched to the requirement**, not to whatever the candidate most enjoyed.
- **Short enough to say in two sentences.**

## Step 3 — Name the gap

Every brief has one. Write it as a sentence the candidate could say out loud:

> "I've built tenant-scoped configuration, routing and quotas — not a full multi-tenant data architecture. It's the
> part of this JD I'd most want to go deep on."

What this does: it converts a defence into a demonstration of judgement. What hiding it does: the interviewer finds
it in ten minutes and stops trusting the rest.

**Test:** if the gap sentence sounds like an apology, rewrite it. It should sound like scoping.

## Step 4 — The guardrails

A fixed list of things that must never be claimed, regardless of how well they would fit the question:

- **Kubernetes cluster ownership.** Services have run on Kubernetes; clusters have not been operated.
- **Go production depth.** Go appears in tooling and reading, not as owned production services.
- **Exactly-once external side effects.** The true claim is replay-safety with idempotent steps and persisted progress.
- **A metric that belongs to another system.** One support-automation number belongs to an earlier system, not to the
  GenAI platform.
- **An unasked-for reference.** Never name a referee who has not agreed.
- **Academic numbers.** No CGPA, no GPA — leave optional fields blank.

If a question invites one of these, the answer is the adjacent true thing, said plainly.

## Step 5 — Questions to ask them

Four, chosen so the answers change the decision:

1. **Level and scope** — what does the first six months own?
2. **On-call** — rotation and shape; ask before an offer, not after.
3. **Band** — fixed, and how it splits from the total.
4. **Why the role is open** — new headcount or backfill, and what happened to the last person.

Never ask four questions in one breath. Pick the two that matter for that interview's stage.

## Output

A single page:

```
ROLE / COMPANY / INTERVIEWER / TIME / LINK

THEIR HARDEST REQUIREMENT
  (one line, quoted from the JD)

YOUR PROOF
  (two sentences, matched to it)

THE GAP
  (one sentence, scoped not apologised)

DO NOT CLAIM
  (only the guardrails that could plausibly come up in this conversation)

ASK THEM
  (two questions for this stage)

LOGISTICS
  (link verified, notice period, time zone confirmed)
```

## Logistics that have actually bitten

- **Rescheduled invitations create duplicates.** Confirm which event is live; decline the stale one.
- **Time zones hide in odd slots.** A 20:00 IST interview is plausible; a 20:00 slot in a company whose other rounds
  were 15:45 is worth confirming.
- **Self-created placeholder events have no attendees.** If the panel is not on the invite, the meeting may not exist
  on their side.
