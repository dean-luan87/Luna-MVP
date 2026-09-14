# Cognitive Chain Audit

## Sufficient Case A

The required chain is replay input → Gateway admission → A-Route → Attention →
Hypothesis → Current World Candidate → `SUFFICIENT` → canonical Stop. The
audit requires no Gap, Re-observation, or next-cycle ingress and checks that
the stop follows the sufficient state.

## Multi-cycle Case B

The required chain is Cycle 1 evidence → `INSUFFICIENT` → canonical Gap →
canonical Re-observation → next-cycle ingress, followed by Cycle 2 new
evidence → Hypothesis Revision → `SUFFICIENT` → Stop.

The audit compares actual refs, not merely field presence, and requires shared
execution/cycle identity where the artifact exposes it.
