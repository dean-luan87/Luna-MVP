# LUNA — OCR Stage-2 Input Sample Policy v0

## Phase

- **Phase-Mainline-GuardedTrial-010**

## Allowed inputs

- `--input-image` must be an **absolute path** to a **regular file**.
- Extensions: `.png`, `.jpg`, `.jpeg`, `.webp`.

## Forbidden inputs

- Camera index, RTSP/HTTP streams
- PDF/DOC/TXT/JSON/YAML as image substitute
- Video files
- Missing paths or directories

## Processing boundary

- Allowed: existence, extension, size, SHA-256 integrity hash.
- Forbidden in this phase: decode pixels for OCR, invoke OCR.
