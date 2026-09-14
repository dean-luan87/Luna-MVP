# LUNA — Phone Local Field Batch 001 Runbook v0 (Phase-PhoneLocalFieldBatch-001)

## Purpose
Provide a step-by-step operational runbook to collect and process a batch of **new phone-recorded** Option A sidewalk videos through the existing `phone_local_controlled_capture` toolchain.

This runbook does not add runtime; it only uses existing tools.

## Hard boundaries (repeat)
- No realtime upload; no controlled_live_stream.
- No full controlled trial; no open user testing.
- No default-on; no execution authority.
- No crossing streets; no complex intersections; no high-density crowds.
- Avoid privacy-sensitive areas; do not intentionally capture close-up faces.

## A) Phone capture checklist (before recording)
- Confirm environment allowed: daylight, dry weather, safe sidewalk segment, low crowd density.
- Confirm privacy area checked: avoid sensitive storefronts/homes; do not follow people.
- Confirm scenario: Option A short walk observe-only, no crossing.
- Start recording while standing still for ~1–2 seconds.

## B) Recording procedure (per sample)
- Record 30–60 seconds.
- Keep camera stable; avoid rapid pans.
- End recording while standing still for ~1–2 seconds.
- Do not edit/trim; keep original file.

## C) Transfer to Mac
Transfer files via AirDrop / cable / local transfer (manual). Do not upload to public services as part of this phase.

Recommended destination:
- `input_videos/phone_local_batch_001/`

Recommended names:
- `phone_local_001_clear_path.mp4`
- `phone_local_002_minor_obstacle.mp4`
- `phone_local_003_narrow_path.mp4`
- `phone_local_004_people_far.mp4`
- `phone_local_005_low_confidence_safe.mp4`

## D) Batch processing (bundle→archive→validator)
Run from repo root:

```bash
cd "/Users/luanlei/Desktop/Luna-Core"
TS=$(date +%Y%m%d_%H%M%S)

python3 tools/run_phone_local_field_batch_001_v0.py \
  --input-dir input_videos/phone_local_batch_001 \
  --output-root "logs/phone_local_field_batch_001_$TS" \
  --operator-id dean \
  --safety-observer-id observer \
  --record-owner-id dean \
  --timebox-ms 30000
```

Outputs:
- `logs/phone_local_field_batch_001_<timestamp>/batch_summary.json`
- `logs/phone_local_field_batch_001_<timestamp>/sample_matrix.json`
- `logs/phone_local_field_batch_001_<timestamp>/bundles/<sample_id>/...`
- `logs/phone_local_field_batch_001_<timestamp>/archives/<sample_id>/...`

## E) Post-run review (what to inspect)
For each sample (in `sample_matrix.json`), verify:
- bundle validator recommendation = `go`
- archive validator recommendation = `go`
- `evidence_type=phone_local_controlled_capture`
- `controlled_live_stream=false`
- `phone_local_capture=true`
- `pending_real_sidewalk_run=true`
- no hard blockers

## F) Stop conditions
Stop this phase when:
- At least 3 newly recorded samples are processed end-to-end with validator=go, OR
- A clear no_go condition occurs (boundary confusion, safety assertion failure, unverifiable archive, lineage loss).

