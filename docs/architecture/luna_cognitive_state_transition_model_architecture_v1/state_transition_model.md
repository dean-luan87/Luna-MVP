# State Transition Model v1

## 定位

本阶段展开 `L(t+1)=F(L(t),Reality(t))` 的架构合同。它描述七个 Core State 如何产生更新候选，不实现状态机、积分器、预测器或 Runtime。

## 分量更新

`Field(t+1)=f(Field(t),Reality)`；`Understanding(t+1)=f(Understanding(t),Evidence,Memory)`；`Goal(t+1)=f(Goal(t),Understanding,Value)`；`Memory(t+1)=f(Memory(t),Experience,Value)`；`Self(t+1)=f(Self(t),GrowthCandidate)`；Value 和 Resource 由各自约束函数提供候选。

每个更新保留来源、Field Scope、时间、置信度、未知和 trace；所有更新默认为 Candidate，并受 Cognitive Stability Constraint 约束。

