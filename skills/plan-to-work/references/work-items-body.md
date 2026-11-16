# Bodies and the registry

Two layers, one fact each. A body describes the work; the registry decides who may do it and what state it is in. Copying either into the other creates the second authority this design exists to prevent.

## Body file

One `work-items.md` per plan, beside the plan it came from. Its job is to be reviewable as a diff and readable without the plan open.

```md
# Work items — <program or plan name>

Source: <record id> at <revision>
Owner of the outcome: <human>
Board: <board id>

## <program>/<PREFIX>-<n> — <short title>

**Type.** AFK | HITL   **Kind.** implementation | integration | review

**Summary.** Three to five short plain sentences: why this exists and what is being done, with no
identifiers and no technical detail.

**Upstream.** <record or artifact> at <revision>; <contract or decision> — one line each, saying what
it is, not just its id.

**Write scope.** <paths this package owns>. Shared or generated files: <named owner, or "none">.

**Excluded.** <what this package deliberately does not do>.

**Acceptance.**
- [ ] <observable check a reviewer can fail>
- [ ] <observable check>

**Verification.** RED: `<command that must fail first>`. GREEN: `<command that must pass>`.
```

Rules that make this file useful rather than decorative:

- **No state, no edges.** No status, no dates, no assignee, no dependency list. Those are registry facts, and a body that says "Ready" or "depends on X" is drift with a timestamp on it — the engine's own backlog already proves the point: its bodies still say "Reviewed" for packages the registry records as integrated. Ordering, where a reader needs it, is read from the registry, not restated here.
- **Full namespaced ids from the first line.** The section heading and the registry id are the same string. No translation table, ever.
- **Acceptance before detail.** Write the checks first; then only the detail a check needs. It is the cheapest way to catch work nobody asked for.
- **No standard operating procedure as acceptance.** "CI green", "PR opened", "review done" are baseline practice, not outcomes.
- **No prescribed edit lists.** Intention, touch points and criteria survive a moving codebase; a line-by-line plan does not.
- **Contract pinning.** When two packages touch one shared contract — a file or wire format, a persisted schema, an API or event payload, a module signature, a config schema — the package that introduces it states the concrete form in its acceptance, and every consumer takes a registry dependency on that package. Never split one contract across packages that each define part of it.
- **Cut list**, under its own heading at the end: what each cut idea would have done, in plain language, and why it was cut.

## Registry mapping

Create with the Loom CLI, not by writing state anywhere:

```
task create --id <program>/<PREFIX>-<n> --board <board> --title "<title>" \
  --goal "<source>@<rev> — see work-items.md#<anchor>" \
  --write-path <path> --acceptance "<check>" --status draft
```

| Body field | Registry | Notes |
|---|---|---|
| Heading id | `--id` | Same string, no transformation. |
| Title | `--title` | The bounded result, imperative. |
| Plan name | `--program`, `--board` | One board per program; `uds.program` is the existing shape. |
| Summary | — | Stays in the body. `--goal` is a pointer, never the summary. |
| Upstream record and revision | `--goal` line | There is no revision field. The body carries the detail; the goal line carries the pin. |
| Write scope | `--write-path` (repeatable) | Declared in the registry because collision prevention depends on it. |
| Acceptance | `--acceptance` (repeatable) | Only checks a reviewer can fail. |
| Type AFK/HITL | Body only | Encodes whether a human must be in the room, not whether the work is claimable. |
| Kind implementation/integration/review | Body only | Describes the package's role in the plan; the registry has no kind. |
| Outcome owner | Body, and the source record | Loom has no owner field. The owner is the human who accepts; naming them twice, consistently, is deliberate. |

Dependencies are the one field with no body counterpart. `--depends-on` is the only edge that exists, because a second copy in prose is a second authority — and it drifts in exactly one direction: the prose stays stale while the registry keeps moving. Create in topological order, since a dependency must exist before a package can name it.

Two known gaps, stated rather than worked around:

- **No source-revision or owner field in the registry.** The `--goal` convention and the body carry them. If the pilot proves the convention is load-bearing, that is engine work with evidence, not something to smuggle in as a naming trick.
- **Dependencies unblock at integration, not acceptance.** `DEP_SATISFIED` is `{accepted, integrated, done}` and there is no per-edge gate. A package that must not start until something is accepted needs that acceptance inside its own scope.

## Evidence

Evidence is an observation, not a claim: the RED command and how it failed, the GREEN commands and their exact results, changed files, remaining gaps, reviewer findings. A passing command without its observed result is not evidence. Evidence lives in the content repository and is named in the registry's evidence field — never pasted into the body, which describes work rather than reporting it.
