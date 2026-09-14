# Luna Navigation Mainline — Thread Wiring v0（导航主流程接线计划）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_MAINLINE_THREAD_WIRING_V0.md`  
**目标（写死）**：先把“导航主流程跑起来”。本轮优先做线程接线 + 主流程贯通 + 最小运行验证；不追求漂亮抽象。  
**不做**：大重构、视觉解释增强、白盒/provenance、模型语义、更多 gate、完整冲突治理实现。  

---

## A. 文档定位

- 当前目标是“把导航主流程跑起来”。  
- 不是做完美架构。  
- 不是做视觉解释增强。  
- 不是做完整冲突治理实现。  

---

## B. 当前最小导航主流程（想打通的闭环）

最小闭环（v0）希望达到：

**输入 → 会话状态锚 →（可选）语义转换 → 主链分流（BridgeDecision/Proposal）→ admission layer → 响应/输出（可观测）→ 导航结果承接（进入导航执行线程/管理器）**

写死说明：  
- 若“导航结果承接”未接上，必须明确断点；本文件以“断点定位 + 接线顺序”优先。

---

## C. 当前线程/链路角色（最少角色划分）

- **输入链**：`VoiceInputSessionManager` 负责把文本组装为 `VoiceInputEvent`，并在开发开关下写入 `luna_voice_semantic_v2` 与 V3 输入包。  
- **状态链**：`VoiceV1SessionStateAnchor` 记录可观测事实（last_user_text/last_system_text/waiting）。  
- **语义链（辅助）**：`SemanticConverterV2` 产出语义包；V2 shadow/assist 仅观测/确认信号，不夺权。  
- **主链分流**：`dispatch_voice_final_text(...)` 生成 `BridgeDecision` 与 proposal（device_control / task_lifecycle 等）。  
- **执行准入**：Resource Gate + Information Confirmation Gate 决定“是否允许执行型 submit”。  
- **输出链**：执行型 submit 仅覆盖 rejected_input / session_wake；响应型 submit 走 Response Submit Template Interface（已冻结）。  
- **导航执行线程/承接（目标）**：应接收 `TASK_LIFECYCLE` 的导航启动 proposal 或长链 task_plan，并驱动真实导航（目前未完全接通）。  
- **观察旁路**：`sidewalk_nav_v1` 目前为 whitebox-only（只写 metadata，不外显播报候选）。  

---

## D. 本轮只接的范围（写死）

- 本轮只把最小导航主流程的“线程边界”接通到可观测层面：  
  - 让导航相关 proposal 真实穿过 **Bridge → Core 边界占位**（不执行，只产出 trace）  
  - 明确导航结果承接仍缺哪一跳
- 不做更多智能增强、不做更多 gate、不做视觉解释、不做白盒/provenance、不做复杂协商。

---

## E. 当前最小验收标准（v0）

至少满足：
- 主流程能从输入走到**可观测输出**（执行型或响应型）  
- 关键线程边界不再是“孤立占位”（至少能看到 BridgeDecision 已进入 Core boundary placeholder trace）  
- 被 gate 拦截时有一致响应（例如 continue-request + information gate 固定模板）  
- 现有 V1 回归不被破坏  

并明确：  
- 若“导航执行线程”仍未接上真实 start_navigation，则本轮验收以“断点定位 + 可观测 trace + 回归不破坏”为准，并在下一轮以最小执行承接替换 placeholder。

