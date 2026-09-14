# PLANNING_CANDIDATE

## PCN Architecture Risk Review

1. PCN becoming Knowledge Graph:
Risk: forcing objective truth graph semantics.
Status: mitigated by personal relatedness semantics and strength_not_equal_truth.

2. PCN copying Memory:
Risk: duplicating stored memory body into PCN.
Status: mitigated by reference-only and memory boundary contract.

3. PCN gaining Source Object Ownership:
Risk: absorbing Self/Role/Relationship/Memory owners.
Status: mitigated by explicit forbidden ownership and source-owner precedence.

4. PCN silently doing Causal work:
Risk: association layer outputs cause/effect conclusions.
Status: mitigated by explicit PCN/Causal boundary and forbidden causal fact generation.

5. Infinite expansion risk:
Risk: activation traverses without resource boundary.
Status: mitigated by resource budget constraints and bounded propagation.

6. Resource constraint missing:
Risk: model ignores runtime/system budget signals.
Status: mitigated by resource constraint reference and degraded projection behavior.

7. Dormancy implemented as delete:
Risk: inactive links removed irreversibly.
Status: mitigated by dormant_not_deleted and reactivation rules.

8. Subjective links forcibly corrected by system rule:
Risk: personal cognition overwritten by external norm.
Status: mitigated by subjective boundary preserving bias/non-rational links.

9. Context overwritten by PCN reverse write:
Risk: PCN mutates context source state.
Status: mitigated by context-to-PCN handoff read-only contract.

10. Second writer risk:
Risk: multiple modules writing same cognitive state scope.
Status: mitigated by owner uniqueness and no_mutual_write constraints.

11. Nested-loop structure violation:
Risk: reducing architecture to one-way Context -> PCN -> Intent.
Status: mitigated by explicit nested bidirectional constraint registry.
