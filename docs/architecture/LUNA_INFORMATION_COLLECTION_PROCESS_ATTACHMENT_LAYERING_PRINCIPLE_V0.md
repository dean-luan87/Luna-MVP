# LUNA — Information Collection / Processing / Attachment Layering Principle v0

## 定位

- **类型**：主线分层原则（mainline layering principle）
- **目的**：明确“信息采集、信息处理、空间挂载”三件事必须分层，避免把地图/GPS/点云误当作现场事实来源，或把锚点层混入核心感知主链。

## 核心结论（一句话）

**YOLO/OCR/语音是核心能力；地图/GPS/点云是增强锚点。信息采集、信息处理、信息挂载必须分开，不能混成一个模块。**

## 三板块分层

### 1) 收集信息（Collection）

负责采集真实世界与用户交互证据（“看见/读到/听到/被用户纠正”）：

- YOLO：对象/载体/区域/风险候选
- OCR：文字/标识/公告/商业信息
- Visual Symbol：标志/印章/Logo 等（需意义确认）
- Voice（用户输入）与 TTS（输出表达）：形成可交互闭环
- 用户反馈：进入 Human Interaction Validation Layer（truth-type 分类，禁止直接覆盖事实）

**属性**：直接感知/直接交互；没有它们系统无法形成基本闭环。

### 2) 处理信息（Processing / Governance）

负责去重、分流、判断变化、判断可信度、判断是否可写（治理承重墙）：

- MidPlatform filtering / candidates
- Scene Delta：变化/替换/移除/过期/重复压缩（不写世界模型）
- WorldContextEvidence：统一包装候选证据（candidate-only）
- Write Readiness：准入评估（WriteReadinessCheck）
- Provisional-first：通过评估 ≠ 事实（先占位/存疑/弱读取）
- Commit/Revision/Quarantine：版本化/回滚/隔离/审计（合同层）

**属性**：治理层；不等于事实来源；不替代感知。

### 3) 挂载信息（Attachment / Space Anchor Layer）

负责把候选信息绑定到位置、范围、路径、空间结构和时间窗口（时空挂载与强化）：

- Map / GPS：外部空间锚点（可能在这里）
- POI：已知地点与服务信息（不能当作现场事实）
- PointCloud / Depth：近场空间结构、距离、障碍、通行形态（增强空间理解）
- Indoor map：室内区域/楼层（不得推断未知楼层）

**属性**：空间挂载/强化层；**不是现场事实来源**。

## 关键原则（防架构错误）

1. **核心感知负责发现事实候选**（YOLO/OCR/用户反馈）
2. **中台治理负责判断候选价值与写入资格**（去重/变化/可信/污染防护/回滚审计）
3. **空间挂载负责让候选具备时空位置**（Map/GPS/点云提供 anchor/scope/freshness/conflict）
4. **世界模型负责保存可复核结构**（必须满足时空绑定宪法）

## 与“地图不等于现场事实”的关系

地图/GPS/POI 只能回答“可能在哪里”，不能回答“现场现在一定这样”。  
现场状态仍必须由 YOLO/OCR/用户反馈/SceneDelta 去验证与更新。

