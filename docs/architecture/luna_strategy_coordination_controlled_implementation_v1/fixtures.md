# Controlled fixtures

The evaluation package covers:

1. single strategy admission;
2. two independent strategies both admitted;
3. explicit strategy defer;
4. missing dependency;
5. explicit redundancy with deterministic retention;
6. explicit incompatibility without winner selection;
7. strategy from a deferred Branch;
8. strategy from a rejected Branch;
9. zero strategies;
10. multiple gaps with independent lineage;
11. Scenario 12 shape: one branch and signage/flow strategies both admitted;
12. already-satisfied upstream state with zero strategies;
13. invalid candidate input fail-closed.

The fixtures use explicit refs and do not derive coordination semantics from Goal,
Question, scenario, case, string similarity, confidence or resource markers.
