# Capability / A / Task / Attention Boundary v1

| Source | May provide | Must not do |
|---|---|---|
| A | Cognitive Need, Cognitive Requirement, semantic reason | select model/Provider or Runtime Admission |
| Task | functional requirement, capability dependency, execution condition | own logical resolution or Provider route |
| Attention | modality, urgency, focus, region/object and budget candidates | select model/Provider or create Need |
| Capability Governance | scope and logical resolution | judge Need/Sufficiency or schedule focus |

Target flow:

`A/Task → Capability Requirement → Scope → Logical Resolution → Runtime
Admission`.

Task's `build_capability_routes_v1` currently performs registry lookup and
execution request candidate construction. It is compatibility orchestration;
the logical scope/resolution responsibility belongs to Capability Governance.
