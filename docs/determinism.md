# A3 Determinism Design

## 1. Scope

- **覆盖**：A3 decision core + advice_rhythm
- **不覆盖**：视觉、多模态、异步写序

## 2. Authority Domain

- 所有影响分支的数值必须在 fixed-point integer domain
- 浮点仅为 shadow/debug
- authoritative 字段：`*_q`

## 3. Replay Modes

| 模式 | 用途 |
|------|------|
| Full replay | 全系统（含视觉、multimodal） |
| Freeze replay | 算法闭环（仅 A3 + rhythm，冻结输入） |
| Diff tool | `tools/diff_traces.py` 定位首次分叉 |

## 4. Acceptance Standard

**相同 quantized input → decision + advice_rhythm 路径字节一致**

验证方式：`tools/replay_freeze_a3.py` 对同一 trace 跑两次，`diff` 无输出。

## 5. Known Non-Deterministic Layer

- 多线程写 trace
- 事件 interleave
- IO 顺序

（与算法闭环无关，属系统层）

## 6. Next Phase

- 单写队列（B 方案）
- 输入源冻结升级
