# v1.8.5 C1 回访工具（C1 Replay Tool）完整设计文档

## 一、工具定位

**C1 回访工具不是 Debug 工具，而是"事后理解 Luna 当时为什么这么看、这么决策"的系统级审计与复盘工具。**

它服务的对象不是模型，而是：
- 决策机制
- 抽帧策略
- 状态切换逻辑
- 安全兜底是否生效

**这是后面能放心升级 C1 / C2 / C3 的基础设施。**

---

## 二、核心问题（必须能回答）

C1 回访工具必须能回答下面 5 个问题（缺一不可）：

1. **当时 C1 处于什么状态？**
   - stable / alert / suspended / recovery

2. **当时输入信号是什么？**
   - 运动、画面变化、风险提示、隐私场景、用户指令等

3. **为什么做出这个决策？**
   - 为什么抽帧 / 为什么停 / 为什么切优先级

4. **这个决策带来了什么结果？**
   - pipeline 是否执行、耗时、是否降级

5. **如果规则不同，结果会不会更好？**
   - 为后续策略调优服务

---

## 三、工程边界（非常重要）

### 3.1 C1 Replay Tool 明确不做的事

- ❌ 不加载视觉模型
- ❌ 不跑 YOLO / OCR / VL
- ❌ 不依赖真实摄像头
- ❌ 不需要 frame / image

### 3.2 它只做一件事

**重放「当时的 C1 决策链」**

这是它能稳定、可维护、可审计的根本原因。

---

## 四、数据输入

C1 Replay 只依赖三类数据：

### 4.1 C1 决策日志（核心）

每一次 C1 决策，都应有一条结构化日志：

```json
{
  "timestamp": 1723456789.123,
  "prev_state": "stable",
  "current_state": "alert",
  "motion_score": 0.82,
  "frame_diff_score": 0.67,
  "privacy_hit": false,
  "user_override": false,
  "allow_frame": true,
  "target_fps": 10,
  "priority": "safety",
  "observation_mode": "local",
  "reason": "sudden motion detected"
}
```

这就是 C1 的"思考痕迹"。

### 4.2 Pipeline 执行摘要（极简）

用于验证 C1 决策是否被正确执行：

```json
{
  "timestamp": 1723456789.130,
  "navigation_executed": true,
  "modeling_executed": false,
  "latency_ms": 6.8
}
```

### 4.3 系统元信息（一次性记录）

用于版本回溯与 A/B 对比：

```json
{
  "luna_id": "luna_001",
  "version": "v1.8.5",
  "hardware": "badge_v1",
  "c1_policy_version": "c1_policy_2024_12_19"
}
```

---

## 五、工程结构

```
c1_replay/
├── __init__.py              # 模块导出
├── replay_loader.py         # 加载 & 解析日志
├── replay_models.py         # 数据结构定义
├── replay_engine.py         # 核心重放逻辑
├── replay_report.py         # 分析与统计
└── replay_cli.py            # CLI 工具（当前阶段足够）
```

**这套结构未来可以无缝接入后台 UI，不用重构。**

---

## 六、三种 Replay 模式

### 6.1 模式 1：事实回放（Default）

**完全复现当时发生了什么**

**用途**：
- 事故复盘
- 安全审计
- 用户投诉分析

**使用**：
```bash
python c1_replay/replay_cli.py factual --c1-log logs/c1.log
```

### 6.2 模式 2：假设回放（What-if）

**同一批日志，换规则跑**

**例如**：
- 如果 motion_threshold 提高？
- 如果 alert 状态下仍允许 modeling？
- 如果 fps 上限改成 5？

**使用**：
```bash
python c1_replay/replay_cli.py what-if --c1-log logs/c1.log --motion-threshold 0.90
```

### 6.3 模式 3：策略对比（A/B）

**同一输入，两套策略**

**输出示例**：
```
Policy A:
  modeling executed: 22%
  suspended time: 9%

Policy B:
  modeling executed: 11%
  suspended time: 15%
```

**这是你后期调 C1 的核心武器。**

**使用**：
```bash
python c1_replay/replay_cli.py compare --c1-log logs/c1.log --policy-a-threshold 0.85 --policy-b-threshold 0.90
```

---

## 七、回访输出结构

### 7.1 时间轴视图（必须）

```
时间      状态      fps    priority    执行结果
10:01:02  stable   2      env          modeling
10:01:05  alert    10     safety       nav only
10:01:06  suspended 0     safety       paused
```

### 7.2 决策原因统计

```json
{
  "suspended_reasons": {
    "motion": 12,
    "privacy": 3,
    "camera_unstable": 2
  },
  "priority_switches": {
    "stable→alert": 5,
    "alert→stable": 4
  }
}
```

### 7.3 风险与异常分析（非常有价值）

检测：
- 连续 alert 未降级
- 高频切换（抖动风险）
- 长时间 suspended
- fps 异常拉满

---

## 八、和未来 Luna 后台的关系

你现在做的 Replay / 日志 / 测试：
- ✅ 本质就是后台的"观测与审计能力"
- ✅ 后期只需接 UI，不改逻辑
- ✅ 每个 Luna 都可以独立查看

**后台未来能看到**：
- C1 状态时间轴
- 抽帧策略变化
- 决策原因
- 版本对比
- 硬件差异影响

**而且**：
- 现在不对外
- 但已经具备 ToB / ToG 能力

---

## 九、使用示例

### 9.1 事实回放

```bash
# 基本使用
python c1_replay/replay_cli.py factual --c1-log logs/c1.log

# 保存报告
python c1_replay/replay_cli.py factual --c1-log logs/c1.log --output report.txt
```

### 9.2 假设回放

```bash
# 如果 motion_threshold 提高到 0.90
python c1_replay/replay_cli.py what-if --c1-log logs/c1.log --motion-threshold 0.90

# 如果 fps_limit 改成 5
python c1_replay/replay_cli.py what-if --c1-log logs/c1.log --fps-limit 5
```

### 9.3 策略对比

```bash
# 对比两种 motion_threshold
python c1_replay/replay_cli.py compare --c1-log logs/c1.log --policy-a-threshold 0.85 --policy-b-threshold 0.90
```

---

## 十、演示脚本

**文件**：`examples/c1_replay_demo.py`

**演示内容**：
- 事实回放
- 假设回放
- 策略对比

**运行**：
```bash
python examples/c1_replay_demo.py
```

---

## 十一、当前阶段的最佳下一步

**不要做 UI，不要接后台**

👉 **先做 CLI 版 Replay Tool**

**原因**：
- 成本最低
- 验证价值最高
- 能立刻发现 C1 设计漏洞

---

## 十二、总结

**C1 回访工具（CLI 版）完成** ✅

**新增文件**：6 个（5 个核心模块，1 个演示脚本）

**功能**：
- ✅ 事实回放（完全复现）
- ✅ 假设回放（换规则跑）
- ✅ 策略对比（A/B 测试）

**设计特点**：
- ✅ 不依赖视觉模型
- ✅ 不依赖真实摄像头
- ✅ 只重放决策链
- ✅ 未来可无缝接入后台 UI

**价值**：
- ✅ 系统级审计与复盘
- ✅ 策略调优的核心武器
- ✅ 升级 C1 / C2 / C3 的基础设施

---

**文档版本**：v1.0  
**最后更新**：2024-12-19


