# Luna Midplatform Protocol Canonical Standard Planning v1

This phase defines unified protocol standards for Luna midplatform before continuing module development. It does not execute protocol runtime, migrate existing protocols, or integrate whitebox runtime.

## Scope

- Phase: `Phase-Midplatform-Protocol-Canonical-Standard-Planning-v1-001`
- Output: Protocol canonical standard plan, numbering/error-code standards, shared code design, existing protocol classification registry.

## Protocol Definition

- EN: `Protocol = Constitution-Guided Process Contract`
- ZH: `协议 = 宪法约束下的流程契约`

## Layer Model

- **L0**: Safety / Constitution Layer
- **L1**: Midplatform System Protocol Layer (cross-module)
- **L2**: Module Protocol Layer (inherits L1)
- **L3**: Capability / Adapter Layer

## Numbering Format

`LUNA-PROTO-{LAYER}-{DOMAIN}-{NAME}-V{VERSION}`

## Error Code Format

`{PROTOCOL_ID}::{ERROR_CLASS}-{NUMBER}`

Error classes: CONST, PROC, IFACE, ASSIM, EVID, STATE, AUTH, TTL, WB, HEALTH

## Shared Code Location

`capabilities/midplatform/protocols/` — pure schema / helper / contract, no runtime side effects.

## Boundaries

- `protocol_standard_planning ≠ protocol_runtime_execution`
- `protocol_code_template ≠ runtime_protocol_engine`
- `whitebox_binding_contract ≠ whitebox_runtime_integration`
- `candidate_protocol ≠ active_protocol_runtime`

## Next Phases (not auto-started)

1. Primary: `Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001`
2. Alt: `Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001`
