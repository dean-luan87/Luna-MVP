# Cognitive Workspace Whitebox v1

```text
Reality / Field / Role / Relationship / Task / Self / Memory
                               ↓
                      Attention Arbitration
                               ↓
                    Cognitive Workspace State
                               ↓
                         Brain Input Package
```

## Control questions

- Who creates a Workspace? Workspace Governance from an admitted Field, Task, and Attention context.
- Who activates a Workspace? Activation Contract after Field and resource validation.
- Who updates a Workspace? Update Contract using candidate inputs and provenance.
- Who selects content? Attention; Workspace does not self-select content.
- Who supplies historical context? Memory Retrieval Candidate through the Memory interface.
- Who owns Goal and final Decision? Brain.
- Who owns Reality mutation? Reality Reducer after Evidence Gateway.
- Who owns Field, Role, Relationship, and Task definitions? Their source systems; Workspace stores references only.
- Who separates multiple Workspaces? Workspace lifecycle and isolation governance.

## Isolation invariants

Attention → Workspace admission is allowed. Memory → Workspace retrieval is
allowed. Field → Workspace context projection is allowed. Workspace → Decision,
Workspace → Reality Write, Workspace → Goal Mutation, Workspace → Identity Mutation,
Workspace → Action, and Workspace → Model/Hardware Invocation are forbidden.

Unknown, Risk, Conflict, and Provenance must remain attached to every package.
Primary and Background Workspaces must not silently merge. B Route is a placeholder only;
no Simulation Runtime is implemented.
