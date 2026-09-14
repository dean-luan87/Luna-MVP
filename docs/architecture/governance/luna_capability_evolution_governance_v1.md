# Luna Capability Evolution Governance v1

## Evolution Modes

| evolution action | governance meaning | required preservation |
| --- | --- | --- |
| add | introduce a new Capability or bounded optional function | identity, owner, Protocol/Contract references, traceability, candidate boundary |
| evolve | change implementation or behavior within declared governance | compatibility evidence and retained authority boundary |
| extend | add a compatible input/output/dependency/context variant | explicit scope and consumer/dependency impact declaration |
| degrade | reduce availability, scope, resource allocation, or permitted operating context | visible limitation, trace, and no hidden privilege expansion |
| replace | introduce a successor while preserving migration and historical evidence | coexistence, compatibility record, rollback and retirement plan |

## Impact Levels

| level | examples | governance response |
| --- | --- | --- |
| low impact | internal change preserving Contracts, boundaries, dependencies, trace, and output semantics | record change and run proportionate compatibility/regression review |
| medium impact | new optional behavior, dependency, context constraint, resource profile, or consumer compatibility requirement | Protocol/Permission/Diagnostics impact assessment and explicit compatibility declaration |
| high impact | candidate/Fact boundary change, input/output semantic change, Protocol version change, permission scope change, State/Decision implication, real external capability or Runtime impact | separate approved phase, constitutional/Protocol/Permission review, migration and rollback evidence; no in-place self-upgrade |

## Extension Strategy

Future Capability forms may add specialized lifecycle states, contextual constraints, assessment dimensions, and non-authoritative service modes. Extensions must be additive and mapped to common governance markers. They cannot replace required traceability, bypass Protocol version validation, introduce a parallel permission system, or convert a candidate output into a Fact.

## Replacement and Rollback

Replacement uses a successor Candidate, compatibility declaration, coexistence period where needed, consumer/dependency migration, and retained historical trace. Rollback selects a previously compatible governed baseline by reference; it cannot erase evidence or silently downgrade a consumer. High-impact rollback remains blocked where semantic compatibility is not demonstrated.

