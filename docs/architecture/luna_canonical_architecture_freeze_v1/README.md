# Luna Canonical Architecture Freeze v1

## Freeze disposition

`ARCHITECTURE_FROZEN` / `RUNTIME_INCOMPLETE`.

This directory is the repository-side canonical architecture entrypoint for subsequent development. It consolidates the completed authority adjudications, vacuum closure, cognitive-flow freeze, contract closure and controlled synthetic implementation records.

The freeze does not declare production or runtime readiness. It freezes ownership, mutation domains, admission boundaries, canonical edges, version/invalidation rules, failure responsibility and deferred boundaries.

## Non-negotiable rules

1. Who has authority owns responsibility.
2. One mutation domain has one canonical authority.
3. Candidate production does not imply admission.
4. Derived state does not own source state.
5. Reads do not imply mutation authority.
6. Policy ownership and enforcement are separate.
7. Persistence does not imply semantic lifecycle authority.
8. There is no global Luna state version.
9. Failures return to the owner responsible for the failed boundary.
10. Historical compatibility does not override canonical architecture.

## Canonical flow

`Brain Concern/Grant → Working Envelope → Semantic Outline + Cognitive Snapshot → A → Attention/Capability → Runtime Admission → Observation/Provider → Evidence → Field/Current World candidates → A → Decision → Task → Action → Provider → Action Result → Task/A/Outcome → Brain adjudication → authorized Loop mechanics.`

This is a governed loop system, not a linear input/output pipeline. Provider and Action results never become World Truth directly.

## How to use this directory

- This freeze directory is the developer-facing reference.
- Detailed adjudication documents remain evidence and history.
- A future change to owner, authority, mutation, admission, canonical edge, precedence, version ownership, failure responsibility or deferred boundary requires architecture review.
- Runtime implementation may proceed only while preserving this ledger.

