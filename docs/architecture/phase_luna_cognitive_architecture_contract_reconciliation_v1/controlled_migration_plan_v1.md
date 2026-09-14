# Controlled Migration Plan

No migration is performed in this phase.

## Stage 1 — Contract authority corrections

Purpose: state Brain, A, B, Loop Engine and Task boundaries without changing
behavior.

Likely files: architecture contracts under this directory, existing A Route
owner documents, Loop boundary documents and B Route boundary documents.

Intentionally untouched: Python implementation, canonical types, enums,
verified runners/verifiers and real capability path.

Canonical type change: no. Runtime change: no.
Rollback: revert reconciliation documents.
Stop condition: owner and authority disagreements are explicit.

## Stage 2 — Shared A/B reasoning input envelope

Purpose: define a bounded package from Brain/Semantic/Filter into A and from A
into B, using refs and source state versions.

Likely files: new architecture contract first; later same-owner adapter types
only if necessary.

Untouched: Loop lifecycle types and Provider/Observation owners.
Canonical type change: preferably no. Runtime change: no.
Rollback: keep existing adapters and do not wire the new envelope.
Stop condition: A/B inputs are distinguishable from Loop mechanics.

## Stage 3 — Narrow Loop Engine cognition authority

Purpose: preserve Loop storage/mechanics while moving semantic judgments to A/B.

Likely files: Dynamic Flow/Loop integration adapters and documentation.
Untouched: lifecycle enums, Closure/Outcome types, Task Manager and Capability.
Canonical type change: avoid. Runtime change: controlled candidate behavior may
change later.
Rollback: retain old candidate fields as compatibility refs.
Stop condition: Loop no longer claims reasoning authority.

## Stage 4 — Rewire A → Loop and A → B boundaries

Purpose: make A the reasoning initiator and Loop the shared state mechanism;
make B A-initiated and bounded.

Likely files: A Route integration adapters and candidate-only fixtures.
Untouched: B1-B4 verified contracts, Provider path and runtime.
Canonical type change: not expected. Runtime change: synthetic candidate routing.
Rollback: adapter-level feature boundary.
Stop condition: no direct Task/Provider/Loop cognition bypass remains.

## Stage 5 — Deprecate duplicate route semantics

Purpose: remove or mark duplicate A/B route-chain meanings after evidence
confirms the target contract.

Likely files: architecture docs and legacy route planning references.
Untouched: source implementations until replacement contract is verified.
Canonical type change: no. Runtime change: no.
Rollback: documentation revert.
Stop condition: one B Route namespace and one A responsibility contract.

## Stage 6 — Controlled integration test

Purpose: validate candidate-only Brain/A/B/Loop/Task boundaries.

Likely files: future controlled fixture/runner/verifier under existing owners.
Untouched: real Provider and model runtime.
Canonical type change: no. Runtime change: synthetic only.
Rollback: delete only new test artifacts.
Stop condition: negative guards and source ownership are observable.

## Stage 7 — Real capability trial

Purpose: only after architecture and controlled contracts stabilize, reconnect a
bounded real capability invocation.

Likely files: existing real capability trial adapter only.
Untouched: no new Provider, no continuous camera, no automatic retry.
Canonical type change: no. Runtime change: explicitly approved and bounded.
Rollback: provider-trial boundary only.
Stop condition: architecture review and terminal verification authorize it.
