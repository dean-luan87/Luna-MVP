# LUNA YOLO Stage-1 Offline Trial Regression v0

- Phase: Phase-Mainline-GuardedTrial-007
- Scope: YOLO Stage-1 offline video only regression aggregation (005-Fix + 006-Rerun).
- Non-goals: OCR / MidPlatform / downstream / navigation / TTS / Qwen / world write / hive upload / camera runtime.

## Inputs
- 005-Fix (10-frame) output root
- 006-Rerun (50/100/200 multi-window) output root
- Optional historical initial roots (005 initial NO_GO, 006 initial CONDITIONAL_GO)

## Outputs
- Regression summary
- Phase matrix
- Window matrix
- Boundary summary
- Hard audit summary
- Closure recommendation (closed_v0)
