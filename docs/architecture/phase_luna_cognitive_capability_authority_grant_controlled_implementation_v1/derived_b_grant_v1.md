# Derived B Grant

## Derivation

Brain-governed A Grant plus A BContingencyRequest produces a
DerivedAuthorityGrantCandidateV1.

## Boundaries

The derived authorities are constrained by the intersection of:

- A delegation authority;
- B Capability Boundary;
- Concern/Work request scope;
- Resource limits;
- Safety/Permission limits;
- requested depth and stopping conditions.

## Rejection cases

- A lacks REQUEST_B;
- requester is not A;
- B asks for unsupported semantic authority;
- B asks to create/split/merge a Concern;
- B asks to control Loop;
- B expands Resource scope;
- B exceeds allowed depth;
- B recursively delegates.

The derived B grant is candidate-only and does not create a child Loop,
Concern, Task, Action or Provider invocation.
