# Reality Decision Formation Go/No-Go v1

## V0 static acceptance criteria

1. Situation is not Decision; Decision is not Action; Action is not Outcome.
2. Option Generation produces possible paths only, not recommendations.
3. Evaluation preserves Survival Impact, Goal Alignment, Capability Fit,
   Resource Cost, Risk/Uncertainty, and Experience Reference.
4. Brain retains the final decision judgment boundary; Neural does not replace
   Brain; Middleware does not own decision authority.
5. Experience is candidate-only reference; it does not directly change a
   Strategy or Decision.
6. B Reflection cannot affect a current Decision Candidate in real time.
7. Decision Confidence handles low support through more information,
   risk-reduction, deferral, or user-confirmation candidates.
8. Fast / Normal / Deep paths are candidate-formation boundaries, not a
   Scheduler or Action mechanism.
9. No Action execution, Runtime, Provider call, automatic Attention change,
   automatic learning, or State mutation is introduced.
10. Reducer remains the sole State mutation authority.

## Verification ownership

Execution Mode: `Planning Only`. Agent performs V0 static checks only. The
final phase verifier is user-terminal only.

## User-terminal verification command

```bash
python3 docs/architecture/cognitive_reality_decision_formation_v1/verify_cognitive_reality_decision_formation_v1.py
```

`final_candidate_decision: COGNITIVE_REALITY_DECISION_FORMATION_ARCHITECTURE_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
