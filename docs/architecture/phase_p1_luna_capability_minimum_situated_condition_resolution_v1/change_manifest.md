# Change manifest

Added:

- `MinimumSituatedConditionRequirementV1`;
- Information-Need-driven minimum condition resolver;
- generic Feasibility integration using resolver output;
- three controlled case families and updated checks;
- phase documentation and architecture index entry.

Modified:

- Situated Capability precondition definition now declares supported condition
  dimensions instead of fixture-defined current required conditions.
- Situated precondition case definitions now call the resolver.

Not modified:

- Provider Runtime, real OCR, YOLO, SLAM, Camera, IMU, Decision, Task, Action,
  Self owner, Field owner, or Capability Slot schema.

The initial documentation recorded `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
The final user-terminal controlled verification reported `25/25` checks
passing, `all_checks_passed=true`, `failed_checks=[]`,
`controlled_logic_result=PASS`, `final_decision=NOT_APPLICABLE`, and
`operational_result=NOT_APPLICABLE_EXECUTION_NOT_REQUESTED`.

Current status: `CONTROLLED LOGIC VERIFIED — PHASE CLOSED FOR DECLARED SCOPE`.
This is documentation closure only and does not claim Real Runtime execution.
