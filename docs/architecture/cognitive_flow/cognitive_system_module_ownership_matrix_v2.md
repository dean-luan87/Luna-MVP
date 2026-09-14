# Cognitive System Module Ownership Matrix v2

| 模块 | 所属层 | 主要职责 | 禁止权限 |
|---|---|---|---|
| Attention Controller | Cognitive Brain | 将目标、上下文、风险、未知、Self State 等候选聚合为认知资源分配候选 | Truth、Decision、Action、Hardware/Model direct call、State mutation |
| Context | Cognitive Brain | 表达当前认知处境、任务/资源/能力/未知约束 | Identity、Decision、Action、Reality modification |
| Goal | Cognitive Brain | 组织当前理解方向与成功条件候选 | Action、Truth、Capability execution、State mutation |
| Workspace | Cognitive Brain | 临时组合激活表示、Schema、约束、未知与假设 | Memory replacement、Decision、Action、Reality mutation |
| Simulation Space | Cognitive Brain | 展开假设、反事实、未来状态候选 | Evidence/Truth generation、hardware access、Action |
| Evaluation | Cognitive Brain | 评价置信、一致性、适用性、风险、信息/推理价值 | Final decision、Action、Truth confirmation、State mutation |
| Feedback | Cognitive Brain / Evolution boundary | 形成错误归因、改进、适应候选 | Automatic learning mutation、Genome/Memory/State rewrite |
| Self State | Cognitive Brain | 聚合自身能力、资源、可靠性、注意、知识可用性、负载的当前认知表示候选 | Middleware ownership、Identity/Personality/Emotion authority、State mutation |
| Experience / Adaptation | Brain Evolution boundary | 将经验反馈形成适应/模式调整候选 | Direct Attention rewrite、Reality override、automatic adoption |
| Neural Protocol Manager | Cognitive Neural Architecture | 信号分类、版本、兼容性、边界、trace、演化提案治理 | Goal/Attention/Truth/Decision/Action/State mutation |
| Neural Paths / Signals | Cognitive Neural Architecture | 跨层传递与调节 Cognitive/Perception/Reflex/Simulation signals | Semantic fact judgment、provider execution、context update |
| Capability Manager | Cognitive Middleware | 将已表达的信息需求解析为可行 capability/bundle candidate | Task/Goal origin、Attention allocation、Decision、direct execution |
| Resource Manager | Cognitive Middleware | 观察并提出 compute/battery/network/storage/provider constraints | Goal override、Attention authority、State mutation |
| Evidence Gateway | Cognitive Middleware | 统一封装 source/time/scope/confidence/uncertainty/trace 的 Evidence Candidate | Truth confirmation、Context/Goal update、Decision/Action |
| Model Adapter | Cognitive Middleware | 归一化 provider-specific input/output 与可靠性元数据 | Cognitive interpretation、provider self-selection、truth assertion |
| Hardware Manager | Cognitive Middleware | 设备抽象、可用性、生命周期与能力边界协调 | Goal/route planning、world action、Self Model ownership |
| Diagnostics | Cognitive Middleware | 健康、延迟、故障、trace 观测 | Cognitive evaluation、priority override、State mutation |
| Body / Capability Provider | Body / Capability Layer | 在未来获准边界内产生原始能力输出与局部健康/保护信号 | Goal、Attention、truth、decision、action authority |

## Overlap prevention

- **Self State:** Body/Middleware supply state signals; Brain owns their cognitive synthesis.
- **Evidence:** Middleware owns packaging; Brain owns context-bound evaluation; no internal layer owns truth.
- **Attention:** only Brain Attention Controller forms allocation candidates; Neural transports, Middleware constrains feasibility.
- **Experience:** belongs to evolution boundary and only produces adaptation candidates; it cannot write attention.
- **Simulation:** belongs inside Brain and remains separated from Evidence/Reality flows.

## Status

`COGNITIVE_SYSTEM_MODULE_OWNERSHIP_MATRIX_V2_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
