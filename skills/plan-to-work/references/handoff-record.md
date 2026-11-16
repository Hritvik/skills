# Gate fields and the staleness record

What every package must carry, what is derived, what is refused, and how a mid-flight source change is recorded.

## Fields

| Field | Status | Reason |
|---|---|---|
| Source id and revision | **mandatory** | Without a pin, "implemented" has no referent. A commit or content hash; never a path or "latest". |
| Outcome owner | **mandatory** | An agent may hold the claim; only a human accepts the outcome. |
| Bounded result | **mandatory** | One sentence, imperative. If it needs two, it is two packages. |
| Observable acceptance | **mandatory** | Each check is something a reviewer can fail on purpose. |
| Write scope | **mandatory** | Minimal paths; collision prevention is only as good as this declaration. |
| Dependency edges | derived | From write paths and from what must be integrated first. Never from project sequencing. |
| Provenance line | mandatory for direct-to-Loom | See `request-triage/references/direct-to-loom.md`. |
| Rationale, design narrative, history | **refused** | The package points at the source. |
| Effort estimate, dates, worker identity | **refused** | Loom and the owner decide these; a copied estimate becomes a promise. |
| Project or milestone edges | **refused** | Those are Throughline's. |
| Standard operating procedure as acceptance | **refused** | "CI green" is baseline practice, not an outcome. |
| Line-level edit lists | **refused** | They go stale against the code the implementer actually reads. |

Where each field is recorded — registry argument, body section, or both — is in [work-items-body.md](work-items-body.md).

## Staleness record

When the source revision moves, the owner's choice is recorded in the source record, not in the package:

```
stale: <package id> | source <record> moved <old revision> -> <new revision> | decided by <owner> on <date>
decision: continue | repackage | cancel
reason: <one line, in the owner's terms>
```

- `continue` states that the newer change is out of scope for this package — a real decision, not a formality.
- `repackage` names the new package and what happens to this one.
- `cancel` names what is released and whether the source stays open.
- An immaterial change — a typo, a comment, a formatting fix — is recorded the same way with `decision: continue` and `reason: immaterial: <what changed>`.

Skipping the record is how a running package silently acquires new intent.
