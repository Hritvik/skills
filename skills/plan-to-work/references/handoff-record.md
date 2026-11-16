# Handoff record

What a package carries, what is derived, and what is refused. Use this when composing a package by hand or checking one before it is created.

## Fields

| Field | Status | Notes |
|---|---|---|
| Source id and revision | **mandatory** | A commit, content hash, or decision id. A path or "latest" is not a pin. |
| Outcome owner | **mandatory** | A named human. An agent may hold the claim; only a human accepts. |
| Bounded result | **mandatory** | One sentence, imperative, specific. |
| Observable acceptance | **mandatory** | Each check is something a reviewer can fail on purpose. |
| Repository and write scope | **mandatory** | Minimal paths, no overlap with other claimable packages. |
| Execution dependencies | derived | From write paths and from prerequisites that must be integrated first. |
| Request link | derived | Written on the source record when the package is created. |
| Provenance line | mandatory for direct-to-Loom | See `request-triage/references/direct-to-loom.md`. |
| Rationale, design narrative, history | **refused** | The package points at the source; it does not restate it. |
| Effort estimate, dates, worker identity | **refused** | Loom and the owner decide these; a copied estimate becomes a promise. |
| Project or milestone edges | **refused** | Those are Throughline's. Duplicating one creates two editable authorities. |

## Staleness decision record

When the source revision moves, the owner's choice is recorded in one short block — in the request record, not in the package:

```
stale: <package id> | source <record> moved <old revision> -> <new revision> | decided by <owner> on <date>
decision: continue | repackage | cancel
reason: <one line, in the owner's terms>
```

- `continue` states that the newer change is out of scope for this package, which is a real decision and not a formality.
- `repackage` names the new package and what happens to this one.
- `cancel` names what is released and whether the request stays open.

An immaterial change — a typo, a comment, a formatting fix — is recorded the same way with `decision: continue` and `reason: immaterial: <what changed>`. Skipping the record is how a running task silently acquires new intent.
