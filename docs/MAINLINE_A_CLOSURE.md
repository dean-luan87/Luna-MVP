# 主线 A 收口说明

**收口日期**：本轮完成即视为主线 A 封版收口。  
**范围**：决策显示器（主线 1）+ Scene Gate v1 轻量控制 + 人工沟通校准 + 超时闭环 + goal 暂停消费点。

---

## 一、本条线交付物

| 能力 | 说明 | 状态 |
|------|------|------|
| 场景判断 | scene_type / scene_supported / scene_gate_state / scene_gate_action | ✅ 已接入 |
| 运行域判断 | runtime_domain_guard → state 与 Scene Gate 输入 | ✅ 已有 |
| 视线/视觉守护 | view_guard → state | ✅ 已有 |
| 短时容错 | predictive_hold → state | ✅ 已有 |
| **Scene Gate 控制** | continue_normal / pause_goal_progress / freeze_to_minimum_mode → state 四字段 + goal_status，主循环写 runtime_ctx | ✅ 已闭环 |
| **人工沟通校准** | 三类触发、短问句、human_check_* 字段；needed 时暂缓高代价动作，有回复则按回复落盘 | ✅ 已闭环 |
| **超时默认动作** | human_check_started_ts + 每帧 check_timeout_and_apply_default，超时写 default_action，与用户回复同一消费路径，resolved 后清理 | ✅ 已闭环 |
| **goal 暂停消费** | should_advance_goal(runtime_ctx)；goal_progress_paused=True 时主循环跳过 SPEAK 推进，打 log goal_progress_skipped_by_scene_gate | ✅ 已闭环 |

---

## 二、关键文件（不改契约前提下可维护）

- **decision_monitor/**：schema.py（state 字段）, builder.py（scene_gate + _apply_scene_gate_control + _apply_interaction_calibrator）, scene_gate.py, interaction_calibrator.py
- **runtime/**：context.py（RuntimeContext 字段）, gates.py（should_advance_goal）, human_calibrator.py（check_timeout_and_apply_default）
- **main.py**：Decision Monitor 块（超时检查、monitor_ctx、写回 runtime_ctx、清理）；_execute_speech_decision 中 Scene Gate 抑制与 should_advance_goal 阻断
- **tools/decision_monitor_viewer.py**：顶部横幅、Scene Gate / 人工沟通校准卡片、state 折叠 human_check_*
- **decision_monitor/CONTRACT.md**：6 层契约与字段来源（含 Scene Gate 轻量控制 + 人工沟通校准）

---

## 三、验收与测试

- 单测：`tests/test_decision_monitor.py` 中 Scene Gate、interaction_calibrator、timeout、should_advance_goal、builder 写入 timeout_triggered 等用例。
- 行为验收：continue_normal 行为不变；pause/freeze 时先可进入人工确认；超时后自动 default_action；用户回复按回复执行；goal_progress_paused 时真实阻断 SPEAK 推进；Viewer 可区分超时与用户回复、可看到 goal 被 Scene Gate 阻断。

---

## 四、可选后续（backlog，不占主线）

- 扩展人工确认问题库或更多触发条件
- 接真实语音/按钮输入替代注入 human_check_response
- 更多“推进 goal”的消费点统一经 should_advance_goal 判断
- 不新增 scene 类型、不改 Dynamic Policy/B2、不改 detector/OCR 主逻辑

---

## 五、一句话

**主线 A：从「能判断边界」到「会按边界行动」+「可人工复核」+「超时落地」+「暂停真实生效」已闭环；本条线收口，后续为 backlog 或下一主线。**
