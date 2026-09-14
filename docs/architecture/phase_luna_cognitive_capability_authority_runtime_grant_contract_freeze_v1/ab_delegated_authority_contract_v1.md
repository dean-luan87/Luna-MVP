# A / B Delegated Authority Contract

## Delegation chain

Brain-governed A grant
→ A creates BContingencyRequestCandidateV1
→ B receives derived bounded grant
→ B produces BContingencyResultCandidateV1
→ A evaluates, adopts or rejects the result
→ Brain retains global adjudication

## A grant

The normal issuer is Brain governance. A grant is scoped to:

- one admitted Concern;
- one Work instance;
- one Goal/context package;
- one resource and safety envelope;
- one validity state/version range;
- one result receiver;
- one responsibility owner.

A may exercise local Need, Hypothesis, evidence relevance, local sufficiency,
reconsideration, Observation/Capability request, B request and local
continuation semantics only inside that grant.

## B derived grant

B's grant must be derived from:

- the Brain-governed A grant;
- the A BContingencyRequest;
- B's own Capability Boundary;
- request scope and depth;
- resource envelope;
- Safety and Permission limits.

B cannot receive more authority than the intersection of those boundaries.

## A remains responsible

A remains responsible for:

- request validity;
- bounded scope;
- whether B result is relevant;
- whether B result is stale;
- KEEP/USE/PARTIAL_USE/SUPERSEDE/DISCARD;
- any later Need, sufficiency, continuation or closure decision.

B is responsible only for producing the requested bounded contingency result.

## No direct B escalation

B cannot:

- issue a new B request to itself;
- create a new Concern;
- grant itself authority;
- grant authority to another role;
- control Loop lifecycle;
- select Provider identity;
- adopt its own result.
