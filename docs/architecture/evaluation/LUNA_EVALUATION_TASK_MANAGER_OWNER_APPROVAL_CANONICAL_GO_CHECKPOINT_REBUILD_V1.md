# Canonical GO Checkpoint Rebuild v1 — Evaluation

Phase: `Phase-Midplatform-Task-Manager-Owner-Approval-Canonical-GO-Checkpoint-Rebuild-v1-001`

1. Top-down scan 26 stages (A–F groups)
2. Generate per-stage canonical checkpoints under `checkpoints/<stage_key>/`
3. Produce centralized gap classification and repair plan
4. Do not overwrite original stage artifacts

After completion: review `first_failed_stage_review_v1.json` and `canonical_checkpoint_gap_classification_v1.json` to choose repair option A/B/C/D.
