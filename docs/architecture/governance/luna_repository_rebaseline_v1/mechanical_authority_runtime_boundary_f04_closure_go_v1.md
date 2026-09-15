# F-04 Mechanical Authority Runtime Boundary Closure GO V1

## Identity and status

- **Finding:** F-04 — Mechanical Authority / Runtime Postflight Exemption Boundary
- **Date:** 2026-09-15
- **Canonical branch:** `luna-current-baseline`
- **Pre-freeze baseline HEAD:** `a57dc342d67d10d4a3575d5224e9182ff76342b8`
- **Parent:** `edbd72a57ac50dbcd9f19cf3de64c2d36fcaafda`
- **Technical status:** `F04_TECHNICAL_STATUS = CLOSED`
- **Engineering status:** `F04_ENGINEERING_STATUS = AWAITING_ENGINEERING_FREEZE`

F-04 is technically closed within the audited mechanical-authority and
runtime-proof boundary. This record does not declare `ENGINEERING_FROZEN`,
`FULL_REPOSITORY_GO`, `PRODUCTION_READY`, or `RELEASED`.

## Phase lineage

1. **P6A — `Phase-P6A-Luna-F04-Mechanical-Authority-Runtime-Postflight-Exemption-Whitebox-Audit-v1-001`** reconstructed the broad mechanical-authority exemption and classified it as an active high-severity finding.
2. **P6B — `Phase-P6B-Luna-F04-Mechanical-Authority-Runtime-Proof-Boundary-Remediation-v1-001`** narrowed the exemption and separated mechanical record fields from runtime-positive signals.
3. **P6C — `Phase-P6C-Luna-F04-Mechanical-Authority-Runtime-Proof-Boundary-Adversarial-Closure-Audit-v1-001`** independently rechecked authority transfer, replacement bypasses, producer/consumer migration, Runtime Grant boundaries, and regression power.
4. **P6D — `Phase-P6D-Luna-F04-Engineering-Freeze-Preparation-v1-001`** prepares this local closure record for the separate user-terminal freeze step.

## Original defect and function/authority root cause

The former Governance Verification Backbone condition allowed
`mechanical_authority=true` to suppress runtime-positive postflight checks
when `runtime_authority=false`. That broad exemption could make mechanical
recording authority appear to excuse runtime start, provider session,
Gateway submission, allocation, or execution signals.

The root cause was:

```text
AUTHORITY_DRIFT_ROOT_CAUSE = MECHANICAL_AUTHORITY_DRIFT
```

The restored function boundary is:

- **Governance Verification Backbone:** verifies profile constraints within
  its declared verification scope. Its PASS is limited to those constraints.
- **Mechanical Authority:** permits formation or recognition of explicitly
  mechanical records only.
- **Runtime Authority:** remains a separate authority for runtime execution
  and runtime-positive signals.
- **Runtime effect and postflight observation:** require their own applicable
  runtime authority and evidence semantics.

The authority restoration result is:

```text
AUTHORITY_RESTORATION_RESULT = PASS
```

Mechanical Authority MUST NOT:

- authorize runtime execution;
- prove runtime execution;
- prove provider invocation or Gateway submission;
- prove an external effect;
- fabricate or bypass Runtime Grant;
- suppress a runtime-positive prohibition check.

The canonical separation is:

```text
MECHANICAL RECORD AUTHORITY
!= RUNTIME EXECUTION AUTHORITY
!= RUNTIME EFFECT PROOF
!= POSTFLIGHT OBSERVATION PROOF
```

In particular:

```text
mechanical_authority
-X→ Runtime Grant
-X→ runtime effect proof
-X→ runtime postflight exemption
```

## Remediation and runtime signal boundary

When `runtime_authority` is false, the Governance Verification Backbone now
checks the runtime-positive signal family regardless of
`mechanical_authority`. A positive runtime signal therefore remains a
blocker under a mechanical-only profile.

The five runtime-positive fields are:

- `runtime_started`
- `provider_session_started`
- `gateway_submission`
- `execution_instance_created`
- `resource_allocated`

These fields are treated as runtime signals in the active postflight
boundary. They cannot receive a mechanical-authority exemption.

The controlled evaluation paths retain separate, explicitly namespaced
mechanical record fields:

- `mechanical_provider_session_record_created`
- `mechanical_execution_identity_record_created`
- `mechanical_resource_allocation_record_created`

Those fields describe controlled record formation. They do not assert a real
provider session, runtime execution instance, Gateway request, or external
resource allocation. They are not generic replacement authority flags and
must not be interpreted as runtime proof.

## Mechanical-only controlled semantics

Mechanical authority continues to support legitimate controlled operations
whose subject is record formation, including provider binding records,
allocation records, and execution-identity records. A mechanical-only
postflight PASS means only that the permitted governance constraints for
that mechanical profile were satisfied.

It does not mean that runtime execution occurred, that a provider was
invoked, that a Gateway submission occurred, or that an external effect was
observed. The controlled provider-session path records mechanical session
formation separately. The controlled binding/allocation/identity path records
mechanical allocation and identity formation separately.

## Runtime-proof behavior

The strengthened runtime boundary has these results:

| Condition | Result |
|---|---|
| `mechanical_authority=false`, runtime-positive signal asserted | Blocked by the existing runtime-authority prohibition |
| `mechanical_authority=true`, runtime-positive signal asserted | Blocked; mechanical authority does not suppress the prohibition |
| `mechanical_authority=true`, all prohibited runtime signals false | Mechanical-only PASS may remain valid, subject to other profile rules |
| mechanical record fields true, runtime fields false | Mechanical-only record formation may remain valid |
| runtime-proof fields missing or malformed | Existing generic postflight semantics are preserved; no runtime proof is claimed |
| mechanical-only profile without Runtime Grant | No Runtime Grant is fabricated or implied |

The remediation does not turn the Governance Backbone into a universal
runtime-proof completeness verifier. Missing-proof semantics outside the
mechanical-authority bypass remain governed by their existing contracts.

## Runtime Grant and adjacent boundaries

Runtime Grant remains separate from mechanical authority. Mechanical authority
cannot create a grant, substitute for a grant, make an absent or unknown
grant valid, or make a stale grant fresh. Stale/freshness semantics remain
the separate F-07 boundary.

F-03 remains frozen with the following invariant:

```text
Action Candidate Formation
!= Resource Execution Feasibility
!= Runtime Execution Authority
```

The F-04 remediation does not change F-03 resource `UNKNOWN` semantics,
candidate readiness, or resource reactions.

## Function and authority principles

The F-04 closure is bound to these Luna function-governance principles:

1. **SINGLE CANONICAL OWNER:** For one authoritative question at one lifecycle layer, exactly one canonical owner/final authority.
2. **FUNCTION MINIMALITY:** A module owns the minimum sufficient function set and does not accumulate adjacent capabilities merely because data is locally available.
3. **CAPABILITY ORTHOGONALITY:** Two modules do not independently own substantially equivalent authoritative capabilities.
4. **NO MULTIPLE FINAL AUTHORITY:** One question does not require two modules to independently reach and maintain the same authoritative conclusion.
5. **FORMATION != ADMISSION:** Candidate formation does not imply admission authority.
6. **ADMISSION != MUTATION:** Admission authority does not imply authoritative-state mutation.
7. **ADMISSION != EXECUTION:** Admission does not imply runtime execution authority.
8. **RECORD != PROOF:** Mechanical or administrative record formation does not constitute runtime or semantic proof.
9. **VERIFICATION SCOPE IS NON-EXPANSIVE:** A verifier PASS proves only properties independently covered by its contract.
10. **AUTHORITY DOES NOT TRANSFER IMPLICITLY:** Refs, booleans, adapters, profiles, compatibility seams, replay modes, controlled modes, fixture modes, and naming conventions cannot silently transfer authority.

## F-01 through F-04 documentation consistency

The local closure records were reviewed at the documentation level against
the principles above:

- **F-01:** Verification authority is bounded; verifier PASS does not expand beyond independently proven scope. `F01_FUNCTION_DOC_ALIGNMENT = PASS`.
- **F-02:** Cognitive Sufficiency and semantic authority remain bounded by the documented cognitive ownership model; the F-02 record does not endorse a duplicate final authority. `F02_FUNCTION_DOC_ALIGNMENT = PASS`.
- **F-03:** Action Candidate Formation, Resource Execution Feasibility, and Runtime Execution Authority remain separate. `F03_FUNCTION_DOC_ALIGNMENT = PASS`.
- **F-04:** Mechanical Record Authority and Runtime Authority remain separate, and the Backbone verification scope is non-expansive. `F04_FUNCTION_DOC_ALIGNMENT = PASS`.

No material wording conflict required changes to the existing F-01, F-02, or
F-03 closure records. The existing records remain auditable lineage receipts.

The documentation-level review found no active function overload,
capability overlap, or multiple-final-authority statement within the F-01 to
F-04 closure scope:

```text
ACTIVE_DOCUMENTED_FUNCTION_OVERLOAD_COUNT = 0
ACTIVE_DOCUMENTED_CAPABILITY_OVERLAP_COUNT = 0
ACTIVE_DOCUMENTED_MULTIPLE_FINAL_AUTHORITY_COUNT = 0
FUNCTION_GOVERNANCE_DOC_ALIGNMENT_PATHS = NONE
```

## Verification receipt

P6B user-terminal verification recorded:

- F-04 focused tests: `21 passed`;
- F-01 through F-04 regression: `165 passed`;
- `git diff --check = PASS`;
- `git diff --cached --check = PASS`;
- `py_compile = PASS`.

P6C adversarial closure recorded:

- `DOCUMENT_INTENT_ALIGNMENT = PASS`;
- `AUTHORITY_DRIFT_ROOT_CAUSE = MECHANICAL_AUTHORITY_DRIFT`;
- `AUTHORITY_RESTORATION_RESULT = PASS`;
- `ACTIVE_MECHANICAL_TO_RUNTIME_AUTHORITY_TRANSFER_COUNT = 0`;
- `MECHANICAL_AUTHORITY_RUNTIME_SIGNAL_BYPASS_COUNT = 0`;
- `ACTIVE_CONTROLLED_MECHANICAL_STALE_COUNT = 0`;
- `REPLACEMENT_MAGIC_BYPASS_FOUND = NO`;
- `CALLER_CONTROLLED_RUNTIME_AUTHORITY_ESCALATION = NO`;
- `MECHANICAL_POSTFLIGHT_PASS_MISREPRESENTED_AS_RUNTIME_PROOF = NO`;
- `F04_RUNTIME_GRANT_ESCALATION = 0`;
- `F04_TESTS_HAVE_REGRESSION_POWER = PASS`;
- `F03_REGRESSION_FOUND = NO`;
- `C1-C20 = PASS`.

The P6C closure-gate receipt is:

| Gate | Result |
|---|---|
| C1 baseline correct | `PASS` |
| C2 expected P6B diff only | `PASS` |
| C3 `runtime_started` bypass eliminated | `PASS` |
| C4 `provider_session_started` bypass eliminated | `PASS` |
| C5 `gateway_submission` bypass eliminated | `PASS` |
| C6 `execution_instance_created` bypass eliminated | `PASS` |
| C7 `resource_allocated` bypass eliminated | `PASS` |
| C8 mechanical provider-session record remains valid | `PASS` |
| C9 mechanical execution-identity record remains valid | `PASS` |
| C10 mechanical resource-allocation record remains valid | `PASS` |
| C11 new mechanical fields cannot become runtime proof | `PASS` |
| C12 no replacement magic bypass | `PASS` |
| C13 caller cannot escalate mechanical declaration into runtime authority | `PASS` |
| C14 mechanical generic PASS not represented as runtime proof | `PASS` |
| C15 Runtime Grant not fabricated or bypassed | `PASS` |
| C16 active stale controlled producers = 0 | `PASS` |
| C17 F-03 no regression | `PASS` |
| C18 tests have real regression power | `PASS` |
| C19 document/function intent aligned | `PASS` |
| C20 authority restoration complete | `PASS` |

The freeze suite was not executed because the pre-existing environment is
missing `luna_badge_v1_2`:

```text
tests/freeze = NOT_EXECUTED
reason = PRE_EXISTING_ENVIRONMENT_DEPENDENCY
```

This is not a PASS and is not an F-04 closure blocker.

No real provider, network, model, camera, or hardware execution was invoked.

## Scope and exclusions

The F-04 closure scope is limited to the mechanical-authority/runtime-proof
boundary. It does not close or remediate:

- F-01, F-02, F-03, F-05, F-07, F-08, F-09, F-10, or F-11;
- stale Runtime Grant behavior under F-07;
- R03 production-engine tuple-unpacking defect;
- caller-supplied authority concerns outside this specific bypass;
- generic runtime-proof completeness;
- provider, network, model, camera, or hardware qualification;
- production runtime qualification;
- release assurance, cryptographic signing, fresh-checkout assurance, or
  immutable/TOCTOU hardening.

This record does not imply `FULL_REPOSITORY_GO`, `PRODUCTION_READY`, or
`RELEASED`.

## Freeze manifest

The exact proposed P6D freeze manifest is five paths: three P6B production
files, the focused F-04 test, and this closure document.

1. `capabilities/midplatform/protocol_manager/module/governance_verification_backbone_v1.py`
2. `capabilities/evaluation/provider_session_controlled_invocation_multiscenario_sandbox/engine_v1.py`
3. `capabilities/evaluation/provider_binding_runtime_allocation_execution_instance_controlled/engine_v1.py`
4. `tests/f04/test_mechanical_authority_runtime_boundary.py`
5. `docs/architecture/governance/luna_repository_rebaseline_v1/mechanical_authority_runtime_boundary_f04_closure_go_v1.md`

## Engineering-freeze boundary

The technical finding is closed, while engineering freeze remains pending.
The next user-authorized freeze step requires:

1. the local governance document to remain in the exact manifest;
2. the corresponding Notion receipt to be synchronized;
3. exact Git staging of the five paths;
4. creation of the exact Git commit; and
5. postflight verification of branch, HEAD, status, diff checks, and the
   committed manifest.

No path is staged or committed by this documentation-preparation phase.

```text
F04_TECHNICAL_STATUS = CLOSED
F04_ENGINEERING_STATUS = AWAITING_ENGINEERING_FREEZE
AUTHORITY_DRIFT_ROOT_CAUSE = MECHANICAL_AUTHORITY_DRIFT
AUTHORITY_RESTORATION_RESULT = PASS

F01_FUNCTION_DOC_ALIGNMENT = PASS
F02_FUNCTION_DOC_ALIGNMENT = PASS
F03_FUNCTION_DOC_ALIGNMENT = PASS
F04_FUNCTION_DOC_ALIGNMENT = PASS

ACTIVE_DOCUMENTED_FUNCTION_OVERLOAD_COUNT = 0
ACTIVE_DOCUMENTED_CAPABILITY_OVERLAP_COUNT = 0
ACTIVE_DOCUMENTED_MULTIPLE_FINAL_AUTHORITY_COUNT = 0

FUNCTION_GOVERNANCE_DOC_ALIGNMENT_PATHS = NONE
F04_FREEZE_MANIFEST = 5 paths listed above
STAGED_PATH_COUNT = 0
UNMERGED_PATH_COUNT = 0

RECOMMENDED_NEXT_PHASE = Phase-P6D-Luna-F04-User-Terminal-Freeze-v1-001
```
