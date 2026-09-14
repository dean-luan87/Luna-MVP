# Implementation Overview

The implementation is isolated under the existing Cognitive Flow integration
tree and reuses existing candidate/reference conventions.

## Candidate layers

- Registry: immutable role capability boundaries, mechanical operations and
  failure vocabulary.
- Types: frozen candidate envelopes for grants, status, revocation, expiry,
  commands, mechanical state/return, derived grants and responsibility.
- Engine: pure candidate construction, validation, bounded mechanical state
  updates and derived B-grant checks.
- Adapter: 36 synthetic scenarios and compact aggregate summary.
- Runner/Verifier: user-terminal-owned JSON reporting and contract checks.

## Authority boundary

A and B receive semantic authority only through scoped grants. The Loop has
mechanical capability only and requires a separate Loop mechanical grant before
accepting a command. The adapter never infers semantic conclusions from Loop
state.

## State and trace

Concern, work scope, source state version, permission/resource references,
responsibility, result receiver, trace and provenance are carried as bounded
references. Historical trace is preserved when a grant is revoked or expires.
