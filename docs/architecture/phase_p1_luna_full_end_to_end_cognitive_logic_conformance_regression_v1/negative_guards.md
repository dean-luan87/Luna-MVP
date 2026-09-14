# Negative guards

The runner retains the existing candidate-only and side-effect guards from
the verified downstream integration and adds the following read-only checks:

- evidence is not promoted to fact;
- hypotheses remain candidate-only and `causal_truth=false`;
- Current World Candidate is not World Truth;
- missing required information does not stop the loop;
- no re-observation is emitted after a sufficient result;
- no model/provider/live observation/action/runtime executor executes.

The conditioning assertions remain fail-closed: if the canonical replay path
does not expose an observed Role/Task effect, the cognitive conformance result
fails. The conditioning implementation phase does not weaken this rule; it
adds the request and candidate surfaces needed for the assertions to be
exercised.
