# F-08 Contract Integrity / Input Validation Closure — GO

## Status and scope

~~~text
F08_STATUS = CLOSED
F08_TECHNICAL_STATUS = GO
F08_ENGINEERING_STATUS = PENDING_FREEZE
AUTHORITY_DRIFT_ROOT_CAUSE = NO_AUTHORITY_DRIFT
~~~

Finding: **F-08 — Input Shape / Contract Defensive Hardening**.

This record documents the scoped technical closure of contract-integrity
defects. It does not declare engineering frozen, full-repository GO,
production readiness, provider/model/hardware qualification, or remote
publication.

The governing architecture chain is:

~~~text
Shape Truth
→ Semantic Meaning
→ Governed Authority
~~~

F-08 is a contract-integrity finding. Its root categories were
STRUCTURAL_SHAPE_CONFUSION, CONTRACT_VALIDATION_OWNER_GAP,
INVALID_TO_EPISTEMIC_COLLAPSE, and ADAPTER_CONTRACT_REPAIR. These are
validation-boundary defects, not authority-transfer defects.

## Original findings and final disposition

| Finding | Scope | Final disposition |
|---|---|---|
| F08-01 | Observation Gateway ingress shape | CLOSED |
| F08-02 | Evidence to Field Event adapter shape | CLOSED |
| F08-03 | Field Event admission input shape | CLOSED |
| F08-04 | Field State Reducer input shape | CLOSED |
| F08-05 | Field State Read Model query shape | CLOSED |
| F08-06 | Cognitive State Formation input shape | CLOSED |
| F08-07 | Task input and context shape | CLOSED |
| F08-08 | A-Route transport shape | CLOSED |
| F08-09 | Runtime preparation shape | CLOSED |
| F08-10 | Context Foundation scalar/nested shape | CLOSED |
| F08-11 | Decision/Action typed internal boundary | TRUSTED_TYPED_INTERNAL |

~~~text
F08_CLOSED_COUNT = 10
F08_TRUSTED_TYPED_INTERNAL_COUNT = 1
F08_REMAINING_DEFECT_COUNT = 0
~~~

TRUSTED_TYPED_INTERNAL means the audited low-level Decision/Action path
receives owner-produced typed DTOs and has no raw public ingress requiring a
second authoritative validator. It does not permit malformed external input
to bypass an owner boundary.

## Contract-integrity protocol

The normative protocol is:

capabilities/midplatform/governance_standards/contract_integrity/luna_contract_integrity_protocol_v1.md

Its rules are:

- INVALID_INPUT != UNKNOWN, UNRESOLVED, or ABSENT.
- Raw, external, or reconstructed input is structurally validated before
  semantic processing.
- The canonical owner validates once; downstream consumers reference the
  resulting typed contract and may only reject locally.
- Normalization is representation-preserving and is not repair.
- An invalid member invalidates a required typed collection.
- A wrong type is not optional absence.
- Adapters may map, preserve provenance, normalize losslessly, or reject;
  they may not invent required information, admission, truth, or authority.
- Deserialization and replay re-enter structural validation.
- Structural validity does not imply admission, truth, authorization, or
  execution eligibility.
- Validation does not create authority or a validation proof token/ref.
- Failure origin remains locally distinguishable from epistemic uncertainty.
- Authority-relevant malformed input fails closed.
- Defensive validation does not create a second final authority.
- Contract changes require producer, adapter, admission, consumer,
  replay/serialization, verifier, and test review.
- Validator targets must be derived from the actual canonical contract;
  validators must not invent required fields or silently repair a
  validator/contract mismatch.

~~~text
PROTOCOL_CREATES_RUNTIME_AUTHORITY = NO
PROTOCOL_REQUIRES_GLOBAL_VALIDATOR = NO
NEW_GLOBAL_VALIDATION_FRAMEWORK_CREATED = NO
VALIDATION_PROOF_CARRIER_CREATED = NO
~~~

The protocol is governance text, not a runtime module, validator service,
Schema Manager, Admission Manager, state owner, truth owner, or authority
owner.

## Final validation model

The canonical flow is:

~~~text
Raw / untrusted structure
→ owner-boundary structural validation
→ typed contract
→ semantic processing
→ admission / mutation / execution under the existing owner
~~~

Malformed structure terminates at explicit local contract rejection. It is
not converted into UNKNOWN, UNRESOLVED, optional absence, an empty valid
collection, a candidate, an admitted record, a canonical state input, or an
execution fact. Valid optional absence and valid semantic UNKNOWN /
UNRESOLVED remain available after structural validation succeeds.

The F-08 implementation closes the audited cases for string-as-sequence,
mapping-shape confusion, unsafe positional assumptions at raw boundaries,
silent default/coercion, invalid-to-epistemic collapse, lossy adapter repair,
and reconstruction without revalidation. The controlled Task handoff was also
aligned with its declared Tuple[str, ...] contract by changing its empty
dependency representation from [] to (); this was upstream producer contract
alignment and did not change Task semantics or authority.

## Authority boundaries

Structural validation does not create:

~~~text
truth
admission occurrence
canonical mutation authority
Runtime Authorization
execution fact
~~~

The cross-finding boundaries remain:

~~~text
F02: Cognitive absence/reference semantics remain semantic-owner governed.
F03: Resource Feasibility != Runtime Authorization.
F04: Mechanical Record != Runtime Reality / Runtime Authority.
F05: DTO / Record / Projection != Governed Gateway Admission State.
F07: DTO / Record / Projection != Governed Runtime Authorization State.
~~~

~~~text
F02_BOUNDARY = PASS
F03_BOUNDARY = PASS
F04_BOUNDARY = PASS
F05_BOUNDARY = PASS
F07_BOUNDARY = PASS
F05_FINAL_AUTHORITY_COUNT = 1
F07_FINAL_AUTHORITY_COUNT = 1
F03_AUTHORITY_MODEL_CHANGED = NO
F05_AUTHORITY_MODEL_CHANGED = NO
F07_AUTHORITY_MODEL_CHANGED = NO
F03_RESOURCE_SEMANTICS_CHANGED = NO
FUNCTION_OVERLOAD = 0
CAPABILITY_OVERLAP = 0
MULTIPLE_FINAL_AUTHORITY = 0
~~~

Contract validators answer only whether structure satisfies the declared
contract. Observation Gateway remains the F-05 admission owner, Permission /
Admission Manager remains the F-07 Runtime Authorization owner, and the
existing semantic, admission, mutation, execution, and verification owners
retain their responsibilities.

## Closure history

The failed verification history is preserved:

1. **P10A** identified 11 contract-integrity findings: four HIGH and seven
   MEDIUM.
2. **P10B** adjudicated owner boundaries and the Contract Integrity Protocol.
3. **P10C** performed the initial implementation.
4. **P10D** initial terminal verification recorded 39 failed / 232 passed.
5. **P10E** corrected two implementation defects. Subsequent evidence reached
   20 focused PASS / 271 applicable regression PASS.
6. **P10F** found three still-uncovered structural defects.
7. **P10G** remediated those three defects and added direct coverage.
8. The first final regression command was invalid because tests/f06 did not
   exist. This was a VERIFICATION_COMMAND_DEFECT, not an implementation
   failure.
9. The next applicable regression recorded 5 failed / 277 passed.
10. **P10I** reduced the five failures to one independent root: an upstream
    Task producer emitted dependency_refs = [] while the canonical contract
    requires Tuple[str, ...].
11. **P10J** aligned that producer from [] to (), with no semantic or
    authority change.

## Verification evidence and limits

The final user-terminal evidence is bound exactly:

~~~text
P10J targeted regression = 35 passed, exit 0
F08 focused = 31 passed, exit 0
F01-F08 applicable regression = 282 passed, exit 0
py_compile = PASS, exit 0
git diff --check = PASS
git diff --cached --check = PASS
staged = 0
unmerged = 0
~~~

The following remain outside the evidence:

~~~text
tests/freeze = NOT_EXECUTED
provider/model/hardware = NOT_EXECUTED
FULL_REPOSITORY_GO = NOT_CLAIMED
PRODUCTION_READY = NOT_CLAIMED
REMOTE_PUBLICATION = NOT_CLAIMED
~~~

## F-08 change surface

The final implementation/protocol/test surface contains 18 tracked modified
implementation paths and two new F-08 paths. The P10J producer is classified
as UPSTREAM_PRODUCER_CONTRACT_ALIGNMENT.

### Tracked implementation paths

1. capabilities/midplatform/core/a_route_orchestration/a_route_orchestration_engine_v1.py
2. capabilities/midplatform/core/a_route_orchestration/a_route_orchestration_static_validators_v1.py
3. capabilities/midplatform/core/cognitive_flow/integration/decision_to_task_manager_controlled_handoff/engine_v1.py
4. capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_engine_v1.py
5. capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_static_validators_v1.py
6. capabilities/midplatform/core/context_foundation/context_foundation_static_validators_v1.py
7. capabilities/midplatform/core/evidence_to_field_event_adapter_v1.py
8. capabilities/midplatform/core/field_event_admission_api_v1.py
9. capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_projection_builder_v1.py
10. capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_query_validator_v1.py
11. capabilities/midplatform/core/field_state_reducer/module/field_state_reducer_module_input_adapter_v1.py
12. capabilities/midplatform/core/observation_gateway/observation_gateway_engine_v1.py
13. capabilities/midplatform/core/observation_gateway/observation_gateway_error_types_v1.py
14. capabilities/midplatform/core/observation_gateway/observation_gateway_static_validators_v1.py
15. capabilities/midplatform/core/runtime_executor/runtime_allocation_execution_instance_v1.py
16. capabilities/midplatform/core/runtime_executor/runtime_allocation_preparation_candidate_v1.py
17. capabilities/midplatform/core/task_manager/module/task_manager_module_input_adapter_v1.py
18. capabilities/midplatform/provider_runtime_governance/provider_binding_runtime_preparation_v1.py

### New F-08 protocol and test paths

19. capabilities/midplatform/governance_standards/contract_integrity/luna_contract_integrity_protocol_v1.md
20. tests/f08/test_contract_integrity_input_validation.py

The closure/governance record is an additional documentation path and is not
counted in the 20 implementation/protocol/test paths above.

## File-size follow-up

~~~text
F08_FILE_SIZE_BLOCKER = NO
~~~

The A-Route engine is 853 lines and the Cognitive Formation engine is 1185
lines. Their large-active-file governance review is:

~~~text
DEFERRED_TO_F11_LARGE_ACTIVE_FILE_GOVERNANCE
~~~

No F-11 implementation was performed in F-08.

## Function and authority ledger entry

The following entry is bound to the existing canonical module and
authority/responsibility ledgers. It does not create an authority transfer.

1. **Canonical Function:** Contract Integrity / owner-boundary structural validation.
2. **Semantic Owner:** The respective canonical domain/forming owner retains semantic meaning; the validator does not define it.
3. **Admission / Decision Owner:** The existing domain admission or decision owner.
4. **Mutation Owner:** The existing canonical state mutation owner.
5. **Execution Authority:** The existing Runtime Executor / Provider owner within its established boundary.
6. **Verification Authority:** Scoped verifier and tests only.
7. **Mechanical Record Authority:** The respective record producer.
8. **Evidence / Observation Owner:** The existing evidence or observation producer and Gateway boundary.
9. **Negative Boundary:** Validation cannot establish truth, admission, authority, canonical mutation, authorization, execution eligibility, or an execution fact.
10. **Authority Transfer Rules:** A validated typed contract becomes eligible for the next owner; no authority transfers through a boolean, ref, adapter, projection, replay record, or validation result alone.
11. **Change Reason:** Prevent malformed structure from being coerced into semantic uncertainty, optional absence, valid candidates, or authority inputs.
12. **Previous → Current:** Implicit coercion/defaulting and lossy adapter repair → owner-boundary rejection followed by typed-contract reference.
13. **Affected Contracts / Callers / Consumers:** The 18 tracked F-08 implementation paths, the Contract Integrity Protocol, the F-08 tests, and the P10J controlled Task producer.
14. **Migration / Compatibility:** Strict declared shapes remain canonical; the controlled producer uses () for empty Tuple[str, ...]; no legacy coercion was restored.
15. **Verification Binding:** P10J targeted 35, F08 focused 31, F01-F08 applicable regression 282, py_compile, and both diff checks are PASS; freeze/provider/model/hardware checks were not executed.
16. **Architecture Linkage:** Contract Integrity Protocol P1–P15, Shape Truth → Semantic Meaning → Governed Authority, and preservation of F02, F03, F04, F05, and F07 boundaries.

~~~text
AUTHORITY_DRIFT_ROOT_CAUSE = NO_AUTHORITY_DRIFT
ARCHITECTURE_AND_FUNCTION_LEDGER_JOINT_REVIEW = REQUIRED
~~~

## Freeze boundary

F-08 has technical GO and is ready for the separate governance steps. This
record does not perform staging or commit and does not mark engineering
frozen.

~~~text
F08_TECHNICAL_STATUS = GO
F08_ENGINEERING_STATUS = PENDING_FREEZE
~~~
