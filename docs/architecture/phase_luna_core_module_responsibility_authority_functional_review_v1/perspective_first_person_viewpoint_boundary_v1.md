# Perspective / First-Person Viewpoint Boundary v1

Physical first-person camera viewpoint and cognitive Perspective are separate.

- Camera pose, geometry, SLAM, and visual framing belong to Perception/Field
  sources.
- Cognitive Perspective may be self-centered, other-centered,
  organization-centered, task-conditioned, or social.
- A first-person camera frame does not prove a self-centered cognitive
  Perspective.

Perspective may consume perception refs, but it must not own camera geometry,
SLAM, identity recognition, face recognition, or speaker recognition.
