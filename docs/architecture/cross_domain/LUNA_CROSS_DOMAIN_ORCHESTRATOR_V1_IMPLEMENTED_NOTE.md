# 跨域旁路：统一主线编排入口（V1）实现说明

## 改了什么

在不改变任何旁路内部逻辑/白盒结构的前提下，把 `voice_final_text_dispatcher` 中原本分散的三段旁路 helper 串联调用，收拢为一个统一入口：

- `_run_cross_domain_orchestrator_v1(...)`

该入口在同一轮主线分流中按固定顺序调用：

1. `risk_interrupt_v1`
2. `sidewalk_nav_v1`
3. `retail_find_item_v1`

并统一传入 `VoiceRuntimeContext`、统一合并 `VoiceFinalTextDispatchResult.metadata`（保持三个并列 key）。

## 为什么仍是 Level 1 / whitebox-only

V1 orchestrator 的定位是“统一编排 helper”，不是全局裁决器：

- 不做 Level 2
- 不做 speaking/runtime 接管
- 不做真实输出候选（不提交 SpeechRequest）
- 不做跨旁路融合输出

只把既有的 whitebox-only 深接入路径收拢，避免后续 hook 越来越多、顺序逻辑散落。

## 怎么验证

```bash
python3 tools/test_cross_domain_orchestrator_v1.py
python3 tools/test_risk_interrupt_v1_context_source_integration.py
python3 tools/test_sidewalk_nav_v1_deep_integration.py
python3 tools/test_retail_find_item_v1_deep_integration.py
```

## 与原分散 hook 模式相比收拢了什么

- 顺序逻辑集中到单一入口（不再在三个分支各自重复串联）
- `runtime_context` 的传递与 metadata 合并路径统一
- 为未来“更强编排/submit 实链/Level 2”预留唯一生长点

## 回退边界

提供最小运行时回退开关（默认不影响行为）：

- `LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1=1`：回退到原“分散 helper 串联”路径

或直接关闭各旁路开关（零侵入）。

## 统一观察摘要（`metadata["cross_domain_orchestrator_v1"]`）

编排层在每轮跑完三条旁路 helper 之后，额外写入一份**总括白盒摘要**（不复制各旁路 dict 的全量字段，也不改各旁路内部结构）。

### 为什么需要这一层

三条旁路各自有并列 metadata key，但缺少「本轮 orchestrator 实际做了什么」的单点视图：谁被开关启用、谁真正写入了结果、谁被风险压制、最终挂了哪些 key。统一摘要减少排查时在多条 metadata 之间来回对账的成本，并为后续 Level 2 准入评审提供编排层证据面。

### 与三条旁路 metadata 的区别

| 维度 | 旁路 `risk_interrupt_v1` / `sidewalk_nav_v1` / `retail_find_item_v1` | `cross_domain_orchestrator_v1` |
|------|----------------------------------------------------------------------|--------------------------------|
| 内容 | 各域白盒细节（事件、候选、压制标记等） | 仅编排视角的短字段列表与布尔标记 |
| 职责 | 单旁路可观测性 | 本轮编排：启用 / 执行 / 压制 / 挂载 key 列表 |
| 行为 | 各 helper 原有逻辑 | **只读**合并后的 metadata 与 context，不改 dispatch 结果 |

### 字段（V1）

- `enabled_capabilities`：环境开关层面启用的旁路 id 列表（固定顺序子集）
- `executed_capabilities`：本轮实际在 `metadata` 中出现的旁路 key（有挂载即视为执行了对应 helper 路径）
- `suppressed_capabilities`：白盒中 `output_suppressed_by_risk=True` 的旁路（当前为 sidewalk / retail）
- `risk_preempt_active`：来自 `risk_summary_v1` 的压制信号（`high`/`critical` 或 `risk_interrupt_preempt`）
- `whitebox_only_mode`：三模块均可导入且 `*_whitebox_only()` 均为 True
- `metadata_keys_attached`：本轮最终挂载的旁路 metadata key 列表（与上三者 key 一致）
- `orchestration_order`：固定顺序 `risk_interrupt_v1` → `sidewalk_nav_v1` → `retail_find_item_v1`
- `event_timestamp`：事件时间戳（毫秒；优先 `VoiceInputEvent.timestamp`）
- `near_real_output_candidate_any`：V1 深接入阶段固定为 `False`（无真实输出候选晋升）

**写入条件**：至少有一条旁路在开关层面为「启用」时才写入该摘要；**全关**时不写入 `cross_domain_orchestrator_v1`（零侵入与「无编排摘要」一致）。

验证：`python3 tools/test_cross_domain_orchestrator_v1.py`。

## 哪些还没做

- 不做跨旁路融合输出与全局裁决器改造
- 不做动态调度/全局打分
- 不做 Level 2（抢占/挂起/恢复）
- 不接 speaking/runtime 的真实来源

