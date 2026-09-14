# LUNA OCR Bridge — Shadow-Only First Wiring Strategy v0 (Phase-OCRBridge-Implementation-RFC-001)

## 首次实现阶段（授权后）**仅允许**

- 在受控路径上 **生成 `OcrEvidencePack` shadow 副本**（内存或侧车文件，不进业务主链）。  
- 对 shadow pack 执行 **validate**（在分项 flag 打开时）。  
- **写 trace / replay / audit**（与现有 TRW 合同对齐；失败则 **abort**，见 Abort 文档）。  
- 输出 **report**（json / md / jsonl，由实现 phase 定义）。

## **必须保持**

- **不**调用真实 MidPlatform。  
- **不**改变 OCR provider **输出语义**（shadow 为 **旁路观测**，不替换原返回值，除非单独 ADR 允许双写且默认关）。  
- **不**影响任务链 / SceneTask / Fusion / Output。  
- **不**写入事实文本层（无 `fact_text_layer` 开闸则禁止）。  
- **不**写世界模型。  
- **不**自动改变 **OCR provider routing**。

## **禁止**

- 真实 MidPlatform / SceneDelta / WorldContext **调用**。  
- 真实导航 / 播报 / TTS。  
- **fact_text_layer** 写入（未单独授权）。  
- 将 **Evaluation Tools routing pack** 当作 **runtime source**。

---

## 与 Governance 冻结一致

OCR **只封装证据**；**解释与是否可信**由 MidPlatform（实现阶段接线后）负责；shadow 阶段 **仅验证封装质量**，不产生业务事实。
