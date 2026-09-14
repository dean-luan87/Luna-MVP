# Implementation Plan（Architecture Only）

1. 以现有 Field、Attention/Decision Integration、Memory、Action Outcome、Selective Learning 和 Self–World Boundary 合同为 canonical 参考。
2. 建立适配器和统一引用，不移动、删除或重写既有资产。
3. 后续实现顺序：Flow State/Trace → Context 与 Candidate 传递 → Outcome/Validation → 受治理的 Memory/Learning 集成。
4. 每个实现模块先登记 Owner、输入输出、禁止依赖和生命周期，再由独立验证器检查。
5. Runtime、Action、自动学习、B Simulation 和模型/硬件接入必须另行批准，不属于本阶段。

