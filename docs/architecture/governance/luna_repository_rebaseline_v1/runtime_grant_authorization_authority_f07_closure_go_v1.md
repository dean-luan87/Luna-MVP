# F-07 Runtime Grant Authorization Authority Closure — GO

Phase: `Phase-P9K-Luna-F07-Closure-Documentation-And-Freeze-Preparation-v1-001`  
Execution Mode: **Documentation / Governance / Freeze Preparation**  
Canonical root: `/Users/luanlei/Desktop/Luna-Core`  
Branch: `luna-current-baseline`  
Expected pre-freeze HEAD: `102b356c7c6cce5727814b2dc455baa9752e5167`

## Closure status

```text
F07_TECHNICAL_STATUS = GO
F07_ENGINEERING_STATUS = NOT_YET_FROZEN
F07_USER_TERMINAL_VERIFICATION = PASS
F07_CLOSURE_TYPE = RUNTIME_IMPLEMENTATION_GO_PENDING_ENGINEERING_FREEZE
```

This document records the P9J technical closure and prepares the exact
engineering freeze. It does not itself freeze the implementation, publish the
branch, or establish a production or full-repository GO.

## Original finding

F-07 identified a Runtime Grant authority defect involving stale/freshness
semantics and the authority origin of runtime authorization.

The original root class was:

```text
DTO_AUTHORITY_ROOT_WITH_SPLIT_VALIDITY_FRESHNESS_REAUTHORIZATION
```

The authority-drift classification is:

```text
MULTI_AUTHORITY_DRIFT
```

The original active architecture allowed a caller-constructible
`RuntimeExecutionGrantDecisionV1` or projection to be interpreted as runtime
authorization. Downstream consumers also interpreted Grant fields as
authorization conclusions. The implementation had no governed,
execution-preparation-scoped authorization state.

The split `validity_status` / `freshness_status` model also allowed the
invalid combination:

```text
validity_status = STALE
freshness_status = FRESH
grant_decision = GRANTED
execution_authorized = True
```

P9G additionally found that a caller could install state in a caller-created
store and select its read view as the query root.

## Authority evolution and final model

The final model is:

```text
Authorization Decision
!=
Authorization State
!=
Governed Transition Origin
!=
Execution Eligibility
!=
Execution Fact
```

The canonical Runtime Authorization Owner is the Permission / Admission
Manager. Its canonical governed transition creates the owner-controlled
authorization state. Grant records and projections describe that result.

The authoritative state key is:

```text
(
    execution_instance_preparation_candidate_ref,
    authorization_ref
)
```

`authorization_ref` identifies one authorization occurrence. Equality,
prediction, copying, serialization, or caller supply of that value does not
prove that the governed transition occurred.

The final authority lifecycle is:

```text
Execution preparation
→ prerequisite evaluation
→ authorization eligibility
→ governed authorization transition
→ AUTHORIZED canonical state
→ Grant projection
→ downstream canonical-state query
→ local execution eligibility
→ runtime progression
```

Invalidation is owner-side:

```text
owner-side invalidation request
→ canonical INVALIDATED state
```

A scope mismatch is a query rejection only. A local resource, session, or
provider failure is an execution-eligibility refusal only. Neither mutates a
genuine authorization automatically.

## P9G failure and P9H remediation

P9G result:

```text
F07_CLOSURE_CRITERIA_PASS_COUNT = 19/24
F07_FINAL_ADJUDICATION = FAIL_MUTATION_AUTHORITY_NOT_CLOSED
```

The remaining defect was:

```text
caller-accessible state mutation
+
caller-selectable query root
```

P9H closed that defect by:

- removing the mutable state store from the public Grant Result;
- removing the authority view from the Grant Decision contract;
- fixing the query root to the Permission / Admission Manager owner-controlled
  canonical state;
- changing invalidation so it uses canonical identifiers and does not accept
  a caller-supplied store;
- ensuring caller-created Store/View objects cannot establish authority.

P9J result:

```text
F07_CLOSURE_CRITERIA_PASS_COUNT = 24/24
F07_FINAL_ADJUDICATION = PASS_READY_FOR_TECHNICAL_GO
```

## Authority ledger

| Boundary | Canonical responsibility | Negative boundary |
|---|---|---|
| Permission / Admission Manager | Runtime Authorization Governance, canonical authorization and invalidation mutation | no allocation, provider execution, or runtime-effect proof |
| Runtime Executor | Runtime allocation, execution-instance progression, and local eligibility | no authorization formation or mutation |
| Provider Runtime Governance | Provider binding, session, and provider eligibility | no authorization formation or mutation |
| Runtime Grant DTO | Decision record and authorization projection | cannot create or prove authorization |
| Read View | Read-only canonical-state query surface | no mutation, installation, invalidation, or replacement |
| Evaluation / Verifier | Scoped descriptive verification | no authorization mutation or authority creation |
| Tests | Adversarial and regression verification | no runtime authority |
| Mechanical record producers | Records of their own outputs | records do not become runtime authority |

Mandatory governance fields:

```text
Canonical Function = Runtime Authorization Governance
Semantic Owner = Permission Governance / Brain policy boundary for prerequisite policy meaning
Admission / Authorization Owner = Permission / Admission Manager
Mutation Owner = Permission / Admission Manager canonical governed transition
Execution Authority = Runtime Executor / Provider Runtime Governance within authorization and local eligibility boundaries
Verification Authority = scoped verifier/test only
Mechanical Record Authority = respective record producer
Evidence / Observation Owner = respective evidence/observation producer
Negative Boundary = Grant, Adapter, Evaluation, Read View, and downstream consumers cannot create authorization
Authority Transfer Rules = only the canonical governed transition creates active authorization; projections and reads do not transfer authority
Change Reason = close F-07 multi-authority drift and split validity/freshness reauthorization defect
Previous → Current = caller-constructible Grant authority and caller-selected state root → owner-controlled governed authorization state and canonical query root
Migration / Compatibility = Grant fields remain descriptive/defensive metadata; downstream consumes canonical state plus local eligibility
Verification Binding = P9I terminal evidence plus P9J C1-C24 whitebox readjudication
Architecture Linkage = F03/F04/F05 aligned authority boundaries; 03.7 constraint governance, 03.8 version/invalidation, 03.9 failure responsibility
```

## Record, state, and execution boundaries

The following boundaries are frozen for F-07:

- Grant DTO != authority.
- `authorization_ref` != proof.
- Read View != mutation authority.
- Caller-created Store != canonical state root.
- Serialized Grant != restored authority.
- Replay record != restored authority.
- `AUTHORIZED` != allocation, execution instance, provider session,
  invocation, or provider-effect fact.
- F-07 governed state answers whether authorization exists for the exact
  preparation subject and scope; it does not establish execution reality.

The original cross-finding principles remain aligned:

```text
F03: Resource Feasibility != Runtime Authorization
F04: Mechanical Record != Runtime Reality / Runtime Authority
F05: DTO / Record / Projection != Governed State
F07: Governed State != Governed Transition Origin
```

## Adversarial closure

```text
CALLER_CREATED_STORE_CAN_ESTABLISH_RUNTIME_AUTHORITY = NO
CALLER_CREATED_VIEW_CAN_ESTABLISH_RUNTIME_AUTHORITY = NO
CALLER_CREATED_GRANT_CAN_AUTHORIZE = NO
SELF_CONSISTENT_FORGED_PACKAGE_CAN_AUTHORIZE = NO
AUTHORIZATION_REF_ALONE_PROVES_AUTHORITY = NO

PUBLIC_RESULT_MUTABLE_STORE_EXPOSURE_COUNT = 0
CALLER_SELECTABLE_AUTHORITY_VIEW_COUNT = 0
DOWNSTREAM_MUTATION_CALLER_COUNT = 0
AUTHORITATIVE_CAPABILITY_OVERLAP = 0
MULTIPLE_FINAL_AUTHORITY = 0
```

A caller-created store can exist as an independent descriptive/test object, but
the canonical query never selects it. Only the canonical owner state occurrence
can satisfy the authorization query.

## Assurance invariant

No System Assurance implementation is introduced here.

The future read-only invariant is:

```text
Runtime progression for
(
    execution_instance_preparation_candidate_ref,
    authorization_ref,
    exact authorization scope
)
requires a matching ACTIVE AUTHORIZED occurrence in the
Permission / Admission Manager canonical authorization state.
```

Grant fields, caller-selected stores/views, and caller-created state DTOs are
not sufficient evidence.

```text
AUTHORIZATION_ASSURANCE_OBSERVABILITY = GOOD
```

## Verification evidence

P9I user-terminal evidence is recorded exactly:

```text
F07 focused = 36 passed
F01-F07 regression = 251 passed
py_compile = PASS
git diff --check = PASS
git diff --cached --check = PASS
staged = 0
unmerged = 0
tests/freeze = NOT_EXECUTED
provider/model/hardware = NOT_EXECUTED
```

P9J read-only closure:

```text
C1-C24 = 24/24 PASS
F07_FINAL_ADJUDICATION = PASS_READY_FOR_TECHNICAL_GO
FUNCTION_OVERLOAD = 0
AUTHORITATIVE_CAPABILITY_OVERLAP = 0
MULTIPLE_FINAL_AUTHORITY = 0
AUTHORIZATION_ASSURANCE_OBSERVABILITY = GOOD
```

No remote, full-repository, production-ready, provider, model, hardware, or
`tests/freeze` claim is made.

## Future architecture review note

The current owner-controlled authorization state lifetime is module-local inside
Permission / Admission Manager and is accepted for F-07.

A future F-09/F-10 review may examine execution isolation, lifecycle/reset
semantics, concurrency, process lifetime, test isolation, and mutation
integrity. That future review must not introduce a universal registry or
generic state manager, and it is not an F-07 blocker.

## Intended F-07 freeze surface

The seven implementation/test paths are:

1. `capabilities/evaluation/runtime_grant_pre_execution_authorization_controlled/engine_v1.py`
2. `capabilities/midplatform/core/runtime_executor/runtime_allocation_execution_instance_v1.py`
3. `capabilities/midplatform/permission_and_admission_manager/module/runtime_execution_grant_v1.py`
4. `capabilities/midplatform/provider_runtime_governance/provider_binding_decision_v1.py`
5. `capabilities/midplatform/provider_runtime_governance/provider_runtime_session_invocation_v1.py`
6. `capabilities/midplatform/permission_and_admission_manager/module/runtime_authorization_state_v1.py`
7. `tests/f07/test_runtime_authorization_scope_transition.py`

This closure document is the eighth intended freeze path.

```text
F07_IMPLEMENTATION_PATH_COUNT = 7
F07_DOCUMENTATION_PATH_COUNT = 1
F07_TOTAL_INTENDED_FREEZE_PATH_COUNT = 8
UNRELATED_PATH_INCLUDED = NO
```

No existing F07-specific architecture ledger required modification; this
document is the canonical F07 closure/governance record for the current
freeze-preparation step.

## Freeze preparation commands

The following commands are for the user terminal after review. They are not
executed in this phase.

```bash
cd /Users/luanlei/Desktop/Luna-Core

git diff --check
git diff --cached --check
git status --short

git add -- \
  capabilities/evaluation/runtime_grant_pre_execution_authorization_controlled/engine_v1.py \
  capabilities/midplatform/core/runtime_executor/runtime_allocation_execution_instance_v1.py \
  capabilities/midplatform/permission_and_admission_manager/module/runtime_execution_grant_v1.py \
  capabilities/midplatform/provider_runtime_governance/provider_binding_decision_v1.py \
  capabilities/midplatform/provider_runtime_governance/provider_runtime_session_invocation_v1.py \
  capabilities/midplatform/permission_and_admission_manager/module/runtime_authorization_state_v1.py \
  tests/f07/test_runtime_authorization_scope_transition.py \
  docs/architecture/governance/luna_repository_rebaseline_v1/runtime_grant_authorization_authority_f07_closure_go_v1.md

git diff --cached --name-only
git diff --cached --stat
git diff --cached --check

git commit -m "fix(runtime): close F-07 authorization authority"

git rev-parse HEAD
git rev-parse HEAD^
git log -1 --format=%s
git diff-tree --no-commit-id --name-only -r HEAD
git show --stat --oneline --summary HEAD
git diff --check
git diff --cached --check
git status --short
git diff --name-only --diff-filter=U
```

The user terminal should confirm that exactly eight paths are staged and that no
unrelated untracked path is staged. No push is implied.

## Notion sync payload summary

The following is a payload summary only; Notion is not modified in this phase.

- **03 — Canonical Architecture:** F-07 Runtime Authorization is a distinct
  governed boundary. Authorization state does not imply allocation, execution,
  or provider effect.
- **03.7 — Constraint Governance:** Permission / Admission Manager owns the
  canonical authorization transition. Runtime and Provider boundaries enforce
  supplied authorization and local constraints without becoming authorization
  owners.
- **03.8 — Version / Invalidation:** authorization state is scoped by
  preparation subject and authorization occurrence; canonical invalidation is
  owner-controlled. Scope mismatch and local runtime failure do not mutate
  authorization.
- **03.9 — Failure Responsibility:** Grant/adapter/projection failures return
  to their record or consuming boundary. Failure cannot fabricate an authorized
  transition; execution refusal is distinct from authorization invalidation.
- **TODO:** future F-09/F-10 review of module-local state lifetime, isolation,
  reset, concurrency, process lifetime, and mutation integrity. Do not create a
  global registry or reopen F-07 without a concrete bypass.

## Pre-freeze status

```text
F07_TECHNICAL_STATUS = GO
F07_ENGINEERING_STATUS = NOT_YET_FROZEN
TESTS_RERUN = NO
TESTS_FREEZE_RESULT = NOT_EXECUTED
PROVIDER_MODEL_HARDWARE_RESULT = NOT_EXECUTED
REMOTE_STATUS = NOT_CLAIMED
```

