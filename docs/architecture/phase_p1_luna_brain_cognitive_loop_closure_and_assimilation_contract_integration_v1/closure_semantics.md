# Closure semantics

The following are distinct:

1. `Stop` is the canonical Cognitive State Formation result for a sufficient
   cognitive state.
2. `ClosureAssessmentCandidateV1` is the loop-local Closure Candidate derived
   from canonical Sufficiency and Stop.
3. `ClosureDecisionCandidateV1` is reused as the controlled Closure Acceptance
   envelope.  Its `decision_ref` is exposed as `closure_acceptance_ref`; it is
   not Decision execution.  The envelope carries
   `responsibility_domain=BRAIN` and `canonical_owner_status=OWNER_UNRESOLVED`;
   it does not establish a Brain runtime authority.
4. `LifecycleClosureCandidateV1` records the accepted lifecycle transition.
5. `BrainAssimilationCandidateV1` is a candidate-only Brain-domain handoff
   after accepted closure; it does not establish a canonical Brain owner.

Closure creation fails closed unless canonical Sufficiency is `SUFFICIENT` and
canonical Stop exists.  Acceptance remains a candidate-only controlled
boundary with unresolved canonical Brain ownership.  No closure candidate is
emitted for an insufficient or stopped-less cognition result.
