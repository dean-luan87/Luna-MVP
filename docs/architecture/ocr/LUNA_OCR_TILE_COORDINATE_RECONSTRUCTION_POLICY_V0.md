# Luna OCR Tile Coordinate Reconstruction Policy v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`

## 0. 实证与范围

- **实证目录**：`paddleocr_failed_sample_isolation_v0`（见 `_eval_out/paddleocr_failed_sample_isolation_v0`）。  
- **size_sensitive**：`labeled_007`、`labeled_019`、`labeled_010` 等样本证明几何变换与分块策略必须与 **native 稳定性** 同步设计。  

## 1. 硬性要求

1. **requires_coordinate_reconstruction=true**（配置）：每个 tile 的检测结果必须携带 **tile 内局部坐标** 与 **到原图坐标系的仿射/缩放参数**（含 downscale ratio、padding、crop offset）。  
2. 合并到全图 evidence 时：**禁止**丢弃变换矩阵或 bbox 映射；**禁止**「只合并文本、不合并几何」。  
3. **overlap tile** 区域：同一物理文本可能被多块识别；必须 **去重合并**（见 downscale/tiling 策略），去重依据为几何 IoU + 文本相似度，低置信保留多假设并标注。  
4. **reading_order**：不得在高不确定度下强制输出单一全局顺序；须在 evidence 标注 `reading_order_confidence`。

## 2. 失败语义

- 坐标回填失败：该 tile 结果标记为 `geometry_unresolved`，**不得**当作高精度空间事实；可触发重试或更小 tile。  
- **禁止**因单 tile 失败导致未捕获异常拖垮整任务；须隔离失败并上报。

## 3. 与 OCR Bridge

最终对外仍只经 **OCR Bridge** 输出 **OCR evidence**（含变换链与置信度），不升级为 fact。
