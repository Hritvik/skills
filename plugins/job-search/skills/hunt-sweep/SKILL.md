---
name: hunt-sweep
description: >
  Runs the job-search sweep: calendar, both inboxes, WhatsApp freshness, LinkedIn threads, then queue-versus-reality —
  in that order, classifying every thread rather than sampling recent ones. Use at the start of a session, when asked
  what is happening or what needs attention, or on a daily/weekly cadence. Encodes the three rules that fail silently:
  never filter no-reply senders (that is where ATS decisions arrive), wait for confirmation email rather than
  concluding from silence, and classify every thread instead of filtering by recency. Does not draft outreach — use
  outreach-voice. Does not fill forms — use ats-apply. Does not decide strategy or comp position.
argument-hint: "[daily|weekly|full]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(date *), Bash(ls *)
---

## Why this is a skill and not a checklist

Every sweep failure so far has been a **skipped step**, not a bad judgement:

- A `no-reply` filter hid a rejection and a closed application for two days.
- A confirmation email landed 60 seconds after an inbox check; the application was rebuilt and submitted twice.
- LinkedIn was skipped entirely on a "quick" sweep, missing two recruiters who had replied "I've left the company"
  and one who had said "happy to talk this week".

The order below is load-bearing. Run it top to bottom; do not reorder for convenience.

## 1. Calendar — both accounts, next 14 days

List events for every connected account. Two failures to watch:

- **Duplicate events from reschedules.** A rescheduled invitation with a new UID leaves the old accepted event in
  place. Two interviews 24 hours apart, both accepted. Check for pairs on adjacent days with the same title.
- **Events with no other attendees.** A self-created placeholder is not an invitation. If only the candidate is on
  the list, the panel may not have the meeting.

Report: date, time, counterparty, and whether the counterparty is actually attached.

## 2. Email — both accounts, newest first

**Never filter `no-reply`, `noreply`, or `notifications` senders.** ATS status mail comes from
`no-reply@*greenhouse-mail.io`, `no-reply@ashbyhq.com`, `no-reply@<company>.com`, `recruiting@`, `myworkday.com`.
Filtering marketing by domain allow-list is fine; filtering automated senders is not.

Read the last 3 days fully. Classify each item:

| Class | Action |
| --- | --- |
| Rejection / closed | Record, close the application, do not chase |
| Interview invite / reschedule | Cross-check the calendar for the duplicate-event problem |
| Recruiter reply | Needs answering within the day |
| ATS confirmation | Evidence — record it |
| Portal activity digest | Ignore; not pipeline |

## 3. WhatsApp — freshness first, then threads

Prove the bridge is fresh before reporting "nothing new": read the most recent chat timestamp. If the newest message
is older than a day across all chats, the bridge is stale, not the world.

Then read every thread where the candidate owes a reply. Note who spoke last — `is_from_me` decides who owes whom.

## 4. LinkedIn — classify every thread

Do not sample the top five. Enumerate threads and classify each:

| State | Meaning |
| --- | --- |
| **You spoke last** | Awaiting them. One follow-up allowed after 5–7 days, never a second |
| **They spoke last** | **You owe them.** This is the only state that needs action today |
| **Closed by them** | "I've left the company", "not my team", "we're not hiring" — record and stop |
| **Invitation pending** | Nothing to do until accepted |

A sweep that reports "no replies" while a thread has them speaking last is wrong.

## 5. Queue vs reality

Parse the queue and compare with what the sweep found:

- Rows whose event has happened → archive (strike through so the parser skips them).
- Rows overtaken by events → archive with the reason.
- Rows with no owner or no date → fix or delete.
- Anything due that the sweep did not surface → the queue is lying; find out why.

## Output — the five-line brief

1. What is due in the next 48 hours, with times.
2. What changed since the last sweep (new replies, confirmations, closures).
3. What the candidate owes someone.
4. What is stale or broken (tooling, portals, credentials).
5. The single highest-value action available today.

Then list owners explicitly: **items only the candidate can do** (captcha, EEO answers, personal facts, WhatsApp sends
where the bridge is read-only) versus **items the agent can do**.

## Freshness proof (Rule 9)

Before reporting "nothing found", prove the source works: run a query you know returns results. An empty result from a
broken source is not a finding. This applies to job search, people search, and inbox reads alike.

## Failure log to check against

- Filtering automated senders → missed rejection.
- Concluding "unconfirmed" from a 60-second gap → duplicate application.
- Sampling threads instead of classifying → missed live recruiter replies.
- Trusting a tab's visual state over the inbox → reported pending on a submitted application.
