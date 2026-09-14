# LUNA — PaddleOCR Dependency Init Recheck Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-004B-Fix**
- Decision subject: 依赖补齐后，PaddleOCR adapter skeleton 能否进入 `init-only` 可用状态（不做 benchmark）。

## GO

- `paddle` / `paddleocr` / `PIL` import ok
- det/rec present，`weights_source=pinned_partial`
- cls 缺失但 correctly `missing_optional`
- `init-only` 成功
- verifier 通过
- fallback candidates 保持
- 无语义/无下游/无 execute/无 TTS

## CONDITIONAL_GO

- 依赖安装失败或 init-only 失败
- 但 fail-closed 成立，未伪造可用
- 仍可进入后续环境修复

## NO_GO

- 依赖缺失却标 `provider_available=true`
- init-only 失败却伪造成功
- cls 缺失却声明 orientation support
- 越界到语义/导航/下游
- `allows_execute_now=true` / `real_tts_invoked=true`
- fallback candidates 被移除

## Recorded verdict

- run: `20260429_104000`
- verdict: **GO**
- hard_blockers: `[]`
- soft_followups: `[]`

## Recommended next

1. **ModelOCR-005** — GT dataset + raw text benchmark（三引擎对照）
2. 保持 004A/004C fallback/candidate 定位不变，不提前设默认 OCR。
