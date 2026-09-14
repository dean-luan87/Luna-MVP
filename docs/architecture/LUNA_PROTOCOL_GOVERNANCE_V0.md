# Luna — Protocol Governance v0（协议治理占位与管理规则冻结）

**文件**：`docs/architecture/LUNA_PROTOCOL_GOVERNANCE_V0.md`  
**性质**：协议治理上位占位文档（冻结治理方向 + 最小管理要求；不做大迁移）  

---

## A. 文档定位（写死）

- 这是 **Luna 协议治理的上位占位文档**。
- 当前目标**不是**迁移所有协议，也不是重构现有协议文档体系。
- 当前只冻结两件事：
  - 未来协议治理方向（跨模块协议逐步上收至中台治理）
  - 最小管理规则（版本号/更新说明/使用范围登记等元信息要求）
- 后续：成熟的跨模块协议将逐步**上收或映射**为中台统一协议（中台为 Source of Truth）。

---

## B. 核心原则（必须写死）

1. **跨模块协议主权归中台**  
   - 任何被多个模块消费的协议，未来都应**上收或映射**为中台统一协议。
2. **模块内协议仍可暂时保留**  
   - 但一旦协议开始跨模块流转，后续必须纳入中台治理范围。
3. **先探索，后收束**  
   - 当前允许模块协议继续辅助边界探索；但成熟后必须统一治理并收口。
4. **协议必须可版本化、可追踪、可回溯**  
   - 后续所有正式协议必须具备：版本号、更新说明（Change Summary / Change Log）、使用范围登记（Where Used）。

---

## C. 协议分层原则（至少两类）

### C1. 模块内协议（Module-local Protocols）

- **定义**：仅在单一模块内部使用，不作为跨模块消费接口。
- **维护者**：模块 Owner 可暂时自行维护。
- **约束**：若后续开始跨模块流转，则必须升级为跨模块协议治理范围（见 C2）。

### C2. 跨模块协议（Cross-module Protocols）

- **定义**：被多个模块消费、或作为中台输入/输出接口的协议。
- **写死**：未来必须以**中台**为 Source of Truth（统一命名、统一版本、统一变更说明、统一 Where Used 登记）。

---

## D. 当前已出现的协议类型（示意，不做完整注册表）

> 这里只做示意，避免未来“协议太多无法监管”；不构建完整注册表。

- Vision Consumable Slice Output Schema（P1）
- Visual Interpretation & Correction Output（P2）
- 语音主线协议（Voice mainline）
- 中台消费候选协议（未来）
- 记忆候选协议（未来）
- 导航分流协议（未来）

---

## E. 未来要补的统一治理能力（占位）

未来治理能力至少应包含（当前只占位，不实现系统）：
- **协议注册表（Protocol Registry）**：协议名称、版本、状态、Owner、索引入口。
- **协议版本号（Version）**：明确主版本/次版本或等价约定（本期不规定具体语义）。
- **协议更新说明（Change Log / Change Summary）**：每次变更可追踪、可回溯。
- **协议使用位置登记（Where Used）**：至少登记“哪些模块/哪些入口”在使用该协议。
- **协议冻结状态（Status）**：例如 `Draft / Active / Frozen / Deprecated`（本期只占位，不规定流程）。

相关系统级规范（占位，供后续收口）：
- `docs/architecture/LUNA_INTER_MODULE_INFORMATION_FLOW_SPEC_V0.md`
- `docs/architecture/LUNA_INFORMATION_TIMING_CADENCE_AND_LENGTH_SPEC_V0.md`

---

## F. 统一管理要求（写成规范要求，不做全量补齐）

写死：从现在开始，**新产生的正式协议文档**应优先按以下最小元信息头字段补齐；旧文档不要求本期全量补齐，但后续可逐步补齐。

### F1. 最小元信息字段（统一要求）

- **Protocol Name**
- **Version**
- **Status**
- **Owner**
- **Last Updated**
- **Change Summary**
- **Where Used**

### F2. 建议写法（模板占位）

```
Protocol Name:
Version:
Status:
Owner:
Last Updated:
Change Summary:
Where Used:
```

---

## G. 当前不做（必须写死）

- 不做现有协议大迁移
- 不做所有协议集中重写
- 不做完整协议注册中心实现
- 不做代码层强制校验
- 不做自动依赖分析

