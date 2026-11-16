---
name: evidence-check
description: >
  Decides whether an application or a message actually happened, and prevents duplicate submissions. Use immediately
  after submitting an application, after sending a message, or whenever asked "is that in / did it go through".
  Encodes the evidence hierarchy (ATS email beats on-screen state beats a URL), the waiting rule (do not conclude from
  absence within minutes), the static-confirmation trap (Greenhouse confirmation URLs render for anyone), and the
  duplicate rules that apply once an application exists. Does not fill forms — use ats-apply. Does not draft or send
  messages — use outreach-voice.
argument-hint: "[company or action]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(ls *)
---

## The question this answers

Not "did the form disappear?" but **"can I prove this submission to someone else?"**

## Evidence hierarchy

Rank every claim by what you can hand to a sceptic:

| Strength | Evidence | Notes |
| --- | --- | --- |
| **Strongest** | ATS confirmation email | `no-reply@*greenhouse-mail.io`, `no-reply@ashbyhq.com`, `no-reply@<company>.com`, `myworkday.com`, `no-reply@hire.lever.co`. Record sender, subject, timestamp |
| Strong | Live transition observed — form replaced by a confirmation view, inputs gone | Real but ephemeral; capture it while it exists |
| Weak | Confirmation page URL alone | **Greenhouse confirmation URLs are static** — `/embed/job_app/confirmation?for=X&token=Y` renders "Thanks for applying!" for anyone. A URL is not evidence |
| None | "The submit button responded" | Buttons respond to clicks that do nothing |
| None | An empty inbox two minutes after submitting | Absence, not evidence |

## The waiting rule

**Never conclude "it didn't submit" from a missing email inside a few minutes.** Confirmations arrive between one and
several minutes after the action, and some ATS platforms send a security code first.

Cost of getting this wrong, measured: a Ping Identity application was declared unconfirmed after a 60-second check.
The confirmation landed the next minute. The form was rebuilt and submitted again — producing **two applications to
the same req**, both confirmed by email.

If in doubt, wait and check again. Rebuilding is the expensive mistake.

## The static-confirmation trap

Recognising a confirmation page is not proof:

- Greenhouse `…/job_app/confirmation?for=<board>&token=<job>` renders on request.
- The real signal is the **transition**: the form had inputs, then it had none, and the URL changed, in one observed
  session.

If the transition was not observed and there is no email, the honest status is **"probably submitted, unverified"**.

## Checked and empty is not the same as not checked

There are two kinds of nothing, and they look identical in a report:

| Kind | What it means | May you say "nothing there"? |
| --- | --- | --- |
| **Checked, empty** | The source was opened, a known-result query proved it works, and it holds nothing relevant | Yes |
| **Not checked** | Nothing was opened. The absence is in the search, not in the world | **No — say what was not checked** |

The second kind is how a rejection sits unread for two days behind a sender filter, and how a resume sent with no
message goes unnoticed for a day. In both cases the sweep was not wrong about what it saw; it was wrong about what it
had looked at.

**Rule:** absence may only be reported per source, with the source named and its coverage stated. "No new replies" is
a claim about five channels or it is a claim about none.

## Duplicate rules

Once an application exists at a company, treat further submissions as costly:

- **Harvey** caps applications at four per 30-day window. Using two on near-identical reqs is waste.
- **Greenhouse** does not visibly block a second application to the same req; it may accept and dedupe silently, or
  it may create a genuine duplicate. It cannot be relied on either way.
- **Never re-submit to prove a submission.** If a form is ambiguous, look for the email, then report the ambiguity.

When a duplicate has happened, correcting it is worth it: one short note — *"my application was submitted twice
within a few minutes, a tooling error on my side, not a second bid; please treat the earlier one as my application"* —
turns a red flag into a sign of care.

## Recording

For every submission, record:

```
company | role | req id | submitted at | evidence type | evidence detail | status
```

Status vocabulary — use exactly these, they are not interchangeable:

- **Confirmed** — ATS email in hand.
- **Submitted, on-screen** — transition observed, no email. Note that the tab was the evidence.
- **Unverified** — nothing but a page URL, or nothing at all.
- **Not submitted** — form still present, or a validation error explains it.

## Smells that mean "check again"

- The confirmation email never arrived but Ashby or Greenhouse confirmed another application the same day.
- The form page reloads with empty fields after a claimed submission.
- The submit button still exists after clicking it.
- A confirmation page renders but no timestamp or employer-specific detail appears.

Any of these: search the inbox with the company name, then with the ATS domain, **without** filtering `no-reply`.
