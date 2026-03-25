# Memory vs Novel Information Channel M0（记忆信息 / 新增信息双通道 M0）交付

## 1. 定位（写死）

本模块是**信息来源通道层**，用于在推理过程中显式区分：

- **记忆信息通道**（memory-derived）：来自既有记忆/经验支持的驱动信息
- **新增信息通道**（newly-observed）：来自当前帧/当前轮新观察得到的信息
- **排除推断通道**（inferred-from-exclusion）：通过排除/剪枝得到的推断信息
- **用户提供通道**（user-provided）：用户反馈/补充信息驱动的内容
- **混合通道**（hybrid）：记忆与新观察共同驱动

**强约束**：本轮只做通道与标记层 + 新信息→记忆候选占位；不做长期记忆系统重构、不做评分系统、不做图书馆写入/检索/注入。

## 2. 代码交付

- 生成器：`decision_monitor/memory_novel_information_channel.py`
- frame 字段：`DecisionMonitorFrame.memory_novel_information_channel`
- Console 接入：
  - `tools/reasoning_console_aggregator.py`（快照聚合）
  - `tools/reasoning_console_server.py`（新增轻量区块展示）

## 3. 数据结构（M0 最小）

- `InformationChannelItem`
  - channel_type: memory_derived / newly_observed / inferred_from_exclusion / user_provided / hybrid
  - channel_label / channel_summary / channel_source_module
  - channel_used_in_reasoning / channel_used_in_decision
- `NovelMemoryCandidate`（占位）
  - candidate_label / candidate_reason / candidate_source
  - candidate_ready_for_memory（M0 默认 false）
- `MemoryNovelInformationChannelResult`
  - information_channels
  - memory_channel_count / novel_channel_count / hybrid_channel_count
  - dominant_reasoning_channel / dominant_decision_channel
  - novel_memory_candidate（可空）
  - channel_summary / channel_applied

## 4. 最小来源标记规则（M0 规则版）

- **user_provided**：存在 `confirmation_input_bridge.confirmation_input_raw_text/type`
- **memory_derived**：`object_temporal_ledger` 有 last_confirmed 信息，或 `experience_evolution` 有 watchlist/promotable 候选（轻量判定）
- **newly_observed**：`visual_candidate_audit` 有候选标签，或 `spatial_expression_sidecar` 有候选（轻量判定）
- **inferred_from_exclusion**：结构树存在 pruned/rejected 节点，或（dead_branch>0 且 issue=high_dead_branch_ratio）作为弱信号
- **hybrid**：memory_derived 与 newly_observed 同时存在
- **dominant**：按通道数量与“是否直接影响决策”的轻量规则输出 dominant_reasoning / dominant_decision

## 5. 新信息 → 记忆候选（占位）

当 `newly_observed` 或 `inferred_from_exclusion` **对当前决策产生关键影响**（M0 以 next_effect / effective_feedback_count 近似）时，生成 `novel_memory_candidate`：

- **只占位**：不写入任何记忆库
- `candidate_ready_for_memory` 在 M0 默认 false

## 6. 与结构树 / 时间轴 / 白盒的结合方式

- **结构树**：root 摘要追加一行 `channel=reasoning:*/decision:*`（轻挂接，不改树主结构）
- **时间轴**：追加一条 info_channel 摘要事件 +（可选）novel_memory_candidate 摘要
- **白盒（成长链）**：Evidence/Hypothesis 与 Experience Governance 白盒结果新增 `information_channel_summary`（一行摘要；不重构五块白盒骨架）

## 7. 测试与验证

- 单测：`tests/test_memory_novel_information_channel.py`（5 类：memory / novel / inferred+cand / user / hybrid）
- smoke：`tools/smoke_memory_novel_information_channel.py`
  - 验证 frame 中存在 `memory_novel_information_channel`
  - JSONL 落盘
  - dominant_* 字段可读
  - novel_memory_candidate 在条件满足时出现

## 8. 结论（M0）

Memory vs Novel Information Channel M0 已完成信息来源“双通道”与标记层，并在 Console/结构树/时间轴/成长链白盒中完成轻量接入；后续复杂记忆治理与图书馆系统必须在该通道层基础上展开，不得绕开。

