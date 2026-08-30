---
name: movie-ticket-finder
description: Run a requirements Q&A, then find live cinema showtimes and recommend theatres, premium formats, and genuinely adjacent seats. Use for recommendation-only movie-ticket research; it does not book, reserve, hold, or purchase tickets.
---

# Movie Ticket Finder

Find the best practical screening, not merely the first available show. This skill is recommendation-only.

## Requirements and durable preferences

Start with requirements already known from the conversation and any durable profile supplied with the plugin. Ask only for missing or ambiguous values that could change eligibility or ranking, using one compact batch:

- movie, language, and acceptable 2D/3D variants
- city, exact date, and allowed start-time window
- party size
- each traveller's origin and whether to optimize for midpoint or one traveller
- quality priorities, budget, and accessibility needs

Summarize the agreed constraints and resolve every relative or exact date in the user's timezone before opening live listings. Treat “between 11 and 4” as inclusive start times unless the user says otherwise. Explicit instructions override a durable profile. Never ask again for facts already established in the conversation or profile.

## Compact browser workflow

Use `browser:control-in-app-browser` for an in-app BookMyShow tab; use Chrome control only when the user requests Chrome. Preserve an existing relevant tab when possible.

1. Open one authoritative city-and-date listing. Confirm the selected movie, city, date, language, and 2D/3D variant from visible page state.
2. Shortlist at most three shows using the user’s hard constraints. Rank them by travel fairness, presentation quality, start time, and price.
3. Inspect seat maps only for the leading candidates. Use the accessibility seat list for exact availability and pricing, then inspect the visual map for physical geometry.
4. Leave the best candidate’s seat map open without selecting seats.

Never select, hold, reserve, book, or purchase tickets. Do not enter login credentials, passwords, OTPs, card details, CVVs, billing data, or payment flows. If the user requests booking, explain that this skill currently stops at verified seat suggestions and requires a separate secure booking capability.

Avoid broad search-engine result collection, repeated full-page snapshots, and opening one tab per theatre. Reuse a listing or cinema page and gather only the state needed for the next decision.

When work spans turns, retain only a compact state: movie/date/window, known origins, shortlisted shows, current seat map, and rejected seats with brief reasons.

## Presentation quality

Prefer verified premium projection and sound labels. For 3D, favor bright laser projection or a well-specified large format. For 2D, prioritize formats such as IMAX Laser, Dolby Cinema, PXL, or a verified 4K laser screen when available. Treat Atmos, Dolby 7.1, and similar labels as evidence, not guarantees; do not invent specifications that the listing does not show.

Balance quality against location. When people travel from different origins, favor a reasonable midpoint or a theatre closer to the person with the harder journey, as requested. If midpoint matters but only one origin is known, ask for the other origin or label the result as optimized only for the known origin. Clearly label a farther option that is included only for superior presentation.

## Seat selection

Never infer physical adjacency from consecutive seat numbers.

Before recommending a pair or group:

- Verify every seat is available in the exact show.
- Inspect the visual auditorium map for aisles, gaps, split blocks, wheelchair spaces, and screen orientation.
- Ensure the seats touch with normal within-row spacing; consecutive numbers across an aisle are not adjacent.
- Prefer the horizontal optical centre within one contiguous block and roughly 55–70% of the auditorium depth from the screen.
- For large-format screens, avoid very front rows. Prefer a slightly off-centre intact pair over seats split by an aisle.
- State the exact row, seats, category, and per-seat price. If geometry is ambiguous, say so instead of guessing.

## Result

Lead with one recommendation, followed by up to two alternatives. For each, include theatre, date, time, verified format, seats, price, travel trade-off, and why it ranks there. Distinguish verified facts from judgement. Mention that availability can change and explicitly state that no seats were selected, held, reserved, or purchased.
