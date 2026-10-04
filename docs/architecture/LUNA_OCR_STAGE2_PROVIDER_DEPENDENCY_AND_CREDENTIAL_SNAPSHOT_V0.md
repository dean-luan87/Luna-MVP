# LUNA — OCR Stage-2 Provider Dependency & Credential Snapshot v0

## Phase

- **Phase-Mainline-GuardedTrial-010**

## Dependencies

- Static **import availability** checks for common OCR-related libraries (`numpy`, `cv2`, `onnxruntime`, etc.).
- **No** OCR model load or inference.

## Credentials

- Optional cloud-related keys may be **presence-checked** only.
- **Must never** log secret values (`secret_values_logged=false`).
- Local/offline OCR paths may treat credentials as **not_required** when no cloud provider is selected.
