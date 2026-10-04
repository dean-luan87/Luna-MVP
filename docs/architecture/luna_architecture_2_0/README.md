# Luna Architecture 2.0 — historical predecessor material

ARCHITECTURE_2_0_STATUS=HISTORICAL_NONCURRENT  
CURRENT_ARCHITECTURE_LINE=Architecture 3.0  
CURRENT_ARCHITECTURE_ENTRYPOINT=docs/architecture/luna_architecture_3_0/README.md

The current canonical architecture entrypoint is [Architecture 3.0](../luna_architecture_3_0/README.md). Architecture 2.0 is retained for historical lineage, architecture evolution evidence, Architecture 3.0 predecessor material, and historical contract, owner and semantic ledgers. Architecture 2.0 material does not automatically carry normative authority into Architecture 3.0.

The statuses, responsibility layering, ledgers and backlog below describe the historical Architecture 2.0 development state; they do not designate the current architecture line or override Constitution 3.0 / Architecture 3.0.

## Historical Architecture 2.0 status

CONSTITUTION_VERSION=Architecture 2.0 Constitution v1  
CONSTITUTION_STATUS=FROZEN  
CONSTITUTION_RULES=C01-C48  
SOURCE_LINEAGE_COVERAGE=162/162  
CANONICAL_ARCHITECTURE_STATUS=DESIGN_IN_PROGRESS  
CANONICAL_ARCHITECTURE_FROZEN=NO

PREDECESSOR=[Luna Canonical Architecture Freeze v1](../luna_canonical_architecture_freeze_v1/README.md)  
PREDECESSOR_STATUS=HISTORICAL_FROZEN_BASELINE  
RELATION=SUPERSEDED_FOR_CURRENT_ARCHITECTURE_DEVELOPMENT

Supersession does not invalidate, delete, or retroactively rewrite historical Architecture Truth. The predecessor remains a historical frozen baseline; this directory records the historical Architecture 2.0 development line. Constitution freeze does not imply current-code conformance or Canonical Architecture freeze. No production remediation, PR-ADMISSION-02 resumption, or Grounding DINO implementation is authorized by these documents.

## Historical architecture documents

- [Architecture 2.0 Constitution v1](architecture_2_0_constitution_v1.md): frozen C01–C48 wording, effective 2026-09-30.
- [Canonical Architecture v0.2](canonical_architecture_v0_2.md): ACM-02 Batch 01 lineage and Batch 02 reconciled D01–D16, two planes, authoritative questions, boundary decisions and open gaps.
- [Canonical Object / Fact / State Ledger v0.1](canonical_object_fact_state_ledger_v0_1.md): Batch 03; OC-01–OC-12 and fact-level boundaries.
- [Canonical Owner / Authority Matrix v0.1](canonical_owner_authority_matrix_v0_1.md): Batch 04; nine responsibility roles and Q01–Q24.
- [Canonical Contract Ledger v0.1](canonical_contract_ledger_v0_1.md): Batch 05; CC-01–CC-26.
- [Semantic Mapping Ledger v0.1](semantic_mapping_ledger_v0_1.md): Batch 06; MAP-01–MAP-25 and protocol-governance reconciliation.
- [Temporal / Validity / Currentness Ledger v0.1](temporal_currentness_validity_ledger_v0_1.md): Batch 07; T-01–T-14, TV-01–TV-16, TM-01–TM-10 and Owner currentness semantics.
- [Identity / Reference / Provenance Ledger v0.1](identity_reference_provenance_ledger_v0_1.md): Batch 08; I-01–I-12, REF-01–REF-12, RI-01–RI-20, PV-01–PV-08 and lineage/reference validity semantics.
- [Governance Integration v0.1](governance_integration_v0_1.md): Pass 01, A2.0-150–163; L0–L5 layering, rule applicability, conflict/evidence routing, and existing ES/EA/WF/TP integration. Candidate only; Batch 09 remains paused.

All D/OC/R/CC/MAP/temporal/identity ledgers remain design candidates, not frozen, implemented, or production-conformant. ACM-02 Batch 01–08 are documented at the canonical level; this does not authorize implementation. [Current Code Architecture Census](../audits/luna_current_implemented_architecture_census_v1.md) is implementation evidence, not target Architecture Truth.

## Normative responsibility layering

| Surface | Responsibility |
| --- | --- |
| 03.7 / Architecture 2.0 | Canonical semantic meaning, Domains, Objects, Owners/Authorities, Canonical Contracts, Semantic Mappings |
| 06.1 | Model/Version factual records |
| 06.2 | Engineering realization rules: provider/adapter/harness implementation and concrete technical integration |
| 06.4 | Interface/protocol evolution governance: version, compatibility, freeze, migration and impact |
| 06.5 | Experiment, failure, audit and runtime evidence |

Canonical Contract is not a Python DTO, API endpoint, wire protocol, or implementation call graph. Semantic Mapping is not a transport protocol. Architecture 2.0 MUST NOT create a second protocol-management system. No ProtocolManager, MappingManager, ArchitectureRegistry, or second freeze system is created or authorized.

## Open backlog

CA-GAP-01 is `OPEN_NARROWED`; CA-GAP-02, CA-GAP-03, CA-GAP-05 and CA-GAP-06 remain OPEN. CA-GAP-04 and CA-GAP-07 are `RESOLVED_AT_CANONICAL_LEVEL` only; neither is implemented or runtime-closed. Five Canonical gaps remain open. `IMPL-AUDIT-TEMPORAL-01=NOT_STARTED` and `IMPL-AUDIT-RESTART-01=NOT_STARTED`. IMPL-NC-01 remains OPEN; target CC-06 / MAP-05, canonical class `INVALID_SEMANTIC_LINEAGE + REFERENCE_ROLE_SUBSTITUTION` (historical shorthand: `SEMANTIC_DRIFT + FABRICATED_LINEAGE`). There is no code remediation authorization.

## Source and status

Repository-side transcription of [Notion 03.7 Architecture 2.0, A2.0-58, A2.0-71–163](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), read 2026-09-30. The frozen Constitution wording is reproduced unchanged in its own file. The ACM-02 ledgers reflect Batch 01–08; A2.0-150–163 is a candidate governance integration pass, not Batch 09 or a second normative source. Future adjudication follows the source architecture governance and must not silently rewrite C01–C48.
