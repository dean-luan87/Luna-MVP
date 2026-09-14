# Luna OCR Image Size and Pixel Budget Policy v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`

## 1. 实证依据

同 **Image Input Gate v0**：`paddleocr_failed_sample_isolation_v0` 已证明 **size_sensitive**（`labeled_007`、`labeled_019`、`labeled_010`）及 **大图 native 不稳定**。本策略将「像素预算」提升为**硬约束**，避免重复撞同一风险。

## 2. 像素与边长预算（与 example 配置对齐）

| 维度 | 实时（realtime） | 重本地（heavy local） | 触发 tiling / 强制异步 |
|------|------------------|------------------------|-------------------------|
| 最大宽 | 配置 `max_width_realtime` | 可放宽 | 超阈值必须 tiling 或 async |
| 最大高 | 配置 `max_height_realtime` | 可放宽 | 同上 |
| 最大兆像素 | 配置 `max_megapixels_realtime` | `max_megapixels_heavy_local` | `max_megapixels_requires_tiling` |

- **禁止**在实时路径上绕过预算将整图原分辨率直送 provider。  
- 超 `max_megapixels_requires_tiling`：**必须** tiling 或进入 async heavy path，**禁止**同步全图 OCR。

## 3. 反馈与证据

- 超限检测须写入 **source chain**（原图 ref、变换后 ref、预算命中原因）。  
- 须可向 **STCM** 报告「大图像默认异步」「超时须通知 orchestrator」（见配置 `stcm_policy`）。

## 4. 禁止项

- 将超 `max_megapixels_realtime` 的整图无降级送入实时 OCR。  
- 无记录地丢弃预算命中信息（影响审计与复现）。
