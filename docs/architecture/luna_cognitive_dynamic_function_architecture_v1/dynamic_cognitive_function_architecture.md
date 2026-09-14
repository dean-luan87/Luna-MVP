# Dynamic Cognitive Function Architecture v1

## 定位

Dynamic Cognitive Function 是 Cognitive State Machine 的上层连续模型。它不把认知过程限制为离散节点，而用有界状态向量描述当前认知活动强度、置信度、资源压力和决策倾向。

## 状态变化

`C(t+1) = F(C(t), Field(t), Self(t), Goal(t))` 只定义接口和变量关系，不实现函数、积分器或 Runtime。所有分量必须有来源、范围、时间与 unknowns。

## Self Regulation

`R(t) = f(Self, Resource, Constitution)` 产生 Attention、Exploration、Compute、Risk 与 Learning Permission 的候选预算。它调节认知资源和阈值，不替代 Understanding、Decision 或 Constitution。

## 个体差异

Cognitive Parameter Space 和 Cognitive Genome 描述认知倾向与能力参数的组合，不是 Identity、人格或不可审计的隐式权重。参数变更必须经过治理、可追溯、可回滚和 Self Review。

