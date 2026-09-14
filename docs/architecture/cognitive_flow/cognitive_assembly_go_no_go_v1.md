# Cognitive Assembly Lifecycle and Resource Governance Go/No-Go v1

## Planning boundary

- Assembly is not an Agent, Task, or Process.
- Neural Governance is the sole Assembly creation coordinator.
- Middleware does not create Assemblies and manages capability candidates only.
- Providers do not participate in Assembly decisions.
- No Scheduler, Runtime mutation, automatic Assembly creation, automatic Attention change, or automatic learning is introduced.

## Static validation

Required Assembly planning documents exist, Mermaid lifecycle/architecture diagrams are present, and no implementation layer is created by this phase.

`final_candidate_decision: COGNITIVE_ASSEMBLY_LIFECYCLE_AND_RESOURCE_GOVERNANCE_ARCHITECTURE_READY_WITH_NOTES`

User-terminal V2 command:

```bash
python3 docs/architecture/cognitive_assembly_lifecycle_resource_governance_v1/verify_cognitive_assembly_lifecycle_resource_governance_v1.py
```

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
