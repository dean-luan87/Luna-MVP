# A Route Perception / Observation Gateway Controlled Integration v1

## Scope

This phase creates one narrow canonical owner: **Observation Gateway Governance**. It normalizes typed provider/user ingress into candidate evidence, forms non-authoritative Observation Candidates, admits or defers them, preserves temporal/correction/contradiction lineage, and emits routing candidates for existing owners and A Route Orchestration.

It does not implement vision, OCR, audio, SLAM, model calls, provider execution, Field mutation, Context assembly, Attention state, world truth, or downstream semantic interpretation.

## Semantic boundary

`Raw Input != Provider Output != Perception Evidence != Observation Candidate != Admitted Observation != Fact != Field State != Current World != Context != Attention != Hypothesis != Intent != Decision != Action`. An `ADMITTED_OBSERVATION` means only that the candidate is structurally admissible for downstream consumers. It never declares external reality true. OCR remains text evidence, visual detection remains a detection candidate, and SLAM remains spatial/geometric evidence.

## Lifecycle and routing

Ingress is normalized into `PerceptionEvidenceV1`, then an `ObservationCandidateV1` is formed. Admission states include `RECEIVED`, `NORMALIZED`, `EVIDENCE_READY`, `OBSERVATION_CANDIDATE_READY`, `NEEDS_CONFIRMATION`, `CONTESTED`, `ADMITTED_OBSERVATION`, `REJECTED`, `REVOKED`, `EXPIRED`, and `SUPERSEDED`.

Routing targets are candidate metadata only. Field, Context, Attention, Hypothesis, Intent influence, Safety, Cognitive Flow, and A Route Orchestration retain their own authority and mutation boundaries.

## A Route adapter

The gateway emits `a-route-ingress:<scenario_id>` when an observation is structurally admitted. This is a typed ingress reference for the existing A Route Orchestration backbone; it does not modify orchestration or bypass its lifecycle.

## Status

Synthetic controlled integration candidate only. Real providers, persistence, semantic compression, Emotion Engine, and B Route remain deferred.

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
