# 主线 2 第二阶段：Skeleton Mix M0 交付说明

**依据**：`docs/SPATIAL_SKELETON_SYSTEM_CONSTITUTION.md` v1.0（冻结）  
**目标**：将骨架组合制第一次落到运行时，使当前帧/当前情境下具有“可见、可记录、可测试”的骨架配比事实。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/skeleton_mix.py` | **新建**。SkeletonMix  dataclass（4 weights + 4 floors + dominant_skeleton + mix_reason）；SAFETY_FLOOR_MIN=0.15；build_skeleton_mix(goal, state, local_goal_spatial_map) 规则型推导。 |
| `decision_monitor/schema.py` | 引入 SkeletonMix；DecisionMonitorFrame 新增 skeleton_mix: Optional[SkeletonMix]。 |
| `decision_monitor/builder.py` | 引入 skeleton_mix；build 中调用 build_skeleton_mix(goal, state, local_goal_spatial_map)，写入 frame.skeleton_mix。 |
| `runtime/context.py` | 新增 skeleton_mix_dominant、skeleton_mix_navigation_weight、skeleton_mix_fine_interaction_weight、skeleton_mix_observation_weight、skeleton_mix_safety_weight、skeleton_mix_reason。 |
| `main.py` | 决策显示器块内，frame 构建后将 frame.skeleton_mix 写入 runtime_ctx（供下一 tick 消费）。 |
| `tools/decision_monitor_viewer.py` | 新增「骨架配比 / Skeleton Mix (M0)」卡片：主导骨架、mix_reason、4 weights、4 floors；sections 增加 skeleton_mix。 |
| `decision_monitor/CONTRACT.md` | 补充 skeleton_mix（Skeleton Mix M0）字段与驱动输入、预留说明。 |

---

## 2. Skeleton Mix 数据结构说明

| 字段 | 类型 | 含义 |
|------|------|------|
| navigation_weight | float | 导航骨架权重 |
| fine_interaction_weight | float | 精细交互骨架权重 |
| observation_weight | float | 观察骨架权重 |
| safety_weight | float | 安全骨架权重 |
| navigation_floor | float | 导航骨架保底 |
| fine_interaction_floor | float | 精细交互骨架保底 |
| observation_floor | float | 观察骨架保底 |
| safety_floor | float | 安全骨架保底（≥ SAFETY_FLOOR_MIN=0.15） |
| dominant_skeleton | str | 当前主导骨架：navigation / fine_interaction / observation / safety |
| mix_reason | str | 本帧配比原因（规则型短句） |

---

## 3. 最小规则型 mix 生成规则说明

- **输入**：goal_type、scene_type、scene_profile（来自 local_goal_spatial_map）、minimum_mode_active、goal_progress_paused、high_level_output_suppressed、runtime_domain_state。
- **规则概要**：
  - **高风险/冻结**：minimum_mode 或 runtime_domain=frozen 或 high_level_output_suppressed → safety 提升（0.5），nav 降。
  - **goal_paused**：safety 提升（0.35）。
  - **近场/桌面交互**：scene_type 含 close_range 或 goal_type 为 hold_for_floor/recheck_environment → fine_interaction 高（≥0.55），navigation 低。
  - **观察/停留**：scene_type 含 stationary 或对应 observation → observation 高（≥0.5）。
  - **室外导航**：scene_profile=outdoor、goal_type=observe_navigate、非 minimum_mode、非 close_range/stationary → navigation 高（0.55），fine 低（0.1）。
  - **路径确认/slow_down**：goal_type=confirm_path 或 slow_down_observe → nav/obs/safety 均衡。
- 权重归一化到和约 1；dominant_skeleton = argmax(四权重)。

---

## 4. Viewer 展示说明

- **卡片标题**：骨架配比 / Skeleton Mix (M0)。
- **第一行**：主导：&lt;dominant_skeleton&gt; · &lt;mix_reason&gt;。
- **第二行**：weight: nav=… fine=… obs=… safe=…。
- **第三行**：floor: nav_fl=… fine_fl=… obs_fl=… safe_fl=…。
- 专家折叠面板中 skeleton_mix 段可展开查看全部字段。

---

## 5. 样本运行结果（测试）

- 见验收：frame.skeleton_mix 存在，4 weights + 4 floors 可读，safety_floor ≥ 0.15，dominant_skeleton ∈ {navigation, fine_interaction, observation, safety}；不同 goal/state（如 detector_floor_due、minimum_mode、risk 高）下 mix 与 dominant 会变化。

---

## 6. 当前哪些 mix 字段已真实化，哪些仍规则型占位

| 项目 | 状态 |
|------|------|
| 4 weights、4 floors、dominant_skeleton、mix_reason | **真实化**：每帧由 build_skeleton_mix 产出并写入 frame、runtime_ctx、Viewer。 |
| 配比数值与 reason 文案 | **规则型占位**：由 goal_type、scene_type、scene_profile、守底状态等规则推导，非学习、非自适应。 |
| 自适应 mix、学习型 mix、按记忆反馈调 mix | **预留**，未实现。 |
| 骨架过滤联动、骨架记忆联动 | **未实现**，本轮不做。 |

---

## 7. 本轮是否通过

- **是**。验收满足：运行时存在可读的 Skeleton Mix（4 weights + 4 floors）；Decision Monitor / Viewer 能显示当前 Skeleton Mix；在不同场景/目标下 mix 与 dominant 会变化（室外导航、近场交互、观察/停留、高风险/冻结）；dominant skeleton 可明确识别；safety_floor ≥ 0.15；不破坏主线 A、主线 2 第一阶段、M0、M1、M1.5、M2 既有链路。
