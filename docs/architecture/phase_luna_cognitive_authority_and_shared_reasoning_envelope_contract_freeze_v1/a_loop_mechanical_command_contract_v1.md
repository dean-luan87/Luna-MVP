# A to Loop Mechanical Command Contract

## Purpose

A sends semantic decisions. Loop performs mechanical state operations. Loop
must not infer commands from data.

## Allowed command candidates

- MATERIALIZE
- RECORD_STATE_VERSION
- RECORD_NEED_REF
- RECORD_REQUIREMENT_REF
- RECORD_PENDING_CANDIDATE
- PAUSE
- WAIT
- RESUME_KEEP
- RESUME_REPLAN
- SUPERSEDE_REQUIREMENT
- RECORD_B_BRANCH_REF
- CLOSE
- FREEZE_FINAL_STATE
- RECORD_OUTCOME_REF
- ARCHIVE_HISTORY_BOUNDARY

## Required command envelope

Every command candidate includes:

- command_ref;
- command_kind;
- issuing_reasoning_owner_ref;
- source_state_version_ref;
- target_loop_ref;
- target_refs;
- reason_refs;
- trace_ref;
- provenance_refs;
- candidate_only=true.

## Command semantics

MATERIALIZE records Brain-governed admission of a persistent concern. It does
not create a new Brain or scheduler.

RECORD_STATE_VERSION, RECORD_NEED_REF, RECORD_REQUIREMENT_REF and
RECORD_PENDING_CANDIDATE persist supplied refs and versions only.

PAUSE, WAIT, RESUME_KEEP and RESUME_REPLAN perform mechanical lifecycle state
updates after A/Brain/Safety/Resource governance supplies the semantic decision.

SUPERSEDE_REQUIREMENT invalidates direct invocation eligibility for the supplied
Requirement ref.

RECORD_B_BRANCH_REF records an A-authorized B branch reference. It does not
create a child Concern or child Loop.

CLOSE and FREEZE_FINAL_STATE require a governed closure decision. They do not
let Loop self-authorize closure.

RECORD_OUTCOME_REF and ARCHIVE_HISTORY_BOUNDARY record bounded references
without assimilation or semantic compression.

## Negative command rules

Loop cannot invent a command, choose a Capability, choose a Provider, decide
sufficiency, decide continuation, create a Concern, create a Task, execute an
Action or mutate Brain state.
