# Benchmark Real Values Smoke — GO / NO_GO Pack v0

## GO

- `collection_scope=readonly_real_values_smoke`
- T0：`no_write_boundary_pass_rate=1.0`，violation counts 全 0
- T1：coverage / poster / public facility / reference 功能计数已采
- T2：全部 `not_collected`；`benchmark_score=null`
- interpretation guard + boundary pass + audit 完整；verifier **GO**

## CONDITIONAL_GO

- 部分 T1 非关键缺失，但 T0/boundary/guard/audit 完整且无越界

## NO_GO

- 运行 OCR/Vision；采集 T2；生成 benchmark claim；比较 provider；写事实层；改 routing

## 下一 phase

1. Simulation Lab crash_recovery + PaddleOCR batch recovery  
2. Poster real OCR gated execution  
3. RealVideo OCRRequest gated submission  
