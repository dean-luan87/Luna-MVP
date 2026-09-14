# Luna Capability State Machine v1

## Transition Model

```text
Candidate
  ↓ governed registration decision
Registered
  ↓ assessment and compatibility review
Reviewed
  ↓ authority approval
Approved
  ↓ explicit lifecycle activation decision
Active
  ↓ freeze baseline decision
Frozen
  ↓ replacement/sunset decision
Deprecated
  ↓ migration closure and dependency removal
Retired
```

## Transition Controls

| from | to | required evidence | authority | prohibited shortcut |
| --- | --- | --- | --- | --- |
| Candidate | Registered | proposed identity, owner, declared inputs/outputs/dependencies, no-write plan | existing L1 Registry process in a future approved phase | self-registration or Runtime activation |
| Registered | Reviewed | assessment, Contract compatibility, Protocol dependency inventory | L1 Protocol Governance + review authority | unreviewed Active state |
| Reviewed | Approved | L0 alignment, Permission/Admission impact review, boundary validation | designated Governance authorities | owner self-approval |
| Approved | Active | explicit lifecycle decision, diagnostics binding plan, compatible Protocol references | L1 Capability Registry Authority | Permission/Runtime activation by implication |
| Active | Frozen | stable baseline, regression/validation evidence, traceable version/dependency identity | L1 Registry + Protocol Governance | in-place unreviewed change |
| Frozen | Deprecated | replacement target, coexistence and sunset plan | L1 Registry + Protocol/Permission review | history deletion or new dependency |
| Deprecated | Retired | dependency migration closure, trace/history retention evidence | L1 Registry Authority | retirement with active unresolved dependencies |

## Admission Flow

```text
Capability Proposal
        ↓
Capability Assessment
        ↓
Contract Compatibility Check
        ↓
Protocol Compatibility Check
        ↓
Permission Scope Review
        ↓
Authority Approval
        ↓
Registration
```

The final Registration step means a governed lifecycle record decision only. It is distinct from Runtime execution, State access, Fact authority, Decision authority, or Action authority. The state machine defines the subsequent review, approval, and active lifecycle transitions; no Registry write occurs in this planning phase.

