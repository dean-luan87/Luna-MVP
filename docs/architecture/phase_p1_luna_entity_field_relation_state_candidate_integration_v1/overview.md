# Phase-P1 Luna Entity-Field Relation State Candidate Integration v1

Status: `GO — VERIFIED — PHASE CLOSED`

This phase minimally closes the Field State representation gap after the
closed relation-bearing Field Event Admission phase. It reuses the existing
`FieldStateCandidate` envelope and adds a typed candidate value for:

`EntityCandidate --OBSERVED_IN_FIELD--> Field`

The integration is candidate-only. It does not create Field Truth, World
Truth, a persistent relation, ownership, identity resolution, or an A-Route
relation bridge.

ROUTE C — `FIELD_STATE_RELATION_REPRESENTATION_GAP` is closed. ROUTE D,
the A-Route relation-consumption bridge, remains deferred.

The intended chain is:

`admitted relation event -> Reducer semantic consumption -> typed
EntityFieldRelationStateValueV1 -> FieldStateCandidate`

The real single-source case must remain insufficient evidence. A controlled
two-event/two-source case is used only to exercise the existing Reducer
selection and typed candidate construction.
