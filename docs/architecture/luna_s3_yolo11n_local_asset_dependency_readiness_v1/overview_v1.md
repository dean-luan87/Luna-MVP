# YOLO11n local asset and dependency readiness

This phase prepares the existing Model Manager / Model Governance path for a
real, externally provisioned YOLO11n asset. It does not download a weight,
install Python packages, import runtime dependencies, or execute inference.

The governed sequence is:

`physical asset → identity → existing contracts → checksum → dependency readiness → technical admission candidate`

The registered asset is `model-asset:yolo11n:weights-v1` at
`vision/detection/yolo/yolo11n.pt`. The current repository inventory found no
physical YOLO11n file, so the honest current state remains
`ASSET_NOT_PRESENT` and `ADMISSION_BLOCKED_ASSET_MISSING`.

`Model Asset Availability != Contract Resolution != Dependency Readiness !=
Execution Admission != Model Quality != BEST_FIT Recommendation`.
