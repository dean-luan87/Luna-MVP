# LUNA — RapidOCR vs macOS Vision Performance Note v0

## Phase

- **Phase-ModelOCR-004C**
- **Comparison rule:** **同一视频、同一抽帧参数**（`frame_step`、`max_sampled_frames`）下对比 wall-clock 与 **平均每帧延迟**。

## Baseline：macOS Vision OCR（004A）

| 项 | 值 |
|----|-----|
| **video** | `/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4` |
| **frame_step** | 30 |
| **max_sampled_frames** | 100 |
| **Wall-clock** | ~**46 s** / 100 帧 |
| **avg** | ~**460 ms/帧** |
| **FPS（折算）** | ~**2.1** |

**结论：** 不适合 Luna **实时/准实时** OCR 主力（导航读牌等）。

## RapidOCR（004C）

**一次归档运行（与 baseline 同视频、同 frame_step / max_frames）：**

| 项 | 值 |
|----|-----|
| **output_root** | `logs/rapidocr_raw_text_004c_20260429_100335` |
| **total_runtime_seconds** | **10.647** |
| **avg_latency_ms_per_frame** | **106.355** |
| **p50_latency_ms_per_frame** | **102.944** |
| **p95_latency_ms_per_frame** | **142.280** |
| **verifier** | **GO**（优于 460ms/帧基线；满足 ≤200ms 叙事目标） |

**依赖快照（见该次 summary `dependency_probe`）：** `rapidocr-onnxruntime` **1.4.4**，`onnxruntime` **1.23.2**，模型目录在 venv 内 `rapidocr_onnxruntime/models`（`cache_detected`）。

## 判定口径（与 GO pack 一致）

| 档位 | avg_latency_ms_per_frame |
|------|----------------------------|
| 优于 Vision（004C verifier **N**） | **&lt; 460** |
| 建议实时候选目标（叙事） | **≤ 200**（非强制门禁，见 GO pack） |
| 介于 200–500 | 可能 **CONDITIONAL_GO**（离线/低频） |

## 说明

- 本对比为 **工程观测**，非严格实验室 benchmark；CPU/GPU、电源策略均影响结果。
- RapidOCR 评估时使用较低 **`text_score`** / **`box_thresh`** 以增加检出（与默认 Vision 阈值不可逐字对齐），对比侧重 **吞吐量级**。
