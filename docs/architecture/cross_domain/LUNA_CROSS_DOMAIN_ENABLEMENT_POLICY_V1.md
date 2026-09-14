# 跨域旁路能力：启用顺序与边界（V1）

## 1. 文档目的

在已落地 3 条跨域旁路能力（并完成模块验证与主线边缘集成验证）的前提下，把它们统一纳入主线启用策略，回答：

- 先开哪条、后开哪条
- 默认开什么级别
- 哪些只能 whitebox-only、哪些场景允许真实外显
- 哪些能力永远受风险链压制
- 若未来挂进主链（输出裁决层），调用与合并顺序怎么排
- 出问题时回退顺序是什么

本文件只做策略收口：**不扩功能、不改实现、不新增模型**。

---

## 2. 三条旁路的当前成熟度（V1）

| 能力 | 设计 | 代码落地 | 模块验证 | 主线边缘集成验证 | 默认关闭 | whitebox-only | 备注 |
|------|------|----------|----------|------------------|----------|--------------|------|
| `risk_interrupt_v1` | 是 | 是 | 是 | 是 | 是 | 是 | 唯一拥有明确 Level 0/1/2 运行分层 |
| `sidewalk_nav_v1` | 是 | 是 | 是 | 是 | 是 | 是 | 产出最小通行建议；高风险/抢占时压制 |
| `retail_find_item_v1` | 是 | 是 | 是 | 是 | 是 | 是 | OCR 为补证接口位；高风险/抢占时压制 |

---

## 3. 默认启用状态（写死）

### 3.1 主线默认基线（所有环境）

当前主线默认应保持：

- `risk_interrupt_v1`：**Level 0（关闭）**
- `sidewalk_nav_v1`：**关闭**
- `retail_find_item_v1`：**关闭**

理由：三条能力均为旁路，默认关闭才能保证“零侵入基线”长期稳定。

### 3.2 观测/灰度的默认姿势（推荐）

当需要验证稳定性或排障时，优先采用“只白盒”而不是外显：

- `risk_interrupt_v1`：**Level 1（whitebox-only）**
- `sidewalk_nav_v1`：`LUNA_ENABLE_SIDEWALK_NAV_V1=1` + `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1`
- `retail_find_item_v1`：`LUNA_ENABLE_RETAIL_FIND_ITEM_V1=1` + `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1`

---

## 4. whitebox-only 与真实外显的边界

### 4.1 全局硬边界：安全链优先（写死）

以下条件任一成立时，**所有非安全型旁路输出都必须被压制**：

- 风险摘要 `risk_level in {high, critical}`
- 或 `risk_interrupt_v1` 本轮判定抢占（上层据此传入 `risk_interrupt_preempt=true` / `risk_interrupt_preempt=True`）

压制含义：

- `sidewalk_nav_v1`：`output_suppressed_by_risk=true` 且 `final_spoken_output=""`
- `retail_find_item_v1`：`output_suppressed_by_risk=true` 且 `final_spoken_output=""`

`risk_interrupt_v1` 本身作为安全链允许外显（在其 Level 2 且满足启用边界时）。

### 4.2 `risk_interrupt_v1` 外显边界（摘自运行策略）

- **默认**：Level 0
- **推荐长期保留**：Level 1（whitebox-only）
- **允许短窗外显/抢占**：Level 2，且满足《`LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`》的事件源可信与回退准备要求

### 4.3 `sidewalk_nav_v1` 外显边界（V1）

仅当同时满足才允许外显一条最小通行建议：

- `LUNA_ENABLE_SIDEWALK_NAV_V1=1`
- `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=0`
- 命中 `scene_type=outdoor_walkway`
- 未被安全链压制（高风险或抢占）

### 4.4 `retail_find_item_v1` 外显边界（V1）

仅当同时满足才允许外显一条最小找货结论：

- `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=1`
- `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=0`
- `gating_passed=true` 且 `active_find_item_intent=true`
- 未被安全链压制（高风险或抢占）
- OCR 仍为补证：外显结论不要求真实 OCR 执行，但不得进入“常驻 OCR 扫描”模式

---

## 5. 主线接入优先级（建议顺序）

当未来把旁路“挂进主链输出裁决层”的编排顺序固定为：

1. **`risk_interrupt_v1`**（安全链，最高优先级）
2. **`sidewalk_nav_v1`**（日常主路最小通行建议；受风险压制）
3. **`retail_find_item_v1`**（场景化补充；受风险压制）

说明：

- 顺序不代表“都要外显”，默认仍建议只白盒；顺序代表“同一轮被调用/汇总时的优先级与压制关系”。  
- 两条非安全链的外显候选，均必须先过“风险压制”门槛。

---

## 6. 回退顺序（出现异常如何止血）

### 6.1 全局回退原则（写死）

遇到异常时，优先回退到 **whitebox-only**，再必要时完全关闭；且优先保证安全链稳定。

### 6.2 推荐回退序列

1. 将新增/外显中的非安全链先退回 whitebox-only：
   - `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1`
   - `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1`
2. 若仍有主链污染或输出异常，直接关闭对应旁路：
   - `LUNA_ENABLE_SIDEWALK_NAV_V1=0`
   - `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=0`
3. 若异常来自安全链外显（Level 2），按风险策略先退到 Level 1，再必要时 Level 0：
   - `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1` → `LUNA_ENABLE_RISK_INTERRUPT_V1=0`

---

## 7. 哪条能力先允许进入更深联调（建议）

按“收益/风险比 + 安全优先”排序：

1. `risk_interrupt_v1`：先允许更深联调（但默认仍 Level 0；灰度以 Level 1 起步；Level 2 必须短窗且可回退）
2. `sidewalk_nav_v1`：第二优先（可先在 whitebox-only 长观察，再小窗口外显）
3. `retail_find_item_v1`：第三优先（先保留为场景化补充；whitebox-only 观察 OCR 触发边界与控噪）

---

## 一句话收束

三条旁路能力已同层级成立；本策略把它们的**启用顺序、默认级别、外显边界、风险压制与回退顺序**统一写死，确保后续即使继续长新旁路，也始终能以“零侵入基线 + 可控灰度 + 可止血回退”的口径接入主线。

