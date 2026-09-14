# Luna Capability Module Standard v1

## Purpose

This standard defines the formal unit for Luna capability packaging, upgrade, replacement, and acceptance.

## Core Definition

A Capability Module is the minimum unit of:

- packaging
- iteration
- acceptance
- lifecycle governance
- integration planning

Each Capability Module must include the following fields in registry/manifest records:

- capability_id
- capability_name
- domain
- owner_layer
- responsibility
- lifecycle_status
- module_version
- api_version
- input_contract
- output_contract
- dependencies
- dependents
- module_api
- implementation_path
- integration_runner
- diagnostics_support
- trace_support
- replay_support
- persistence_authority
- fact_admission_authority
- action_execution_authority
- runtime_authority
- replacement_policy
- upgrade_policy
- deprecation_policy
- known_limitations
- ready_evidence
- last_updated

## Scope Boundary

The following assets are internal to a capability module by default and must not be automatically registered as project-level Capability Modules:

- subsystem
- component
- policy
- protocol
- adapter
- runner
- verifier

Promotion to top-level Capability Module requires explicit governance decision and evidence.

## Status Authority

Lifecycle status must follow the lifecycle registry and cannot skip evidence-gated transitions.

## Versioning

- module_version tracks implementation package generation.
- api_version tracks external contract compatibility.
- version changes must follow upgrade/deprecation policies.
