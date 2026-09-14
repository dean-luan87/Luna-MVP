# A2 Current World Representation Module Summary v1

## Purpose

A2 is the **Current World Representation (CWR) System**. It makes governed
Field representation usable for later cognition without creating a second
state store or a parallel mutation path. It reads governed Field State and
temporal representation, derives Field Snapshot views, and assembles a
task-scoped, minimum-sufficient, read-only Current Cognitive Context.

## Actual asset mapping

| Concern | Existing asset entry points | A2 role |
| --- | --- | --- |
| Context skeleton | `capabilities/cognitive_flow/current_cognitive_context/context_types_v1.py`, `context_builder_v1.py`, `current_cognitive_context_v1.py` | Read-only Context object and controlled assembly. |
| Context records | `context_inputs_v1.py`, `context_records_v1.py`, `information_gap_v1.py`, `context_sufficiency_v1.py`, `context_lifecycle_v1.py` | Inclusion/exclusion records, gaps, sufficiency, and lifecycle representation. |
| CWR fixture integration | `capabilities/cognitive_flow/current_world_representation_integration/current_world_representation_envelope_v1.py`, `integration_fixture_v1.py`, `integration_dryrun_v1.py` | Fixture-only envelope, integration cases, and controlled DryRun evidence. |
| Source representation | A1 Field State, State Version, Transition Record, History Projection, Field Snapshot, and governed Read Model assets | Read-only sources for CWR assembly. |

Primary architecture entries are
`current_world_representation_system_architecture_v1.md`,
`current_world_representation_integration_contract_v1.md`,
`current_world_representation_envelope_contract_v1.md`, and
`current_world_representation_capability_status_matrix_v1.md` under
`docs/architecture/cognitive_flow/`.

## Responsibilities

A2 is responsible for reading and organizing:

- governed Field State and temporal organization;
- Field Snapshot and Read Model views;
- a task-scoped Current Cognitive Context;
- selection inclusion and exclusion records;
- Information Gap and Context Sufficiency records;
- Context lifecycle and multi-context representation;
- a read-only Current World Representation Envelope.

Its allowed inputs are A1 state, version, transition, history, snapshot, and
Read Model representations. Its outputs are Context, selection
inclusion/exclusion records, gap and sufficiency records, and the read-only
Envelope.

## Required distinctions

- **State != Snapshot**: State is a governed current description; Snapshot is
  a derived read view.
- **Snapshot != Context**: a Context selects the minimum sufficient slice for
  a task and records what it includes or excludes.
- **Context != Hypothesis**: Context contains governed references and explicit
  uncertainty, not an explanation.
- **Envelope != Field State**: an Envelope carries read-only representation
  references and is never an authoritative state source.
- **CWR != World Understanding**: CWR reports what Luna can currently read and
  organize; it does not explain why the world is this way or what to do.

## Authority and A3 boundary

A2 has no Field State writeback authority. Any information that could affect
Field State must take the only lawful route:

```text
Event Candidate -> Admission -> Field State Reducer -> Field State
```

A3 Cognitive Analysis may read Current Cognitive Context. It may not turn a
Context, Snapshot, Envelope, or Read Model result into a writable state input.

## Maturity record

| Area | Current maturity |
| --- | --- |
| Architecture | Complete. |
| Contract | Complete. |
| Controlled skeleton | Complete. |
| Fixture DryRun | Complete. |
| Runtime integration | Incomplete. |
| Production readiness | False. |

No runtime system, live Reducer/Read Model integration, database, network, or
model execution is implied by the fixture work.
