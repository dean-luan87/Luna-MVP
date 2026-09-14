# Shadow Replay 验证清单

## 概述

Shadow Replay 是一个"只读式"的回放机制，用于验证旧功能（legacy navigation, OCR, decision）是否仍然正常工作，同时不影响 C1 的状态机和 Pipeline 执行节律。

## 核心原则

- ✅ **被动消费同一帧源**：使用与 C1 相同的视频帧
- ✅ **输出日志 / 结果**：记录旧功能的执行结果
- ❌ **不能影响 C1 的状态机**：不修改 C1 的任何状态
- ❌ **不能改变 Pipeline 的执行节律**：不改变 fps、执行频率等

## 这个视频能验证的历史功能

### 1. 旧视觉链路是否还活着

- [ ] **YOLO 检测**
  - 是否能正常识别物体
  - 是否存在 crash / 内存泄露
  - 检测结果是否合理

- [ ] **OCR 提取**
  - 是否能正常提取文本
  - 提取的文本是否准确
  - 是否存在异常错误

- [ ] **QwenVL 描述**
  - 是否能正常生成描述
  - 描述质量是否合理
  - API 调用是否正常

### 2. 新旧系统行为对比

- [ ] **执行频率对比**
  - C1 跳过 ModelingExecutor 时，Legacy 是否仍然执行
  - 新旧系统的执行次数统计
  - 算力节省情况

- [ ] **延迟对比**
  - Legacy 回放的平均延迟
  - 与 C1 主系统的延迟对比
  - 是否存在性能退化

### 3. 世界模型差异

- [ ] **SceneState 对比**
  - 旧 SceneState vs 新 SceneState
  - 哪些信息是"冗余的"
  - 哪些信息是"真正有价值的"

- [ ] **数据一致性**
  - Legacy 检测结果 vs C1 检测结果
  - 是否存在数据不一致
  - 不一致的原因分析

## 运行方式

### 基础测试（无 Shadow Replay）

```bash
python3 examples/c1_v02_real_input_validation.py --duration 1 --video test_video.mp4
```

### 启用 Shadow Replay

```bash
python3 examples/c1_v02_real_input_validation.py --duration 1 --video test_video.mp4 --replay-legacy
```

## 输出文件

- **C1 验证日志**: `artifacts/c1_v02_validation_log.json`
- **Shadow Replay 日志**: `artifacts/shadow_replay_<timestamp>.jsonl`

## 注意事项

⚠️ **重要**：
- Shadow Replay 是"影子"，不是"第二个大脑"
- 不要让它控制执行
- 不要让它修改 C1 参数
- 不要让它反向影响决策

## 下一步

完成 Shadow Replay 验证后，可以：
1. 分析日志，找出旧功能的潜在问题
2. 对比新旧系统，评估迁移效果
3. 决定是否需要进一步优化或迁移


