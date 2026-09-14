# Synthetic sandbox and Scenario 12

The sandbox is a deterministic scenario harness, not Docker, a VM, a process
sandbox, or a network sandbox. It uses `synthetic=true`, `controlled=true`, and
`no_real_*_effect=true` records.

It covers normal completion, governance block, authorization failure, runtime
failure, provider failure, and lifecycle control. Scenario 12 keeps independent
signage and human-flow provider lineages. Their results are opaque synthetic
refs only; no OCR, VLM, detector, camera, SLAM, YOLO, model, or world semantic
payload is produced.
