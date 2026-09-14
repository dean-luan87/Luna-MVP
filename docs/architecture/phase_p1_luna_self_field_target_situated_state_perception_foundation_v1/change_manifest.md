# Change Manifest

Added:

- `SituatedConditionStateCandidateV1`;
- `SituatedStatePerceptionRequestV1` and result contract;
- input-driven situated condition derivation engine;
- controlled cases for visibility, completeness, scale, relation stability,
  unknown state, dynamic transitions, and same-need situated contrast;
- Runner and fail-closed Verifier.

Modified:

- `SituatedCapabilityStateV1` now carries derived condition candidates;
- generic Feasibility records required unknown conditions and routes them to
  the existing condition-gap path;
- generic condition-gap lineage includes the situated-state reference;
- architecture README index.

Not modified:

- Provider Runtime, real providers, OCR, YOLO, SLAM, A-Route, cognition
  owners, Decision, Task, Action, or device control.

No runtime command was executed by the Agent.

## Output-contract repair

The first user-terminal verification recorded `27/28` checks passing.  The
only blocker was `no_device_control`: the top-level forbidden-behavior
projection omitted the explicit `device_control=false` field.  Static audit
found no device invocation, device mutation, camera control, movement control,
or other device-control path.  This was classified as
`VERIFIER_OUTPUT_CONTRACT_GAP`.

The repair adds the explicit false field to the top-level Runner projection,
the Situated State Perception behavior projection, and the downstream
precondition-result behavior projection.  No cognitive logic changed.

The post-fix terminal verification reported `30/30`,
`all_checks_passed=true`, `controlled_logic_result=PASS`,
`failed_checks=[]`, and empty validation errors.  Final status:
`CONTROLLED LOGIC VERIFIED — PHASE CLOSED FOR DECLARED SCOPE`.
