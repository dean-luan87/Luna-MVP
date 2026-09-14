# Change Manifest

## Modified

- Existing Capability Registry: added the object-detection Slot declaration.
- Existing Model Registry: added the YOLO11n Model declaration.
- Existing Provider Registry: added the YOLO local Provider declaration.
- Governed-record producer: reads declaration registries and binding records.

## Added

- Capability↔Model binding registry.
- Model↔Provider binding registry.
- Declaration baseline validator, Runner, and Verifier.
- Phase documentation.

## Not changed

- canonical owners;
- canonical enums/types;
- Runtime Admission production;
- model loading or Provider invocation;
- Observation, Action, Field, Current World, or Brain state.

