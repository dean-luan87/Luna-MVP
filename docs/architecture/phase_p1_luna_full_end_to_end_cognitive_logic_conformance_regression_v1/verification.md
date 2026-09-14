# Verification

Run the new runner, then verify its generated transient summary. The runner
reuses the existing verified cognition-to-Action-Candidate composition and
executes the contrast requests through `CognitiveStateFormationEngineV1`.

The verifier checks:

- operational E2E through Action Candidate and candidate-only Runtime
  Executor handoff;
- all forbidden behavior flags remain false;
- every required cognitive assertion is individually reported;
- contrast results contain observed semantic comparisons;
- missing evidence produces a canonical Gap and no premature Stop;
- conflicting evidence remains candidate/uncertain;
- no Role/Task assertion is passed from metadata alone;
- any capability gap forces `cognitive_logic_result=FAIL`;
- `final_decision=GO` only when both operational and cognitive results are
  `PASS`.

The conditioning implementation phase adds the request/mapping and
candidate-only semantic surfaces required by this regression. The expected
current result is not asserted here: the user must run the Runner and Verifier,
which compare actual conditioned outputs and fail closed on missing effects.
