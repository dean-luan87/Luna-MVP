# LUNA — PaddleOCR Adapter Skeleton Test Matrix v0

## Phase

- **Phase-ModelOCR-004B**
- Verifier: `tools/verify_paddleocr_adapter_skeleton_v0.py`

| ID | Check | Expected |
|----|------|----------|
| A | manifest readable | summary/readiness JSON exists |
| B | det/rec pinned_partial | det+rec present + `weights_source=pinned_partial` |
| C | cls optional/not_claimed | cls optional + orientation false + rotated not_claimed |
| D | fail-closed on missing dep | if dep missing => `fail_closed=true` |
| E | no fake raw text | skeleton sample has empty candidates |
| F | semantic disabled | false |
| G | allows_execute_now false | false |
| H | real_tts_invoked false | false |
| I | no downstream | true |
| J | trace/whitebox/readiness files | present |
| K | fallback candidates | includes RapidOCR + macOS Vision |
| L | init-only path | no benchmark implied |

Verdict:
- GO: all checks pass.
- CONDITIONAL_GO: deps missing but fail-closed effective.
- NO_GO: fake-ready, boundary violation, missing fallback, or malformed outputs.
