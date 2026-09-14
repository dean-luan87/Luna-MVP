# Luna OCR Downscale and Tiling Policy v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`

## 1. 实证依据

`paddleocr_failed_sample_isolation_v0`：**downscale_max_1600 / 1024** 等变体使 `labeled_007` / `labeled_019` 等 **size_sensitive** 样本在子评测中达到 **exit_code=0**，证明 **降采样是有效工程缓解**；同时 **labeled_010** 说明 **仅靠降采样仍可能残留 native 风险**，须配合 **tiling、异步与超时**。

## 2. 降采样（Downscale）

- `downscale_policy.enabled=true`；**保持宽高比**；记录 **downscale_ratio** 写入 source chain。  
- **preferred_max_side** / **fallback_max_side**：优先与兜底边长，与 Isolation 中 1600/1024 实证对齐可调。  
- 降采样失败：不得崩溃；降级为更小边长、tiling、或 defer async。

## 3. 分块（Tiling）

- `tiling_policy.enabled=true`；`tile_max_side`、`tile_overlap_ratio` 控制块大小与重叠。  
- **max_tile_count_sync**：同步路径硬上限，防止实时风暴。  
- **max_tile_count_async**：异步路径上限，配合队列与 STCM deadline。  
- **重叠块**必须配置 **重复文本去重**（`requires_duplicate_text_merge=true`），避免拼接噪声。

## 4. 禁止

- 超像素阈值仍坚持单请求全图同步 OCR。  
- 分块 OCR **不**记录 tile 索引与坐标变换（违反坐标重建策略，**禁止**）。

## 5. 与 STCM

- 大图像默认异步；分块/降采样超时须通知 orchestrator；**过期 tile 结果不得单独驱动动作**（与配置 `stcm_policy` 一致）。
