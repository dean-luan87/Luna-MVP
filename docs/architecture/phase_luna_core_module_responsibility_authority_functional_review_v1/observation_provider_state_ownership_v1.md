# Observation / Provider State Ownership v1

| State | Classification | Owner |
|---|---|---|
| Observation Request identity/version/lifecycle | AUTHORITATIVE | Observation/FPO boundary |
| Provider identity/admission/invocation/session | AUTHORITATIVE within runtime contract | Provider Governance |
| Provider Result | EXTERNAL runtime result/reference | Provider/Executor |
| Evidence Candidate/admitted Evidence | CANDIDATE / structurally admitted | Gateway/Evidence boundary |
| Gateway admission record | AUTHORITATIVE admission record | Observation Gateway |
| Current World/Field handoff | REFERENCE_ONLY candidate | Current World/Field owners |
| source versions/trace/provenance | REFERENCE/derived lineage | source and boundary owners |

No boundary owns semantic Truth or A state.
