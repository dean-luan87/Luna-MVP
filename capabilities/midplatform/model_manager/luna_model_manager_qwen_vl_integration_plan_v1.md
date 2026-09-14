# Luna Model Manager — Qwen-VL Real Provider Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-Planning-v1-001`  
**Layer:** Model Manager → Provider (Qwen-VL)  
**Mode:** Planning only — 定义迁移架构与验证边界，不删除 Teacher Adapter 遗留模块。

---

## 1. 战略定位

Qwen-VL 不再是「特殊 Teacher」，而是 Model Manager 管辖下的标准 provider：

```json
{
  "model_id": "qwen_vl",
  "type": "vision_language_model",
  "capabilities": ["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
  "provider_type": "external_teacher",
  "owner": "model_manager"
}
```

**验证目标：** Luna 能否把一个真实模型完整纳入生命周期管理，而非验证 Qwen 能力本身。

---

## 2. 架构迁移

### Before（冻结为前置成果）

```
L1 → Teacher Router → Qwen Adapter → Evidence
```

### After（本阶段规划）

```
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
L2.5 Decision Validation
        ↓
Model Manager（Capability Match + Routing + Lifecycle Gate）
        ↓
Qwen-VL Provider（model_manager/providers/qwen_vl/）
        ↓
Evidence Candidate
        ↓
Validation
```

---

## 3. 模块布局

```
model_manager/
├── registry/          # model_registry_v1.json — qwen_vl lifecycle_state
├── capability/        # capability_registry — unknown_scene_reasoning
├── routing/           # model_routing_engine_v1
├── lifecycle/         # admission / activation / deprecation
├── evaluation/        # model_evaluation_engine_v1
└── providers/
    └── qwen_vl/
        ├── qwen_vl_provider_adapter_v1.py
        ├── qwen_vl_request_builder_v1.py
        ├── qwen_vl_response_parser_v1.py
        ├── qwen_vl_provider_profile_v1.json
        └── governance/qwen_vl_model_manager_provider_policy_v1.json
```

`teacher_adapter/providers/qwen_vl/` **保留冻结**，本阶段在新路径建立 Model Manager 归属的 provider 层，通过薄封装复用已验证的 request/parser/real_provider 逻辑。

---

## 4. 本阶段验证点

| # | 验证点 | 说明 |
|---|--------|------|
| 1 | Model Registry 接管 | `discovered→candidate→evaluating→admitted→active`，禁止 `if provider=="qwen"` |
| 2 | Capability Routing | `unknown_scene` → `unknown_scene_reasoning` → `qwen_vl` routing_candidate |
| 3 | 不适合场景拒绝 | `read_small_text` → OCR 优先，Qwen `not_selected` |
| 4 | Lifecycle 联动 | v1 active → v2 candidate → eval → active → v1 deprecated |
| 5 | Provider 边界 | 仅 evidence_candidate，禁止 fact/plan/execution |

---

## 5. Smoke Cases

- **A** unknown_scene → MM 选 Qwen → Evidence Candidate → Validation
- **B** shopfront_sign → OCR selected，Qwen noop
- **C** API timeout → provider_error_candidate → fallback_plan_candidate → L2
- **D** 幻觉「This is Starbucks」无证据 → unsupported_claim → reject
- **E** qwen_vl v1 active / v2 upgrade → v1 deprecated

---

## 6. 边界（必须保持）

**允许输出：** `teacher_evidence_candidate`, `scene_hypothesis_candidate`, `visual_reasoning_candidate`  
**禁止输出：** `scene_fact`, `selected_plan`, `tool_execution`, `fact_write`

---

## 7. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001`

完成 DryRun 后，优先接入**本地模型**（InternVL / MiniCPM-V）验证 External vs Local 统一管理。
