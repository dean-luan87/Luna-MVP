# Middleware Capability Organization Candidate v1

Middleware consumes a Reallocation Candidate and returns:

- `middleware_situation_update_candidate`: bounded availability/resource observation;
- `capability_organization_candidate`: available capability, missing capability, candidate combination, resource impact, fallback option;
- `future_capability_session_candidate`: a proposed future session only.

Middleware does not decide Goal completion, select a Provider, invoke a Provider, or determine cognitive truth.
