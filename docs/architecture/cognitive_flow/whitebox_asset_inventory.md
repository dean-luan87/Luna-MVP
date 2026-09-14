# Whitebox Asset Inventory v1

## Discovery result

No canonical top-level `whitebox/`, `frontend/`, or `backend/` directory exists. The main whitebox estate is the Model Test Lens under `capabilities/midplatform/model_test_lens/`, including static UI, local runner bridge, adapters, diagnostics, and test-board records.

| 组件 | 位置 | 功能 | 依赖 | 迁移建议 |
|---|---|---|---|---|
| Model Test Lens static site | `capabilities/midplatform/model_test_lens/static_site/` | 静态 web UI shell (`index.html`, `app.js`, `styles.css`) | Browser/static assets | **KEEP**：保持开发与测试可视化入口；未来读取 Cognitive Trace。 |
| Observation compact UI | `.../static_site/luna_observation_compact_ui_v1.js` | 观察信息压缩展示 | Observation trace/view data | **MIGRATE**：升级为 Evidence Field / Input Attention 的只读面板。 |
| Situation understanding panel / trace | `.../luna_situation_understanding_panel_v1.js`; `...trace_view_v1.js` | Situation candidate 与 trace 可视化 | Situation candidate records | **MIGRATE**：显示 Current World Understanding Candidate，明确不是事实。 |
| Attention UI | `.../observation_attention_engine_v1.js`; `.../observation_attention_priority_panel_v1.js` | 现有观察注意力展示与优先级 UI | Observation UI state | **REPLACE (control role) / MIGRATE (visual role)**：不得控制新 Attention Controller；可显示 source pool, arbitration, allocation, inertia。 |
| Planning UI / trace | `.../luna_agent_planning_panel_v1.js`; `...trace_view_v1.js` | Agent planning presentation | planning candidates | **MIGRATE**：改为 Process Candidate / Runtime Instance 可视化；不要展示为直接 action plan。 |
| Perception HUD | `.../perception_hud_view_v1.js` and HUD assets | 视觉/感知叠加和调试展示 | Perception/runner outputs | **KEEP/MIGRATE**：作为 evidence source、confidence、scope、conflict 的可视化层。 |
| Model insight / collaboration panels | `.../model_insight_layer_v1.js`; `multi_model_collaboration_panel*` | 模型洞察与多模型协作展示 | model / provider metadata | **MIGRATE**：展示 Capability Bundle Candidate 与 provider availability；不赋予模型控制权。 |
| Scene-task-model activation panel | `.../scene_task_model_activation_panel*` | 场景/任务/模型激活视图 | legacy model activation state | **REPLACE (authority) / MIGRATE (observability)**：改为 Attention Allocation + Capability Composition trace。 |
| SLAM diagnostic panels | `.../slam_diagnostic_panels.js` | SLAM 指标和诊断 | SLAM evaluation outputs | **KEEP**：作为空间 evidence 的调试面板。 |
| Runner bridge UI and admission UI | `.../runner_bridge_ui_v1.js`; `.../runner_invocation_admission_v1.js` | 本地 runner 与准入可视化 | local runner bridge | **KEEP/MIGRATE**：保留为人工测试工具；未来仅接收 Capability Invocation Candidate，不能接受认知模块直接调用。 |
| Local runner bridge service | `.../local_runner_bridge/local_runner_bridge_server_v1.py` | localhost HTTP runner bridge | local execution environment | **KEEP (test-only)**：保持隔离，标记为受控开发工具，不纳入 Cognitive Runtime。 |
| Human correction / visual comparison assets | Model Test Lens static-site files and overlays | 人工校正、视觉对比、图层展示 | UI data / review process | **MIGRATE**：用于 Evidence conflict review 与 trace replay。 |

## Cognitive Whitebox target

Existing whitebox assets can become a **Cognitive Whitebox** only as a read-only observability system. Recommended future panes are:

1. Evidence source, scope, confidence, and conflict;
2. Current World Understanding / Context / Goal candidates;
3. Attention source pool, controller arbitration, allocation, lifecycle;
4. Workspace / simulation / evaluation candidates;
5. Kernel constraint and consistency candidates;
6. Process Candidate / Runtime Instance lifecycle;
7. feedback and error-attribution candidates.

The UI must never mutate Cognitive State, approve truth, directly invoke models, or bypass Reducer authority.

**Whitebox estate status: `KEEP` as diagnostics, `MIGRATE` as Cognitive Whitebox; no direct cognitive authority.**
