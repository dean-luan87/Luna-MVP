# Assimilation boundary

Assimilation is represented only by the existing
`BrainAssimilationCandidateV1`.  It carries the controlled accepted closure, cognitive
outcome, source state, trace, and provenance references.

The candidate explicitly remains candidate-only and sets all forbidden effects
false: no World Truth declaration, Decision creation, Action execution, Intent
mutation, Memory mutation, Experience mutation, Learning execution, automatic
loop generation, or automatic Task generation.  Memory, Experience, and
Knowledge owners may later evaluate a candidate through their own admission
contracts; this phase does not call or mutate them.

This is a Brain-domain candidate handoff, not proof of a canonical Brain
assimilation owner.  The integration records
`responsibility_domain=BRAIN` and `canonical_owner_status=OWNER_UNRESOLVED`;
no Brain state is mutated.
