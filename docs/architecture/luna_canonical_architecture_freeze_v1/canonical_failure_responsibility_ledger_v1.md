# Canonical Failure Responsibility Ledger v1

| Failure | Detector / boundary | Responsible owner | Semantic consequence | Global consequence | Direct forbidden target |
|---|---|---|---|---|---|
| Stale Requirement | A/Attention adapter | A / adapter for translation | A reconsideration | Brain only if Grant/Concern affected | no direct Action/Brain mutation |
| Grant revoked/expired | Brain/consumer admission | Brain for Grant; enforcing boundary for block | A/Decision/Task local consequence | Brain | no stale execution |
| Permission revoked | Permission/consumer admission | Permission Governance for policy; consumer for enforcement | A/Task/Decision | Brain if global | no stale observation/action |
| Resource unavailable/degraded | Diagnostics/Resource/Runtime | Diagnostics for fact; Resource for policy; enforcing boundary for block | A/Task/Decision | Brain if reserve/protected state | no automatic semantic acceptance |
| Capability unsupported | Capability Governance | Capability Governance | A requirement change | Brain if Goal/Concern impact | no direct Provider choice |
| Capability↔Model mismatch | Binding validation | Capability Governance | A/Runtime consequence | Brain if global | no Model/Capability cross-mutation |
| Model missing/degraded | Diagnostics/Model/Runtime | Model for declaration; Diagnostics for observed fact; Runtime for eligibility | A/Task | Brain if protected capability | no registry rewrite by Diagnostics |
| Provider incompatible/unavailable | Provider/Runtime Admission | Provider Governance / Runtime Admission | Task/A/Observation consequence | Brain if protected mode | no Model Registry mutation |
| Runtime Admission blocked/stale | Runtime Admission | Runtime Admission | A/Task/Decision | Brain if policy/protected resource | no Observation-ready candidate |
| Observation invalid/failed | Observation/Gateway | Observation or Gateway | A requests more/alternative evidence | Brain if global | no World Truth |
| Provider invocation failed | Provider | Provider Governance | Task/A/Outcome | Brain if global | no fabricated Evidence/success |
| Evidence malformed/stale/duplicate | Gateway/Diagnostics | Gateway for mapping/admission; Diagnostics for fact | A/Field/World | Brain if global | no Field/World mutation |
| Field transition invalid | Field admission/reducer | Field | A/Context/World consequence | Brain if operational policy | no Gateway mutation |
| Current World stale | Current World/State Formation | Current World boundary | A uses/defer/requires evidence | Brain if global | no World Truth declaration |
| Decision revoked/superseded | Decision Governance/Brain | Decision Governance or Brain override | A/Task/Action | Brain | no Task/Action continuation under stale commitment |
| Task blocked/not ready | Task | Task | A/Decision local consequence | Brain if Concern/Grant | no semantic replan by Task |
| Action admission blocked | Action Governance | Action Governance | Task/A/Outcome | Brain if global | no Provider invocation |
| Action Result partial/failed/stale | Action/Provider return boundary | Action/Provider for result; adapter for mapping | Task/A/Outcome | Brain if global | no direct Task completion/Concern closure |
| Outcome stale/contested | Outcome Evaluation | Outcome Evaluation | A/Brain review | Brain | no Concern closure by Outcome |
| Protocol drift/mismatch | Diagnostics/validator | Diagnostics for detection; Protocol for lifecycle | affected consumer/owner | Brain only if policy | no protocol rewrite by Diagnostics |
| Diagnostics conflict/unknown | Diagnostics | Diagnostics | consumer decides whether usable | Brain may choose degradation | no admission/remediation decision |
| Envelope stale/invalid | Working Envelope | Working Envelope | A/Brain chooses semantic consequence | Brain for Grant/Concern | no direct replan/closure |
| Perspective invalidated | Perspective Projection | Perspective boundary | A re-consumes projection | Brain only if Role authority changed | no Role/World mutation |

Retry, fallback, remediation and scheduling are not implicit failure owners. Any future implementation requires its own reviewed contract without changing this responsibility map.

