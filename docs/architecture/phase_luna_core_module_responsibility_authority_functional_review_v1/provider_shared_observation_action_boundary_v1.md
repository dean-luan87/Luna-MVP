# Shared Provider / Observation / Action Boundary v1

Observation and Action may share Provider identity, admission, health,
resource, invocation, failure and trace infrastructure.

Their source contracts remain distinct: Observation acquires information;
Action creates an external/system side effect. A shared Provider cannot collapse
these semantics or bypass either owner.
