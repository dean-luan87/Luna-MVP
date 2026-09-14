# Implementation Summary

The bridge preserves cognitive source references, creates minimum evidence-only
Requirements, reuses the existing Scope/Resolution/Gap chain, and emits
candidate-only replanning after bounded failure. It does not infer missing
capabilities, select technical dependencies, or execute any improvement.

The bridge also represents a provisional plan/next-step boundary. Only the
current minimum Need forms a Requirement. Sufficiency can produce
`STOP_SUFFICIENT`; remaining candidates stay non-binding and
`NOT_REQUIRED_AFTER_SUFFICIENCY` is not a capability failure.
