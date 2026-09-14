# Action Architecture Plan v1

## Phase

- Phase: Phase-Luna-Action-Architecture-Planning-v1-001
- Stage: Action Architecture Planning
- Execution Mode: Planning Only
- Canonical owner: Action Governance

## Objective

Define Luna Action Governance planning contracts for candidate formation, readiness, boundary enforcement, and handoff contracts without implementing runtime execution.

## In Scope

- planning/schema/contract/boundary/scenario/reuse mapping/verifier
- Action Candidate and Execution Readiness Candidate semantics
- Decision to Action influence boundary and Task/Executor boundary contracts

## Out Of Scope

- runtime action execution
- actuator command emission
- scheduler execution
- database or device operations
- task creation or runtime task orchestration

## Core Freeze

- Decision != Action
- selected Decision Candidate != Action Execution
- Action Candidate != Runtime Command
- Eligible/Ready/Authorized != Executed
- Action Governance != Executor
- Action Governance != Task Manager

## Stop Condition

All required planning artifacts complete and static checks ready, then stop at WAITING_FOR_USER_TERMINAL_VERIFICATION.
