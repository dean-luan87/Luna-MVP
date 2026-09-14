# Luna Voice 宪法 v1（正式约束）

> 文风要求：约束式、冷静、明确、不留模糊空间。  
> 本宪法适用于 Luna Voice capability 的所有实现与未来 provider 接入；违反即视为越界污染。

## 第一章：主权原则

1. Voice 不是主权系统。  
2. Core 是裁决骨架；任务与执行的最终裁决只属于 Core/TaskChain。  
3. Voice 不得拥有或模拟以下权力：  
   - 任务裁决权  
   - 记忆写入权  
   - 白盒控制权  
   - 规则治理权  

## 第二章：输入原则

1. 所有语音输入必须先落 **标准对象**：`VoiceInputEvent`。  
2. 禁止“裸文本”绕过标准对象直接进入主链。  
3. 当前上下文必须由 Core 注入为 `VoiceRuntimeContext`；Voice 不得自造主权上下文。  
4. 输入解析只能产出 **轻意图候选**：`VoiceIntentCandidate`。  
5. VoiceIntentCandidate 不得承担宽推理、人格推理或复杂知识问答的主链裁决职责。  

## 第三章：执行权限原则

1. 执行结果仅允许三类：  
   - 直接执行  
   - 确认后执行  
   - 拒绝执行 / 降级处理  
2. 高风险或不确定动作禁止直接执行。  
3. 行为不是命令，行为是证据：  
   - 输入指令与环境/任务冲突时，必须触发确认/澄清。  
4. Voice/Bridge 只能提交 proposal/query/response，禁止在 capability 内部“自执行”。  

## 第四章：输出治理原则

1. 任何模块不得直连 TTS。  
2. 主动沟通不得直控 TTS；只能提交 `SpeechRequest` 进入 Output Plane。  
3. 输出必须统一治理：去重、冷却、占用、优先级、模式限制均由治理层裁决。  
4. 高风险输出必须模板化/白名单化（Stage-1 固化原则，不在本轮实现）。  

## 第五章：白盒与留痕原则

1. Voice 全链路必须可观察、可回溯。  
2. 至少必须可留痕以下阶段对象：  
   - 输入：VoiceInputObservation  
   - Bridge：DialogueBridgeObservation  
   - 模型转述：ModelMediationObservation  
   - 输出裁决：OutputDecisionObservation  
   - 播放：PlaybackObservation  
3. 白盒观察对象的存在优先于任何接线实现。  

## 第六章：外部大模型接入原则

1. 外部模型是能力提供方，不是主权方。  
2. 外部模型不得接触 Luna 核心：  
   - Core 状态机  
   - TaskChain 细节  
   - Whitebox 链路与阈值  
   - 内部系统信息与治理细节  
   - 记忆核心结构  
3. 外部模型不得污染 Luna 核心：模型输出只能是候选，必须被治理与规则处理。  
4. 系统信息默认不可暴露；除非明确白名单化与脱敏。  

## 第七章：运行态原则

1. Restricted device mode 优先级最高，必须优先裁决与限制输入/输出。  
2. 长待机/关机导致会话与任务上下文失效，默认进入新任务（由 Core 判定）。  
3. 工作态禁止升级：在运行态不得引入未审计的新接线、新 provider、新模型。  
4. 设备运维治理域不纳入本轮语音主线；不得以运维治理为理由突破宪法边界。  

