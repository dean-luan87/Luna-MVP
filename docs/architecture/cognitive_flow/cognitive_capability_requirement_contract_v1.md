# Cognitive Capability Requirement Contract v1

A cognitive need is translated into a capability requirement, never a direct model call.

```json
{"cognitive_need":"environment_obstacle_understanding","required_evidence":["spatial_structure","object_presence","confidence"],"priority":"candidate","constraints":{}}
```

Fields include request id, intent reference, evidence requirement, capability reference, constraints, and trace. Brain/A Route know evidence needs, not YOLO, SAM, OCR, or provider internals.
There is no direct model call from a cognitive capability requirement.
