# Luna — RealVideo OCR Text-Bearing Sample Planning GO/NO_GO Pack v0

## GO

- text-bearing 规划完整（12 cases / 采样 / ROI / GT / metrics / governance / checklist）
- prior CONDITIONAL_GO 归因为 `sample_limitation_not_chain_failure`
- `no-write boundary` 通过；`verifier=GO`

## CONDITIONAL_GO

- 非关键规划字段缺失，但主矩阵 / GT / boundary / audit 完整
- 无越界行为

## NO_GO

- 读视频、抽帧或跑 OCR；生成 evidence
- fusion / Scene Delta；写事实层
- benchmark 或 provider 比较宣称；改 routing；audit 缺失
