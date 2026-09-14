# LUNA — PaddleOCR Dependency Init Recheck Matrix v0

## Phase

- **Phase-ModelOCR-004B-Fix**

| Check | Expected | Result |
|------|----------|--------|
| paddle import | ok | ok (`3.3.1`) |
| paddleocr import | ok | ok (`3.5.0`) |
| PIL import | ok | ok (`12.2.0`) |
| cv2 import | ok | ok (`4.10.0`) |
| numpy import | ok | ok (`2.2.6`) |
| det status | present | present |
| rec status | present | present |
| cls status | missing_optional | missing_optional |
| weights_source | pinned_partial | pinned_partial |
| dependency readiness | ready | ready |
| fail_closed | false after deps ready | false |
| init-only | attempted and success | attempted=true, ok=true |
| benchmark executed | must be false | false (not run) |
| semantic disabled | true | true |
| execute disabled | true | true |
| real_tts disabled | true | true |
| fallback candidates | rapidocr + vision | preserved |

## Artifacts

- `logs/paddleocr_dependency_readiness_004b_fix_20260429_104000.json`
- `logs/paddleocr_adapter_skeleton_004b_fix_20260429_104000/paddleocr_adapter_skeleton_summary.json`
- `logs/paddleocr_adapter_skeleton_004b_fix_20260429_104000/paddleocr_adapter_readiness.json`
