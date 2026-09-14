# Luna Architecture Consolidation Strategy v1

## Strategy

Consolidation is registry-first and non-destructive. Existing assets remain in
place while canonical layer, owner, status, and migration intent are recorded.
No implementation is rewritten in this phase.

## Order

1. Freeze the five-layer definition.
2. Assign one owner and one layer to each registered module.
3. Register allowed and forbidden dependencies.
4. Map aliases and historical assets to canonical IDs.
5. Record orphan modules and unresolved semantic duplicates as remediation
   candidates.
6. Re-audit before any Runtime or Capability activation.

## Remediation priority

- P0: illegal authority/dependency path or missing owner for a canonical-core
  module.
- P1: orphan module, unresolved duplicate canonical owner, or missing boundary
  contract needed before Runtime.
- P2: naming, documentation, and future Social/Emotion expansion.

## Non-destructive policy

`merge`, `alias`, `historical`, and `keep_parallel` are planning decisions only.
Deletion, overwrite, Runtime activation, provider execution, and Action
execution are out of scope.

