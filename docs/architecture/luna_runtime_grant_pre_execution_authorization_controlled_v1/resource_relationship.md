# Resource relationship

Resource feasibility is an input condition, not a grant and not an
allocation. `SATISFIABLE` permits the grant decision to consider execution;
it does not reserve CPU/GPU/memory, select a worker, or create an execution
identity. `UNAVAILABLE` is owned by Resource Governance / the Runtime
allocation boundary and produces a denied grant without changing cognition.

The subsequent order remains grant authorization first, followed by any
authoritative allocation and execution-instance realization owned downstream.
No concrete resource identity is generated in this phase.
