# Inventory and reuse

Reused canonical boundaries:

- `capabilities/vision/registry/vision_registry.py` — existing Vision Registry surface
- Capability Registry boundary — identity, contract, dependency, lifecycle
- Model Manager / Model Contract Repository — model/provider admission only
- FPO / Active Observation Control — Observation Need and capability requirement
- Observation Gateway — evidence ingress and candidate/truth boundary
- Vision Manager and OCR Manager — future capability/provider surfaces
- System Maintenance — diagnostics, degradation, and rollback candidates
- Brain Golden Baseline — no Provider-to-Brain shortcut

The implementation adds one narrow registry integration package; it does not
create a second registry or semantic owner.
