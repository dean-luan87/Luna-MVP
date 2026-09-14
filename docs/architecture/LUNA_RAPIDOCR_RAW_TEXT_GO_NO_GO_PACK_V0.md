# LUNA — RapidOCR Raw Text Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-004C**
- **Subject:** 是否将 **RapidOCR / ONNXRuntime** 保留为 **Priority 1A 轻量实时/准实时候选**（叙事层级见路线图；本包仅评估）。

## GO

| # | 条件 |
|---|------|
| 1 | Provider 可运行；**avg_latency_ms_per_frame &lt; 460**（优于 004A macOS Vision 同参基线） |
| 2 | 建议目标（叙事）：**avg ≤ 200 ms** — 可作为「准实时」叙事起点（非唯一门禁） |
| 3 | raw text candidates + trace/replay/whitebox **完整** |
| 4 | safety：**无语义、无下游、无 TTS、无 execute** |
| 5 | Verifier **A–N** 通过，`verdict=GO` |

## CONDITIONAL_GO

- **200 ms &lt; avg ≤ 500 ms**，且 schema/safety 完整 → 可作 **离线/低频** 候选。
- **model_asset_status** 未 pinned，但 `cache_detected` 且路径可记录 → soft follow-up。

## NO_GO

| # | 条件 |
|---|------|
| N1 | Provider 不可用或无法输出 raw text candidates |
| N2 | **avg ≥ 460 ms**（不优于 macOS Vision 基线） |
| N3 | 语义/导航/下游/`allows_execute_now`/`real_tts_invoked` 违规 |
| N4 | trace/replay/whitebox 缺失 |
| N5 | **运行时强依赖在线拉模型**且无法记录路径/hash（`reproducibility_risk` 不可接受） |

## OCR 候选层级（叙事，非本包修改代码）

| Priority | 候选 | 定位 |
|----------|------|------|
| **1A** | RapidOCR / ONNXRuntime | 轻量实时/准实时 **候选**（本包评估对象） |
| **1B** | PaddleOCR lightweight | 准确率主候选；依赖 + 004B |
| **2** | macOS Vision OCR | fallback / 对照基线；**非实时主力** |
| **3** | PaddleOCR-VL / DeepSeek-OCR 等 | 复杂版面、离线非实时 |

## Recommended next

- **ModelOCR-004B：** Paddle adapter + dependency readiness（**优先**）。
- **ModelOCR-005：** Ground truth / benchmark（与 004B 解耦）。

**禁止在本包内：** OCR benchmark 全文启动、YOLO×OCR 协同实现。
