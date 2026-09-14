# Luna Evaluation — YOLO Evidence ReadOnly Consumer GO / NO_GO Pack v0

## GO

- `evidence_count_observed>0`；`provider=yolo_candidate_adapter`  
- `synthetic_count=0`；`real_detector_count=evidence_count`；`detector_mode=real_yolo`  
- 全部 `not_fact`；无 forbidden keys；audit 无写路径  

## CONDITIONAL_GO

- 非关键聚合缺失；无越界  

## NO_GO

- 标 fact；导航；写事实层；改 registry  
