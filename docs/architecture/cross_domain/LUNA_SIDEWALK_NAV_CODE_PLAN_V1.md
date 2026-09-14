# 人行道导航闭环：最小代码实现计划（V1）

## 1. 第一版代码目标

### 第一版要落成什么（写死）

在《`LUNA_SIDEWALK_NAV_MIN_IMPLEMENTATION_V1.md`》基础上，第一版代码只实现：

1. 接收最小环境输入（可来自占位/规则/后续再接视觉管线）
2. 产出最小 `scene_type=outdoor_walkway` 级别判断与 `sidewalk_confidence`
3. 接入风险快扫结果，并保证 **风险链优先于普通导航提示**
4. 在无高风险、且未被 `risk_interrupt_v1` 抢占时，产出 **一条** 最小通行建议
5. 完整白盒留痕（可回放、可对账）

### 第一版不做什么（写死）

- 不做复杂转向规划、多路口多阶段决策
- 不做交通灯完整逻辑
- 不做地图重规划与地图构建
- 不做 OCR 细节链主导（V1 默认不触发）
- 不做多模型协同

### 为什么这样切

- 与第一优先 `risk_interrupt_v1` 对齐：**先安全、再主任务提示**
- 用最小状态与白盒把“日常主路”跑通，再扩场景

---

## 2. 建议代码落点（不绑死文件名，但给明确归属）

### 2.1 环境初判入口

- **建议**：新增旁路模块目录 `capabilities/cross_domain/sidewalk_nav_v1/`（与 `risk_interrupt_v1` 并列）
- **入口函数**：`evaluate_sidewalk_nav_v1(...)`  
  - 输入：最小环境特征摘要（见下）+ 可选任务上下文  
  - 输出：`scene_type`、`sidewalk_confidence`、`navigation_hint` 候选 + 白盒 dict

### 2.2 风险快扫结果如何接入

- **建议**：复用与 `risk_interrupt_v1` 同一套 **风险等级语义**（`low|medium|high|critical`），或映射到统一 `risk_summary`：
  - 若已有独立风险模块：只读其输出，不在本模块内做轨迹预测
  - 若无：可先 **mock / 规则占位**（仅开发/验证用），由开关控制

### 2.3 最小通行建议生成落点

- **建议**：放在 `sidewalk_nav_v1` 内部，作为纯函数式组合：
  - 输入 = 环境初判 + 风险摘要 +（可选）任务下一步意图
  - 输出 = `navigation_hint` 字符串或结构化枚举 + `final_spoken_output` 摘要

### 2.4 白盒记录落点

- **建议**：与现有模式一致，写入上层 `metadata["sidewalk_nav_v1"]`（或等价键），避免污染顶层字段过多
- 与 `risk_interrupt_v1` 并列：`metadata` 中可同时存在 `risk_interrupt_v1` 与 `sidewalk_nav_v1`（由裁决逻辑决定最终播报）

### 2.5 与 `risk_interrupt_v1` 的交界点（写死）

- **顺序**：先合并风险快扫 → 再判断是否被 `risk_interrupt_v1` 抢占/压制
- **规则**：
  - 若 `risk_interrupt_v1` 已产生 `interrupt_applied=true` 或运行策略为 Level 2 且本轮需抢占：**人行道导航的 `final_spoken_output` 必须为空或被标记为 suppressed**
  - 若仅 whitebox-only：人行道导航可照常产建议，但最终播报仍受统一裁决口约束（见运行策略）

---

## 3. 最小状态字段（第一版需要）

| 字段 | 含义 |
|------|------|
| `current_scene_type` | 当前场景类型，V1 至少 `outdoor_walkway` / `unknown` |
| `sidewalk_confidence` | 人行道/可通行判断置信度 0~1 |
| `current_navigation_hint` | 当前最小通行建议（枚举或短句摘要） |
| `risk_override_active` | 是否因风险链而压下普通导航提示 |
| `last_risk_level` | 最近一次风险等级（用于冷却/去重，可选） |

---

## 4. 最小白盒字段（第一版必须）

| 字段 | 含义 |
|------|------|
| `scene_summary` | 环境初判摘要（含 scene_type、关键约束） |
| `sidewalk_detected` | 是否判定为人行道/可通行步行环境 |
| `risk_summary` | 风险快扫摘要（level/type/hint） |
| `navigation_hint` | 最小通行建议（无风险且未被压制时有效） |
| `output_suppressed_by_risk` | 普通导航是否被风险链压制 |
| `final_spoken_output` | 经裁决后拟播报内容摘要（可能为空） |
| `event_timestamp` | 事件时间戳（ms） |

---

## 5. 最小执行顺序（文字版）

1. 输入进入（环境特征 + 风险快扫 + 可选任务/GPS/偏好）
2. 环境初判 → `current_scene_type`、`sidewalk_confidence`
3. 风险快扫结果接入 → `last_risk_level`、`risk_summary`
4. 若存在高风险或 `risk_interrupt_v1` 要求抢占 → **压下** 人行道导航播报候选，`risk_override_active=true`
5. 若无高风险且未被压制 → 生成 `current_navigation_hint` / `navigation_hint`
6. 写白盒 `metadata["sidewalk_nav_v1"]`
7. 输出给上层语义 / 任务链 / 播报（由统一输出裁决口最终选一条）

---

## 6. 验证入口（第一版代码完成后怎么测）

### 6.1 用例矩阵（最小）

| 场景 | 预期 |
|------|------|
| 无风险 + outdoor_walkway | 产生最小导航提示；`output_suppressed_by_risk=false` |
| 高风险或 risk_interrupt 抢占 | `output_suppressed_by_risk=true`；`final_spoken_output` 不以导航为主 |
| 默认关闭旁路 | 不挂载 `sidewalk_nav_v1`；主链零侵入 |

### 6.2 建议脚本

- 新增：`tools/test_sidewalk_nav_v1.py`（与 `test_risk_interrupt_v1_integration.py` 同风格）
- 断言：白盒字段齐全、`risk_override_active` 与 `output_suppressed_by_risk` 一致

---

## 7. 回退边界

### 7.1 降级为「只白盒」

建议新增开关（实现阶段再落代码，此处只定义语义）：

- `LUNA_ENABLE_SIDEWALK_NAV_V1=1`
- `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1`（默认 true）

行为：只写 `metadata["sidewalk_nav_v1"]`，**不**向播报层输出导航句。

### 7.2 完全关闭

- `LUNA_ENABLE_SIDEWALK_NAV_V1=0`  
行为：模块不执行、不挂载 metadata，**不影响主链**。

### 7.3 与风险链冲突时

- 优先遵循《`LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`》：先退回风险链 whitebox-only 或关闭，再处理人行道导航异常。

---

## 8. 当前阶段不做项（再次写死）

- 不做复杂路径规划
- 不做 OCR 细节链主导
- 不做地图构建
- 不做复杂交叉路口逻辑
- 不做多模型协同

---

## 一句话收束

先把人行道导航闭环的 **代码落点、状态与白盒字段、执行顺序、验证与回退** 写清楚，再进入 `sidewalk_nav_v1` 的最小代码实现；并与 `risk_interrupt_v1` 保持 **风险优先、导航可压下** 的固定交界。
