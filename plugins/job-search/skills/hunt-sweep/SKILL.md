---
name: hunt-sweep
description: >
  Runs the job-search sweep and proves that it ran: enumerates every connected source first, reads each one, then
  reports against a coverage ledger where any unread source forces a PARTIAL verdict. Use at the start of a session,
  when asked what is happening or what needs attention, or on a daily cadence. Encodes the failures that happen
  silently: filtering no-reply senders (where ATS decisions arrive), concluding from silence before the confirmation
  email, sampling threads instead of classifying them, and the one that breaks all the others — reporting a partial
  sweep as clean. Does not draft outreach — use outreach-voice. Does not fill forms — use ats-apply.
argument-hint: "[daily|weekly]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(date *), Bash(ls *)
---

## The failure this skill exists to prevent

On 16 November a sweep read two channels out of six and reported the result as "clean". The rule against doing that
was already written in this file, in bold, and it changed nothing.

That is the lesson: **a rule stated in prose cannot fail, so it does not get followed.** Only an artifact fails. This
skill now produces one — the coverage ledger — and the report is written against it.

## Step 0 — Enumerate, then write the ledger before reading anything

Call the discovery surface first. Never assume "both accounts" is a fact; it is a phrase until a call returns two.

| Source | Enumerate with | The trap |
| --- | --- | --- |
| Email | `list_accounts` | Omitting `account` silently resolves to **one** mailbox, not all of them |
| Calendar | `list-calendars` | Each calendar lists the accounts behind it; a `primary` on one account is not both |
| WhatsApp | `list_chats(sort_by=last_active)` | A name search proves a chat exists, not that the bridge is fresh |
| LinkedIn | `get_inbox` | Preview text is truncated; a thread's true last speaker needs the conversation |
| Queue | parse `queue.md` | Rows dated before today are drift, not history |

Write this block now, every line `NOT READ`, and keep it in the response draft:

```
COVERAGE — <date time>
email/<account>       NOT READ
cal/<account>         NOT READ
whatsapp              NOT READ
linkedin              NOT READ
queue                 NOT READ
VERDICT: PENDING
```

**Why before and not after.** A ledger written after the sweep is a description, and descriptions can be rationalised
to match what was actually done. A checklist written first is a contract: the holes are visible while there is still
time to close them.

## Step 1 — Calendar, every account, next 14 days

Two failures to watch:

- **Duplicate events from reschedules.** A new UID leaves the old accepted event in place. Two interviews on adjacent
  days, both accepted. Look for pairs with the same title.
- **Events with no other attendees.** A self-created placeholder is not an invitation — if only the candidate is on
  the list, the panel may not have the meeting.

Record: date, time, counterparty, and whether the counterparty is attached.

## Step 2 — Email, every mailbox, newest first

**Never filter `no-reply`, `noreply` or `notifications` senders.** ATS status mail comes from
`no-reply@*greenhouse-mail.io`, `no-reply@ashbyhq.com`, `no-reply@<company>.com`, `recruiting@`, `myworkday.com`.
Marketing can be excluded by domain allow-list; automated senders cannot.

Read the last 3 days fully. Classify each item:

| Class | Action |
| --- | --- |
| Rejection / closed | Record, close the application, do not chase |
| Interview invite / reschedule | Cross-check the calendar for the duplicate-event problem |
| Recruiter reply | Needs answering within the day |
| ATS confirmation | Evidence — record it |
| Portal digest | Ignore; not pipeline |

## Step 3 — WhatsApp, freshness before threads

Read the newest timestamp across all chats first. If the newest message anywhere is older than a day, the bridge is
stale — that is a tooling finding, not a quiet day.

Then read every thread where the candidate owes a reply. `is_from_me` decides who owes whom.

## Step 4 — LinkedIn, classify every thread

Do not sample the top five. Enumerate and classify each:

| State | Meaning |
| --- | --- |
| **You spoke last** | Awaiting them. One follow-up after 5–7 days, never a second |
| **They spoke last** | **You owe them.** The only state that needs action today |
| **Closed by them** | "I've left the company", "not my team" — record and stop |
| **Invitation pending** | Nothing to do until accepted |

Preview text lies about the last speaker when a thread carries an attachment. Open the thread when a message is
attached, deleted, or shorter than the preview suggests.

## Step 5 — Queue vs reality

- Rows whose event has passed → archive.
- Rows overtaken by events → archive with the reason.
- Rows with no owner or date → fix or delete.
- **Anything due that the sweep did not surface → the queue is lying; find out why before reporting.**

## The report gate

Two verdicts, and only two:

- **`COMPLETE`** — every source enumerated in Step 0 was read.
- **`PARTIAL`** — at least one was not. Name the unread sources **first**, before any findings.

"Clean", "nothing new" and "no changes" are **findings, never verdicts.** They may only appear attached to
`COMPLETE`. A sweep with an unread source is `PARTIAL` even when everything it did read looked empty.

Per-source status vocabulary — use these words:

| Status | Means |
| --- | --- |
| `read n` | Opened, `n` items in scope |
| `EMPTY` | Opened, returned nothing, **and a known-result query proved the source works** |
| `FAILED <reason>` | Attempted, did not return — auth, timeout, tool error |
| `NOT READ` | Never attempted. Forces `PARTIAL` |

## Disclose every filter

Before reading a source, write down any narrowing: date window, sender exclusion, folder, top-N, pagination.

**The filter is the finding.** On 16 November a `date >= today` filter on one mailbox, applied before reading it, is
the same error class as the `no-reply` exclusion that hid a rejection for two days: narrow the source, then treat the
narrowed result as the world. If the output does not name the filter, a reader cannot tell a quiet inbox from a
truncated one.

## Freshness proof — per source, not per sweep

An empty result from a broken source is not a finding. For each source that returns nothing, run one query known to
return results and record it. One proof for the whole sweep proves nothing about the sources that were skipped.

## No light passes

If there is time for two channels, read two and report `PARTIAL`. There is no such thing as a quick sweep; there is a
sweep, and there is the part of it that was done. Naming it "light" is how it gets reported as finished.

## Output — ledger, then the brief

The coverage block comes **first**, before any finding, so a reader sees the holes before the conclusions.

Then five lines:

1. What is due in the next 48 hours, with times.
2. What changed since the last sweep.
3. What the candidate owes someone.
4. What is stale or broken — tooling, portals, credentials.
5. The single highest-value action available today.

Then split owners explicitly: **only the candidate can do** (captcha, EEO answers, personal facts, WhatsApp sends on a
read-only bridge) versus **the agent can do**.

## Failure log

- Reporting a partial sweep as clean (16 Nov) — four channels unopened, and a resume sent to a recruiter with no
  message went unseen for a day.
- Filtering automated senders (13 Nov) — a rejection and a closed application hid for two days.
- Concluding "unconfirmed" from a 60-second gap — a duplicate application to the same req.
- Sampling threads instead of classifying — two recruiters who had replied "I've left the company".
- Trusting a tab's visual state over the inbox — reported pending on a submitted application.
