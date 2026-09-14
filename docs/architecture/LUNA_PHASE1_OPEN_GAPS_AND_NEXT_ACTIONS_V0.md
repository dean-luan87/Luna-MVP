# Luna Phase 1 — Open Gaps & Next Actions v0（一期未实现缺口与下一批动作清单）

**文件**：`docs/architecture/LUNA_PHASE1_OPEN_GAPS_AND_NEXT_ACTIONS_V0.md`  
**性质**：务实清单（盘点缺口与断点；不写大规划、不补理念、不展开实现细节）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`

---

## A. 已冻结但未实现的专题清单（按模块归类）

> 口径：**已有冻结/设计文档（或明确占位），但代码尚未落地**，或只落了 stub/只读观察。

### A1. 视角模块（Vision）主线实现缺口

- **Vision 输出协议 schema（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（J 节“下一步最小实现方向”）
- **解释/纠偏层最小接入（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（C3/E/F）
- **可消费切片层真实落代码（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（C4/H）
- **快链/慢链真实调度（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（F）
- **碎片建模三层路线的协议与更新机制（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（G）

### A2. 中台调度缺口（Platform Orchestration）

- **中台消费接口（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（H/J；中台是唯一消费调度器）
- **多源消费边界落代码（未实现）**  
  - 目标：确保视角不直接驱动语音/记忆/导航执行（目前多为文档冻结，需后续接口面落地）

### A3. 慢链与沉淀缺口（联网补证/记忆/碎片沉淀）

- **联网补证触发规则与超时/过期处理（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（F/H；慢链范围）
- **碎片沉淀候选协议（未实现）**  
  - 来源：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（C5/G/H3）
- **记忆消费边界与升格规则（未实现）**  
  - 说明：视角侧写死“不直接写记忆”，但记忆侧的消费契约仍需专题化落地

### A4. 导航执行缺口（当前明确暂不进入）

> 说明：本期已把“目标确认与承接链”推进到正式事实层，并完成 handoff consume-bound 的最小承接；**真实导航执行仍未进入**（符合当前克制策略）。

- **handoff 真实消费 bound 后的执行入口（未实现）**  
  - 相关：`docs/architecture/voice/LUNA_NAVIGATION_HANDOFF_CONSUME_BOUND_V0.md`（H 节边界写死）
- **真实导航启动与地图接入（未实现/明确暂缓）**

### A5. 治理与运行缺口（占位已补，但未实现）

- **模块打标标准（占位，未实现）**  
  - 视角：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（K）  
  - 语音：`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（I）
- **信息处理超时方案（占位，未实现）**  
  - 视角：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（L）  
  - 语音：`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（J）
- **模块报错处理方案（占位，未实现）**  
  - 视角：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`（M）  
  - 语音：`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（K）
- **视角运行时治理分支（占位，未实现）**  
  - 目标：为“目标生命周期/挂起监控/恢复窗口”等运行时治理能力预留专题入口（不影响 P1/P2 主线接线）。  
  - 相关：`docs/architecture/vision/LUNA_VISUAL_TARGET_LIFECYCLE_MANAGER_V0.md`
- **Risk Gate（未实现，明确暂缓）**  
  - 相关设计：`docs/architecture/voice/LUNA_CONFLICT_TOPIC_03_RISK_GATE_V0.md`

---

## B. 当前主线断点清单（“哪里还没闭环”）

> 口径：只写“事实状态/断点”，不写解决方案细节。

### B1. 导航目标确认与承接链（已阶段性打通到事实层）

- **已具备**：目标从候选到正式事实层的链路与观测面（只读评估链 + `destination_bound_v0` 写入 + handoff consume-bound 观测）。  
- **断点**：consume-bound 之后仍未进入真实执行（按当前策略应保持暂缓）。

### B2. 视角输入与消费链（已冻结架构，但实现断点尚多）

- **已具备**：架构分层、消费边界、快慢链分工、碎片建模路线、对接关系（文档冻结）。  
- **断点**：缺少可消费切片的统一 schema 与中台消费接口，导致“视角链”难以系统性进入主链消费（目前主链仅有 V3 的 summary-only input pack 与 V2 的 shadow read，尚不构成视角模块主线）。

### B3. 中台调度（架构写死，但接口面缺失）

- **断点**：中台作为唯一消费调度器的接口面未落地，视角/语音/记忆/联网补证的统一调度口径无法进入可回归实现。

### B4. 治理与运行（占位已补齐，但未进入实现）

- **断点**：打标/超时/报错三类系统坑位已被明确为必需，但仍处于“占位未实现”状态，后续需要专题化推进。

---

## C. 下一批最小工程动作清单（只列可执行动作，不做大规划）

> 口径：每条动作必须满足“最小、可冻结、可回归”，并能在不破坏已冻结主线的前提下推进。

### C1. 视角侧（优先级最高的一组）

- **(1) Vision 可消费切片输出协议 schema v0（只定义 schema + 最小样例，不接模型）**  
  - 目标：让“可消费切片”首次具备稳定接口面，为中台消费做准备。
- **(2) 中台消费接口占位（只读接线 + metadata 观测，不做裁决）**  
  - 目标：把“中台唯一调度器”的架构纪律落到一个最小可观测入口。
- **(3) 视角主线断点梳理与最小接线（只读）**  
  - 目标：把“哪些输出可以进入快链/慢链”的入口钉死，避免直接消费连续流。

### C2. 中台调度（紧随其后）

- **(1) Need-* Routing v0（只读观测层）**  
  - 目标：形成“导航/非导航/风险/追问”等分流建议的观测面，不改变主链裁决。

### C3. 慢链与沉淀（保持克制）

- **(1) 碎片沉淀候选协议 v0（只定义承载位与边界）**  
  - 目标：让“沉淀”先有可承载、可回滚的最小结构，不直接写记忆事实。

### C4. 治理与运行（先做专题清单，不直接上实现）

- **(1) 打标标准/超时/报错：分别开 3 个专题文档（只做口径冻结）**  
  - 目标：把占位变成可推进的专题入口，但不在本轮展开实现策略。

