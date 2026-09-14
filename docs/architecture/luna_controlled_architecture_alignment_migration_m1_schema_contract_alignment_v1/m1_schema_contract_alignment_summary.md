# PLANNING_CANDIDATE

## Summary

This M1 package defines candidate-only schema and contract overlays for Dynamic
Cognitive Architecture v2 alignment with current Luna engineering assets.

## What Is Preserved

- Field State Reducer remains the only field-state writer.
- Observation remains the evidence intake and handoff owner.
- Memory remains the persistence owner and cannot be overridden by PCN.
- PCN remains a future projection and activation boundary only.
- Task Manager remains downstream orchestration only.
- Model Manager and Protocol Manager remain support-governance organs only.
- OCR and Vision remain evidence producers only.

## What Is Added

- Ownership mapping for the candidate schema surfaces.
- Compatibility aliases between existing contracts and new candidate contracts.
- Candidate contracts for field, observation, memory, PCN, intent, causal,
  experience, A/B route, and decision inputs.
- Explicit boundary rules and rollback records.

## Verification Position

The verifier in this directory performs static completeness and boundary checks
only. It does not import business modules, execute runtime, call models, or
modify files.