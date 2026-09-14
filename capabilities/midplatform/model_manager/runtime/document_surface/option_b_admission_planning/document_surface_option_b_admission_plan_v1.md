# Option B Dependency & Model Candidate Admission Planning v1

Planning-only phase for `segmentation_candidate_route`. No active model, no download, no install, no execution.

Pipeline: **candidate → admission → preflight → controlled execution**

## Answers

1. **Candidate model types:** Family A (classical/lightweight), B (general lightweight seg), C (document-specific), D (depth/geometric assisted)
2. **Registry fields:** model_candidate_id, family_type, capability, output types, dependency/weight/license profiles, admission_status_candidate, active_status=false
3. **Dependency checks:** python_package, model_weight, runtime_binary, hardware_requirement — all install/download/execution blocked in planning
4. **No-download guarantee:** policy flags + admission_status + failure_output=dependency_not_admitted_candidate
5. **Output contract:** allowed 6 candidate types; forbidden OCR/fact/layout/caption; wrapper required for text-default models
6. **Preflight:** 12 checks before any controlled execution
7. **Block conditions:** license_unknown, weight too large, uncontrolled download, semantic fact default output, etc.
