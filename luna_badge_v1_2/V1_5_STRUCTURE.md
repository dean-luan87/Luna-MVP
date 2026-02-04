# Luna Badge v1.5 完整结构

## 版本信息
- **版本**: v1.5
- **Phase-1**: 结构骨架（已完成）
- **Phase-2**: 模块填充（已完成）
- **状态**: 可运行、可验收、可回滚

---

## 📁 目录结构

```
luna_badge_v1_2/
├── models/                          # 模型注册、适配器与能力管理
│   ├── __init__.py
│   ├── registry/                    # 模型注册表
│   │   ├── __init__.py
│   │   ├── model_registry.json
│   │   └── model_schema.json
│   ├── adapters/                    # 模型适配器层
│   │   ├── __init__.py
│   │   ├── base_adapter.py          # 基类适配器
│   │   ├── vision_adapter.py        # 视觉模型适配器
│   │   ├── ocr_adapter.py           # OCR 模型适配器
│   │   ├── asr_adapter.py           # ASR 模型适配器
│   │   └── tts_adapter.py           # TTS 模型适配器
│   └── capabilities/                # 能力声明
│       ├── __init__.py
│       ├── capability_schema.json
│       └── model_capabilities.json
│
├── features/                        # 功能开关管理
│   ├── __init__.py
│   └── feature_flags.json
│
├── governance/                      # 模型输出治理与兜底机制
│   ├── __init__.py
│   ├── output_controller/           # Model Output Controller (MOC)
│   │   ├── __init__.py
│   │   ├── controller.py           # 总控流程
│   │   ├── normalizer.py           # 输出标准化
│   │   ├── validator.py            # 输出合法性校验
│   │   ├── conflict_detector.py    # 冲突检测
│   │   ├── arbiter.py              # 规则驱动仲裁器
│   │   ├── decision_schema.json    # 决策输出结构
│   │   ├── test_moc_basic.py       # MOC 基础测试
│   │   └── MOC_PHASE2_COMPLETE.md  # MOC 完成报告
│   └── fallback/                    # Fallback / PlanB 系统
│       ├── __init__.py
│       ├── fallback_policy.yaml    # 策略配置文件
│       ├── fallback_executor.py    # 执行器逻辑
│       ├── test_fallback_basic.py  # Fallback 基础测试
│       └── FALLBACK_PHASE2_COMPLETE.md
│
├── task_chain/                      # 任务链执行与状态管理
│   ├── __init__.py
│   ├── task_state.py                # 任务状态枚举（6 种状态）
│   ├── task_node.py                 # 可恢复的最小执行单元
│   ├── task_context.py              # 任务唯一事实源
│   ├── task_chain_manager.py        # 核心管理器
│   ├── test_taskchain_basic.py      # TaskChain 基础测试
│   ├── TASKCHAIN_PHASE2_COMPLETE.md
│   └── cache/                       # 任务持久化与恢复
│       ├── __init__.py
│       ├── task_cache_manager.py
│       └── task_snapshot_schema.json
│
├── system/                          # 系统级监控与稳定性管理
│   ├── __init__.py
│   └── watchdog/                    # Watchdog & Fail-Safe
│       ├── __init__.py
│       ├── watchdog_monitor.py     # 监控器（检测 5 类异常）
│       ├── failsafe_trigger.py     # 失败保险触发器（4 级 Fail-Safe）
│       ├── restart_recovery_flow.py # 恢复流程
│       ├── test_watchdog_basic.py   # Watchdog 基础测试
│       └── WATCHDOG_PHASE2_COMPLETE.md
│
├── metrics/                         # 运行时指标与日志
│   ├── __init__.py
│   ├── metrics_collector.py         # 指标收集器（统一 API）
│   ├── metrics_reporter.py          # 指标报告生成器
│   └── metrics_schema.json          # 指标 Schema
│
├── tests/                           # 测试模块
│   ├── __init__.py
│   └── acceptance/                  # 验收测试
│       ├── __init__.py
│       ├── test_moc_decision.py     # MOC 决策验收
│       ├── test_fallback_routing.py # Fallback 路由验收
│       ├── test_taskchain_pause_resume.py  # TaskChain 暂停/恢复验收
│       ├── test_watchdog_failsafe.py        # Watchdog Fail-Safe 验收
│       └── test_end_to_end_stub.py          # 端到端 Stub 验收
│
├── tools/                           # 工具脚本
│   └── run_acceptance.py            # 验收测试运行器（一键运行）
│
├── logs/                            # 运行时日志
│   ├── __init__.py
│   └── runtime/
│       ├── __init__.py
│       ├── runtime_metrics.log      # 性能指标日志（JSONL）
│       ├── execution_trace.jsonl    # 执行跟踪日志（JSONL）
│       └── error_log.jsonl          # 错误日志（JSONL）
│
├── config/                          # 系统级配置
│   ├── system_config.yaml
│   ├── task_domain_config.yaml
│   └── risk_level_config.yaml
│
└── 文档/
    ├── V1_5_PHASE1_COMPLETE.md     # Phase-1 完成报告
    ├── V1_5_PHASE2_COMPLETE.md     # Phase-2 完成报告
    └── V1_5_STRUCTURE.md            # 本文档
```

---

## 🔧 核心模块说明

### 1. Model Output Controller (MOC)
**位置**: `governance/output_controller/`

**职责**: 模型输出治理的中心控制器
- 接收多个模型输出
- 标准化、验证、冲突检测、仲裁
- 返回符合 `decision_schema.json` 的决策结果

**关键文件**:
- `controller.py`: 总控流程
- `normalizer.py`: 输出标准化
- `validator.py`: 输出合法性校验
- `conflict_detector.py`: 显式冲突检测
- `arbiter.py`: 规则驱动仲裁器

**验收**: ✅ 所有测试通过

---

### 2. Fallback / PlanB Policy
**位置**: `governance/fallback/`

**职责**: 兜底机制的配置化结构
- 策略即配置（YAML）
- 4 种 action: switch_model (B1), degrade_capability (B2), cross_domain (B3), abort
- 尝试次数计数、冷却期机制

**关键文件**:
- `fallback_policy.yaml`: 策略配置文件
- `fallback_executor.py`: 执行器逻辑

**验收**: ✅ 所有测试通过

---

### 3. TaskChain 稳定化
**位置**: `task_chain/`

**职责**: 任务状态主权者
- 状态管理（6 种状态：PENDING, RUNNING, PAUSED, COMPLETED, FAILED, ABORTED）
- 节点执行、上下文管理
- 中断/恢复、失败处理

**关键文件**:
- `task_state.py`: 任务状态枚举
- `task_node.py`: 可恢复的最小执行单元
- `task_context.py`: 任务唯一事实源（data/attempts/history）
- `task_chain_manager.py`: 核心管理器

**验收**: ✅ 所有测试通过

---

### 4. Watchdog & Fail-Safe
**位置**: `system/watchdog/`

**职责**: 及时止损，把控制权交还给系统与用户
- 检测 5 类异常：执行卡死、模型异常、状态不一致、PlanB 循环、环境突变
- 4 级 Fail-Safe 行为：FS-1 软干预、FS-2 任务重置、FS-3 系统暂停、FS-4 终止并恢复
- 恢复流程

**关键文件**:
- `watchdog_monitor.py`: 监控器
- `failsafe_trigger.py`: 失败保险触发器
- `restart_recovery_flow.py`: 恢复流程

**验收**: ✅ 所有测试通过

---

### 5. Runtime Metrics & 验收脚本
**位置**: `metrics/`, `tests/acceptance/`, `tools/`

**职责**: 可证明、可验收、可回滚
- 三类日志：execution_trace.jsonl、runtime_metrics.log、error_log.jsonl
- 指标收集器（统一 API）
- 验收测试套件（5 个测试）

**关键文件**:
- `metrics/metrics_collector.py`: 指标收集器
- `metrics/metrics_reporter.py`: 指标报告生成器
- `tests/acceptance/*.py`: 验收测试
- `tools/run_acceptance.py`: 验收测试运行器

**验收**: ✅ 所有验收测试通过

---

## 📊 数据流

### 完整链路

```
TaskNode 执行
   ↓
模型 Adapter 输出（Stub/Real）
   ↓
Model Output Controller 决策
   ├─ 标准化
   ├─ 验证
   ├─ 冲突检测
   └─ 仲裁
   ↓
TaskChain.handle_result()
   ├─ commit → 完成节点
   ├─ fallback → FallbackExecutor
   └─ abort → 中止任务
   ↓
FallbackExecutor（如需要）
   ├─ 查策略
   ├─ 执行下一步
   └─ 更新上下文
   ↓
TaskChain 状态更新
   ↓
Watchdog 监控（周期性）
   ├─ 检测异常
   └─ 触发 Fail-Safe（如需要）
   ↓
MetricsCollector 记录
   ├─ execution_trace.jsonl
   ├─ runtime_metrics.log
   └─ error_log.jsonl
```

---

## 🧪 验收测试

### 运行验收测试

```bash
cd luna_badge_v1_2
python3 tools/run_acceptance.py
```

### 测试覆盖

1. **test_moc_decision.py**: MOC 决策验收
   - 主模型高置信 → commit
   - 主模型低置信 + 次模型高置信 → commit(次)
   - 冲突 → fallback

2. **test_fallback_routing.py**: Fallback 路由验收
   - 按 fallback_policy.yaml 路由
   - attempts 累积
   - exhausted → abort

3. **test_taskchain_pause_resume.py**: TaskChain 暂停/恢复验收
   - running → paused → resumed 状态一致
   - 恢复后仍能继续 handle_result

4. **test_watchdog_failsafe.py**: Watchdog Fail-Safe 验收
   - node 超时 → FS-2
   - 写入 error_log + execution_trace

5. **test_end_to_end_stub.py**: 端到端 Stub 验收
   - 贯通：TaskNode → Adapter Stub → MOC → PlanB → TaskChain → Watchdog

**结果**: ✅ 所有 5 个验收测试通过

---

## 📝 日志格式

### execution_trace.jsonl（执行跟踪）

```json
{
  "ts": 1734501000,
  "trace_id": "uuid",
  "task_domain": "navigation",
  "node_id": "n1",
  "event": "moc_decision | fallback | node_start | node_end | watchdog",
  "payload": {}
}
```

### runtime_metrics.log（性能指标）

```json
{
  "ts": 1734501001,
  "metric": "latency_ms",
  "value": 182,
  "tags": {
    "domain": "navigation",
    "model_id": "vision_model_v1",
    "version": "1.0.0"
  }
}
```

### error_log.jsonl（错误日志）

```json
{
  "ts": 1734501002,
  "error_type": "timeout | invalid_output | contradiction | state_mismatch",
  "severity": "low | medium | high",
  "context": {}
}
```

---

## ✅ 验收标准

### v1.5 必须回答的 4 个问题（数据证明）

1. ✅ **系统是否卡死过？**
   - Watchdog 触发率：可记录
   - 卡死恢复率：可记录
   - 所有异常都有 error_log

2. ✅ **模型是否拖慢系统？**
   - 延迟分位数：P50/P95 可记录
   - 超时率：可记录
   - 熔断次数：可记录

3. ✅ **PlanB 是否可控且有效？**
   - 触发原因分布：可记录
   - 耗尽率：可记录（max_attempts 控制）
   - 成功回收率：可记录

4. ✅ **决策是否可复盘？**
   - MOC 决策路径完整性：100% 覆盖率
   - 所有决策都有 trace 记录

---

## 🎯 关键特性

1. **规则驱动，不引入学习**
   - 所有决策基于固定规则
   - 所有策略来自配置文件
   - 不依赖模型具体实现

2. **完整的可观测性**
   - 三类日志：execution_trace、runtime_metrics、error_log
   - 所有关键事件都有 trace
   - 所有异常都有 error_log

3. **可复现的验收测试**
   - 使用 Stub 模型输出
   - 不依赖真实模型
   - 可 CI 集成

4. **状态主权清晰**
   - TaskChain 是状态主权者
   - 所有模块通过标准接口对接
   - 状态转换有明确规则

---

## 📈 代码统计

- **Phase-1**: 47 个文件（结构骨架）
- **Phase-2**: 
  - Python 模块：~20 个
  - 测试文件：8 个
  - 配置文件：3 个
  - 代码行数：~3000 行（不含注释和空行）

---

## 🚀 下一步

✅ **v1.5 Phase-2 全部完成**

可以进入 **模型接入 Phase（受控接入）**

因为：
- 所有核心模块已完成
- 指标收集和验收测试都已就绪
- 接入后任何异常都可追踪
- 任何退化都有数据证据
- 任何策略变更可回归测试

---

**最后更新**: 2025-12-16




