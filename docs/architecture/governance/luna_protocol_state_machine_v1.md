# Luna Protocol State Machine v1

## Transition Flow

```text
Draft
  ↓ proposal completeness
Review
  ↓ authority + compatibility acceptance
Approved
  ↓ explicit activation decision
Active
  ↓ baseline freeze decision
Frozen
  ↓ replacement/sunset decision
Deprecated
  ↓ migration completion and dependency removal
Retired
```

## Allowed Transitions

| from | to | required evidence | authority | prohibited shortcut |
| --- | --- | --- | --- | --- |
| Draft | Review | proposal, scope, owner, impact classification | Protocol owner + L1 Protocol Governance intake | Draft → Active |
| Review | Approved | L0 alignment, Contract/traceability/compatibility review | L1 Protocol Governance | reviewer self-approval or Capability approval |
| Approved | Active | explicit activation decision, compatibility declaration, diagnostics binding plan | L1 Protocol Governance | Runtime/Permission activation by implication |
| Active | Frozen | stable baseline, regression evidence, version identity | L1 Protocol Governance | editing the active version in place |
| Frozen | Deprecated | replacement/sunset and migration plan | L1 Protocol Governance | deletion of traceability history |
| Deprecated | Retired | no allowed active dependency and migration closure evidence | L1 Protocol Governance + Registry lifecycle confirmation | retirement with unresolved dependency |

## Exceptional Handling

- A detected Constitution conflict returns the proposal to Draft or blocks it; no lower layer can resolve it by exception.
- A breaking change creates a new Draft version; it cannot mutate an Active/Frozen version in place.
- A security, provenance, or boundary violation may suspend reference eligibility pending L1 review, but Diagnostics cannot retire or approve a Protocol automatically.

## State Semantics

No lifecycle state creates a Fact, Decision, Action, State write, Memory write, Capability activation, or Runtime authorization. Protocol lifecycle manages governed compatibility, not domain execution.

