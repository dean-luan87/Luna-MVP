# Shared Loop Engine Target Contract

## Target role

Loop Engine is a shared persistence and execution-state mechanism used by A
and B. It is not a cognitive subject, a Brain, a Planner, a Scheduler or a
second governance layer.

## Loop-retained data

- loop_id;
- concern_ref;
- reasoning_owner_ref, identifying the A or B working context;
- state-version lineage;
- execution-state lineage;
- Need and Requirement refs;
- pending candidate refs;
- pause, wait and resume state;
- resource-state refs;
- trace and provenance refs;
- closure-state mechanics;
- parent, branch and dependency relation refs;
- history-boundary refs.

All retained external data remains a ref or bounded candidate metadata. Loop
does not copy authoritative world, Intent, Role, Field, Emotion, Safety,
Resource, Task, Experience, Memory, Provider or Model state.

## Loop-excluded authority

Loop does not own:

- reasoning semantics;
- cognitive authority;
- Hypothesis authority;
- sufficiency authority;
- branch authority;
- Capability selection authority;
- concern ownership;
- result adoption;
- continuation or termination judgment;
- Provider/model identity.

## A and B use

A and B may use the same Loop Engine implementation without sharing:

- cognitive authority;
- local reasoning state;
- Hypothesis authority;
- sufficiency judgment;
- branch decision.

A B working branch does not automatically mean another Loop. One Loop may
reference multiple governed Capability paths when A or B requests them.

## Mechanical lifecycle boundary

Brain/Safety/Resource/A/B governance proposes lifecycle decisions. The Loop
Engine stores and exposes candidate lifecycle transitions only after the
governed input is present. It may preserve PAUSED, WAITING, DEFERRED, STOPPED
and COMPLETED mechanics, but may not decide their semantic reason.

## Migration constraint

The current Loop candidate types and closure/package records should be reused.
The migration should narrow authority declarations before removing or renaming
any fields. Canonical enums and types remain unchanged in this phase.
