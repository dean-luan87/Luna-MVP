# Luna Runtime Grant / Pre-execution Authorization v1

This phase establishes the first authoritative, non-runtime execution
authorization boundary for the perception chain. It consumes complete,
governed preparation candidates and produces a time-bounded
`RuntimeExecutionGrantDecisionV1`. It does not allocate resources, create an
execution instance, start a provider session, submit to Observation Gateway,
or invoke a provider or model.

The canonical owner is the existing Permission / Admission Manager. No new
Runtime Grant super-owner is introduced. Runtime Executor remains the owner of
allocation realization and execution identity; Provider Governance owns
provider-domain eligibility and binding; Observation Gateway owns post-runtime
observation ingress admission; FPO owns semantic active-observation control.

The controlled order is:

`Provider Binding Candidate → Runtime Allocation Preparation → Execution
Instance Preparation → Runtime Execution Grant → future allocation / instance
realization → Runtime Observation → Gateway ingress admission`.

`GRANTED` means permission to proceed at the authorization boundary. It does
not mean `STARTED`, allocated, bound, or observed.
