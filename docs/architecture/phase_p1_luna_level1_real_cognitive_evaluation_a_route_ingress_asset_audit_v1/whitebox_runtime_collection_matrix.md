# White-box Runtime Collection Matrix

| Signal | Status | Current evidence / limitation |
|---|---|---|
| Goal | `OBSERVABLE_VIA_EXISTING_TRACE` | White-box synthetic nodes and refs. |
| Concern | `OBSERVABLE_VIA_EXISTING_TRACE` | Same; no general runtime collector. |
| Role | `DERIVABLE` | Profile has role ref; runtime role transition not instrumented. |
| Context | `DERIVABLE` | Profile/context refs exist when supplied. |
| Attention | `SYNTHETIC_ONLY` | State Formation fixture/engine. |
| Observation Request | `OBSERVABLE_VIA_EXISTING_TRACE` | Trace node and FPO candidates. |
| Observation cycle | `DERIVABLE` | Trace cycle index/profile adapter. |
| Capability call | `PARTIALLY_OBSERVABLE` | Narrow provider trace; no general runtime stream. |
| Evidence available | `OBSERVABLE_VIA_EXISTING_TRACE` | Evidence node refs and RF-DETR precedent. |
| Evidence consumed | `NOT_INSTRUMENTED` | Profile has counts but no general consumption event. |
| Evidence ignored | `NOT_INSTRUMENTED` | Profile explicitly marks ignored targets not observed. |
| Current World Candidate | `SYNTHETIC_ONLY` | Candidate fixtures/controlled formation. |
| Hypothesis | `SYNTHETIC_ONLY` | Candidate fixtures and narrow RF-DETR adapter. |
| Hypothesis revision | `SYNTHETIC_ONLY` | Existing synthetic revision fixture. |
| Sufficiency | `SYNTHETIC_ONLY` | Candidate/evidence-coverage logic. |
| Information Gap | `SYNTHETIC_ONLY` | Candidate detector/policy. |
| Re-observation | `SYNTHETIC_ONLY` | Candidate policy and trace fixture. |
| Stop reason | `NOT_INSTRUMENTED` | V1 node exists; no general runtime producer. |
| Decision handoff | `PARTIALLY_OBSERVABLE` | Narrow RF-DETR summary; no general runtime. |
| Owner transition | `OBSERVABLE_VIA_EXISTING_TRACE` | Stage/owner refs in controlled traces. |
| Latency | `UNAVAILABLE` | White-box profile marks latency unavailable. |
| Resource usage | `UNAVAILABLE` | White-box profile marks resource usage unavailable. |

Unavailable and not-instrumented values must remain explicit, never zero-filled.

