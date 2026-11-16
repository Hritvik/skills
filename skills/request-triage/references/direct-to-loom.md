# Direct-to-Loom provenance and acceptance intent

A package that starts in Loom without a Throughline request must still be answerable later: who asked, what they wanted, and who says it is done. Record both blocks on the package itself. They are short on purpose — long provenance is a sign the ask needed Throughline.

## Provenance line

One line, on the package, in addition to whatever Loom records natively:

```
provenance: <source> | asked by <person> | <date> | pinned <path or artifact> at <revision>
```

- `source` is where the ask actually came from: `pasted`, a swept item id such as `gmail:<threadId>`, a thread link, or a conversation reference. `verbatim` alone is not provenance.
- `asked by` is a person or a named group. An agent asking on someone's behalf names that someone.
- `pinned` is required whenever the ask refers to a spec, design, contract, or file. Use the commit or content hash, not "latest".
- If two of these are unknown, the disposition is `clarify`, not direct-to-Loom.

Example:

```
provenance: gmail:18c2f0a9 | asked by Dana Whitfield | 2026-11-13 | pinned docs/api/ratings.md at 4f1c2de
```

## Acceptance intent

State what the requester will do to decide it worked, in their terms:

```
accepts: <owner> | <the observable thing they will check> | evidence: <test, run, screenshot, or record>
```

- **The owner is a human, never the implementing agent.** An agent can produce evidence; it cannot accept its own outcome.
- **The check is observable.** "Works properly" is not acceptance; "the export finishes under two minutes for the 40k-row fixture" is.
- Write the acceptance intent from what the requester said. If it has to be invented, ask rather than assert.
- The package closing, the review approving, and the receipt landing are all evidence that can feed acceptance. None of them is acceptance.

## When these blocks do not fit

If writing the provenance line needs more than a line, or the owner cannot be named, or the acceptance needs a history of decisions to make sense — the ask is not direct-to-Loom eligible. Open a Throughline request and let `plan-to-work` carry the handoff, where the context can live durably instead of being compressed onto a package.
