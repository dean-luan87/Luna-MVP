# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement Controlled Short-Window Trial Preparation Blocker And Allowlist v0（阻断项与白名单冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_CONTROLLED_SHORT_WINDOW_TRIAL_PREPARATION_BLOCKER_AND_ALLOWLIST_V0.md`  
**性质**：Phase-Next-154：列出进入下一阶段短窗 preparation 的白名单/黑名单，并区分 hard blockers 与 soft follow-ups（无代码）

---

## 1) Hard Blockers（硬阻断项；写死触发即 no_go）

任一出现即判 **no_go**（必须阻断并进入修复冲刺）：

- 无 `start_event_observed` 却出现 started（started 判据不唯一/被绕过）
- 无 started 却出现 release/window 打开（release 越界）
- started 后无法 closure（started-but-unclosed）
- closure 后 `side_effects_released` 未回落为 false（收口失败）
- illegal path 无法被识别/拦截
- 出现 default-on 风险（任何默认路径自动触发真实启用）
- 下一阶段会实质性扩大 side effects 面却无新增边界控制

---

## 2) Soft Follow-Ups（软补强项；不阻断 go/conditional_go）

建议项（不影响当前边界成立）：

- 153 evaluation JSON 输出的只读归档（CI artifact）与版本化
- reason codes 更细粒度的标准化编号（不改边界语义）

---

## 3) Allowlist（下一阶段允许做；写死）

允许进入下一阶段（controlled short-window trial preparation）后做：

- 在 **非默认路径** 下进行 controlled short-window trial preparation
- 继续沿用 151 唯一 start_event 判据
- 继续沿用 started 后短时 release window（必须可回落）
- 继续沿用最小成功/失败/收口路径
- 继续沿用显式 gated real-start intent
- 增加更严格的观测、审计、窗口限制、人工确认限制（不改变 started/release/closure 边界）

---

## 4) Denylist（下一阶段禁止做；写死）

下一阶段绝对禁止：

- default-on
- full controlled trial
- 扩大 side effects 面（新增真实副作用类别）
- 绕过 start_event 判据
- 去掉 closure 强制收口
- 将 preparation_go 等同于 started
- 将 dry-run / shadow 证据当成 real started 证据
- 在未新增治理定义前扩大运行时长或运行范围

