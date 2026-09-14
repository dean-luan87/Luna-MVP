# Single Model Interaction Validation Governance Standard V1

**Standard ID:** `SingleModelInteractionValidationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001`  
**Upstream GO:** `P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO`

## 目的

验证模型结果能否成为中台下一轮决策输入，而非继续测试 MobileSAM 执行本身。

## 治理链（本阶段扩展）

```
Runner Execution → Result Envelope → Result Candidate
    → Midplatform Processing → Observation Update Candidate
    → followup_model_route_candidate → new_task_candidate
```

## 五条硬约束

1. **Result Envelope → 中台输入** — 禁止 MobileSAM output 直出 UI 路由  
2. **Result 不污染 Observation** — attention record 保持 candidate，结果仅作 evidence；`result_candidate_not_observation_owner`  
3. **中台二次调度** — 禁止 MobileSAM → OCR API pipeline bypass  
4. **Human Correction** — priority signal only；禁止修改 mask  
5. **Trace 闭环** — Image → … → Observation Update → New Task Candidate 须可追溯  

## 本阶段禁止

- OCR / Detection runner execution  
- fact write / auto fact admission  
- MobileSAM 输出 fact label（如「这是路牌」）  
- 覆盖 segmentation boundary owner / Visual Expression  
- 用户纠错作为 ground truth  

## Case 1

`Case-1-MobileSAM-to-OCR-Route-Candidate`：街景图 → MobileSAM regions → 中台判定 OCR 候选 → **不跑 OCR**。

## Human Correction 中台入口

用户纠错 **必须** 先进入 Human Correction Layer → Midplatform Analysis，**禁止** raw log 直训。

归因四类 → 路由五出口（训练只是其中之一，且须 `pending_review`）。

详见 `correction_attribution_taxonomy_v1.json` 与 `correction_midplatform_analyzer_v1.py`。

`Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001`
