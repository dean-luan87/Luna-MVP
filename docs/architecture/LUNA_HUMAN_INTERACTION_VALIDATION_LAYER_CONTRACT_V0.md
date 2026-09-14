# LUNA — Human Interaction Validation Layer Contract v0

## Phase

- **Phase-HumanInteraction-Validation-001**

##定位

这是一个 **future branch contract（只定义，不接 runtime）**：把“用户反馈”从单一的“确认/否认事实”升级成 **人机互动验证层（Human Interaction Validation Layer）**。

它不是简单问“对不对”，而是把反馈拆成不同 **truth-type**，并支持未来 **情感引擎** 读取“精神世界层”的意义表达。

##核心判断（不可简化）

- 机器判断正确 ≠ 人类体验正确  
- 人类反馈真实 ≠ 事实层面真实  
- 事实不成立 ≠ 情感意义无效  

因此：**用户反馈不能直接覆盖世界事实**，只能改变证据状态、触发复核、或进入精神世界/情感画像分支。

##主线原则引用：语言即世界

本合同受主线原则约束：

- `docs/architecture/LUNA_LANGUAGE_AS_WORLD_MAINLINE_PRINCIPLE_V0.md`

其核心要求是：现实事实与语言世界必须分层存储与受控使用，避免“事实正确但关系失败”或“语言可信但污染事实”的两类系统性错误。

##三层连接模型

### 1) 现实世界层（World / Factual）

时间、地点、物体、文字、路径、商户、事件。

### 2) 人机互动层（Interaction）

用户确认、否认、纠正、补充、比喻、玩笑、幻想、误导。

### 3) 精神世界层（Mental / Emotional）

情绪投射、关系隐喻、个人意义、幻想叙事、真实的谎言（事实为假但情感为真）。

##Truth-type 分类（必须分类，禁止直接覆盖）

- `factual_confirmation`：事实确认（“对，这就是东门”）
- `factual_correction`：事实纠正（“不对，这是西门”）
- `subjective_interpretation`：主观解释（“这里让我觉得很压抑”）
- `metaphorical_mapping`：隐喻映射（“他像一条鱼”）
- `imaginative_projection`：幻想投射（“纸箱是我的城堡”）
- `emotional_truth`：情感真实（事实不成立但表达真实感受）
- `possible_falsehood`：可能谎言（与多源证据冲突）
- `playful_or_roleplay_statement`：玩笑/角色扮演（不进入事实层，可进入人格/情感上下文）

##存储与引用规则（强制）

### A) 事实层与精神层必须分开存储

- **事实层**：只允许读取/写入与现实世界可验证相关的数据结构
- **精神层**：承载 `emotional_truth/metaphorical_mapping/imaginative_projection/...` 等意义表达

### B) 交叉引用（双向可追溯）

- 事实层证据可以引用精神层反馈（用于解释/体验），但不得当作事实
- 精神层反馈必须引用其来源证据与上下文（时间/地点/交互场景）

##WorldContextEvidence 的读取规则（约束接口）

世界模型侧 **只能**消化（且仍需验证）：

- `factual_confirmation`
- `factual_correction`

并要求：

- 记录来源、时间、上下文、确认方法（如 `confirmation_method=user_confirmed`）
- 不得因为一次反馈就把 candidate 直接提升为“事实写入”

情感引擎未来可读取：

- `emotional_truth`
- `metaphorical_mapping`
- `imaginative_projection`
- `subjective_interpretation`
- `playful_or_roleplay_statement`

##示例（“真实的谎言”）

### “这个纸箱是城堡”

- 事实层：`object=cardboard_box`，`literal_castle=false`
- 精神层：`imaginative_projection=castle`，`emotional_context=play/ownership/fantasy`

### “他是一条鱼”

- 事实层：`literal_fish=false`
- 精神层：`metaphorical_mapping=fish`，含候选意义（slippery/attractive/distant/...），`requires_context=true`

##与“存疑证据用户确认插入任务”的关系

“插入确认任务”只是 **触发与编排**（低优先级、短窗口、不打断）；其产出的用户反馈必须进入本层进行 truth-type 分类与双层存储/引用，禁止直接覆盖事实。

