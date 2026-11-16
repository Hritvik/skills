---
name: role-sourcing
description: >
  Finds roles worth applying to, in the right order, without wasting time on closed reqs or title inflation. Use when
  asked to find jobs, to widen the pipeline, or when the application queue is empty. Encodes the channel ordering
  (LinkedIn for freshness, hiring.cafe weekly for the remote-India intersection, ATS APIs for applyability, Hacker
  News monthly for small companies, job boards for presence only), the employer-tier axis that replaces title
  matching, req-decay checks before spending time on a form, and the comp gate as an offer-stage filter rather than a
  screening filter. Does not fill forms — use ats-apply. Does not decide comp position at offer — that is a
  negotiation call.
argument-hint: "[weekly|remote|indian-market|adjacent-tech]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(curl *), Bash(python3 *), Bash(ls *)
---

## The model that matters

**Title is the wrong axis.** "Staff Engineer" at a 40-person startup and "Senior Engineer" at a global captive can pay
the same, or inverted. The only stable filter is **employer tier** — companies whose staff-level fixed pay clears the
candidate's floor, regardless of what they call the role.

Two consequences:

1. Curate a list of employers that clear the gate, then check *their* boards. Do not search titles across boards.
2. Reject by employer tier, not by title. A "Principal" at a services company is not a step up.

## Channel order

| Order | Source | Cadence | Why |
| --- | --- | --- | --- |
| 1 | **LinkedIn job index** | daily | Freshest signal; filter `date_posted=past_24_hours` to see genuinely new reqs, and read the apply type |
| 2 | **hiring.cafe** | weekly | The only place that surfaces India + remote + staff in one query. Filters are URL-encoded JSON in `?searchState=` — `{"searchQuery":"staff software engineer backend","workplaceTypes":["Remote"]}` returned 25 roles across 16 companies. Unchanged in 24 hours, hence weekly |
| 3 | **Greenhouse / Ashby / Lever board APIs** | weekly | Exact live reqs with apply URLs. `/v1/boards/<slug>/jobs?content=false` and `api.ashbyhq.com/posting-api/job-board/<slug>` |
| 4 | **Hacker News "Who is Hiring"** | monthly | Posted on the 1st; queryable via Algolia (`tags=comment,story_<id>`). Surfaces small profitable companies that never appear elsewhere — one such query produced a remote-India staff Java role with a stated band |
| 5 | **Job boards (Naukri, Foundit, Cutshort, Instahyre, Weekday, Wellfound)** | monthly | **Presence, not search.** Naukri shows every salary as "Not Disclosed", so the comp gate cannot be applied there |
| 6 | **Referrals** | continuous | The only channel with real volume at senior comp. A first-degree contact at a target company beats any volume of applications |

## Before spending time on a form

Three checks, in order — each has already cost an hour:

1. **Re-resolve the req.** Search-result IDs decay within days. Two roles found on one day were closed by the next.
   Confirm the posting still exists on the company's own board before opening a form.
2. **Check for a required school field** and whether the candidate's institution is listed. If not, the form cannot be
   completed truthfully.
3. **Check the apply path**: Greenhouse/Ashby embed = automatable; Workday = per-tenant account and the most expensive
   form in the stack; own-portal (Google, Microsoft, Visa, LinkedIn) = authenticated, effectively manual.

## Comp gate — applied late, not early

| Band (fixed) | Action |
| --- | --- |
| ≥ target | Pursue normally |
| 64–100% of target | **Do not decline early.** Run the process, decide at offer |
| < 64% | Declinable early |

Rules:

- The gate is **fixed**, not total. A large quoted CTC does not pass it.
- Indian offers typically run fixed at 70–75% of CTC — a ₹1.0–1.1 Cr "total" may fail a fixed floor.
- Never quote the floor unless asked. When asked, give the fixed number, not a total.
- Never let a low posting band pre-screen a role that could negotiate.

## Dedupe

Before adding anything, check it against what is already applied. Applying twice to one req within a week looks
careless; several applications inside one ATS in a week dilute the strongest one.

## Output shape

A short list, each row carrying: company, role, level, location, posted age, band if stated, apply path, and
**why it survives the tier filter**. Plus one line on what was rejected and why — the rejects are the useful part
next time.

## Small companies

The best-fit roles are often 10–50 person product companies. They are also where a staff title most often means
below-floor fixed pay. Include them, but ask the band before spending interview cycles — not before applying.
