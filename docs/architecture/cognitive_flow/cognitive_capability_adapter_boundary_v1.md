# Cognitive Capability Adapter Boundary v1

Visual, Language, and Audio Adapter skeletons have one responsibility: emit declared synthetic Evidence Candidates.

```text
Adapter Skeleton -> Evidence Candidate -> Cognitive Flow
```

They do not infer final situation/intent, call an external source, invoke a model, control a device, or bypass Evidence Admission.

