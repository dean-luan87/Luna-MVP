# Luna-2 项目上下文（Project Context）

本文档为仓库级上下文说明，供新成员与 AI 助手快速把握项目定位、红线与架构入口。详细架构见 [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md)，功能与使用见根目录 [README.md](../README.md)。

---

## 项目定位

**Luna-2** 是集成**视觉感知、语音交互与智能导航**的综合性 AI 系统。在代码层面，重点包含：

- **A3 决策引擎**：基于多源信号输出环境模式（safety_level、control_mode、advice_budget_scale 等）。**A3Engine** 本身纯函数、无副作用、可确定性复现；**A3Runtime** 会写 rhythm_state、engagement、eligibility、view_confidence，属于状态演进，两层需区分。
- **视觉流水线**：统一视觉入口（LV2→LV3→LV4、C1/B2、被动 ROI/Path/Branch）。视觉不直接驱动执行，只通过 **ObservationFrame** 与 **A3Signals** 进入决策链。
- **C 决策链**：L1 硬安全 → L2 环境 → L3 不确定性，产出执行意图并经 veto 适配执行。
- **干预与建议**：介入资格、节律、参与度、建议预算等，与 A3 模式协同。

---

## 技术红线（必守）

1. **确定性护栏**  
   任何对 Luna 视觉导航的修改，必须通过 **`tools/determinism_guard.py`** 方可视为有效。该脚本对比两段 trace 的 decision 序列（seq + safety_level + control_mode）。

2. **标注资产**  
   Phase 3.3 人类标注答案视为**不可变资产**，不反写策略、不触碰模型；学习阶段须离线消费 answers。

---

## 决策权责边界

A3、C、Intervention、Advice、Vision pipeline 等多层参与时，权责必须唯一锚点，避免 AI 或人工修改时误触：

- **最终执行意图 = C 决策 + 执行 veto**  
  C 链（L1/L2/L3）产出是否通过、理由与事实；执行层 `apply_c_veto` 得到最终执行意图并写 trace。A3 的 EnvironmentMode、Intervention 的 eligibility、Advice 的 budget 等只影响「输入给 C 的 snapshot」或下游策略，不直接决定执行意图。

---

## 当前阶段目标

（以下由维护者填写，使本文档成为**动态定位文档**而非仅静态结构描述。）

- **当前版本目标**：（例：v1.8.5 闭环、C1 Active 可回放等）
- **当前阶段任务**：（例：稳定化、D1 回归、某 gate 收口等）
- **当前冻结版本/基线**：（例：FROZEN_BASELINE_v0.9.0、某 fixture 版本）
- **当前风险点**：（例：某模块尚未通过 determinism_guard、某依赖待升级等）

---

## 标准测试视频

- **文件**：项目根目录 **`test_video_complex_6m42s.mp4`**（6 分 42 秒）。
- **用途**：A3 trace、vision pipeline、ROI/Path/Branch 等验证的固定入口。
- **示例**：
  ```bash
  python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4
  python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
  ```

---

## 核心目录速览

| 路径 | 说明 |
|------|------|
| **a3/** | A3 引擎：A3Engine、A3Config、SafetyLevel/ControlMode、gates、providers |
| **runtime/** | 主循环、ObservationFrame、A3Runtime、trace 写入 |
| **vision_pipeline/** | 视觉流水线控制器、LV2–LV4、C1 控制器、B2、被动 ROI/Path/Branch |
| **core/** | 系统 snapshot、场景状态、决策控制器、语音门控、风险评估、观察者模式等 |
| **c/** | C 决策链：L1/L2/L3、build_c_input、decide、CResult |
| **intervention/** | 介入资格、节律、参与度（engagement） |
| **advice_budget/** | 建议预算、仲裁、参与度调制 |
| **vision_perception_b1/** | B1 感知：passive_roi、path/branch、pipeline |
| **map_d0/**、**roi_learning_c1/**、**pal_roi_bridge/** | 地图、ROI 学习、PAL–ROI 桥接 |
| **main.py** | 应用入口 LunaBadgeMVP，协调 pipeline、obs_loop、A3、C |
| **tools/** | 确定性护栏、A3 trace 运行/分析、回放、压力测试、各类 guard/verify |

---

## 主数据流（简要）

1. **帧输入** → `main.py` 的 `process_frame()`。
2. **视觉流水线** → `PipelineController.process_frame()`：LV2 质量门 → LV3 语义路由 → LV4 导航/建模执行器；产出 navigation_result、modeling_result。
3. **观测采样** → `obs_loop.step(_build_real_obs)` 得到 `ObservationFrame`（seq, sampled, motion/path/branch/roi, pal, complexity, vc 等）。主循环每 tick 仍运行，C 决策每 tick 仍运行，A3Runtime 仍会收集信号；**仅 rhythm/engagement 的推进**受 `obs.sampled` 控制（非 sampled 时不推进 L2/TTL/冷却等）。
4. **A3** → `A3Runtime.on_observation(obs)` 在 `should_advance_state(obs)` 为真时更新 rhythm/engagement/eligibility；模式由 `Provider.collect()` + `A3Engine.tick(signals)` 得到 EnvironmentMode。
5. **C 决策与执行** → `create_snapshot()` → `c.controller.decide(snapshot)` → `apply_c_veto(c_result)` → 写 trace（snapshot、env_mode、c_decision、execution_intent）。最终执行意图由 C 决策 + 执行 veto 决定（见上文「决策权责边界」）。

---

## 稳定化阶段建议

在「继续开发」之前，建议先完成：**用 `tools/determinism_guard.py` 跑一次完整回归**，确认当前代码（瘦身/重启后）两段 trace 的 decision 序列一致。确认稳定后再进入新功能阶段。

---

## 延伸阅读

- 整体模块与职责：[docs/ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md)
- 安装、配置与演示：[README.md](../README.md)
- C1 与 Phase B：`docs/V1_8_5_*`
- 冻结/基线、审计与门控：`docs/Frozen_*`、`docs/System_*`、`docs/BC_*`、`docs/Bring_Up_*`
- A3 测试：`docs/A3_Test_Runbook_v0.md`
