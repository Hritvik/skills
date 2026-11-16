---
name: outreach-voice
description: >
  Writes and reviews the voice of outreach messages — LinkedIn DMs and connection notes, recruiter and agency emails,
  referral asks, hiring-manager notes — so they read as one engineer writing to another rather than a CV compressed
  into a paragraph. Use when drafting or reviewing any message to a recruiter, hiring manager, peer, or referral, or
  when asked to make an existing draft sound human. Contains mechanical tests that fail on template-shaped writing,
  a banned-construction list, and channel-specific shapes. Does not decide who to contact or what the ask should be
  strategically — use the outreach protocol and message-protocol for Stage 0 inputs and evidence selection. Does not
  write résumés or CV bullets — use resume-bullet-writer. Does not write application form free-text answers where the
  employer has asked for the candidate's own words.
argument-hint: "[draft text, recipient, or channel]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(ls *), Bash(wc *)
---

## The problem this skill exists to prevent

A message can satisfy every input a protocol asks for and still read as machine-written. The failure is not
insufficient specificity — it is **shape**: a five-part pitch (hook, credibility, context, ask, sign-off) compressed
into ninety words becomes a CV welded together with commas.

Real example, sent to a recruiter who never replied:

> ❌ "Sneha — 51 mutual connections, and I build the systems you're hiring for: GenAI platform infrastructure and
> Kafka-based orchestration at Meesho, eight years in as an IC by choice. Would like to connect about staff-level
> backend roles at Coupang."

Every input was satisfied. The message is still an advertisement.

## The four mechanical tests

Any single failure means rewrite. These are not scored or averaged — one failure is fatal.

1. **Say the first eight words out loud.** Would you say them to the person's face?
   *"Sneha — 51 mutual connections"* fails. *"Hi Sneha — we know a lot of the same people"* passes.
2. **No sentence may carry three or more comma-separated claims.** Split it, or delete a claim. People do not weld
   clauses; they say one thing, then another.
3. **Could this be sent unchanged to a different person at the same company?** If yes, it is a broadcast with a name
   pasted on.
4. **Delete any mutual-connection count.** Mutuals may inform *whether* you write. They never appear in the text — a
   count is a fact about the graph, not a detail about the person.

## Banned constructions

| Banned | Why |
| --- | --- |
| "I build the systems you're hiring for" | Sales cadence, not speech |
| "Would like to connect about…" | Formal register no human uses |
| "I came across your profile" | Signals a list, not a person |
| "I hope this message finds you well" | Filler; spend the words elsewhere |
| CV summarised in category nouns ("infrastructure and orchestration at X, N years as an IC by choice") | Three claims welded; reads as a headline |
| "As a [title] with [N] years…" | Job-board language |

## The reference pair

> ❌ "Sneha — 51 mutual connections, and I build the systems you're hiring for: GenAI platform infrastructure and
> Kafka-based orchestration at Meesho, eight years in as an IC by choice. Would like to connect about staff-level
> backend roles at Coupang."

> ✅ "Hi Sneha — we seem to know a lot of the same people, so I'll skip the pitch.
> I'm at Meesho, mostly on the platform side — the team that runs our model routing and evaluation, plus a Kafka
> pipeline I rebuilt last year.
> Are you working on backend hiring at Coupang at the moment?"

What the second one removes: the number, the pitch verb, the stacked clauses, the formal ask. What it adds: a reason
to keep reading, one concrete detail, and a question a person can answer in ten seconds.

## Assembly rule — short formats carry two parts, not five

| Channel | Parts | Limit |
| --- | --- | --- |
| LinkedIn connection note (2nd degree) | why them + intent to connect | ≤300 characters, hard |
| LinkedIn DM (1st degree) | why them + one question | ≤90 words |
| Recruiter email (in-house) | role/level question + one credibility line | ≤130 words |
| Agency email | what you want + the numbers line + one ask | ≤130 words |
| Referral ask | the specific role + one question | ≤90 words |
| Hiring manager | a responsibility from their JD + one question | ≤110 words |

If a draft needs a third clause to be true, **the message is too small for the claim — cut the claim, not the
honesty.** A shorter true message beats a longer hedged one.

## Drafting procedure

1. **Find one artefact.** Something they wrote, shipped, posted, or said — a JD line, a talk, a repo, a comment. A
   mutual count is not an artefact. If nothing exists, write to someone else.
2. **Write the first sentence as speech.** Type it the way you would say it; do not start from a template.
3. **Add one concrete detail** about your work — a system, a number, a decision. One, not three.
4. **Ask one question** they can answer in ten seconds. Never two, never a favour plus a question.
5. **Run the four tests.** Rewrite on any failure. Do not rationalise a pass.

## Evidence discipline

Claims must come from the candidate's own verified record. In a job-search workspace that means the canonical
`application-facts.md` and the tracker — never from memory of what sounds impressive.

- Say **"services deployed on Kubernetes"**, never that clusters were operated.
- Say **"replay-safe with idempotent steps"**, never "exactly-once external side effects".
- Quote the fixed/total split correctly: fixed first, total second. Never paraphrase "fixed" out of a total.
- Never use a metric that belongs to a different system than the one being discussed.

## Reviewing someone else's draft

Lead with the specific test that fails, not with taste. *"The first eight words are a number from the profile
header — say them aloud"* is actionable. *"This feels off"* is not. Then give one rewrite, not three options.

## When silence is the feedback

If a template shape has produced no replies across several recipients, the problem is the shape, not the recipients.
Count the replies before defending the template.
