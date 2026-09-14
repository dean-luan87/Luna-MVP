# Integration Mapping

## Canonical path

1. `RealProviderExecutionEngineV1` performs the existing local YOLO11n
   Provider Runtime call.
2. Its native detection and visual evidence candidates remain the source
   records. Runtime Observation and Evidence references are retained.
3. `VisualEvidenceFieldProjectionCandidateV1` projects those references into a
   Field-compatible candidate. Its `region_ref_candidate` remains a detection
   image-region candidate.
4. `FieldEventCandidateV1` is formed only when an explicit Field context
   reference is available. This event is still candidate-only.
5. `admit_field_event(...)` performs the existing structural and temporal
   admission. No `admitted=true` value is used to bypass that API.
6. The admitted `reducer_input_candidate` passes through
   `FieldKernelReducerAdapterV1` and then to the existing candidate-only Field
   State Reducer Module.

## Authority

Field Event Admission owns event admission. Field State Reducer remains the
sole Field State transition/mutation authority. The current Reducer Module is a
controlled candidate skeleton: it does not persist state, admit facts, invoke
providers, or trigger actions.

The existing Reducer evidence contract may require more than one admitted
event/source before it builds a Field State candidate. This integration does
not fabricate a second event or source to satisfy that contract. A legal
admitted visual event may therefore end at the Reducer `insufficient_evidence`
candidate boundary while still proving that the canonical input/admission path
was respected.

## Unresolved path

An empty `field_ref_candidate` is represented as
`field_ref_resolution_status=UNRESOLVED`. No Field Event is formed, no event is
admitted, and no reducer input is produced. This is fail-closed behavior, not a
Field absence claim.
