# Intent Architecture Risk Review v1

Status: PLANNING_CANDIDATE

| Risk | Failure mode | Planning control | Blocking condition |
|---|---|---|---|
| Parallel Intent system | New assets silently replace the frozen Intent Governance owner | Candidate-only assets and explicit existing-asset mapping | A second active owner or writer is required |
| Classifier collapse | Intent becomes a label predicted from text | Preserve formation trace, uncertainty, alternatives, and source-owned references | Intent can only be represented as a class label |
| Potential Intent ownership drift | Context or PCN emits Intent | Potential Intent remains owned by Intent Governance | Existing owner must create final Intent |
| PCN activation conflation | Activation, strong links, or repeated links are treated as Intent | Explicit non-equivalence guards | PCN contract mandates Intent output |
| Field/Role pressure conflation | Obligation or pressure is asserted as subjective direction | Treat both as influence references | Existing owner mandates equivalence |
| Emotion ownership drift | Emotion creates or changes Intent directly | Emotion influence candidate only; no cross-write | Emotion runtime is required for planning |
| Memory ownership drift | Recall or experience pattern becomes Intent | Reference-only influence; Intent formation stays governed | Memory must write Intent state |
| Single-winner collapse | Competition deletes alternatives | Coexistence, suppression, dormancy, reactivation retained | Downstream requires destructive winner selection |
| Dominance/Decision collapse | Temporary dominance is treated as an approved choice | Dominance remains candidate state with release conditions | Action requires dominance as authorization |
| Threshold pseudo-truth | A score automatically promotes or proves Intent | No fixed score threshold; evidence and provenance remain explicit | Existing active contract requires threshold truth |
| Carryover/Context merge | Persistent Intent is made part of Mental Field Continuity | Related references, independent owners | Carryover requires Context mutation |
| Long-term Intent/Identity merge | Persistent direction rewrites Self identity | Self influence and future feedback are candidate-only | Identity mutation is required |
| Resource data loss | Low resources delete sources or dormant Intent | Only reduce active projection/expansion breadth | Resource controller requires deletion |
| Causal leakage | Intent layer produces explanations or counterfactual conclusions | Handoff references only | Causal result is required as Intent output |
| Task/Goal leakage | Intent automatically creates Goal or Task | Goal and Task keep their existing owners | Existing Task Manager requires Intent ownership |
| Action Intent naming collision | Downstream execution envelope is confused with subject Intent | Mark Action Intent as `DO_NOT_REUSE` for the Intent ontology | Same active schema ID is unavoidable |
| Runtime premature activation | Planning contracts are imported into Runtime | Planning-only status and no runtime imports | Runtime activation is required to validate semantics |
| Persistence premature freeze | Storage decisions hard-code lifecycle semantics | Defer persistence and numeric retention policy | Planning requires production storage |

## Review conclusion

No structural owner conflict was found. Existing assets can be reused as boundaries or references while the older Intent-like vocabularies are aligned explicitly. The phase may proceed as planning, but no asset in this directory is an active schema, production enum, FSM, runtime service, or authorization path.
