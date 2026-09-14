# Single-Frame Limitations

One YOLO frame can provide a visual detection, bbox/frame geometry, and
scale-ratio candidates. It cannot establish relative motion or temporal
stability. `condition:stable-relation:v1` is therefore `UNKNOWN`.

This phase does not claim real camera state, real Self motion, real viewpoint
sensing, real relative-motion sensing, multi-frame tracking, IMU, or SLAM.
Unknown required conditions remain fail-closed and do not authorize OCR.
