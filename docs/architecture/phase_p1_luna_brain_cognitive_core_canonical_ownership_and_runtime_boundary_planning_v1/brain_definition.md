# Brain / Cognitive Core definition

## Definition

For the current architecture, Brain is the system-level cognitive
responsibility domain that coordinates concerns, requests cognitive work,
tracks Brain-local coordination references, and receives bounded results from
canonical cognition and downstream Governance owners.

This definition does not establish Brain as a concrete runtime owner. The
runtime owner status remains `OWNER_UNRESOLVED`.

## Responsibilities that may belong to Brain

- hold the global concern/goal context as references;
- request or coordinate a cognitive loop through an approved protocol;
- preserve identity and provenance across loop cycles;
- consume canonical Sufficiency and Stop results;
- receive Closure Candidates and Assimilation Candidates;
- make future Brain-local coordination decisions only through an explicitly
  authorized contract.

## Responsibilities outside Brain

- Intent mutation;
- Context or Field mutation;
- Observation acquisition or evidence admission;
- Attention, Hypothesis, Current World, Sufficiency, Gap, Revision, and Stop
  production;
- Decision, Task, Action, model, or Provider execution;
- Memory or Experience admission/mutation;
- Knowledge promotion, Learning mutation, or World Truth declaration.

Brain is therefore a coordination/protocol domain, not a super-owner of all
cognitive and operational state.
