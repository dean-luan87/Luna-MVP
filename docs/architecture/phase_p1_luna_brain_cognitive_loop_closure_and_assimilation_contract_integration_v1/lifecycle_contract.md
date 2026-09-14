# Lifecycle contract

`BrainCognitiveRequestV1` is a Brain-domain, candidate-only request envelope
with stable refs for Brain subject, Goal, Intent, Concern, Context, and
Information Need.  It carries `canonical_owner_status=OWNER_UNRESOLVED`;
this integration does not establish a Brain runtime owner.
`BrainCognitiveLoopInstanceV1` records the mechanical loop identity and the
canonical A-Route execution refs.  It does not create semantic cognition.

The loop may contain one cycle for a sufficient case or two causally linked
cycles for the gap/re-observation case.  The loop does not schedule itself,
spawn a new loop, invoke a Provider, or execute a Task/Action.
