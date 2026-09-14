# Luna Governance Asset Discovery Report v1

## Audit posture

This is a read-only discovery snapshot after `LUNA_CORE_ARCHITECTURE_BASELINE_READY`. No existing code, directory, or historical asset was modified, moved, renamed, merged, or deleted.

## Scan scope

| Root | Files scanned (excluding `__pycache__` and `.pyc`) |
|---|---:|
| `capabilities/` | 5,567 |
| `docs/architecture/` | 6,071 |
| `tools/` | 2,322 |
| Total | 13,960 |

Path-name keyword discovery produced heuristic candidate counts:

| Candidate family | Count |
|---|---:|
| Model management | 704 |
| Capability governance | 70 |
| Provider | 346 |
| Admission | 219 |
| Calibration / benchmark / baseline / drift | 167 |

Counts are discovery signals, not claims that every matching file owns the corresponding concept.

## Findings

### Model Manager

A substantial implementation and governance surface already exists at `capabilities/midplatform/model_manager/` (519 non-cache files). It includes model and capability registries, lifecycle policies/processors, admission policies/processors, resource/health diagnostics, provider adapters, dry-run surfaces, and integration plans. The active baseline is `capabilities/registry/baselines/model_manager_module_baseline_v1.json`, which explicitly marks `luna.model_manager` as `active` and forbids real inference, provider runtime calls, model training, state mutation, fact admission, and production dispatch.

### Capability Registry

There is a canonical-looking registry plane under `capabilities/registry/`, including `luna_capability_registry_v1.json`, lifecycle registry, manifests, schemas, dependency map, and module baselines. A second capability registry exists under `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`; it is a duplicate-owner candidate requiring mapping, not deletion.

### Admission

Admission is present at several scopes: model admission governance, capability registry/lifecycle admission, field/provider admission, recognition-model admission planning, and runtime admission dry-runs. The discovery result is therefore “present but distributed”; the target mapping must distinguish Model Admission, Capability Admission, Provider Admission, and Runtime Admission.

### Calibration

Calibration and performance evidence exist as capability calibration standards, model benchmark records, OCR/provider benchmark registries, baseline manifests, drift/readiness documents, and evaluation tools. The assets are rich but distributed across governance, evaluation, model manager, and field-understanding surfaces. No consolidation was performed in this phase.

### Provider

Provider adapters and provider registries exist for vision, OCR, voice, emotion interfaces, spatial evidence, Qwen-VL, and local model runtime. They are mapped as Capability/Provider boundary candidates; no provider is granted Brain, Goal, Reality, or Memory authority.

## Ownership conclusion

The project already has most of the requested governance assets. The primary risk is not absence but parallel surfaces and historical layering. The immediate engineering action should be canonical ownership mapping and duplicate resolution review, not another Model Manager or Capability Registry implementation.

## V2 scope guard

This phase does not authorize code changes, file moves, deletions, renames, new runtime modules, provider calls, model calls, hardware access, or action execution.
