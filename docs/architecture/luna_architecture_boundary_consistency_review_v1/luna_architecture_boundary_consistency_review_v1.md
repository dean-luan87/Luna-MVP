# Luna Architecture Boundary Consistency Review v1

## Scope

This is a lightweight boundary health check after the Self / Social Self
refactoring. It is not a full repository engineering audit and does not
recompute historical long-file, duplicate-asset, or verification-only issues.

## Checks

1. Canonical Owner uniqueness: Role and Relationship belong to Social Self;
   Identity, Capability, Regulation, and Evolution belong to Self; Emotion
   Context belongs only to Integration; Constitution remains L0.
2. Permission consistency: Self and Social Self cannot overwrite each other,
   Constitution, Capability Reality, Brain, or Action.
3. Cognitive Flow compatibility: the new External World → Social Self →
   Integration → Brain → Self Evaluation → Decision view is a context subflow
   compatible with the existing evidence/Field/Brain/Decision flow.
4. Constitution scope: L0 constrains Self and Social Self but is not owned by
   either layer.
5. Capability Governance scope: Self knows its capability state; Capability
   Governance independently manages definition, admission, calibration, and
   implementation options.
6. Emotion boundary: Integration-only context placeholder, not Self, Social
   Self, Decision, Action, Value, or Identity authority.

## Boundary result

Historical references may remain in old assets, but they are non-authoritative
until an explicit migration phase. This phase produces no code, Runtime, file
move, module deletion, or full engineering-health result.
