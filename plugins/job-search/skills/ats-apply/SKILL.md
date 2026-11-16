---
name: ats-apply
description: >
  Fills job application forms without losing an hour to widgets. Use when applying to a role, when a form will not
  submit, or when asked to pre-fill an application. Encodes the pre-flight checks (required school field, captcha,
  broken resume widget, cookie banner), the widget taxonomy per ATS (Greenhouse react-selects, Ashby type=submit
  yes/no buttons, Workday spinbutton dates, Instahyre selectize), and the read-the-errors discipline that unlocks
  most "broken" forms. Does not decide which roles to apply to — use role-sourcing. Does not judge whether a
  submission succeeded — use evidence-check. Never answers EEO questions, never invents personal facts.
argument-hint: "[job-url or company]"
allowed-tools:
  Read, Write, Edit, Glob, Grep, Bash(ls *)
---

## Pre-flight, before typing anything

Three checks save the most time. Do them first.

| Check | Why |
| --- | --- |
| **Is `School` required, and is the candidate's school in the list?** | Some boards (Stripe, Nexla) require it, offer ten IITs, and omit IIT Ropar. No free text, no "Other" that validates. The application cannot be completed truthfully — stop and say so |
| **Is there a captcha?** | reCAPTCHA enterprise blocks submission and gives no error. One human click. Detect it before filling: `iframe[src*=recaptcha]`, `textarea[name=g-recaptcha-response]` with an empty token |
| **Does the resume widget register files?** | On some Greenhouse boards the widget consumes the input and stores nothing. Verify `input.files.length` after upload, never the success message |

Also dismiss any **cookie banner** before diagnosing anything. A consent overlay swallows clicks silently: the submit
button appears enabled, clicking does nothing, and no error appears.

## Fill order

1. Text inputs (name, email, phone, links, employer, title).
2. Location and country selects.
3. Screening questions (yes/no).
4. Education and work history.
5. Resume upload — last, so a widget failure does not lose earlier work.
6. Consent and acknowledgement.
7. Submit.

## Widget taxonomy

| ATS | Widget | What works | What fails |
| --- | --- | --- | --- |
| Greenhouse | react-select (country, city, degree, discipline) | click the control, press ArrowDown to open, type, wait for the menu to leave "Loading…", then Enter — or click the exact option by its own coordinates | JS `click()` on an option paints the label without committing React state; validation then reports the field missing |
| Greenhouse | file upload | **board-specific.** GitLab, Twilio, Okta accept it; Stripe, OneTrust, Nexla consume the input and store nothing | trusting the toast instead of `input.files` |
| Ashby | yes/no options | trusted click **after** the cookie banner is gone | the buttons are `type="submit"` — clicking submits the form and triggers validation, which looks like a missing-field loop |
| Ashby | inline text fields (city, "add skill") | focus by **Tab** from the previous field, type, then pick from the dropdown | clicking the field first, or setting `.value`, both fail silently |
| Workday | date fields | keyboard typing — the month is a **spinbutton** expecting numeric `MM` | the string "May" is rejected with *"The field From is required"* |
| Workday | step buttons | trusted coordinate click | JS `.click()` often does not advance the flow |
| Instahyre | selectize chips (skills, education, locations) | click the control, then click the option row | the chip renders but the Angular model stays invalid; the education row re-renders its inputs away |
| iCIMS | form in a same-origin iframe | open the iframe URL directly so it becomes the top document | `pageDirtyFlag` arms `beforeunload` and can wedge the tab |

**General tell:** a field that *looks* like a text box but ignores typing is usually a react-select. Fivetran's "How
did you hear", Oscilar's city and Instahyre's education all presented as text inputs and were dropdowns.

## Read the errors before concluding the form is broken

When submit does not advance, this is the next action — not a retry, and not a claim that the form is undriveable.

```
harvest: [role=alert] text
harvest: every node whose text matches /required|missing|correction|error/i
harvest: any toast ("There were problems submitting…")
harvest: aria-invalid="true" controls and their labels
```

Two examples of what this found:

- *"Missing entry for required field: What city do you live in?"* — a field that had been typed into but never committed.
- *"The field From is required and must have a value. Current value is MM/2022"* — a date format problem, not a missing field.

An hour was spent calling Workday unautomatable before anyone read its error messages.

## What is never filled by the agent

- **EEO / voluntary disclosures** — gender, disability, veteran status. The candidate answers every time, unless they
  supply the answer explicitly in the conversation.
- **Personal facts that do not exist in the record** — home address, postal code, date of birth, travel willingness.
  Ask; never infer.
- **Captchas.**
- **Campus claims.** If the school list lacks the candidate's institution, do not substitute another campus.

## When to stop and hand off

Stop rather than grind when:

- The required school list excludes the candidate's institution.
- A captcha blocks submission — one human click.
- A required field needs a fact the candidate has not supplied.
- Three distinct approaches to one widget have failed and the field is cosmetic (a city box, a skills chip) — finish
  everything else, then hand over a single action.

## Finish

Immediately after submitting, run `evidence-check`. Do not close the tab before the evidence is captured — on boards
that send no email, the tab is the only proof.
