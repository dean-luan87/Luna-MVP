# Luna 语音长输入拆解接入 v1 — 变更清单

## 1. 新增对象/脚本

| 路径 | 说明 |
|------|------|
| `capabilities/voice/bridge/voice_long_input_task_planner.py` | 入口：`run_long_input_task_planning_v1` |
| `capabilities/voice/bridge/voice_long_input_domain_classifier.py` | 规则版 `classify_long_input_text` |
| `capabilities/voice/bridge/voice_long_input_instruction_mapper.py` | `map_long_input_instructions` |
| `capabilities/voice/bridge/voice_long_input_task_plan_builder.py` | `build_task_plan_v1_from_candidates` |
| `capabilities/voice/schemas/voice_long_input_instruction_candidate.py` | 指令候选 |
| `capabilities/voice/schemas/voice_long_input_parse_result.py` | `VoiceLongInputParseResult` |
| `shared/schemas/task_plan.py` | `TaskPlan` 增加 `knowledge_collaboration_pending`、`task_optimization_pending`、`next_stage` |
| `tests/test_voice_long_input_task_planning_v1.py` | 场景 1–7 |

## 2. 长输入骨架流转

```
切段后长文本
  → run_long_input_task_planning_v1
  → split_segments（>3 段 → 澄清）
  → classify_long_input_text → DomainClassificationResult
  → map_long_input_instructions → 候选列表
  → build_task_plan_v1_from_candidates → TaskPlan(v1)
  → VoiceLongInputParseResult
```

## 3. 当前支持的模式（规则版）

- 单任务导航 / 观察  
- 顺序双任务（如「先去…，再…」）  
- 条件从句（两段：「…，如果…」）  
- 导航 + 伴随观察（分句）  
- 不支持域（如自动挂号）→ `rejection_needed`  
- 分段过多 → `clarification_needed`  

## 4. 当前不支持

- LLM/真实 ASR 语义  
- V2/Final、真实知识协同与优化执行  
- 复杂任务图、多分支恢复  

## 5. 为什么仍不是「完整长语音理解系统」

仅 **规则骨架 + 白名单映射**；模型接入后替换分类器/映射器实现，**不改变**协议顺序与 `task_plan_v1` 形状。

---

说明文档：[LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md](./LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md)
