# Dynamic Function Simplification

复杂模块统一收敛为：

`L(t+1) = F(L(t), Reality(t))`

Field 是输入状态空间；Memory 是历史影响函数；Attention 是转移控制候选；Decision 是 State → Action Candidate 映射；Learning 是 State Transition Optimization Candidate。Self Regulation 提供资源、风险和许可约束。

这只是数学/架构抽象，不代表本阶段实现统一函数 Runtime。

