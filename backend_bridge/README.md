# backend_bridge（Stage-0）

本目录用于声明与占位：**whitebox / memory / logs / traces / audit** 的逻辑归属属于
`individual_backend_capability`（个体 Luna 后端能力层），不是 Voice/Vision/Emotion 的附属模块。

## Stage-0 原则

- **不强迁**：不把现有实现强行搬到这里
- **不重构**：不改写运行逻辑、不改主链行为
- **只做边界**：用 README / bridge / facade 占位方式明确 ownership 与未来 split 方向

## 后续（非 Stage-0）

未来可能演进为：
- 独立 Python package / 独立服务
- 通过稳定 API 暴露给 Core Framework 与各 capability

