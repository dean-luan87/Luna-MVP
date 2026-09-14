# Summary

The repository now contains a callable, bounded first real-provider path for
the existing local YOLO11n provider. The first terminal run must establish
`provider_real_execution_verified=true`; until then it remains false. A
successful result must return through the existing Runtime Observation
Envelope, Gateway, A-Route, and Cognitive State Formation path with all
downstream execution flags false.

The provider admission mapping now uses the source FPO
`capability-requirement:...` reference required by the canonical admission
predicate. The provider-runtime normalization retains its separate
`provider-requirement:...` lineage identity and no admission rule is weakened.

The real-provider request now remains inside the controlled Gateway boundary
(`controlled_integration_only=true`). Source dimensions are taken from the
actual selected image: 5712x4284. Provider boxes are original-image pixel
coordinates and are not distorted to fit a 640x480 label.

Known environment dependencies are the declared local YOLO11n weights and the
installed `ultralytics` and `torch` packages. Provider quality and real-world
model performance are outside this phase.

The long-term integration standard is maintained in the [Luna External Model /
Provider Integration SOP v1](../luna_external_model_provider_integration_sop_v1.md).
