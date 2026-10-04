# Architecture 2.0 — Temporal / Validity / Currentness Canonical Ledger v0.1

BATCH=ACM-02 07  
STATUS=TEMPORAL_CURRENTNESS_LEDGER_CANDIDATE  
CANONICAL_ARCHITECTURE_FROZEN=NO  
TEMPORAL_CONCEPT_COUNT=14  
TEMPORAL_INVARIANT_COUNT=16  
TEMPORAL_MAPPING_RULE_COUNT=10  
GLOBAL_CURRENTNESS_OWNER=NO  
LATEST_RECORD_IMPLIES_CURRENT=NO  
NOT_EXPIRED_IMPLIES_CURRENT=NO

Repository-side transcription of [Notion 03.7 Architecture 2.0, A2.0-127–137](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), read 2026-09-30. This ledger records canonical semantic vocabulary and contract obligations, not a Python enum, runtime DTO, implementation, or production conformance. The [frozen Constitution v1](architecture_2_0_constitution_v1.md) remains unchanged.

### A2.0-127｜ACM-02 Batch 07 — Temporal / Validity / Currentness Canonical Ledger
**STATUS:** TEMPORAL_CURRENTNESS_LEDGER_CANDIDATE
**INPUT:** C27/C28/C32/C42/C43/C44; D03/D07/D10/D11/D12/D16; CC-08/10/13/15/16/24/25; MAP-07/09/12/14/15/23/24
**CONSTITUTION_BASE:** C01–C48 FROZEN
**CODE_CHANGE_AUTHORIZED:** NO
Temporal facts, validity and currentness are distinct semantic dimensions. A timestamp is not a currentness proof. An expiry reference is not an interpreted expiry. The latest record is not automatically the current record.

### A2.0-128｜Canonical Temporal Concepts
**T-01 OBSERVED_TIME**
When an observation/sensing act sampled or captured its source, under the observation contract.
Owner: source observation/execution semantics.
Does not mean the represented world event occurred at that exact time.
**T-02 OCCURRED_TIME**
When the represented event is asserted/estimated to have occurred in the represented domain.
May be unknown, interval-valued, estimated or source-declared.
Must not be fabricated from observed_time.
**T-03 EFFECTIVE_TIME**
When a fact/state/change is semantically effective for the target domain.
May equal occurred_time only when explicitly bound by contract.
Critical for Field reduction and state supersession.
**T-04 RECEIVED_TIME**
When a target boundary/system received the information.
Operational/provenance fact.
Does not establish occurred/effective time.
**T-05 RECORDED_TIME**
When a record was persisted/registered.
Custody/history fact.
Does not establish semantic currentness.
**T-06 DECISION_TIME**
When an Authority issued a decision.
Does not by itself define the entire validity interval.
**T-07 EFFECT_TIME**
When an authorized effect is attempted/performed.
Effect-time authorization dependencies must be current according to the effect contract.
**T-08 VALID_FROM / VALID_UNTIL**
Bounded validity interval for an object/decision/state when the domain contract defines one.
Absence of VALID_UNTIL does not mean perpetual validity.
**T-09 EXPIRY**
A validity-ending condition based on time or interpreted expiry semantics.
Expiry may be absolute time, duration from a defined anchor, lease/session lifetime, or another explicitly governed temporal condition.
An expiry_ref without an Owner-governed interpretation is not sufficient.
**T-10 INVALIDATION**
An Owner/Authority-governed event/decision that makes a previously usable semantic object no longer valid/current for a defined scope.
Invalidation may occur before expiry.
**T-11 SUPERSESSION**
A governed relation in which a later/stronger/authoritative semantic object replaces another for a defined scope.
Supersession is not mere chronological laterness.
**T-12 STALENESS**
A consumer/domain judgment that information may be too old or insufficiently refreshed for a specified use.
Staleness is purpose/scope dependent.
Stale != false; stale != invalid unless the contract says so.
**T-13 CURRENTNESS**
Owner-governed answer to:
“Is this object/state/decision the presently authoritative usable state for this subject/scope under this domain contract?”
Currentness is not a timestamp field.
Currentness may depend on validity, invalidation, supersession, lifecycle state, reconciliation state, required dependencies and domain-specific rules.
**T-14 TEMPORAL_UNCERTAINTY**
Explicit uncertainty about observed/occurred/effective/validity time or ordering.
Must survive mappings when material to downstream semantics.

### A2.0-129｜Temporal Non-Equivalence Invariants
TV-01 OBSERVED_TIME != OCCURRED_TIME by default.
TV-02 OCCURRED_TIME != EFFECTIVE_TIME by default.
TV-03 RECEIVED_TIME != OBSERVED_TIME by default.
TV-04 RECORDED_TIME != CURRENTNESS.
TV-05 DECISION_TIME != VALIDITY_INTERVAL.
TV-06 LATEST_TIMESTAMP != CURRENT_STATE.
TV-07 VALID != CURRENT by default.
TV-08 NOT_EXPIRED != CURRENT by default.
TV-09 EXPIRED implies unusable only within the contract scope that defines expiry.
TV-10 INVALIDATED != HISTORICALLY_FALSE; history remains intact.
TV-11 SUPERSEDED != DELETED.
TV-12 STALE != FALSE.
TV-13 UNKNOWN_TIME != NOW.
TV-14 missing timestamp must not be filled with receipt/record time unless the target semantic role explicitly is receipt/record time.
TV-15 temporal ordering alone cannot create Authority or semantic precedence.
TV-16 clock time/monotonic/process-local counters are implementation mechanisms; their semantic use requires a contract.

### A2.0-130｜Validity State Vocabulary
Canonical architecture permits the following semantic answers where a domain needs validity:
VALID
INVALIDATED
EXPIRED
SUPERSEDED
NOT_YET_VALID
UNKNOWN_VALIDITY
NOT_APPLICABLE
This is not a universal runtime enum requirement. Domains may realize narrower state vocabularies, but must not collapse materially distinct states when downstream behavior depends on the distinction.
Currentness answers where required:
CURRENT
NOT_CURRENT
UNKNOWN_CURRENTNESS
NOT_APPLICABLE
Again, this is semantic vocabulary, not a mandated DTO enum.
Rule:
VALID does not automatically imply CURRENT.
CURRENT normally requires valid/not-invalidated/not-superseded plus domain-specific currentness basis, but each Owner contract defines exact requirements.

### A2.0-131｜Owner Currentness Model
There is NO Global Currentness Owner.
For each OC-06 or decision whose currentness matters, the Canonical Contract must identify:
SUBJECT_IDENTITY
SCOPE
CURRENTNESS_QUERY_OWNER
VALIDITY_BASIS
INVALIDATION_OWNER
SUPERSESSION_RULE
TEMPORAL_BASIS
RECONCILIATION_REQUIREMENT_IF_ANY
UNKNOWN_BEHAVIOR
DEPENDENT_EFFECTS.
A dependent domain may:
- query an Owner-governed currentness projection;
- consume a versioned currentness result under an explicit freshness/validity contract;
- cache a projection only when cache semantics are governed.
A dependent domain may not:
- infer currentness from latest row/file/event;
- infer currentness from successful prior use;
- infer currentness from an unexpired timestamp alone;
- self-repair unknown currentness by assuming true.

### A2.0-132｜Domain Temporal / Currentness Allocation
**D03 Lifecycle & Availability**
Owns lifecycle/current availability for governed assets.
Activation time, transition time and availability observation are distinct.
ACTIVE is a lifecycle/current state, not permanent eligibility.
Restart cannot infer ACTIVE merely from a historical declaration/record unless D03 reconciliation contract permits it.
**D07 Permission & Effect Authorization**
Entry Admission and Runtime Effect Authorization have separate validity/currentness.
A Grant/Decision must define subject/effect/scope plus validity/invalidation semantics.
Effect-time authorization must interpret required dependency currentness at CC-08/09.
An expiry_ref string/object identity alone is insufficient.
D07 does not become Owner of D03/D06/D08 currentness; it consumes their governed answers.
**D10 Observation / Evidence**
Observation temporal provenance must preserve observed/source/received roles where known.
Evidence admission does not convert observation time into world-event time.
Evidence can remain historically valid Evidence while no longer sufficiently fresh for a current-world use.
**D11 Field**
Field event formation must preserve/derive occurred/effective semantics explicitly.
Reducer/state formation uses governed effective/supersession/conflict rules, not “last timestamp wins”.
Historical events remain history after supersession/invalidation.
Field Current State currentness belongs to D11.
**D12 Current World**
Current World is a projection with its own formation/currentness judgment.
It may require current D11 state and sufficiently applicable Evidence/Context, but it does not own source currentness.
Projection can become NOT_CURRENT even while source historical records remain valid.
**D16 Memory & Experience**
Memory preserves historical temporal meaning.
Retrieval recency is not world currentness.
A memory may be valid history and stale/inapplicable for present reasoning.
Memory revision/supersession preserves prior history/provenance.
**P-D Restart/Reconciliation**
Restart/process loss cannot globally reset or restore currentness.
Each stateful Owner re-establishes or answers its own state under CC-25.
Until required reconciliation succeeds, dependent currentness may be UNKNOWN_CURRENTNESS.
Process-local in-memory existence is not canonical currentness.

### A2.0-133｜Effect-Time Dependency Rule
For every effect-authorizing contract, dependencies are classified per effect as:
STATIC_IDENTITY_OR_DECLARATION
CURRENT_STATE_REQUIRED
VALIDITY_REQUIRED
EFFECT_TIME_RECHECK_REQUIRED
OPTIONAL_CONTEXT
NOT_APPLICABLE.
There is no universal rule that every dependency must be re-read immediately before every effect.
There is also no universal rule that an earlier successful check remains valid.
The contract must declare which dependencies require effect-time recheck and what counts as a sufficiently current Owner answer.
This resolves the architectural shape of CA-GAP-02 without prematurely enumerating every implementation dependency.

### A2.0-134｜Temporal Mapping Rules
TM-01 Source temporal roles survive mapping unless explicitly transformed with basis.
TM-02 A mapping may derive target EFFECTIVE_TIME only from declared source semantics/rules.
TM-03 RECEIVED_TIME may always be added as target provenance, but cannot overwrite source time.
TM-04 TARGET_CURRENTNESS is always a target Owner judgment when required; it is never copied.
TM-05 Validity may be preserved only when source and target validity semantics are proven equivalent; otherwise target validity is newly judged.
TM-06 Expiry must carry an interpretable anchor/unit/condition or governed reference to them.
TM-07 Temporal uncertainty/conflicting clocks/order ambiguity remain explicit if material.
TM-08 Remote transport delay may affect received_time/freshness but cannot silently redefine observed/effect time.
TM-09 Restart/replay must distinguish historical recorded order from semantic effective order.
TM-10 Evaluation replay time is not original runtime time unless explicitly modeled as a new observation/effect.

### A2.0-135｜CA-GAP-04 Adjudication
Previous gap:
CA-GAP-04 Expiry / Temporal Validity.
Architecture-level semantic gap is now sufficiently resolved:
- canonical temporal roles defined;
- validity vs currentness separated;
- expiry semantics bounded;
- Owner currentness model defined;
- effect-time dependency rule defined;
- mapping/restart temporal rules defined.
Therefore:
CA-GAP-04_ARCHITECTURE_STATUS=RESOLVED_AT_CANONICAL_LEVEL.
However implementation conformance is NOT established.
The existing runtime grant expiry interpretation and concrete effect-time checks must later be mapped/audited against this ledger.
Create implementation reconciliation item:
IMPL-AUDIT-TEMPORAL-01
Question: Do RuntimeExecutionGrantV1 and all effect-authorizing paths implement interpretable validity/expiry/currentness and effect-time dependency semantics without ref-only or recency inference?
Status: NOT_STARTED.
Do not call CA-GAP-04 “implemented” or “closed in runtime”.

### A2.0-136｜CA-GAP-07 Adjudication
Previous gap:
CA-GAP-07 Restart / Process Currentness.
Architecture-level semantic gap is now sufficiently resolved:
- no global currentness owner;
- each domain Owner owns reconciliation/currentness;
- process-local state is not canonical currentness;
- unknown after restart remains unknown for dependent effects;
- CC-24/25 + TM-09 define target behavior.
Therefore:
CA-GAP-07_ARCHITECTURE_STATUS=RESOLVED_AT_CANONICAL_LEVEL.
Implementation conformance remains unproven.
Create:
IMPL-AUDIT-RESTART-01
Question: Which current implementations store authoritative state process-locally, how is state re-established after restart, and where can restart accidentally turn historical/persisted state into assumed current state?
Status: NOT_STARTED.

### A2.0-137｜Batch 07 Adjudication
- CANONICAL_TEMPORAL_CONCEPTS=14
- TEMPORAL_NON_EQUIVALENCE_INVARIANTS=16
- CANONICAL_VALIDITY_SEMANTICS_DEFINED=YES
- CANONICAL_CURRENTNESS_SEMANTICS_DEFINED=YES
- GLOBAL_CURRENTNESS_OWNER=NO
- LATEST_RECORD_IMPLIES_CURRENT=NO
- NOT_EXPIRED_IMPLIES_CURRENT=NO
- EFFECT_TIME_RECHECK=CONTRACT_SPECIFIC
- TEMPORAL_MAPPING_RULES=10
- CA_GAP_04_ARCHITECTURE_STATUS=RESOLVED_AT_CANONICAL_LEVEL
- CA_GAP_07_ARCHITECTURE_STATUS=RESOLVED_AT_CANONICAL_LEVEL
- REMAINING_OPEN_CANONICAL_GAPS=5
- NEW_IMPLEMENTATION_AUDITS=2
- RUNTIME_CONFORMANCE_ESTABLISHED=NO
- CANONICAL_ARCHITECTURE_FROZEN=NO
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
- TEMPORAL_CURRENTNESS_LEDGER_STATUS=CANDIDATE
Next: ACM-02 Batch 08 — Identity / Reference / Provenance Canonical Ledger. Define when identity is preserved vs linked vs newly formed, distinguish semantic reference from trace/provenance/reference-shaped strings, and establish admissible lineage rules across D01/D05/D06/D09/D10/D11/D16. This directly prepares final adjudication of IMPL-NC-01 and CA-GAP-01 without code changes.

## Local status and non-implementation boundary

CA-GAP-04 and CA-GAP-07 are RESOLVED_AT_CANONICAL_LEVEL only. IMPL-AUDIT-TEMPORAL-01 and IMPL-AUDIT-RESTART-01 are NOT_STARTED. The remaining open Canonical gaps are CA-GAP-01, CA-GAP-02, CA-GAP-03, CA-GAP-05 and CA-GAP-06. IMPL-NC-01 remains OPEN. This documentation does not establish runtime expiry enforcement, process-restart conformance, code remediation authorization, PR-ADMISSION-02 resumption, or Grounding DINO implementation.
