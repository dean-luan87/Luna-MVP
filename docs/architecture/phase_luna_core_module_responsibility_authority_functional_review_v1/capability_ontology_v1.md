# Capability Ontology v1

| Concept | Canonical meaning | Classification/owner |
|---|---|---|
| Capability | portable functional ability that can satisfy a requirement | canonical Capability Governance concept |
| Capability Slot | stable contract position for one or more compatible implementations | canonical Capability Governance |
| Capability Requirement | structured functional request | candidate/ref from A or Task; consumed by Capability Governance |
| Capability Scope | assessment of whether a requirement is inside a governed domain | candidate result owned by Capability Governance |
| Capability Resolution | logical module/slot resolution | candidate result owned by Capability Governance |
| Model Asset | governed model identity, weights, version, path, checksum and loader metadata | Model Manager |
| Model Capability Mapping | declaration that an asset can support a capability/slot under contracts | shared mapping contract; Model Manager supplies asset side, Capability Governance owns capability side |
| Executable Capability Candidate | logically resolved capability whose supplied runtime prerequisites are admitted | candidate from Runtime Admission |
| Provider | runtime implementation/execution boundary | Provider Governance |

Capability is not Model. Capability is not Provider. A model/provider can be
replaced while the logical capability and slot remain stable.
