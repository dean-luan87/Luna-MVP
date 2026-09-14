# Current World Representation — A2 Final Asset Index v1

## 1. Architecture and planning documents

| Asset | Status | Purpose | Runtime asset |
| --- | --- | --- | --- |
| `current_cognitive_context_architecture_plan_v1.md` | frozen planning | defines Context position and inputs | no |
| `minimum_sufficient_field_representation_v1.md` | frozen planning | defines recoverable selection scope | no |
| `current_cognitive_context_permission_matrix_v1.md` | frozen planning | freezes Context authority | no |
| `current_cognitive_context_object_contract_v1.md` | frozen planning | specifies Context object shapes | no |
| `current_world_representation_system_architecture_v1.md` | frozen planning | defines CWR system/layers | no |
| `current_world_representation_integration_contract_v1.md` | frozen planning | defines CWR handoffs | no |
| `current_world_representation_permission_matrix_v1.md` | frozen planning | freezes cross-module authority | no |
| `current_world_representation_envelope_contract_v1.md` | frozen planning | defines reference-only Envelope | no |
| `current_world_representation_controlled_dryrun_plan_v1.md` | frozen planning | reserves six-case DryRun | no |
| `current_world_representation_post_review_v1.md` | completed review | records A2.9 review evidence | no |
| `current_world_representation_capability_status_matrix_v1.md` | completed review | records capability status | no |
| `current_world_representation_boundary_register_v1.md` | completed review | freezes CWR boundaries | no |
| `current_world_representation_regression_baseline_v1.md` | completed review | freezes A2.8 baseline expectations | no |
| `current_world_representation_closure_go_no_go_pack_v1.md` | completed review | records closure candidate/risk posture | no |

## 2. Core Python and contract surfaces

| Asset group | Status | Purpose | Runtime asset |
| --- | --- | --- |
| `capabilities/cognitive_flow/field_kernel/core/` | existing skeleton | Identity, Unit, Relation, State, Snapshot surfaces | no — fixture reuse only |
| `capabilities/cognitive_flow/field_kernel/temporal_evolution/` | existing skeleton | State Version, Transition, History, lifecycle surfaces | no — fixture reuse only |
| `capabilities/cognitive_flow/current_cognitive_context/` | A2.6 skeleton | derived Context, records, gaps, sufficiency, lifecycle | no — fixture reuse only |
| `capabilities/midplatform/core/field_state_reducer/` | existing authority | Reducer input/output and mutation-authority contract | no — not invoked by A2.8 |
| `capabilities/midplatform/core/field_state_read_model/` | existing query boundary | read query/result surfaces | no — not invoked by A2.8 |
| `capabilities/cognitive_flow/current_world_representation_integration/integration_types_v1.py` | A2.8 | fixed DryRun result object | no |
| `capabilities/cognitive_flow/current_world_representation_integration/integration_fixture_v1.py` | A2.8 | six deterministic fixtures | no |
| `capabilities/cognitive_flow/current_world_representation_integration/current_world_representation_envelope_v1.py` | A2.8 | read-only Envelope object | no |
| `capabilities/cognitive_flow/current_world_representation_integration/integration_dryrun_v1.py` | A2.8 | fixed in-memory chain assembly | no |
| `capabilities/cognitive_flow/current_world_representation_integration/integration_validators_v1.py` | A2.8 | result/static negative validators | no |
| `capabilities/cognitive_flow/current_world_representation_integration/contract_v1.json` | A2.8 | DryRun/Envelope contract | no |

## 3. Runner, verifier, and evidence outputs

| Asset | Status | Purpose | Runtime asset |
| --- | --- | --- | --- |
| `runner/run_current_world_representation_integration_dryrun_v1.py` | A2.8 controlled tool | writes fixed fixture JSON outputs | no |
| `verifier/verify_current_world_representation_integration_dryrun_v1.py` | A2.8 component verifier | validates fixture results; not final-phase verifier | no |
| `docs/current_world_representation_integration_dryrun_implementation_v1.md` | A2.8 documentation | actual asset mapping and DryRun limits | no |
| `docs/current_world_representation_integration_dryrun_runbook_v1.md` | A2.8 documentation | controlled command/output instructions | no |
| `_eval_out/current_world_representation_integration_dryrun_v1_smoke_v0/` | effective evidence output | result, case matrix, verification JSON | no — fixture output only |

The index contains no production asset, real runtime activation, or authorization to invoke existing Reducer/Read Model runtime code.
