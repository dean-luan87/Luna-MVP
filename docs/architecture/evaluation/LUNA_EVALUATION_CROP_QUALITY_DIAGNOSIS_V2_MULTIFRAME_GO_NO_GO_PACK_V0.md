# Crop Quality Diagnosis v2 Multiframe GO/NO_GO Pack v0

## GO

- 30 EP v4 / crop / OCR 链路进入诊断；几何、bbox、帧偏移、亮度/模糊、投影、empty pattern、visual、hypothesis、decision 均输出
- `root_cause_confirmed=false`；Semantic v4 与 SV rerun 继续阻断；无 OCR、无新 crop；no-write boundary 通过

## NO_GO

- 运行 OCR 或生成新 crop；把 empty OCR 写成 no-text fact；确认 root cause 无证据；生成 Semantic/SV；写事实层；benchmark/provider 宣称
