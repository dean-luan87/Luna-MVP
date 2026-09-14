# Role Identity and Lifecycle v1

Conceptual Role identity fields are `role_ref`, `subject_ref`, domain/
relationship, scope, source, validity, version, provenance, effective context,
constraints, and uncertainty when inferred.

Role candidates may come from user declaration, profile/account, organization,
Task, Intent, Context, Memory, Observation, or external systems. A candidate
source is not the Role owner.

Target lifecycle:

`candidate → source-admitted → applicable → suspended/expired/revoked →
superseded`.

The applicable source owner controls authoritative identity/lifecycle. Context
and Task can constrain applicability; Brain can constrain policy. The current
repository has candidate/ref assets but no unified lifecycle runtime, which is
a contract/adapter/runtime gap rather than a reason to create a Manager.
