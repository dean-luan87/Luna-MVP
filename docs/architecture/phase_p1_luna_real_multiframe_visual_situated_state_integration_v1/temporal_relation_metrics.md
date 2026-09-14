# Temporal Visual Relation Metrics

For each real provider observation, the Runner retains bbox and actual frame
dimensions, then computes normalized candidates:

- bbox center and normalized center `(cx / frame_width, cy / frame_height)`;
- normalized width and height;
- bbox area ratio;
- cross-frame center delta and Euclidean center distance;
- cross-frame normalized size delta;
- cross-frame area delta.

Raw pixel coordinates are not compared across frames. Metrics are derived only
when both observations contain valid bbox and frame geometry. They remain
candidate measurements and do not imply motion truth or object identity.
