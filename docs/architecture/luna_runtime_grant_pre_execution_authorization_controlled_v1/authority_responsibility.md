# Authority and responsibility

The grant authority is:

- `authority:runtime-execution-authorization`
- owner: `Permission / Admission Manager`
- responsibility:
  `responsibility:runtime-execution-authorization-decision`

The Governance Backbone profile declares the pair and preflight validates the
mapping. A candidate-only artifact cannot issue this decision. A helper that
sets `execution_authorized=true` is treated as an authoritative effect and
must use this owner and responsibility pair.

Failure ownership remains local to the decision authority: permission denial
belongs to Permission / Admission Manager; provider eligibility denial to
Provider Governance; safety or constitutional veto to its policy owner;
resource unavailability to Resource Governance / Runtime; and execution
failure to Runtime Executor. A complete request rejected by the grant owner is
not relabeled `INVALID_UPSTREAM_REQUEST`.

Requester Owns Requirement Complexity and Executor Owns Execution Complexity
remain separate: the requester supplies complete semantic and execution
references, while runtime owners retain resource and execution internals.
