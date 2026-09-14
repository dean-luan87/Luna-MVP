# LUNA Evaluation — PaddleOCR Benchmark GO / NO-GO Pack v0（Phase-PaddleOCR-Evaluation-Benchmark-001）

## GO

- **Materialize = GO**；**pinned manifest** 可读。  
- **样本数**：`0 < sample_count <= 20`；每张 **image_path** 可读。  
- **产物齐全**：summary、sample_matrix、raw、normalized、evidence、quality_metrics、runtime_metrics、error_report、audit。  
- **审计**：`network_request_invoked=false`，`model_cache_modified=false`，**routing / RapidOCR / runtime / whitebox / MidPlatform / 世界模型 / 中台语义** 均为 **false**。  
- **`accuracy_pass_claimed`** 不得在无 ground truth 评估样本时为 **true**。  
- **`benchmark_verdict`** 与 **`constructor_ok`** 一致（**GO** 时 constructor 必须成功）。  
- **verifier `verdict=GO`**。

## CONDITIONAL_GO

- Benchmark 跑完且产物齐全，但 **部分样本 predict 失败**（错误报告完整）。  
- **无足够 ground truth**，准确率仅 **not_applicable**（runner 侧 **`accuracy_interpretation`** 非 `computed`）。  
- **内存 / CPU 细粒度**不可测且已在 metrics 中 **null + 说明**。

## NO_GO

- **样本数 = 0** 或 **> 20**。  
- **Materialize 非 GO** 或 **pinned / manifest 缺失**。  
- **网络请求**或 **模型缓存被修改**。  
- **constructor 失败** 但 summary 仍标 **GO**。  
- **无 ground truth 却宣称准确率通过**（`accuracy_pass_claimed` 违规）。  
- **输出缺失**或 **verifier 发现硬失败**。
