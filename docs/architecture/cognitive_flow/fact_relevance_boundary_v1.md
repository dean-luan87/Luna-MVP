# Fact Relevance Boundary v1

## Inclusion rule

Context Projection may include a fact when it is within the declared read scope,
current Attention Requirement, temporal window, or explicit interface request.
This is a projection and bandwidth rule, not a judgment of importance, risk, or
value.

## Permitted transformation

- selecting current Observable State;
- selecting State Change candidates;
- selecting fact-level Relevant Constraints;
- carrying Unknowns and validity;
- preserving Provenance and confidence;
- reducing duplicate representations without changing meaning.

## Forbidden transformation

Projection cannot convert `water_depth: 60cm` into `risk: dangerous`, a voice
pattern into `user_is_sad`, or a closed exit into `recommendation: reroute`. It
cannot add a Goal, Decision, Action, plan, prediction, emotion, or Situation.

The A Route receives the package and performs Situated Understanding. Brain and
Emotional Cognition remain responsible for higher-level interpretation.
The projection does not add a Goal and does not add a Decision.
