# Dependency and Adapter Probe Planning v1

Planning-only phase for the Option B controlled execution dry run chain. No runtime execution, no segmentation execution, no dependency installation, no model download, no adapter import, no image read, and no fact output are permitted.

## 1. Dependency discovery strategy
- Treat dependency discovery as a metadata-only planning activity that maps each candidate to its expected dependency contract.
- Use the candidate registry, preflight outcome, and prior Option B admission policy to enumerate expected dependencies by candidate family.
- Record each dependency under a planned probe record with `dependency_name` and `dependency_expected` only.
- Do not attempt package resolution, installation, import, or runtime execution during planning.
- If dependency expectations are ambiguous or not explicitly confirmed, place the probe in a blocked planning state pending owner review.

## 2. Adapter discovery strategy
- Treat adapter discovery as a metadata-only planning activity that inventories the expected adapter contract for each candidate.
- Use candidate metadata and protocol alignment notes to identify the named adapter that would be required in a later execution stage.
- Record `adapter_name` and `adapter_present` as planned values only.
- Do not import, instantiate, or execute any runtime adapter during this phase.
- If adapter identity is not explicit or not admitted by policy, mark the probe as blocked pending owner review.

## 3. Rollback policy
- If dependency expectations or adapter expectations are unresolved, preserve the planning state and roll back to `no_execution_state`.
- No fallback to Option A is allowed during this planning phase.
- No model activation, no skill activation, and no registry mutation are permitted as part of rollback handling.

## 4. Abort policy
- Abort the future probe stage if any dependency expectation is unknown, any adapter is not explicitly admitted, or any runtime boundary is violated.
- Abort if owner approval is missing for a dependency or adapter exception.
- Abort if the candidate remains `candidate_only` or `not_fact` under the Option B policy boundary.

## 5. Owner approval gate
- Owner approval is required before any real dependency or adapter probe execution in the subsequent dry-run phase.
- Approval gates must be documented explicitly in the planning record and summary.
- Until approval is granted, the dependency probe remains blocked and non-executing.

## 6. Evidence requirements
- Evidence must be traceable to the scope, readiness, and preflight decisions already established for the Option B chain.
- Each planned probe record must include:
  - `candidate_id`
  - `dependency_name`
  - `dependency_expected`
  - `dependency_present`
  - `adapter_name`
  - `adapter_present`
  - `probe_status`
  - `candidate_only`
  - `not_fact`
- Evidence must remain metadata-only, non-executing, and reviewable without runtime side effects.

## 7. Runtime boundary
- `runtime_execution_allowed = false`
- `segmentation_execution_allowed = false`
- `dependency_probe_execution_allowed = false`
- `image_read_allowed = false`
- `model_download_allowed = false`
- `dependency_install_allowed = false`
- `active_model_selected = false`
- `active_skill_selected = false`
- `active_registry_update_allowed = false`
- `runtime_activation_allowed = false`
- `ocr_allowed = false`
- `vlm_allowed = false`
- `layout_allowed = false`
- `caption_allowed = false`
- `fact_admission_allowed = false`

This planning artifact is intentionally limited to document preparation for the subsequent dependency-and-adapter-probe dry-run phase.
