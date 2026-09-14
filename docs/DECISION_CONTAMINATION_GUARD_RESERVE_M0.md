# Decision Contamination Guard Reserve M0（污染抵抗 / 决策污染观察占位层）交付

## 1. 定位（写死）

为未来**决策治理层上位能力**预留接口与观察位，覆盖方向包括（**当前均不实现算法**）：

1. 污染判断  
2. 污染溯源  
3. 污染成因分析  
4. 污染扩散观察  
5. 污染抵抗  
6. 污染消化 / 清洗  
7. 多模型 / 多决策 / 投票议会式复核  

**M0 只做**：潜在入口、潜在传播链、潜在阻断/抵抗位点的 **reserve / observation**；**不**输出「已被污染/未被污染」强结论。

## 2. 交付件

| 组件 | 路径 |
|------|------|
| 占位层 | `decision_monitor/decision_contamination_guard_reserve.py` |
| Frame 字段 | `decision_contamination_guard_reserve`（`DecisionContaminationGuardReserveResult`） |
| Runtime 摘要（占位） | `runtime/context.py`：`contamination_observation_summary`、`contamination_entry_risk_hint`、`contamination_mitigation_reserved` |
| 时间轴 | 事件类型 `contamination_guard_reserved`（`append_contamination_guard_event`） |
| 结构树 | `tree_summary` 追加 `contamination_reserved=true`（当 guard_applied） |
| Console | `tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py` 轻量区块 |
| Viewer | `tools/decision_monitor_viewer.py` 卡片 + 专家展开 |
| 单测 | `tests/test_decision_contamination_guard_reserve.py` |
| smoke | `tools/smoke_decision_contamination_guard_reserve.py` |

## 3. 数据结构（摘要）

- `ContaminationEntryPointReserve`：`entry_point_type`（user_input / memory_recall / novel_information / strategy_injection / environment_observation / task_context / …）、`entry_point_risk_level`、`entry_point_observed`  
- `ContaminationFlowReserve`：`flow_stage`（input / hypothesis / recheck / …）、`flow_spread_possible`、`flow_block_point_possible`  
- `ContaminationMitigationReserve`：`mitigation_type`（shadow_validation / watchlist_only / multi_model_review / vote_council_reserved / …）、`mitigation_reserved_only=True`  
- `DecisionContaminationGuardReserveResult`：`multi_model_review_reserved`、`vote_council_reserved` 默认 **True**（槽位预留）

## 4. 最小生成规则（M0）

只读现有 frame 粗映射：confirmation → user_input；memory_novel channel → memory / novel；knowledge + strategy shadow → strategy_injection；environment_task_context_reserve → env / task；hypothesis / recheck / object_search → flow 占位；mitigation 列表为固定 reserve 槽位 + 可选 experience 钩子。

## 5. 原则（写入 CONTRACT）

后续白盒与治理体系中，应显式预留「决策污染观察与抵抗」层，用于观察污染如何进入、如何扩散、如何被阻断、如何被消化。当前只做 reserve，不做强判断。未来该层需兼容多模型、多决策、投票议会式复核机制。

## 6. 结论（M0）

占位层已接入 frame / Console / Viewer / 时间轴 / 结构树摘要；**不**实现真实抗污染系统。
