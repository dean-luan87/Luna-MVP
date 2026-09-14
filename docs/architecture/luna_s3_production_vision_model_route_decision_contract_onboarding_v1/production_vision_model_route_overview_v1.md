# S3 Production Vision Model Route Decision and Contract Onboarding

This phase onboards YOLOv5n, YOLO11n, and YOLO26n into the existing Model
Manager / Model Contract Repository. It does not execute inference, download
weights, or alter S3 observation-control or evidence semantics.

The route roles are fixed as candidates only:

- YOLOv5n: `LEGACY_REFERENCE`
- YOLO11n: `STABILITY_COMPARATOR`
- YOLO26n: `PRIMARY_CANDIDATE`

`PRIMARY_CANDIDATE` is not `BEST_FIT` and is not production approval. Local
YOLO11n and YOLO26n weights are not present in the inspected repository-visible
asset locations, so their route admission remains blocked by asset presence.
