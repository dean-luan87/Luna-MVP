# Cognitive Governance Plane Architecture v1

## Purpose

The Cognitive Governance Plane is Luna's autonomous nervous-system-like
management layer. It manages how the system is registered, admitted, authorized,
diagnosed, resourced, run, and changed. It does not think, decide goals, or
become a second Brain.

```text
Luna Cognitive Constitution
          ↓
Cognitive Governance Plane
---------------------------------------------
Protocol Governance
Registry Plane
Admission Governance
Authority Governance
Diagnostics Governance
Resource Governance
Runtime Governance
Change Governance
---------------------------------------------
          ↓
Cognitive Runtime / Systems
          ↓
Field / Reality / Attention / Capability
```

## Component placement

- **Constitution**: highest constraint; says what must not be violated. It
  does not register, schedule, or execute.
- **Protocol Manager**: protocol lifecycle, version, compatibility, deprecation,
  and migration review.
- **Registry Plane**: Capability Registry, Model Registry, Hardware Registry,
  Field Registry, and Authority Registry; answers “what exists”.
- **Admission**: entry gate; answers “may this object enter”.
- **Authority Governance**: who may create, approve, modify, run, observe, or
  revoke an object.
- **Diagnostics**: detects anomaly, drift, degradation, and protocol errors;
  emits Diagnostic Candidate, never Action.
- **Resource Governance**: manages compute, energy, memory, time, network, and
  sensor budgets in coordination with Attention.
- **Runtime Governance**: manages Process, Tick, Wake-up, lifecycle, and
  scheduling mechanics; it has no cognition authority.

## Unified governance lifecycle

All governed objects use:

```text
Draft → Review → Admission → Active → Deprecated → Archived
```

This lifecycle applies to Protocol, Model, Capability, Hardware, Field, and
Authority entries. Admission is not execution. Diagnostics and Change
Governance may create candidates for pause, rollback, or deprecation.

## Non-goals

The plane does not modify Reality directly, create Goals, make Decisions,
execute Actions, interpret Evidence, or replace Brain/A Route. No Model Runtime,
Provider Runtime, OCR, SLAM, Hardware Runtime, Action, B, Emotion, or Role is
implemented in this architecture phase.

The plane does not create Goals and does not make Decisions. No Provider
Runtime, No OCR, No SLAM, No Hardware, No Action, No B, No Emotion, and No Role
are implemented.

No Provider Runtime is implemented.
