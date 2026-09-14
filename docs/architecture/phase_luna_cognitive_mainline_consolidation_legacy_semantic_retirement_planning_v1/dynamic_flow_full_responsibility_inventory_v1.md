# Dynamic Flow full responsibility inventory

| Current behavior | Current location | Current callers/fixtures | Target disposition | Replacement / removal precondition |
|---|---|---|---|---|
| Input candidate/plan validation | `cognitive_dynamic_loop_engine_v1.py::_validate_input` | Dynamic Flow Runner/Verifier, real-input adapters | KEEP_AS_SHARED_COMPUTATION | Preserve candidate-only and non-binding plan guards |
| State-version suffix advancement | `_advance_state_version` | Dynamic Flow scenarios and real-input integration | KEEP_AS_SHARED_COMPUTATION | A supplies semantic source version; shared transition builder remains valid |
| Need lookup | `_need_map` | Dynamic Flow fixtures | KEEP_AS_SHARED_COMPUTATION | Lookup is not selection authority |
| Next Need selection from plan/non-plan refs | `_select_next_need`, `run_case` | A03/B/C/D cases, A compatibility wrapper | MOVE_TO_A | A bridge produces accepted Need decision and replacement Need |
| Reconsideration object construction | `_reconsideration` | B/C/D fixtures, A compatibility wrapper | COMPATIBILITY_ONLY | A/B decision refs must replace semantic construction |
| Sufficiency interpretation | `run_case` evidence branches | A03/A04/D/E fixtures, real capability trial | MOVE_TO_A | A owns local sufficiency; old output remains compatibility source |
| Next-step disposition | `run_case` | all Dynamic Flow verifiers and A wrapper | MOVE_TO_A | A NextStep decision maps to Loop command |
| STOP_SUFFICIENT termination bookkeeping | `run_case` | A03/A04/D06/E01–E06 | KEEP_AS_SHARED_COMPUTATION + MOVE_DECISION_OUT | A emits STOP; Loop mechanically closes; fixture migration required |
| Capability availability interpretation | `run_case` | C01–C06 | MOVE_TO_A / CAPABILITY GOVERNANCE | Scope/Resolution/Capability result enters A reassessment |
| Execution outcome vs requirement satisfaction mapping | `run_case` | D01/D05/D06 | MOVE_TO_A | A evaluates separated outcome fields |
| Evidence update acceptance by state version | `run_case` | state/reconsideration cases | KEEP_AS_SHARED_COMPUTATION | Accepted/ignored evidence record may remain mechanical |
| Hypothesis invalidation and replacement refs | `run_case` | B01–B06 | MOVE_TO_A | A owns hypothesis interpretation; Flow carries refs |
| Provisional plan and non-materialized refs | input/output types and `run_case` | plan/early-stop fixtures | KEEP_AS_SHARED_COMPUTATION | Plan remains candidate-only and non-binding |
| Stale Requirement detection | final state comparison | F-series and capability integration | CONVERT_TO_LOOP_MECHANICAL + CAPABILITY REASSESSMENT | A/Capability provides stale disposition; Loop blocks direct invocation |
| Invocation eligibility filtering | final output | real capability trial | MOVE_TO_A / CAPABILITY GOVERNANCE | Resolution/admission owns readiness; A requests only current Need |
| Trace/provenance assembly | output construction | all Dynamic Flow tests | KEEP_AS_SHARED_COMPUTATION | Later shared trace protocol may consolidate helpers |
| Lifecycle/reference bookkeeping | output fields | Dynamic Flow and Loop integrations | CONVERT_TO_LOOP_MECHANICAL | Use mechanical command/return contract |

No item is safe for removal merely because a compatibility wrapper exists.

