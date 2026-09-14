# Luna Phase Verification Execution Authority Standard v1

## Overview

This standard defines four verification levels and authority boundaries.

## V0 Static Checks

Includes:
- Required file existence checks.
- JSON/YAML parse checks.
- py_compile checks.
- Standard import checks.
- AST/field/registry/mermaid static checks.
- Editor diagnostics checks.

Default executor:
- Agent

Allowed result:
- STATIC_CHECK_READY

V0 cannot grant GO.

## V1 Controlled Component Validation

Includes:
- Controlled Runner.
- DryRun Runner.
- Smoke Runner.
- Result Verifier.
- Fixture immutability checks.
- Deterministic comparison checks.
- Negative case execution checks.
- Synthetic/fixture-isolated execution checks.

Executor:
- Agent only when explicitly authorized by Execution Mode and phase instruction.

Allowed result:
- COMPONENT_VALIDATION_PASSED
- BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION

V1 cannot grant final GO.

## V2 Final Phase Verification

Includes:
- docs/architecture/<phase>/verify_<phase>.py

Executor:
- User Terminal Only

Required output sections:
- CHECKS
- FAILED_CHECKS
- PASSED_CHECK_COUNT
- FAILED_CHECK_COUNT
- BLOCKER_COUNT
- FINAL_DECISION
- NEXT

## V3 Final Audit And Decision

Executor:
- ChatGPT Only

Audit responsibilities:
- Verify path and interpreter context.
- Verify check count integrity.
- Verify failed checks and blocker count.
- Verify FINAL_DECISION and NEXT consistency.
- Verify agent boundary compliance.
- Verify real side-effect boundary.
- Issue final phase decision.

## Core Authority Rule

Only user-executed V2 plus ChatGPT V3 audit can grant GO.
