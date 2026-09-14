# Cognitive Concept Layer DryRun Validation Matrix v1

| Validation area | Required evidence | Failure condition | Validation owner |
| --- | --- | --- | --- |
| Schema | Six serialized candidates with required fields | Missing or empty required field | Independent verifier |
| Mapping | Each fixed case has its expected Concept type | Case absent or type mismatch | Independent verifier |
| Candidate boundary | `candidate_only=true`, `fact_status=not_fact` | Fact or authority-bearing field present | Independent verifier |
| Provenance | Source, Translation, capability, and matching trace references | Broken trace chain | Independent verifier |
| Semantic boundary | Candidate has no factual, decision, action, or state authority | Boundary flag or forbidden field fails | Independent verifier |
| Negative guards | No runtime/provider/state/memory/learning/language execution flags | Any forbidden flag is true | Independent verifier |
| Determinism | Canonical JSON from two fixed executions is identical | Run outputs differ | Independent verifier |

The matrix assesses only fixed serialized evidence. It does not validate concept truth, world understanding, or a real semantic inference process.
