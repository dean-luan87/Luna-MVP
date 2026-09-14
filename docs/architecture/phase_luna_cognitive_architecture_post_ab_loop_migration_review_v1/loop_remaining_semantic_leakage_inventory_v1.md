# Loop Remaining Semantic Leakage Inventory

| Location / behavior | Finding | Classification | Reason |
|---|---|---|---|
| `cognitive_loop_continuity_candidate_engine_v1.py::_local_disposition` | derives `SUFFICIENT`, `RECONSIDER`, `DEFER`, `INSUFFICIENT` from fixture/lifecycle | REAL LEAKAGE | Loop integration code constructs semantic conclusions rather than receiving A refs |
| same engine `_continuity_and_resume` | selects `KEEP`, `REPLAN`, `SUPERSEDE`, `WAITING` and creates Reconsideration candidate | REAL LEAKAGE | Resume semantic decision is supposed to be A/Brain-owned; Loop should store command/result |
| same engine `_capabilities_and_growth` | assigns candidate path status for stale/duplicate/diminishing/resource cases | AMBIGUOUS | It is a controlled growth fixture, but status resembles capability/cognition judgment |
| lifecycle closure engine closure assessment | exposes local suggestion and closure candidate while acceptance is Brain-governed | COMPATIBILITY_ONLY | Assessment is explicitly non-authoritative and lifecycle remains OPEN until acceptance |
| lifecycle closure engine `CLOSURE_DISPOSITION_BY_REASON` | maps closure reason to disposition | COMPATIBILITY_ONLY | Candidate mapping is explicit; closure decision owner is Brain/Cognitive Flow governance |
| Loop mechanical command engine | applies supplied commands and returns mechanical refs | NONE | Mechanical responsibility is within target Loop boundary |
| A→Loop adapter | maps A semantic candidates to mechanical commands | NONE | Adapter does not infer semantic values |

## Review result

The new authority/grant bridge prevents semantic Loop authority at the controlled boundary, but the older Loop continuity candidate engine still contains semantic construction logic. This is a P0 architecture cleanup before claiming the Loop engine is purely mechanical; it does not justify modifying it in this review.
