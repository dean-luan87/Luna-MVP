# Executable Capability Candidate Boundary v1

An Executable Capability Candidate represents a logically resolved capability
whose supplied runtime prerequisites have passed the Runtime Admission
assessment for bounded execution.

It carries logical resolution, slot, admitted model asset/version/path,
Provider compatibility, permission/resource/safety refs, valid source version,
expiry/staleness, trace and provenance.

It does not imply:

- Provider has been admitted or invoked;
- model weights were loaded;
- evidence exists;
- Task succeeded;
- A Need was satisfied;
- World Truth was established.

The candidate is created only when assessment status is
`READY_FOR_EXECUTABLE_CANDIDATE`. Blocked or degraded assessments do not
produce an executable candidate unless a future contract explicitly defines a
degraded execution path.
