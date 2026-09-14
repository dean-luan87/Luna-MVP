# Implementation Overview

## Location

capabilities/midplatform/core/cognitive_flow/integration/authority_grant_mechanical_command_controlled/

## Candidate-only components

- authority grant, status, revocation and expiry candidate types;
- mechanical command and validation candidate types;
- Loop mechanical state and return candidate types;
- derived B grant candidate;
- authority/responsibility binding candidate;
- static role capability boundary registry;
- deterministic validation and mechanical state engine;
- synthetic fixture and adapter;
- compact Runner and Verifier.

## Reuse

The package reuses the authority freeze contracts, existing cognitive-flow
candidate-only conventions, trace/provenance string references and existing
Loop mechanical command semantics. It does not create a new global owner or
modify existing Dynamic Flow/Loop engines.

## Runtime boundary

All outputs are immutable candidate records. No command is sent to a real Loop,
Brain, Provider, model, camera or scheduler.
