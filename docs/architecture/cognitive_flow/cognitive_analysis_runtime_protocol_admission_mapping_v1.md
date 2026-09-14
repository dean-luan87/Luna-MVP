# A3 Cognitive Analysis Runtime Protocol Admission Mapping v1

## Position

A3 Cognitive Analysis Runtime is a governed Capability, not an independent authorization system. Its governance chain is:

```text
Runtime Capability
        ↓
L1 Protocol Registry / Capability Registry
        ↓
L1 Admission Check
```

`runtime_authorized=false` remains unchanged. This mapping neither registers nor activates Runtime.

## Existing L1 Mapping

| Existing governance asset | A3 Runtime mapping | Current handling |
| --- | --- | --- |
| Capability Registry — `capabilities/midplatform/model_manager/registries/capability_registry_v1.json` | future record: `capability_id=cognitive_analysis_runtime`, `capability_type=cognitive_analysis`, owner `Cognitive Flow`, lifecycle `candidate` | registration required; not applied in this phase |
| Capability Manifest | no standalone L1 manifest asset was located in the direct governance scope | do not create a parallel A3 manifest; Registry-owned manifest/record is required in a future L1 phase |
| Model/Skill Admission Contract — `LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1` | declares A3 Runtime as a capability route subject to existing admission | referenced only; no model/skill/runtime admission is applied |
| Permission / Admission Contract — Permission & Admission Manager | `runtime_access_admission` is the governing request class | reference existing permission governance only; no runtime-specific permission model |
| Runtime Boundary Contract | A3 Boundary Contract plus L1 Runtime Boundary Contract preserve candidate-only output | no Runtime activation, State writeback, Fact/Decision/Action mutation |
| Output Contract — `LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1` | A3 output is Candidate-only with evidence trace, uncertainty, provenance, and flags | no Fact promotion |
| System Diagnostics Protocol | Permission/Admission Diagnostics and Protocol Manager Diagnostics carry health, contract drift, and validation status | diagnostic reference only; no runtime health process is started |
| Protocol Manager | Protocol Manager Registry Adapter, Admission Candidate, Boundary Checker, and Diagnostics are the L1 route | A3 maps references only; no protocol registration, load, dynamic binding, or activation |

## Admission Contract Mapping

The future A3 Capability registration must declare:

- **required_contracts**: Model/Skill Admission, Permission/Admission, L1 Input Candidate, L1 Output Candidate, Input/Output Symmetry, Protocol Traceability, and Runtime Boundary references.
- **input_schema**: Context Reference, Evidence References, Hypothesis References, and Analysis Question Reference only.
- **output_schema**: Analysis Result Candidate, Evidence Trace, Uncertainty, Warning Codes, Provenance, and Runtime Flags.
- **dependency**: A2 Context construction by reference, governed Evidence/Hypothesis references, Protocol Manager, Permission & Admission Manager, and independent validation.

## Boundary Mapping

Allowed output is candidate analysis only. Forbidden behavior includes Fact mutation, Decision mutation, Action execution, State writeback, Context/Snapshot/Event/Evidence mutation, and any Runtime-specific permission authority.

## Diagnostics Mapping

Future L1 diagnostics must surface Runtime health, Contract drift, validation status, permission/admission status, and boundary violations. A3 must report through those existing channels rather than create a second diagnostics protocol.
