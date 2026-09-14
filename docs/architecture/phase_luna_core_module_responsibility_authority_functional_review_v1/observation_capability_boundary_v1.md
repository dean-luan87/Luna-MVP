# Observation / Capability Boundary v1

Target flow:

`A Cognitive Requirement + Attention refs → Capability Requirement → Logical
Capability Resolution → Runtime Admission → Executable Capability Candidate →
Observation Request → Provider Admission/Invocation`.

Observation consumes executable acquisition capability refs. It does not select
Model/Provider or perform Runtime Admission. The request may be formed before
or alongside Capability resolution, but execution cannot proceed without a
valid executable capability handoff.
