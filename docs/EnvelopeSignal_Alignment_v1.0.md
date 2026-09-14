# EnvelopeSignal Cross-Domain Alignment v1.0

## 统一信号契约
- `present`: 是否存在压力/危险
- `level`: NONE / LOW / MEDIUM / HIGH
- `domain`: VISION / EMOTION / SOCIAL / SYSTEM
- `type`: 域内自定义
- `time_to_event`: 可选
- `reason_codes`: 只解释，不裁决（append-only）

## 视角系统 ↔ 情感引擎对齐
- VISION: STATIC / DYNAMIC / ZONE / RELATIVE_MOTION
- EMOTION: CONFLICT / OVERLOAD / BOUNDARY / GRIEF（示例）

## 语义准则
- 立场差异不是错误
- EnvelopeSignal 只表示张力/压力，不输出动作
- within_envelope 只是可接受性口径，不等于“危险”

## 命名对照表（稳定性优先）
| 设计概念 | 实际文件/路径 |
| --- | --- |
| DebugView | `luna_badge_v1_2/governance/output_controller/debug_view.py` |
| EnvelopeBus | `luna_badge_v1_2/governance/risk_center/interfaces/bus.py` |
| Debug CLI | `tools/debug/dump_bc_snapshots.py` |
