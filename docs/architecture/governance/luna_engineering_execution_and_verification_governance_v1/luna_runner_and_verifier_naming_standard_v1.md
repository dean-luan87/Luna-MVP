# Luna Runner And Verifier Naming Standard v1

## A. Phase Runner

Naming examples:
- run_<capability>_controlled_dryrun_v1.py
- run_<capability>_smoke_v1.py
- run_<capability>_controlled_execution_v1.py

Runner responsibility:
- Execute one scoped run workflow.
- Produce structured output for result verification.
- Must not emit final phase GO.

## B. Result Verifier

Naming examples:
- verify_<capability>_controlled_dryrun_result_v1.py
- verify_<capability>_smoke_result_v1.py

Result Verifier responsibility:
- Verify one runner output.
- May be run by Agent only when explicitly authorized by phase and execution mode.
- Has no final phase decision authority.

## C. Final Phase Verifier

Canonical location:
- docs/architecture/<phase_directory>/verify_<phase_name>.py

Final Phase Verifier responsibility:
- Verify full phase deliverables and contracts.
- V2 authority only.
- User Terminal Only.

## Prohibited Patterns

- Result Verifier pretending to be Final Phase Verifier.
- Runner output claiming GO.
- Agent replacing Final Phase Verification with Result Verifier pass.

## Authority Reminder

- Runner and Result Verifier are component-level verification assets.
- Final Phase Verifier is phase-level verification asset.
- Final GO requires user-executed V2 plus ChatGPT V3 audit.
