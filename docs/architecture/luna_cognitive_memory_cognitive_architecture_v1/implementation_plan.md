# Cognitive Memory Implementation Plan v1

This phase is Architecture Only. The read-only inventory found reusable assets:

- `docs/architecture/luna_cognitive_information_lifecycle_v1/` for states, value, decay, folding, compression, retention, and ownership;
- `docs/architecture/luna_cognitive_field_architecture_v1/` and `docs/architecture/luna_cognitive_field_temporal_evolution_architecture_v1/` for current Field and evolution context;
- `docs/architecture/luna_cognitive_information_processing_pipeline_architecture_v1/` for Experience extraction and governed candidates;
- `docs/architecture/luna_knowledge_memory_boundary_architecture_v1/` for Knowledge admission and Memory boundaries;
- `docs/runtime/luna_cognitive_memory_runtime_integration_v1/` for existing Runtime contracts and adapters;
- `docs/architecture/luna_role_architecture_v1/` and Self/Social Self assets for scoped growth boundaries.

Existing Memory-related capability includes `memory_candidate.py`, `memory_governance.py`, `memory_retrieval.py`, `memory_runtime.py`, `memory_store.py`, `self_memory_adapter.py`, and `social_memory_adapter.py`. They are not modified, moved, or duplicated.

Duplicate risks include parallel Memory Store, Retrieval, Governance, and Lifecycle definitions. Owner conflicts are resolved here by mapping, not by migration: Memory System owns memory objects; Information Lifecycle owns lifecycle policy; Self/Social/Role/Field consume candidates in their own scopes. Future migration is adapter-first and requires a separate implementation phase.

