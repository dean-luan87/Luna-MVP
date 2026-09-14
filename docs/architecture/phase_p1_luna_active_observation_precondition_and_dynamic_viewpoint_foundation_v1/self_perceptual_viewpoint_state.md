# Self perceptual viewpoint state

`SelfPerceptualViewpointStateV1` is a time-bounded candidate projection of the
existing Self State Awareness model. It carries orientation, motion, stability,
current view, visible regions, and sensor availability references.

Self State answers “what is my current perceptual condition?” It does not
decide whether OCR should run, select a Goal, choose a Target, move the device,
or issue an Action. The reducer remains the Self State mutation authority; this
phase produces no state mutation.

The controlled fixture uses categorical values only. It does not claim a real
camera, head-pose, IMU, or motion measurement.

