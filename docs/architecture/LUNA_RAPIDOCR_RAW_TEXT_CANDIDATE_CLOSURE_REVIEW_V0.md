# LUNA — RapidOCR Raw Text Candidate Evaluation Closure Review v0

## Phase

- **Phase-ModelOCR-004C-Closure**
- **Purpose:** 正式复审 **Phase-ModelOCR-004C** 代表性运行、性能与 verifier，**冻结** RapidOCR 在 Luna 中的**能力定位**；**不新增代码、不进入 benchmark**。

## 上游关系（已成立）

| 阶段 | 结论 / 定位 |
|------|-------------|
| **004A-Closure** | macOS Vision OCR = **GO**，**非实时主力**；fallback / 对照基线 |
| **004C** | RapidOCR + ONNXRuntime = **GO**；**轻量实时/准实时候选**（本文件收口） |
| **PaddleOCR** | det+rec **pinned_partial**；**004B** 补 adapter + dependency readiness |

## 归档运行（004C）

| 项 | 值 |
|----|-----|
| **video_path** | `/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4` |
| **frame_step** | `30` |
| **max_sampled_frames** | `100` |
| **output_root** | `logs/rapidocr_raw_text_004c_20260429_100335` |
| **samples** | `100` |
| **wall-clock** | **10.647 s** / 100 帧 |
| **avg_latency_ms_per_frame** | **106.355** |
| **p50_latency_ms_per_frame** | **102.944** |
| **p95_latency_ms_per_frame** | **142.280** |
| **折算吞吐** | 约 **9.4 FPS**（100 / 10.647；观测值，非严格 lab） |

## 与 macOS Vision（004A 同参基线）对比

| 指标 | macOS Vision（004A） | RapidOCR（004C 归档） |
|------|----------------------|------------------------|
| 100 帧 wall-clock | ~**46 s** | **10.647 s** |
| 约 ms/帧 | ~**460** | **~106** |
| 约 FPS | ~**2.1** | ~**9.4** |
| 实时主力 | **否** | **仅候选**（见下节） |

**结论（性能维度）：** RapidOCR 在**同视频、同采样**下**明显快于** macOS Vision，满足 004C verifier **N**（&lt; 460 ms/帧）与 **GO** 口径。

## Verifier

| 项 | 值 |
|----|-----|
| **verdict** | **GO** |
| **hard_blockers** | `[]` |
| **工具** | `tools/verify_rapidocr_raw_text_v0.py` |

## 能力定位（冻结 — 勿误读）

1. **RapidOCR** = **轻量 OCR 候选**，已成功跑通 **raw text harness** 与边界；**不是**「已验收默认 OCR」「不是」离线默认唯一源。
2. **尚未完成** **Ground Truth / 原文准确率 benchmark**（**005** 及后续）；**不得**因延迟优势单独宣告为「默认 OCR」。
3. **macOS Vision** 继续：**fallback / 对照基线**，非实时主力。
4. **PaddleOCR**：仍为 **主候选之一**（准确率路径），**004B** 优先补齐 adapter 与依赖就绪。
5. **路线含义：** 004C 把工程从「只剩 Vision fallback」与「Paddle 未 fully ready」之间的空档中拉出 **可落地的轻量候选**；**下一步仍以 004B → 005（GT/benchmark）顺序为主**，**006** 做多引擎对照时再并排 Rapid / Vision / Paddle。

## Closure verdict

- **Phase-ModelOCR-004C-Closure：** **GO**（见 `LUNA_RAPIDOCR_CLOSURE_GO_NO_GO_PACK_V0.md`）。

## Recommended next（路线图层级）

| 顺序 | 阶段 | 说明 |
|------|------|------|
| **1** | **ModelOCR-004B** | PaddleOCR adapter skeleton + dependency readiness |
| **2** | **ModelOCR-005** | Ground Truth Dataset & Raw Text Benchmark |
| **3** | **ModelOCR-006**（叙事） | RapidOCR vs Vision vs Paddle **原文**对比 |
| **4** | **ModelOCR-Closure**（叙事） | 默认离线源 / fallback / 复杂版面源决策 |

**本 Closure 不启动：** 005 benchmark 实现、YOLO、中台、语义与下游。

## Cross-references

- `LUNA_RAPIDOCR_CAPABILITY_STATUS_MATRIX_V0.md`
- `LUNA_RAPIDOCR_BOUNDARY_REGISTER_V0.md`
- `LUNA_RAPIDOCR_VS_MACOS_VISION_PERFORMANCE_NOTE_V0.md`
