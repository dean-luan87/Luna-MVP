# Luna Badge v1.4.6 发布说明

**版本代号**: v1.4.6 – Dynamic Safety Broadcast Orchestrator  
**发布日期**: 2024-12-XX  
**版本定位**: 导航播报链路的高可靠性升级版本

---

## 一、版本概述

v1.4.6 是 1.4 系列中的关键里程碑，解决传统播报系统"堆叠、延迟、抢占混乱、缺少调度策略"的结构性问题，正式引入**多维调度 + 动态节流 + 优先级抢占 + 语义合并**的播报决策体系。

本版本为 1.4.7 的"语义型任务链问询系统"与未来 1.5 的"任务中心"奠定底层基础。

---

## 二、核心功能

### 2.1 多路播报调度 Router（安全 / 导航 / 系统）

- **三通道调度结构**：
  - `SafetyChannel`：安全播报通道（P0 优先级）
  - `NavChannel`：导航播报通道（P1 优先级）
  - `SystemChannel`：系统/任务播报通道（P2-P3 优先级）

- **优先级规则矩阵**：
  - P0 (Safety) > P1 (Navigation) > P2 (Task) > P3 (Chat)
  - 同优先级内按 FIFO 顺序

- **短时间窗口限流机制**：
  - 安全播报：0.8 秒窗口
  - 导航播报：2.0 秒窗口
  - 避免播报阻塞和重复

### 2.2 动态时间窗口（Dynamic Time Window）

系统会根据以下因素自动调整播报节奏：

- 当前位置复杂度（人员密度、障碍密度）
- 用户移动速度
- 场景类型（室内 / 室外）
- 事件紧急程度

实现真正的**环境自适应节流（Adaptive Throttling）**。

### 2.3 播报内容语义合并（Semantic Merge）

- 短时间内重复或相似逻辑会进行合并播报
- 降低噪音与冗余语句
- 提升用户体验

### 2.4 播报抢占（Preemption）机制

- **安全播报高优先级队列（SafetyQueue）**：
  - 紧急安全播报可随时抢占正在播报的内容
  - 安全队列优先于主队列
  - 2 秒内不重复相同安全播报（限频机制）

- **抢占逻辑具备完整的恢复流程**：
  - 主队列内容不丢失，只是被暂时抢占
  - 安全播报完成后，主队列可恢复

### 2.5 统一 TTS 调用入口（TTSRouterFacade）

- **全局唯一播报入口**：`TTSRouterFacade.emit()`
- **语义化接口**：
  - `speak_system()`：系统播报
  - `speak_task()`：任务播报
  - `speak_nav()`：导航播报
  - `speak_safety()`：安全播报
  - `speak_chat()`：闲聊播报

- **全项目规范化**：
  - 所有 `tts_manager.speak()` 调用已替换为统一入口
  - 确保优先级统一管理
  - 时间窗口/节流统一生效

### 2.6 任务链联动（TaskChain Integration）

- 所有播报事件接入 `TaskChainManager` 事件流
- 支持任务链中断 / 继续 / 合并
- 为 1.4.7 的"问询与确认能力"提供基础能力

### 2.7 事件来源标注与日志化

所有播报都带有：

- 事件类型
- 来源模块
- 优先级
- 时间戳
- 决策路径

便于后续 AI 调试、错误回溯与模型训练。

---

## 三、技术架构

### 3.1 TTS 调度层架构

```
导航/安全 → NavigationVoiceRouter → TTSRouterFacade → QueueManager → PriorityScheduler → RuntimeDriver → TTS 引擎
系统/任务 → TTSRouterFacade → QueueManager → PriorityScheduler → RuntimeDriver → TTS 引擎
```

### 3.2 优先级调度器（PriorityScheduler）

- **PriorityBand 分段**：
  - P0_SAFETY：安全播报（priority >= 90）
  - P1_NAV：导航播报（priority >= 70）
  - P2_TASK：任务/系统播报（priority >= 40）
  - P3_CHAT：闲聊播报（priority < 40）

- **调度规则**：
  1. 安全队列永远优先（P0）
  2. 主队列内按 Band 排序（P1 > P2 > P3）
  3. 同 Band 内按 priority 降序
  4. 同 priority 按 FIFO

### 3.3 安全播报队列（SafetyQueue）

- **独立队列**：`_safety_queue`（deque）
- **限频机制**：2 秒内不重复同一句安全播报
- **抢占能力**：安全播报可跳过时间窗口限制

---

## 四、主要变更文件

### 4.1 新增模块

- `task_engine/tts/priority_bands.py`：优先级分段定义
- `task_engine/tts/priority_scheduler.py`：统一优先级调度器
- `task_engine/tts/routers/time_window_gate.py`：时间窗口节流控制
- `task_engine/tts/routers/navigation_voice_router.py`：导航语音路由器（TTS Routers 层）
- `docs/step13_migration_plan.md`：TTS 调用规范化迁移计划

### 4.2 增强模块

- `task_engine/tts/tts_manager.py`：
  - 新增安全队列（SafetyQueue）支持
  - 新增 `push_safety()` 方法
  - 新增 `pop_next()` 方法（使用 PriorityScheduler）
  - 修改 `pop_all()` 使用统一调度器

- `task_engine/tts/router_facade.py`：
  - 新增 `emit()` 统一入口
  - 新增语义化接口（`speak_system`, `speak_task`, `speak_nav`, `speak_safety`, `speak_chat`）

- `task_engine/tts/runtime_driver.py`：
  - 修改 `process_once()` 使用 `pop_next()` 逐条处理
  - 更新 `_speak_utterance()` 输出包含 band 信息

- `task_engine/tts/tts_policy.py`：
  - 新增 `TTSPolicy.band()` 方法

### 4.3 规范化替换

以下文件中的 `tts_manager.speak()` 调用已全部替换为 `TTSRouterFacade` 统一入口：

- `task_engine/ask/ask_runtime.py`（10 处）
- `core/flow_engine/runtime.py`（4 处）
- `task_engine/scene/scene_runtime.py`（3 处）
- `task_chain/task_chain_manager.py`（5 处）
- `decision_core/decision_core.py`（3 处）

**总计替换**：25 处

---

## 五、测试验证

### 5.1 单元测试

- `tests/v1_4_6d/test_tts_priority_scheduler.py`：优先级调度器测试（8 个测试用例，全部通过）
- `tests/v1_4_6d/test_time_window_gate.py`：时间窗口节流测试
- `tests/v1_4_6d/test_navigation_voice_router_window.py`：导航语音路由器集成测试
- `tests/v1_4_6d/test_e2e_navigation_voice_throttle.py`：E2E 节流测试
- `tests/v1_4_6d/test_navigation_speech_e2e.py`：导航语音 E2E 测试

### 5.2 Demo 脚本

- `scripts/demo_safety_queue_e2e.py`：安全队列 E2E Demo（5 个场景）
- `scripts/demo_priority_scheduler_step12.py`：优先级调度器 Demo（5 个场景）
- `scripts/demo_tts_router_facade_step13.py`：TTSRouterFacade Demo（5 个场景）

### 5.3 验证结果

- ✅ 所有模块导入成功
- ✅ 单元测试全部通过
- ✅ E2E Demo 运行成功
- ✅ 优先级调度器正常工作
- ✅ 安全队列抢占机制正常
- ✅ 时间窗口节流正常
- ✅ 无循环导入问题
- ✅ 无语法错误
- ✅ 无 linter 错误

---

## 六、工程级完备性检查

| 能力项 | 实现情况 | 备注 |
|--------|---------|------|
| 三通道播报调度 | ✅ 已完成 | 可稳定运行 |
| 时间窗口限流 | ✅ 已完成 | 可配置化 |
| 动态节流（根据速度/环境） | ✅ 已完成 | 可扩展更多传感指标 |
| 播报抢占机制 | ✅ 已完成 | 同步恢复逻辑 |
| 语义合并（短句聚合） | ✅ 已完成 | 简版实现，可在 1.4.7 深化 |
| Router 决策表达式 | ✅ 已完成 | 逻辑清晰，可引入权重模型 |
| 任务链联动 | ✅ 已完成 | 进入任务事件流 |
| 错误恢复与 FailSafe | ✅ 已完成 | 避免播报死锁 |
| 测试 Demo | ✅ 已完成 | 各场景运行正常 |

**结论**：v1.4.6 已达到工程级封版条件。

---

## 七、价值总结

### 7.1 对产品的影响

这是导航体验从"播报系统"升级为"决策系统"的关键节点。

从业务角度，v1.4.6 带来：

1. **更安全**：
   - 安全播报不再被阻塞
   - 高危场景能确保第一时间提醒

2. **更智能**：
   - 可以根据场景自动调整播报节奏
   - 不会啰嗦、不会延迟

3. **更可控**：
   - 每个播报都能追踪决策路径
   - 并可被任务链、问询系统复用

4. **更接近未来的"智能引导"**：
   - 为 1.5 的"智能任务链生成器"铺路

### 7.2 技术价值

- **统一架构**：所有 TTS 调用通过统一入口，便于维护和扩展
- **可观测性**：完整的日志和追踪能力
- **可扩展性**：模块化设计，易于添加新的播报类型和调度策略
- **可测试性**：完整的单元测试和 E2E 测试覆盖

---

## 八、已知限制与未来改进

### 8.1 已知限制

1. **语义合并**：当前为简版实现，可在 1.4.7 深化
2. **动态节流**：当前基于固定规则，未来可引入机器学习模型
3. **多模型调度**：当前为单模型，1.4.8 将引入多模型并行

### 8.2 未来改进方向

- v1.4.7：任务链问询（目标确认 / 中断确认 / 下一步建议）
- v1.4.8：多模型调度框架（视觉/语音/导航行为融合）
- v1.4.9：Plan-B 极限场景应急能力
- v1.4.10：全链路 stress test
- v1.4.11：视角导航"复眼模式"调度版

---

## 九、迁移指南

### 9.1 从 v1.4.5 升级到 v1.4.6

1. **更新 TTS 调用方式**：
   ```python
   # 旧方式
   tts_manager.speak("文本", priority=75)
   
   # 新方式
   from task_engine.tts.router_facade import get_tts_router_facade
   router = get_tts_router_facade()
   router.speak_nav("文本")
   ```

2. **使用语义化接口**：
   - 导航播报：`router.speak_nav()`
   - 安全播报：`router.speak_safety()`
   - 任务播报：`router.speak_task()`
   - 系统播报：`router.speak_system()`
   - 闲聊播报：`router.speak_chat()`

3. **保留 meta 信息**：
   ```python
   router.speak_task("文本", meta={"stage": "task_start", "task_id": "xxx"})
   ```

### 9.2 兼容性说明

- v1.4.6 保持向后兼容，旧的 `tts_manager.speak()` 调用仍可工作
- 但建议尽快迁移到新的统一入口，以获得完整的调度和节流能力

---

## 十、致谢

感谢所有参与 v1.4.6 开发的团队成员。

---

## 十一、相关文档

- `docs/step13_migration_plan.md`：TTS 调用规范化迁移计划
- `docs/tts_policy_usage.md`：TTS 策略使用指南
- `docs/tts_router_time_window.md`：时间窗口节流文档
- `docs/navigation_voice_migration_guide.md`：导航语音迁移指南

---

**Luna Badge v1.4.6 正式发布**












