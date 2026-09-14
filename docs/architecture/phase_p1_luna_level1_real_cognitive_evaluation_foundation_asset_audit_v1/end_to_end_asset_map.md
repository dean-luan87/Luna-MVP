# End-to-End Asset Map

Target chain:

`Real Dataset / World Sample → Dataset Registry → layered GT → Cognitive Test Case → A-Route cognition → White-box Trace/Profile → Evaluation Result → durable archive → baseline/comparison → Knowledge/Experience candidate`

| Stage | Asset / location | Status | Runtime reachability | Evidence-based finding |
|---|---|---|---|---|
| World source | `capabilities/evaluation/dataset_registry/types_v1.py`, `registry_declaration_v1.json` | Canonical foundation | No real data registered | Registry is explicit and evaluation-only; declaration is `UNREGISTERED_FOUNDATION`. |
| Explicit registration | `dataset_registry/registration_v1.py` | Implemented | Registration function exists | Requires explicit caller input; rejects automatic promotion from `_tmp_eval_inputs`, `_tmp_eval_out`, `_eval_out`; does not scan or load media. |
| World Sample | `DatasetSampleManifestV1` | Canonical type | Composition-ready | Carries media, provenance, source versions, hash, annotation/GT refs, conditions and case refs. |
| World/Observation GT | `AnnotationGroundTruthRefV1`; Level-1 GT refs | Partial | Candidate/reference only | A GT reference is available, but no integrated real sample annotation admission or layered GT persistence was found. |
| Cognitive Test Case | `level1_field_cognition_suite/composition_v1.py`, `types_v1.py` | Implemented composition | Not persisted/integrated | Composes from a supplied sample; no registry membership or real sample store is enforced by composition. |
| Category corpus | `level1_field_cognition_suite/corpus_v1.py` | Declarative | Synthetic declaration | Sixteen diagnostic categories are present; the manifest intentionally starts with zero datasets/samples. |
| Capability governance | Midplatform capability registries/bindings | Canonical external boundary | Narrow real Roboflow path evidenced | Capability/model/provider/runtime records exist; this audit does not treat them as cognitive execution proof. |
| Observation/Evidence | FPO real vision evidence types and Roboflow PoC | Partial / narrow real precedent | One provider smoke path | Candidate evidence and Gateway handoff are observable for RF-DETR; general A-Route connection is not evidenced. |
| A-Route cognition | `cognitive_state_formation`, `a_route_orchestration`, active observation control | Controlled/synthetic | Not real connected | Engines and candidates are explicitly synthetic/candidate-only or controlled. |
| White-box | `a_route_cognitive_whitebox_foundation` | Canonical observation foundation | Synthetic trace only | V1 trace/profile/gap contracts and fixtures exist; runtime collection is absent. |
| Result envelope | `evaluation/common/evaluation_report_schema_v0.py`; Model Test Lens envelope | Precedent | Artifact-oriented | Common report is evaluation-only but explicitly not whitebox; Model Test Lens envelope is model-centered. |
| Evidence archive | `_eval_out`, `_tmp_eval_out`, TestBoard | Generated/protected evidence | File artifacts | No canonical durable archive contract was found. TestBoard protects artifacts but is not the evaluation source-of-truth. |
| Baseline/comparison | Model evaluation engine and dual-route candidates | Planning/Plane B precedent | No general cognitive comparison | Existing model comparison is candidate-only and does not preserve a same-case Luna-version history. |
| Knowledge/Experience | Memory/Experience/Learning assets | Boundary only | Not integrated | No safe evaluation-archive-to-candidate extraction path was found; automatic promotion is forbidden. |

## Overall readiness

The existing pieces can support a future bounded implementation, but the chain is not currently proven end-to-end for one real registered World Sample entering a real Luna A-Route cognition and becoming a durable, reproducible baseline.

