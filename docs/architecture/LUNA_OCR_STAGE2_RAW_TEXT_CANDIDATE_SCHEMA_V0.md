# LUNA — OCR Stage-2 Raw Text Candidate Schema v0

## Phase

- **Phase-Mainline-GuardedTrial-008**

## Intent

本阶段只定义与校验 **raw_text candidate** 的最小合同（schema），用于：

- provider 输出（未来阶段）统一对齐
- 禁止语义解释/下游消费的前提下，仅允许 raw_text 记录

## Minimal schema（v0）

- `text`: string
- `confidence`: number in \([0,1]\)
- `bbox`: array \([x1,y1,x2,y2]\)
- `source_attribution`: object (optional)

## Boundary

- 不要求真实 provider 输出
- 不允许 semantic interpretation

