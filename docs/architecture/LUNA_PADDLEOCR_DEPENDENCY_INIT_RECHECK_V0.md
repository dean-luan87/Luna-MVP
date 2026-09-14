# LUNA — PaddleOCR Dependency Readiness & Init-Only Recheck v0

## Phase

- **Phase-ModelOCR-004B-Fix**
- Scope: 仅补依赖与 `--init-only` 复测；不跑 benchmark，不接下游。

## Pre-install status（`.venv-tx`）

- `paddle`: missing
- `paddleocr`: missing
- `PIL`: ok
- `cv2`: ok
- `numpy`: ok

## Install command

```bash
pip install paddlepaddle paddleocr pillow
```

## Post-install status（`.venv-tx`）

- `paddle`: ok `3.3.1`
- `paddleocr`: ok `3.5.0`
- `PIL`: ok `12.2.0`
- `cv2`: ok `4.10.0`
- `numpy`: ok `2.2.6`

## Recheck run（recorded）

- dependency readiness report:
  - `logs/paddleocr_dependency_readiness_004b_fix_20260429_104000.json`
  - result: `readiness_status=ready`, `fail_closed=false`
- init-only smoke output_root:
  - `logs/paddleocr_adapter_skeleton_004b_fix_20260429_104000`
  - mode: `init-only`
  - provider available: true
  - init-only attempted: true / ok: true
- verifier:
  - `tools/verify_paddleocr_adapter_skeleton_v0.py --output-root logs/paddleocr_adapter_skeleton_004b_fix_20260429_104000`
  - verdict: **GO**
  - hard_blockers: `[]`

## Boundary checks

- `raw_text_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `orientation_support=false`
- `rotated_text_handling=not_claimed`
- fallback candidates unchanged:
  - `rapidocr_onnxruntime_v0`
  - `macos_vision_ocr_system_v0`

## Notes

- `init-only` 过程中 PaddleX 输出了模型创建/缓存日志（位于 `~/.paddlex/official_models/...`）；本阶段不做 benchmark，只验证 provider 可初始化。
