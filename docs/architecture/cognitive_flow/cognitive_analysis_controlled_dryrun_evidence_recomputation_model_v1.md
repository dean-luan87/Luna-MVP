# A3 Controlled DryRun Evidence Recomputation Model v1

## Purpose

This design defines the future independent-evidence recomputation boundary for the frozen A3 Controlled DryRun baseline. Its purpose is to detect a serialized result that is internally well-formed but semantically inconsistent with the frozen fixture, contract, and boundary rules.

`design_only: true`. This document authorizes neither a Runner/Verifier change nor any execution.

## Current Verifier Boundary

The current verifier is file-based. It reads the Runner's serialized result, case-result, negative-guard, and reference-closure files; it does not invoke the Runner or retain Runner memory. It independently checks the output envelope: required files, baseline and contract references, case counts and uniqueness, aggregate counts, reference counts, runtime flags, and guard-summary cardinality/truth values.

Its current limitation is intentional but material: it trusts serialized per-case semantics and guard proof at their reported granularity. A result can therefore satisfy the envelope without the verifier independently deriving every case meaning or every guard proof.

## Future Recomputation Model

The strengthening verifier must derive expected results from frozen source assets before comparing them with serialized output.

1. Load the frozen Contract and baseline identifier.
2. Rebuild the immutable fixture collection only in a separately approved controlled regression phase.
3. Derive each case's expected semantic outcome from fixture fields and Contract invariants, without consuming a Runner `passed` value as proof.
4. Recompute local-reference closure, permission boundaries, warning aggregation, and each Negative Guard's static/execution proof.
5. Compare recomputed facts with the serialized case and aggregate outputs.
6. Report a specific divergence for every mismatch; never convert a mismatch into a warning-only pass.

The future verifier remains an observer. It may read frozen fixtures and output artifacts, but must not create State, Context, Snapshot, Event, Fact, Decision, Observation execution, or runtime side effects.

## Evidence Sources

| Evidence source | Role in recomputation |
| --- | --- |
| `cognitive_analysis_object_contract_v1.json` | frozen object, enum, invariant, permission, and runtime-boundary authority |
| frozen fixture builder and fixture records | per-case source of expected status, reasons, references, warnings, and candidate-only flags |
| static validators and invariants | deterministic structural and prohibited-behavior rules |
| canonical baseline manifest | identifies the baseline whose semantics and inventory are being protected |
| canonical `run1` output inventory | comparison artifact, never a source of expected semantics |
| serialized run output | observed claim to compare, never self-authenticating proof |

## Expected Semantic Derivation

For each frozen case, recomputation must establish: admission condition, result status, required reason/warning signals, evidence relation, unresolved/unknown preservation, and zero-execution permissions. The derived record must be keyed by the immutable `case_id` and use the fixture's declared `expected_status` rather than a Runner-supplied pass flag.

Aggregate pass, failure, blocker, warning, guard, and reference totals must be recomputed from those derived records. A mismatch between an aggregate and its case evidence is a blocker for the strengthening verifier.

## Non-Goals

- No new Case, Guard, Enum, Dataclass, Contract, Fixture, or baseline.
- No modification to the current Runner, Verifier, Serializer, or output artifacts.
- No analysis runtime, model, network, database, clock, randomness, or automatic UUID use.
- No reclassification of a Hypothesis Candidate as Fact, or of analysis output as State, Event, or Decision.
