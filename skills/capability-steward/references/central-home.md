# Central Capability Home

Use this reference when locating or creating the portfolio home, changing its registry, or migrating artifacts from product repositories.

## Valid home

A valid home is a directory containing both:

- `capability-home.yaml` with `kind: capability-steward-home`
- `registry.yaml` listing every authoritative capability artifact by stable ID and home-relative path

The marker identifies the coordination boundary. The registry provides the single discovery surface. Artifact files remain split so independent efforts can edit different records concurrently.

When the user authorizes a new home, initialize these files from [../assets/capability-home.yaml](../assets/capability-home.yaml) and [../assets/registry.yaml](../assets/registry.yaml), then register the first artifact in the same change.

Do not hardcode a machine-specific home path in the skill. Resolve the home from accessible workspace roots or a user-supplied location.

## Resolution guard

Before any artifact mutation:

1. Search accessible workspace roots for `capability-home.yaml`.
2. Read each candidate and retain only markers whose `kind` is `capability-steward-home`.
3. Require exactly one candidate.
4. Read its `registry.yaml` before selecting or creating an artifact.

No candidate means the central home is unavailable, not that the active repository should become a home. Multiple candidates are ambiguous and require user direction.

## Registry rules

Registry entries contain at least:

- stable artifact ID
- artifact kind
- home-relative path
- current status when present in the artifact
- owner or explicit ownership gap when present

Keep paths relative to the home so the collection is portable. Grouping entries by `efforts`, `contracts`, and `decisions` is recommended but not mandatory.

For every mutation:

- Add new artifacts to the registry in the same change.
- Update a path when moving an artifact; do not create a second ID.
- Retain superseded history according to the artifact model.
- Remove a registry entry only when its artifact was intentionally removed or migrated.
- Validate that every registry path exists and every authoritative YAML artifact is registered.

## Product repositories

Product repositories may contain implementation plans, architecture documents, schemas, test evidence, or source code referenced by central artifacts. Link these with a repository identifier and repository-relative path; do not use machine-specific absolute paths.

Do not place authoritative capability maps, contracts, expectations, commitments, or cross-effort decisions in product repositories. If a product needs a discoverability hint, use ordinary project documentation that links to the central artifact by stable ID; do not copy the artifact content.

## Migration

When a repo-local artifact already exists and the user authorizes consolidation:

1. Preserve its stable IDs, authorship, decisions, and history.
2. Move it under the central home using a clear home-relative path.
3. Convert broken relative technical links into repository identifiers plus repository-relative paths.
4. Register the central path.
5. Validate the central copy before removing the repo-local authoritative copy.
6. Confirm that no other authoritative copies remain in accessible product repositories.
