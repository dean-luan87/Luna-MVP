# Constraint Lifecycle v1

Safety policy: `defined → active → superseded/revoked`.

Permission: `candidate/evidence → granted/denied → active → expired/revoked/
superseded`.

Resource: `policy → available facts → budget/reservation → consumed/released/
exhausted`.

These are separate lifecycle domains, not one global Constraint state machine.
