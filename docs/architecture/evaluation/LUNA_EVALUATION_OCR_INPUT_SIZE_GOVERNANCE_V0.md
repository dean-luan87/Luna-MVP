# Luna Evaluation — OCR Input Size Governance v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`  
**范围**: 评测流水线与离线批跑；**不**在本阶段执行 OCR 二进制。

## 1. 与 Failed Sample Isolation 的对齐

评测运行器（如 `run_paddleocr_labeled_set_*`）在构造 provider 输入前，须遵守与主线一致的 **ImageInputGate** 语义：

- 引用实证：`_eval_out/paddleocr_failed_sample_isolation_v0` 中 **size_sensitive**（`labeled_007`、`labeled_019`、`labeled_010`）及 **大图 native 风险** 结论。  
- **禁止**评测为方便而默认「整图原分辨率直送」若该路径在配置中标记为 **realtime-forbidden**。  
- 评测允许 **full-image** 仅当显式标签为 `evaluation` / `async`，且仍须记录 **downscale/tiling** 链路与 **坐标回填**。

## 2. 评测专用要求

- 批跑须记录：`gate_decision`、`max_side_applied`、`tile_count`、`coordinate_transform_id`。  
- 对比「治理前 vs 治理后」须使用独立 run id，**不得**伪造 summary。  
- 失败须可定位到 **sample_id + transform 阶段**（与 Stability-Recovery 口径兼容）。

## 3. 禁止

- 为追求 benchmark 分数绕过像素预算。  
- 将评测结果直接写 MidPlatform / WorldModel。
