# LUNA — RapidOCR Closure Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-004C-Closure**
- **Subject:** 是否认定 **004C** 已收口，且 RapidOCR **定位**（轻量候选、非默认 OCR）已冻结。

## GO（Closure）

| # | 条件 |
|---|------|
| 1 | 004C harness 已跑通；**output_root** 含 summary / per-sample / trace / replay / whitebox |
| 2 | **verdict=GO**，**hard_blockers=[]** |
| 3 | **Raw text only**；**no semantic / no downstream / no execute / no TTS** |
| 4 | **性能**相对 macOS Vision 同参基线 **明显更优**（avg_latency_ms &lt; ~460） |
| 5 | 能力矩阵与边界登记已完成 |

**Closure 结论：** **GO**

## CONDITIONAL_GO

- 本 Closure **不使用**；004C 归档已为 **GO**。若未来仅 partial verifier，须重评并升版矩阵。

## NO_GO（Closure 语境）

| # | 条件 |
|---|------|
| N1 | OCR 输出语义/导航或进入下游 |
| N2 | `allows_execute_now=true` 或 `real_tts_invoked=true` |
| N3 | trace/replay/whitebox **缺失** |
| N4 | **性能不优于** macOS Vision 基线（同参） |
| N5 | 在文档中 **错误宣称** RapidOCR 为默认 OCR 或已 GT 验收 |

## Recommended next phase

| 优先级 | 阶段 |
|--------|------|
| **P1** | **ModelOCR-004B** — PaddleOCR adapter skeleton + dependency readiness |
| **P2** | **ModelOCR-005** — Ground Truth Dataset & Raw Text Benchmark |
| **P3** | **ModelOCR-006**（叙事）— 多引擎原文对照 |
| **P4** | **ModelOCR-Closure**（叙事）— default / fallback / complex 源决策 |

**禁止在本 Closure 包内启动：** 005 全文实现、YOLO×OCR、将 RapidOCR 写入默认主线配置。
