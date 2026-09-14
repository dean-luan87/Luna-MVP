# Luna Governance Core Architecture v1

## Purpose

This planning baseline places existing A3 Cognitive Analysis, Translation Layer, and Runtime Boundary governance assets into Luna's L0/L1 architecture. It defines governance responsibilities only; it does not implement a Governance Runtime, modify a Capability, register a Capability, or activate Runtime.

## Governance Layers

```text
L0 Constitution Layer
  immutable cognitive and authority principles
        ↓
L1 Protocol Governance Layer
  contract identity, input/output compatibility, traceability, boundary rules
        ↓
L1 Permission / Admission Layer
  request eligibility, permission reference, output admission eligibility
        ↓
L1 Capability Registry Layer
  capability identity, owner, lifecycle, declared dependencies
        ↓
L1 Diagnostics Layer
  contract drift, validation status, boundary violations, lifecycle signals
        ↓
Governed Capability Execution
```

## L0 Constitution Layer

L0 freezes principles that no Capability may override:

- Observation/Evidence/Model output is not Fact by default.
- Candidate is not Fact, Decision, Action, State, Memory, or Value judgment.
- Reducer remains the only Field State mutation authority.
- External provider/model identity is provenance, never a Cognitive Entity by itself.
- Hive, Experience, Cognitive Analysis, and external models cannot bypass governed admission or write State directly.

## L1 Protocol Governance Layer

L1 owns Contract references and compatibility rules. For A3, this includes candidate-only input/output symmetry, allowed primitive types, required evidence/context/provenance/trace references, stable Negative Guard inventory, and serializer-compatible output evidence. Protocol Governance does not execute a Capability or create a new A3-specific protocol authority.

## L1 Permission / Admission Layer

L1 owns whether a future request may proceed and whether a future output may enter a separately governed next layer. It references the existing Permission & Admission route; no Capability may invent a runtime-specific permission model. A candidate validation result is not an admission grant.

## L1 Capability Registry Layer

L1 owns Capability identity, owner, lifecycle, dependencies, and manifest/record governance. A3 Translation and Runtime mappings remain candidate/reference-only until a separately authorized L1 registration phase writes the existing Registry.

## L1 Diagnostics Layer

L1 owns reporting of contract drift, validation outcomes, permission/admission status, boundary violations, and lifecycle status through the existing Protocol Manager and Permission/Admission diagnostics route. It does not perform a health Runtime in this phase.

## Current A3 Placement

Negative Guards and forbidden operations are L0-derived L1 boundary rules. Runtime flags are serialized diagnostic evidence. Candidate/Fact separation is a constitutional principle enforced through L1 Contract and Admission checks. Provenance and trace are L1 Protocol Traceability requirements. No A3 asset becomes an independent Registry, Permission Manager, Admission system, or Diagnostics system.

