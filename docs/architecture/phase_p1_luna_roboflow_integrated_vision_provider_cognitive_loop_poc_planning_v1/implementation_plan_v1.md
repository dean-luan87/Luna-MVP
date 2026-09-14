# Future Implementation Plan

This document is a plan only; no implementation is authorized by this phase.

## Step 1 — declaration and adapter inventory

Add a repository-backed Roboflow Provider declaration only under the existing
Provider Governance registry conventions. Add model/workflow and capability
compatibility declarations under their existing owners. Do not create a
Roboflow registry or selector.

## Step 2 — no-runtime adapter

Implement a narrow Roboflow Provider adapter behind the existing Provider
admission/result boundary. It should accept an admitted Observation request,
canonical upstream refs, and an external request contract; it must return a
Provider Result or a typed failure without source mutation.

## Step 3 — evidence translation

Translate object detection and OCR outputs into existing candidate evidence
families. Keep raw schema private to the adapter and preserve frame/ROI,
provider/model/workflow, versions, confidence, uncertainty and provenance.

## Step 4 — cognitive return seam

Connect admitted evidence to the existing Current World candidate/B1-B2
read-only input and A/hypothesis/sufficiency boundary. Use the existing
information-gap and re-observation candidate mechanisms. Do not force
Decision/Task/Action into the primary test.

## Step 5 — controlled verification

Build a caller-aware, candidate-only PoC verifier with happy path and negative
cases: missing provenance, stale result, conflicting detection/OCR, missing
ROI, provider error, revoked constraint, no evidence, and insufficient exit
evidence. It must inspect actual wiring and must not assert a hardcoded exit.

## Likely future files

- existing Provider registry/declaration extension;
- one Roboflow adapter under the existing FPO/provider integration boundary;
- one external-result-to-evidence translation adapter if the existing OCR
  shape cannot be reused;
- one caller-aware PoC runner/verifier;
- phase documentation and trace scenario manifest.

## Explicitly not planned

No new Manager, Provider Selector, Model Selector, scheduler, planner,
Memory/Experience architecture, UI, camera service, long-running video path,
or production deployment.

