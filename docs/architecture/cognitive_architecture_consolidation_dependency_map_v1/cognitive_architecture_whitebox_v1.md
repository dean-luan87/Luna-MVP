# Cognitive Architecture Consolidation Whitebox v1

## Ownership questions

1. Who owns Reality? Evidence / Reality Update Pipeline and the Reality
   Reducer own accepted Reality transitions.
2. Who owns Field? Field System owns Field State; Role and Relationship are
   Field-bound projections.
3. Who owns Attention? Attention System owns resource allocation and
   arbitration.
4. Who owns Goal and Intent? Their contracts and Brain Review own authority;
   Task maintains continuity only.
5. Who owns Decision? Brain owns final judgment; Decision Commitment is a
   governed candidate transition.
6. Who owns Action? Action Boundary owns permission, authorization, risk, and
   execution isolation.
7. Who owns Experience and Learning? Experience System owns records; Learning
   produces candidates and does not automatically mutate source domains.
8. Who owns Capability? Capability Governance owns admission and state; a
   Provider supplies evidence candidates only.

## Allowed flow

```text
Evidence → Reality Update Candidate → Reducer
Reality → Field → Situation / Hypothesis / Expectation
Field + Self + Goal + Task + Attention → Workspace / Global State
Workspace + Evidence + Candidates → Brain Evaluation
Brain → Decision Candidate → Decision Commitment
Decision Commitment → Action Request Candidate → Action Boundary
Outcome Evidence → Experience → Learning Candidate → Future Adaptation Candidate
```

## Prohibited paths

- `Learning → Reality` write.
- `Emotion Context → Decision` override.
- `Capability → Goal` creation.
- `Provider → Brain` direct access.
- `Model → Decision` direct path.
- `Hardware → Value` or `Identity` mutation.
- `Action Boundary → Reality` direct write.
- Any module silently acquiring a writer role from a reader relationship.

Reader write authority is never implied by a read relationship.
reader write authority is never implied by a read relationship.

## Required audit questions

- Does every module dependency have a type: Required, Optional, Candidate, or
  Future Interface?
- Does every state have exactly one normative Owner and an explicit Writer?
- Are candidate outputs distinguishable from facts, decisions, and actions?
- Are Unknown and Provenance retained at every cross-domain boundary?
- Does the matrix preserve Brain, Attention, Action Boundary, and Reducer
  authority?
- Are future Model, Hardware, Emotion Runtime, B Simulation, and Capability
  Runtime paths placeholders rather than active execution?

## Negative audit evidence

This phase does not implement Runtime, Scheduler, Model, Provider, Hardware,
Action, B Simulation, automatic Learning, or new cognitive modules. It does not
weaken a prior verifier, delete passed assets, or hardcode a pass result.
