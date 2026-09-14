# Negative guards

The controlled integration preserves these guards:

- closure without canonical Sufficiency is rejected;
- closure before canonical Stop is rejected;
- Evaluation does not create cognition or closure;
- Cognitive State Formation does not mutate Brain;
- closure/assimilation are reference-only;
- Memory, Experience, and Knowledge are not promoted automatically;
- no Decision, Task, or Action executes;
- live Observation and model/provider invocation remain disabled;
- Field and World Truth boundaries remain unchanged.

The Runner includes exactly one dynamically exercised negative probe:
attempting closure with no canonical Sufficiency must return a rejected
precondition.  The Runner/Verifier separately reports `guard_present` and
`guard_runtime_covered`; all other listed guards are structurally enforced but
not dynamically exercised by this phase.
