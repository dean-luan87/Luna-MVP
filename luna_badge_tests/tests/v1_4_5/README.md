# Luna Badge v1.4.5 测试套件

**版本**: v1.4.5  
**创建日期**: 2025-01-05

---

## 测试文件说明

### 1. conftest.py
**作用**: pytest fixtures 配置
- `flow_template_registry` - 流程模板注册表
- `flow_planner` - 流程规划器
- `flow_runtime` - 流程运行时
- `query_engine` - 问询引擎
- `decision_core` - 决策核心

---

### 2. test_model_scheduler.py
**测试内容**: 模型调度器功能
- `test_model_selection_prefers_low_latency_and_capability` - 模型选择优先低延迟
- `test_model_scheduler_single_and_fallback` - 单模型执行和 fallback 链

**运行方式**:
```bash
pytest tests/v1_4_5/test_model_scheduler.py -v
```

---

### 3. test_flow_engine.py
**测试内容**: 流程引擎功能
- `test_hospital_flow_plans_and_runs` - 医院流程规划和执行

**运行方式**:
```bash
pytest tests/v1_4_5/test_flow_engine.py -v
```

---

### 4. test_decision_core.py
**测试内容**: DecisionCore 端到端测试
- `test_decision_core_routes_to_hospital_template` - 决策核心路由到医院模板

**运行方式**:
```bash
pytest tests/v1_4_5/test_decision_core.py -v
```

---

### 5. test_task_chain_manager.py
**测试内容**: 任务链管理器功能
- `test_insert_subtask_pauses_parent_and_runs_child` - 插入子任务时暂停父任务

**运行方式**:
```bash
pytest tests/v1_4_5/test_task_chain_manager.py -v
```

---

### 6. test_query_engine.py
**测试内容**: 问询引擎功能
- `test_query_engine_goal_question_and_answer` - 目标问题和答案处理

**运行方式**:
```bash
pytest tests/v1_4_5/test_query_engine.py -v
```

---

## 运行所有测试

### 方法 1: 快速模式
```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
pytest tests/v1_4_5/ -q
```

### 方法 2: 详细模式
```bash
pytest tests/v1_4_5/ -v
```

### 方法 3: 运行单个测试文件
```bash
pytest tests/v1_4_5/test_model_scheduler.py -v
```

---

## 测试结果

**最新执行结果**: 6/6 测试通过 ✅

```
tests/v1_4_5/test_decision_core.py::test_decision_core_routes_to_hospital_template PASSED
tests/v1_4_5/test_flow_engine.py::test_hospital_flow_plans_and_runs PASSED
tests/v1_4_5/test_model_scheduler.py::test_model_selection_prefers_low_latency_and_capability PASSED
tests/v1_4_5/test_model_scheduler.py::test_model_scheduler_single_and_fallback PASSED
tests/v1_4_5/test_query_engine.py::test_query_engine_goal_question_and_answer PASSED
tests/v1_4_5/test_task_chain_manager.py::test_insert_subtask_pauses_parent_and_runs_child PASSED

6 passed in 0.03s
```

---

## 测试覆盖

### 功能覆盖
- ✅ 模型调度器 - 模型选择、单模型执行、fallback 链
- ✅ 流程引擎 - 模板规划、任务链执行
- ✅ DecisionCore - 端到端流程
- ✅ 任务链管理器 - 插入子任务、暂停父任务
- ✅ 问询引擎 - 问题生成、答案保存

### 边界测试
- ✅ 模型选择策略
- ✅ Fallback 机制
- ✅ 任务链执行流程
- ✅ 子任务插入机制

---

## 注意事项

1. 确保在项目根目录运行测试
2. 测试不依赖真实模型或外部服务
3. 所有测试都是单元测试，使用 mock 数据
4. 测试文件位于 `tests/v1_4_5/` 目录，与旧测试隔离

---

## 扩展测试建议

### 短期扩展
1. **医院场景下插入上厕所任务** - 测试任务链切换
2. **多模板选择** - 测试模板注册表的优先级逻辑
3. **任务恢复机制** - 测试子任务完成后恢复父任务

### 中期扩展
1. **真实模型集成** - 对接 YOLO / OCR 模型的集成测试
2. **性能测试** - 测试模型调度器的并发性能
3. **错误处理** - 测试各种异常场景

### 长期扩展
1. **端到端场景测试** - 完整用户流程测试
2. **压力测试** - 大量并发任务链测试
3. **回归测试** - 确保新版本不破坏旧功能

---

**维护者**: Luna Badge Team  
**最后更新**: 2025-01-05

