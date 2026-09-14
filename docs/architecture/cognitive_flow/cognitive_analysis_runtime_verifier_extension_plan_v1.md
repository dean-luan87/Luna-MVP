# A3 Cognitive Analysis Runtime Verifier Extension Plan v1

## Purpose

This plan describes how a future, separately authorized verifier extension could assess Runtime outputs without trusting Runtime self-attestation. It changes neither the existing DryRun Verifier nor the frozen baseline.

## Starting Point

The current DryRun Verifier is file-based and checks the serialized output envelope. Evidence Review records that independent per-case semantic recomputation and per-guard dual-proof recomputation remain strengthening work. Any Runtime verifier extension must complete those foundations before adding Runtime-specific checks.

## Planned Verification Domains

| Domain | Future verification requirement | Runtime self-report is insufficient because |
| --- | --- | --- |
| Runtime output validation | recompute output shape, version, source Context linkage, candidate status, lifecycle, warnings, and result totals from independent evidence | output serialization can be internally consistent but semantically false |
| Evidence trace validation | verify every used evidence/hypothesis/context reference, provenance link, lifecycle signal, and local closure | a Runtime can omit, substitute, or misclassify a source while retaining a valid-looking result |
| Semantic boundary validation | recompute unknown, revoked, stale, insufficient, contradiction, and competing-hypothesis outcomes | candidate status must not be silently upgraded |
| Authority boundary validation | independently establish absence of State/Snapshot/Context/Event/Fact mutation and Decision/Action/Observation execution | flags alone do not prove absence of prohibited behavior |
| Negative Guard extension | require static and execution dual proof for all frozen guards; add only separately approved Runtime-specific guards | a summary boolean is not a proof of every boundary |
| Determinism and historical evidence | compare approved repeated execution evidence and preserve canonical historical artifacts | a single passing result cannot establish stable behavior |

## Evidence Model

The future verifier must use Contract authority, immutable input fixtures or approved runtime test records, static source evidence, independently collected execution evidence, and a protected baseline/reference inventory. It must recompute expected semantics before comparing them to Runtime output.

It may read Runtime artifacts but may not call back into Runtime to obtain a passing answer, modify results, mutate State, or perform Decision/Action behavior.

## Extension Preconditions

1. Independent semantic recomputation is implemented and reviewed.
2. Every frozen Negative Guard has independently verifiable static and execution evidence.
3. Runtime input/output Contract versioning is separately approved without modifying the frozen DryRun Contract in place.
4. A boundary impact assessment proves A2 Context-only input and Reducer-only State mutation remain intact.
5. Human authorization explicitly permits the verifier-extension phase.

## Non-Goals

- No verifier implementation or execution in this phase.
- No weakening, removal, or relabeling of DryRun checks.
- No final phase decision authority for the verifier itself.
- No authorization of Runtime or any external model/capability.
