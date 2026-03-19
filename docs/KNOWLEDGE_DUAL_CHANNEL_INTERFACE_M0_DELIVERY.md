# Knowledge Dual-Channel Interface M0（知识双通道接口预留层 M0）交付

## 1. 定位（写死）

本模块是**接口预留层**，不是图书馆系统。当前只负责定义与输出：

- **沉淀候选通道**（Persist Candidate）：哪些内容未来值得沉淀
- **优化/查策略候选通道**（Optimization Candidate）：哪些问题未来需要查策略/模板支持
- **策略注入口**（Injection Slot）：未来图书馆策略从哪里注入、怎么注入（仅 slot，不执行）

本轮明确不做：图书馆本体、写入/检索、策略召回、策略自动注入、评分系统、对比/替换逻辑、反馈机制细化、历史统计与自动治理。

## 2. 交付件

- 实现：`decision_monitor/knowledge_dual_channel_interface.py`
- 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `knowledge_dual_channel_interface`）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_knowledge_dual_channel_interface.py`
- smoke/JSONL：`tools/smoke_knowledge_dual_channel_interface.py`

## 3. 数据结构（M0）

- `KnowledgePersistCandidate`
- `KnowledgeOptimizationCandidate`
- `KnowledgeInjectionSlot`
- `KnowledgeDualChannelInterfaceResult`

字段以 `decision_monitor/knowledge_dual_channel_interface.py` 为准。

## 4. 最小生成规则（M0）

- Persist Candidate：优先依据 `optimization_feedback_loop.worth_persisting_to_library` 生成候选；不做真实写库
- Optimization Candidate：issue 持续/建议无效/数据不足时，标记 `needs_external_strategy_support=true`（占位，不做 lookup）
- Injection Slot：按 issue/hint 粗映射目标模块（例如分支问题→`hypothesis_layer`），只输出 reserved slot，不执行注入

## 5. CONTRACT 强约束（写死）

图书馆系统正式接入前，统一通过 Knowledge Dual-Channel Interface 预留层承接沉淀候选、优化候选与策略注入口；不得提前散落实现图书馆写入、查找或注入逻辑。

## 6. 结论（M0）

双通道与注入口已占坑并接入 frame/JSONL/Console；后续图书馆接入应优先复用本接口预留层。

