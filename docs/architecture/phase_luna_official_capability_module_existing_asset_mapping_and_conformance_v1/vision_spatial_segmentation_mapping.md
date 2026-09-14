# Vision, spatial, segmentation, and face mapping

`object_detection` maps to common object/environment awareness and the
existing `detection_v1` dependency. `spatial_mapping` maps to the existing
SLAM/spatial capability and `slam_v1`; this does not establish a distinct VIO
or trajectory Module. `mobile_sam_v1` is a model asset with segmentation
metadata, but no authoritative Module record was found. Face-related assets
likewise lack a canonical official Module record. Both remain explicit review
gaps.

The S3 YOLO11n path is a bounded provider/model evidence path and is not a
`YOLO Capability Module`.
