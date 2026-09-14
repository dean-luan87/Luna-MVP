# Information Need Authority

Information Need is split into four separate authorities.

| Sub-authority | Existing evidence | Semantic owner | Mutation/registration owner | Brain relation | Decision |
|---|---|---|---|---|---|
| Need Formation | A-Route `form_information_need(...)` forms a candidate from governed objective conditions minus Current World coverage and reuses `CognitiveNeedCandidateV1` | `A-Route Cognitive Responsibility` (candidate formation only) | `OWNER_UNRESOLVED` for admission/registration | REQUEST / CANDIDATE FORMATION | `RESOLVED_FOR_CANDIDATE_FORMATION` |
| Need Admission / Registration | no canonical Need registry/admission API found; capability bridge consumes a Need rather than admitting one | `OWNER_UNRESOLVED` | `OWNER_UNRESOLVED` | REQUEST | `OWNER_UNRESOLVED` |
| Need Lifecycle Tracking | Cognitive Flow carries current need/state references and dynamic-loop continuity candidates | Cognitive Flow Governance for mechanical reference lifecycle | Cognitive Flow candidate state only | COORDINATE / REFERENCE_ONLY | `RESOLVED_TO_EXISTING_OWNER` for tracking mechanics |
| Need Satisfaction Evaluation | `CognitiveSufficiencyCandidateV1` and engine output | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME | `RESOLVED_TO_EXISTING_OWNER` |

The Need bridge contract describes a “bounded information/evidence need formed
by cognitive governance” and provides source Intent, Context, Field,
Hypothesis, and Attention refs. The A-Route adapter now owns only candidate
formation; no canonical Need admission/registration operation was added
(`cognitive_need_capability_requirement_bridge_types_v1.py:12-30`).

Satisfaction is different: the canonical validator requires Sufficiency to be
owned by Cognitive State Formation Governance, and the engine produces the
Sufficiency, Gap, Revision, and Stop candidates under that owner
(`cognitive_loop_types_v1.py:88-135`; `cognitive_state_formation_engine_v1.py:549-630`).
