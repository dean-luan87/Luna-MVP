# B2 Runtime State Machine v0.5 实现总结

## ✅ 已完成

### 1. 状态机实现
- **文件**: `vision_pipeline/b2/v03/runtime_state_machine.py`
- **功能**: 完整的 6 状态状态机
  - INIT → WARMING_UP → ACTIVE
  - WARMING_UP → SUSPENDED
  - SUSPENDED → ACTIVE
  - ACTIVE → SUSPENDED
  - ACTIVE → READ_ONLY（外部设置）
  - ANY → ERROR（外部设置）

### 2. 集成到 B2
- **文件**: `vision_pipeline/b2/v03/b2_v03.py`
- **修改**:
  - 在 `tick()` 开始处调用状态机
  - 状态机先于判断逻辑运行
  - 只有 `can_trigger=true` 且 `state=ACTIVE` 才能向 C 发送消息
  - 每帧都写入 `runtime_state` 和 `state_gate` 到 trace

### 3. Trace Schema
- **文件**: `traces/b2_runtime_trace_schema_v0.5.json`
- **内容**: 完整的 JSON Schema 定义

### 4. 文档
- **文件**: `vision_pipeline/b2/v03/RUNTIME_STATE_MACHINE_V05.md`
- **内容**: 完整的状态机设计文档

## 🔑 关键特性

### 状态门控
- 只有 `ACTIVE` 状态才能触发判断
- 所有其他状态都有明确的 `blocked_by` 原因
- 状态机先于判断逻辑运行

### Trace 完整性
- 每帧都包含 `runtime_state` 和 `state_gate`
- 如果 `can_trigger=false`，必须提供 `blocked_by`
- 符合三条铁律要求

### C 消息控制
- C 永远不应该看到 WARMING_UP / SUSPENDED / READ_ONLY
- C 只接收来自 ACTIVE 的结果
- 状态机确保这一点

## 📊 状态转移示例

```
INIT (frame_count < 10)
  ↓
WARMING_UP (frame_count >= 10, 但窗口未完成或未稳定)
  ↓
ACTIVE (窗口完成 + 稳定时间 >= 1.5s)
  ↓
SUSPENDED (如果稳定性条件破坏)
  ↓
ACTIVE (恢复稳定 >= 1.5s)
```

## 🎯 下一步

1. Web Trace Viewer（按 state 着色）
2. 集成真实的视觉检测模块
3. 多镜头 / Viewpoint 调度设计

