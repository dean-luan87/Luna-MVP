# Luna Capability Catalog v1

## Directory Reuse Decision

This repository has many domain-specific registry and manifest assets (for example under model governance, vision/ocr provider registries, and architecture governance docs), but no unified capability-module registry foundation.

This catalog uses:

- human-readable architecture docs: docs/architecture/capability_registry/
- machine-readable registry assets: capabilities/registry/

No existing runtime behavior modules were modified.

## Completed Modules

| Capability | Capability ID | Domain | Responsibility | Status | Version | Dependencies | Input | Output | Runner | Diagnostics | Trace | Replay | Current Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Field State Reducer | luna.field_state_reducer | midplatform.field_state | Reduce admitted field events into field state candidate and projection candidate under governance boundaries. | functional_module_ready | module v1 / api v1 | none | admitted events + state snapshots | candidate + projection + diagnostics + trace + replay key | tools/evaluation/midplatform/run_field_state_reducer_module_integration_v1.py | yes | yes | yes | Not production-enabled by default; candidate-only boundary. |
| Task Manager | luna.task_manager | midplatform.task_orchestration | Coordinate task orchestration lifecycle, dependency routing, interruption/recovery candidates, and governed handoff through consolidated module API. | functional_module_ready | module v1 / api v1 | luna.field_state_reducer (optional), luna.model_manager (optional) | task + governance handoff signals | task lifecycle/result candidates + diagnostics + trace + replay key | tools/evaluation/midplatform/run_task_manager_module_integration_v1.py | yes | yes | yes | Candidate-only boundary; no direct runtime dispatch or state mutation. |
| Model Manager | luna.model_manager | midplatform.model_governance | Govern model admission, capability-first routing, ownership/resource evaluation, and lifecycle planning in controlled scope. | functional_module_ready | module v1 / api v1 | luna.permission_and_admission_manager (optional), luna.system_diagnostics (optional) | model request + ownership/resource/version snapshots | model selection/lifecycle/fallback candidates + diagnostics + trace + replay key | tools/evaluation/midplatform/run_model_manager_module_integration_v1.py | yes | yes | yes | Candidate-only boundary; no direct runtime execution or state mutation. |
| Permission And Admission Manager | luna.permission_and_admission_manager | governance.permission_admission | Resolve candidate-only permission and admission eligibility across evidence/provenance/consent/ownership/authority/risk/conflict/revocation checks. | functional_module_ready | module v1 / api v1 | none | admission request candidates + subject/resource/policy/evidence/provenance/risk snapshots | admission decision candidates + rejection reasons + diagnostics + trace + replay | tools/evaluation/midplatform/run_permission_and_admission_manager_module_integration_v1.py | yes | yes | yes | 20-case integration pass with deterministic replay and strict non-execution boundary. |
| Observation Manager | luna.observation_manager | midplatform.observation | Organize unified candidate-only observation requests, context binding, vision/OCR evidence association, and admission handoff generation. | functional_module_ready | module v1 / api v1 | luna.task_manager (optional), luna.vision_manager (optional), luna.ocr_manager (optional), luna.permission_and_admission_manager (optional), luna.protocol_manager (optional) | observation request candidates + task/scene/attention/region/temporal contexts | observation candidate + admission handoff candidate + diagnostics + trace + replay | tools/evaluation/midplatform/run_observation_manager_module_integration_v1.py | yes | yes | yes | 20-case integration pass with deterministic replay and boundary-preserved candidate-only outputs. |
| Navigation Manager | luna.navigation_manager | midplatform.navigation | Assemble candidate-only navigation request intake, route/progress/evidence fusion, deviation/risk governance, guidance/arrival/task/speech handoff outputs. | functional_module_ready | module v1 / api v1 | luna.task_manager (optional), luna.observation_manager (optional), luna.field_state_reducer (optional), luna.vision_manager (optional), luna.ocr_manager (optional), luna.permission_and_admission_manager (optional), luna.protocol_manager (optional), luna.speech_manager (optional) | navigation request candidates + route/progress/evidence/context snapshots | route/deviation/risk/guidance/arrival + task/speech handoff candidates + diagnostics + trace + replay | tools/evaluation/midplatform/run_navigation_manager_module_integration_v1.py | yes | yes | yes | 20-case integration pass with deterministic replay and strict boundary-preserved candidate-only outputs. |

## Building Modules

| Capability | Capability ID | Domain | Responsibility | Status | Version | Dependencies | Input | Output | Runner | Diagnostics | Trace | Replay | Current Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Vision Manager | luna.vision_manager | perception.vision | Candidate-only visual signal/evidence packaging and model handoff candidate assembly. | functional_module_ready | module v1 / api v1 | none | task context plus visual request signals | vision candidate packages plus diagnostics and replay refs | tools/evaluation/midplatform/run_vision_manager_module_integration_v1.py | yes | yes | yes | 18-case integration pass with boundary-preserved candidate-only outputs and deterministic replay. |
| OCR Manager | luna.ocr_manager | perception.ocr | Candidate-only OCR module assembly: request governance, engine capability handoff candidate, evidence envelope, diagnostics, and deterministic trace/replay. | functional_module_ready | module v1 / api v1 | luna.vision_manager (optional), luna.model_manager (optional), luna.permission_and_admission_manager (optional) | OCR request + source/frame refs + region/human correction candidates | structured OCR evidence envelope + diagnostics + trace + replay | tools/evaluation/midplatform/run_ocr_manager_module_integration_v1.py | yes | yes | yes | 18-case integration pass with raw evidence preserved and boundary flags fully clean. |
| Speech Manager | luna.speech_manager | voice.speech | Manage voice and speech guidance pathways under governance controls. | functional_module_ready | module v1 / api v1 | luna.model_manager | dialogue/tts requests and speech text candidates | speech output plane candidates, diagnostics, trace, and replay | tools/evaluation/midplatform/run_speech_manager_module_integration_v1.py | yes | yes | yes | Candidate-only boundary; no real ASR/TTS/VOP runtime. |
| Protocol Manager | luna.protocol_manager | midplatform.protocols | Manage candidate-only protocol registry/checking, lifecycle, compatibility, admission, and impact analysis for midplatform flows. | functional_module_ready | module v1 / api v1 | none | protocol operation request candidates + version/governance snapshots | protocol governance outcomes + diagnostics + trace + replay | tools/evaluation/midplatform/run_protocol_manager_module_integration_v1.py | yes | yes | yes | 18-case integration pass with deterministic replay and boundary-preserved candidate-only outputs. |

## Skeleton Modules

| Capability | Capability ID | Domain | Responsibility | Status | Version | Dependencies | Input | Output | Runner | Diagnostics | Trace | Replay | Current Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Memory Manager | luna.memory_manager | midplatform.memory | Provide governed working memory skeleton services. | skeleton_ready | module v1 / api v1 | none | planned memory operations | planned memory operation results | none | no | no | no | Skeleton file only; no integration runner. |
| System Diagnostics | luna.system_diagnostics | system_health | Provide system health governance and diagnostics framing. | skeleton_ready | module v1 / api v1 | none | system health status | diagnostics outputs | none | yes | no | no | No standalone module API or integration runner. |

## Planned Modules

| Capability | Capability ID | Domain | Responsibility | Status | Version | Dependencies | Input | Output | Runner | Diagnostics | Trace | Replay | Current Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Field Read Model | luna.field_read_model | midplatform.field_read_model | Serve field-state read projection outputs. | planned | module v1 / api v1 | luna.field_state_reducer | planned | planned | none | no | no | no | No dedicated implementation or runner found. |
| Action Manager | luna.action_manager | execution.action | Manage action planning and release governance boundaries. | planned | module v1 / api v1 | none | planned | planned | none | no | no | no | No dedicated implementation path found in current assets. |

## Internal Components (Not Top-Level Capability Modules)

Inside Field State Reducer, these are internal components and remain non-top-level:

- policy_evaluation
- policy_selection
- state_reduction
- trace_builder
- replay_builder
