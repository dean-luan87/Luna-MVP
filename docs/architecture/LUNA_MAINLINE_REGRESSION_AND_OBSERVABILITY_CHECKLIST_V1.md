# 主线统一回归与观测清单（V1）

## 目标

把当前系统“已落地且相互联动”的主线能力，收敛为一个**固定回归入口**，用于后续每次工程改动后按清单执行回归与对账，避免靠手工记忆脚本与开关。

本文件只做整理，不改代码。

---

## 1. 当前必须覆盖的主线模块（事实清单）

### 1.1 submit / request / playback / cancel 真链路（输出链骨架）

- **submit 最小闭环**：`SpeechRequest` 生成 → `VoiceOutputPlaneV1.submit()` 调用成立  
- **request 真源**：`request_runtime`（created/submitted/terminal）可对账  
- **playback 真源（V1）**：`playback_runtime`（started/finished/failed/cancelled）可对账；**dry-run 不伪造**  
- **最小真实执行层**：`playback_plane_v1` + `audio_worker_v1`（单线程/单队列）  
- **最小 cancel 真能力**：按 `request_id` 取消“待执行或正在执行”的请求并产出 `playback_cancelled`

### 1.2 orchestrator（跨域编排与统一摘要）

- `cross_domain_orchestrator_v1`：固定顺序 `risk → sidewalk → retail`  
- 统一观察摘要：`metadata["cross_domain_orchestrator_v1"]`

### 1.3 三条旁路 Level 1 深接入（whitebox-only）

- `risk_interrupt_v1`：Level 1 深接入 + Level 2 受限试点（默认关闭）  
- `sidewalk_nav_v1`：Level 1 / whitebox-only  
- `retail_find_item_v1`：Level 1 / whitebox-only

### 1.4 risk_interrupt_v1 两条试点路径（可控观察态）

两条路径并存（均默认关闭），并已具备观测与回退：

- **Level 2A**：preempt-before-submit  
- **Level 2B**：cancel+replace（pending only）

并具备：

- P0：`pilot_state_transition`（回退到 L1/L0 可统计）  
- P1：cancel+replace 越界检查字段（`risk_level` / `target_output_category`）  
- analyzer 最小聚合：`tools/analyze_risk_interrupt_v1_pilot.py`  
- 观察窗口模板：`LUNA_RISK_INTERRUPT_V1_PILOT_WINDOW_REVIEW_TEMPLATE_V1.md`

---

## 2. 当前必须执行的回归脚本清单（固定入口）

> 说明：下列脚本均位于 `tools/`。建议每次改动后按 §5 顺序执行。

### 2.1 Smoke（默认必跑，成本低）

- `python3 tools/test_real_output_submit_v1.py`  
  - **测什么**：submit 最小闭环（dry-run 下的 submit_invoked/selection/cutover/request_terminal 等节点）
- `python3 tools/test_request_runtime_source_v1.py`  
  - **测什么**：request 真源事件序列（created/submitted/failed/rejected/terminal）
- `python3 tools/test_playback_runtime_source_v1.py`  
  - **测什么**：playback 真源（dry-run 不伪造；执行路径下终态正确）
- `python3 tools/test_cross_domain_orchestrator_v1.py`  
  - **测什么**：跨域编排入口与 orchestrator 统一摘要字段
- `python3 tools/test_interrupt_cancel_v1.py`  
  - **测什么**：cancel 真能力 + `playback_cancelled` 终态不与 finished 混淆

### 2.1.x Unified Env Min Wiring V1 Validation Gate（改到相关范围时必跑）

> **失败即阻断**：若该项失败，则不得视为通过相关改动验收；发布/合入前必须修复或更新 contract + smoke + analyzer 并重新验证。

- **何时必跑（适用范围）**：只要改动涉及以下任一范围，就必须跑此项：  
  - `capabilities/voice/runtime/voice_final_text_dispatcher.py`  
  - `unified_env_min_wiring_snapshot_v1` 相关输出结构（`type`/`data`/`metadata` 承载方式）  
  - `tools/analyze_unified_env_min_wiring_v1.py`  
  - `tools/smoke_compare_unified_env_min_wiring_v1.py`  
  - `unified_env_fill_shadow_v1` / `unified_env_summary_shadow_v1` / min wiring metadata 接线
- **固定执行命令**：
  - `python3 tools/smoke_compare_unified_env_min_wiring_v1.py --envelope-jsonl logs/unified_env_min_wiring_snapshot_v1.jsonl --flat-jsonl logs/window_real_unified_env_min_wiring_round02.jsonl`
- **通过标准**：
  - exit 0
  - 输出包含：`OK: envelope and flat results match`
- **关联文档**：
  - `docs/contracts/UNIFIED_ENV_MIN_WIRING_V1_CONTRACT.md`
  - `docs/validation/UNIFIED_ENV_MIN_WIRING_V1_SMOKE.md`

### 2.2 深链路验证（改到相关模块时必须跑）

- `python3 tools/test_real_playback_execution_v1.py`  
  - **何时必跑**：改动 `playback_plane_v1` / `audio_worker_v1` / 输出执行链  
  - **测什么**：started→finished/failed/cancelled 四事件闭合

### 2.3 旁路深接入回归（改到旁路/编排/metadata 时必须跑）

- `python3 tools/test_risk_interrupt_v1_deep_integration.py`
- `python3 tools/test_sidewalk_nav_v1_deep_integration.py`
- `python3 tools/test_sidewalk_env_summary_v1_integration.py`（稳定化 summary 主线接入 + sidewalk 消费）
- `python3 tools/test_retail_env_summary_v1.py`（retail_env_summary_v1 稳定化 builder）
- `python3 tools/test_retail_env_summary_v1_integration.py`（稳定化 summary 主线接入 + retail 消费）
- `python3 tools/test_retail_find_item_v1_deep_integration.py`

### 2.4 risk_interrupt_v1 试点链路回归（改到试点逻辑/观测/开关/聚合时必须跑）

- `python3 tools/test_risk_interrupt_v1_level2_pilot.py`（Level 2A）
- `python3 tools/test_risk_interrupt_v1_cancel_replace_v1.py`（Level 2B pending-only）
- `python3 tools/test_risk_interrupt_v1_pilot_state_transition.py`（P0 回退 telemetry）
- （可选）`python3 tools/analyze_risk_interrupt_v1_pilot.py --input <trace.jsonl>`  
  - **测什么**：指标可统计 + suspicious 样本导出入口可用

---

## 3. 当前必须关注的观测文件/trace（对账入口）

### 3.1 JSONL trace（主线统一落盘）

- `LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL` 指向的 JSONL  
  - 典型包含：`request_runtime`、`playback_runtime`、`output_decision`、`pilot_state_transition`、以及 submit/selection/cutover 等

### 3.2 analyzer 输出（risk 试点窗口）

- `logs/analyze_risk_interrupt_v1_pilot_<UTC>.md`
- `logs/analyze_risk_interrupt_v1_pilot_<UTC>.json`

### 3.3 关键“实现说明/状态图”（只读参考）

- `docs/architecture/LUNA_MAINLINE_SYSTEM_STATUS_MAP_V1.md`
- `docs/architecture/cross_domain/LUNA_REAL_OUTPUT_SUBMIT_V1_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_REQUEST_RUNTIME_SOURCE_V1_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_PLAYBACK_RUNTIME_SOURCE_V1_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_REAL_PLAYBACK_EXECUTION_V1_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_CROSS_DOMAIN_ORCHESTRATOR_V1_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_LEVEL2_PILOT_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_CANCEL_REPLACE_IMPLEMENTED_NOTE.md`
- `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_PILOT_WINDOW_REVIEW_TEMPLATE_V1.md`

---

## 4. 当前关键开关矩阵（回归必看）

> 注意：下列开关均应默认关闭；回归时按脚本要求显式打开。

### 4.1 输出链骨架

- `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`：submit 闭环总开关（默认 0）
- `LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS`：是否走执行路径（默认 0）
- `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1`：启用新执行层（默认 0）

### 4.2 cancel 真能力

- `LUNA_ENABLE_INTERRUPT_CANCEL_V1`：cancel 能力总开关（默认 0）

### 4.3 orchestrator/旁路（白盒）

- `LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1`：紧急回退到“非统一入口”（默认不设置）
- `LUNA_ENABLE_RISK_INTERRUPT_V1`：risk 旁路总开关（默认按环境）
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY`：强制白盒模式（默认按环境）

### 4.4 risk Level 2 试点（默认全部关闭）

- `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT`：Level 2A（preempt-before-submit）
- `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT`：Level 2B（pending-only cancel+replace）

---

## 5. 每次改动后的最小回归建议顺序（可执行）

### 5.1 基线 Smoke（建议每次必跑）

1. `python3 tools/test_real_output_submit_v1.py`
2. `python3 tools/test_request_runtime_source_v1.py`
3. `python3 tools/test_playback_runtime_source_v1.py`
4. `python3 tools/test_cross_domain_orchestrator_v1.py`
5. `python3 tools/test_interrupt_cancel_v1.py`

### 5.2 若改到执行层/播放相关（追加）

6. `python3 tools/test_real_playback_execution_v1.py`

### 5.3 若改到旁路/编排/试点观测（追加）

7. `python3 tools/test_risk_interrupt_v1_level2_pilot.py`
8. `python3 tools/test_risk_interrupt_v1_cancel_replace_v1.py`
9. `python3 tools/test_risk_interrupt_v1_pilot_state_transition.py`
10. `python3 tools/analyze_risk_interrupt_v1_pilot.py --input <本次 trace>`

---

## 一句话收束

先把“主线统一回归与观测入口”固定为可执行清单，后续所有工程推进都按这份清单跑回归、看 trace、再做结论。

