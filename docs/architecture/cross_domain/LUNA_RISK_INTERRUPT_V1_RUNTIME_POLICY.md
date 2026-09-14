# 风险打断闭环 V1：运行策略与启用边界

## 1. 当前能力状态

`risk_interrupt_v1` 当前已具备三层成立：

- 设计成立
- 模块级验证成立
- 主线边缘集成验证成立

且最关键的边界成立：

- **默认关闭时，对主链零侵入**

对应实现与验证产物：

- 旁路模块：`capabilities/cross_domain/risk_interrupt_v1.py`
- 模块验证：`tools/test_risk_interrupt_v1.py`
- 主线边缘集成验证：`tools/test_risk_interrupt_v1_integration.py`
- 说明：`docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_IMPLEMENTED_NOTE.md`

## 2. 启用级别（Level 0/1/2）

本能力的运行启用分为三级：

### Level 0：关闭（默认）

- `LUNA_ENABLE_RISK_INTERRUPT_V1=0`
- 行为：不抢占、不挂起、不输出风险播报；不挂载白盒字段（零侵入）

### Level 1：whitebox-only（长期保留态推荐）

- `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1`
- 行为：**只记录白盒**（含 original_output/risk_event_summary/interrupt_reason 等），不抢占、不挂起

### Level 2：真实抢占（谨慎启用）

- `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=0`
- 行为：允许 `high/critical` 风险触发最小抢占与 `paused_by_risk` 标记（仍不做自动恢复）

## 3. 默认策略（写死）

### 3.1 默认态（当前主线默认）

- **默认 Level 0**：关闭，不影响主链

### 3.2 长期保留态（推荐）

- 优先将能力作为可长期保留的旁路底座：
  - **默认仍为 Level 0**
  - 需要观测/排障时，允许切到 **Level 1（whitebox-only）**

### 3.3 Level 2 的定位

- Level 2 不是默认能力，不应常开
- 只有在满足启用边界与回退策略已准备好时，才允许短窗口开启

## 4. Level 2 启用边界（何时允许真实抢占）

### 4.1 风险事件源可信要求（V1 口径）

进入 Level 2 的前提：

- 风险事件来源必须是“高可信”的风险/行为链路输出（可以是规则/传感器/已验证模型，但需要有稳定口径）
- 风险事件必须包含最小字段（risk_type/risk_level/direction_hint/distance_band/confidence/timestamp）

不满足则：

- 只能 Level 1（whitebox-only），不得真实抢占

### 4.2 允许触发抢占的风险等级（写死）

- 仅允许：`high | critical`
- `medium`：默认只入白盒（必要时才播报，V1 不建议开播报）
- `low`：仅留痕

### 4.3 允许先试的场景（V1）

建议只在“行走中风险打断闭环”相关的场景先试：

- 出门后人行道通行
- 室外道路边缘通行
- 拥挤通道/商场走廊等动态障碍场景

### 4.4 当前禁止直接开抢占的场景（V1）

在缺少更完整恢复与去重机制前，以下场景不建议开启 Level 2：

- 长时间连续播报场景（容易形成抢占风暴/重复播报）
- 任务链对“挂起/恢复”有严格一致性要求但尚未接入状态机保护的场景
- OCR/细节驱动型场景（与安全抢占的优先级冲突更复杂）

## 5. 运行期监控指标（开启后看什么）

### 5.1 核心计数指标

- `interrupt_applied` 次数
- `task_paused` 次数（paused_by_risk）
- whitebox-only 记录数（Level 1）

### 5.2 质量指标（最小集合）

- **误抢占风险**：明显不该抢占的场景发生抢占（需人工抽样 + 白盒回放）
- **输出异常**：抢占后播报为空/重复/与风险不一致
- **白盒字段完整率**：每次风险事件是否都留下完整字段（缺失视为不可运营）

### 5.3 用户实际听到的输出（可追溯）

- 通过白盒字段 `final_spoken_output` 与 `interrupt_reason` 抽样复核

## 6. 回退策略（出现问题怎么立刻关掉）

### 6.1 必须退回 Level 1（whitebox-only）的条件

满足任一条件即退回 Level 1：

- 出现误抢占（抢占不该发生，影响主任务）
- 输出异常（空播报/重复播报/明显误导）
- 白盒字段不完整（无法回放/无法定位）

操作：

- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1`（保留观测，停止抢占）

### 6.2 必须退回 Level 0（关闭）的条件

满足任一条件即退回 Level 0：

- 发现主链污染（默认关闭时仍出现行为变化或字段注入）
- 影响主任务链稳定性（任务状态异常、持续挂起无法恢复等）
- 出现无法快速止血的播报故障

操作：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=0`

### 6.3 回退后必须保留的证据

- 白盒字段快照（risk_interrupt_v1）
- 当时的环境变量快照（两开关值）
- 触发样本的 original_output 与最终输出

## 7. 当前阶段不做项（写死）

- 不做自动恢复
- 不做复杂风险融合
- 不做多模型来源接入
- 不直接并入默认主链

## 一句话收束

`risk_interrupt_v1` 当前进入可长期保留态：**默认 Level 0（关闭）**，需要观测时用 **Level 1（whitebox-only）**；只有满足启用边界且回退策略准备就绪时，才允许短窗口进入 **Level 2（真实抢占）**。

