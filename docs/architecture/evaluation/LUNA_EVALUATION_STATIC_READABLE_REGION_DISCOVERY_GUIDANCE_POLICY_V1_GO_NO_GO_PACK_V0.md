# GO / NO_GO — Static Readable Region Discovery Guidance Policy v1

## GO

- discovery scope、candidate schema、filtering、classification、view guidance、ranking、capture handoff、OCRRequest gate link、human assist、unresolved/expired 齐全  
- 当前 case 缺 task/scene 时 `readable_region_discovery_invoked_now=false`，不伪造 readable region  
- 禁止默认泛扫文字；无 detector/OCR/camera；无 runtime action；verifier=GO  

## CONDITIONAL_GO

- 仅 policy 定义；当前 case 等待 task/scene 与 ranked information source area  

## NO_GO

- 默认 full-frame text search、detector/OCR/camera、伪造 readable region、OCRRequest 生成、事实层/WorldModel/SceneDelta 写入、benchmark/provider 宣称  

## 一句话

在已定位的信息源候选区域内定义 readable region 发现、筛选、用户对准引导与 static capture/OCRRequest 未来门；本阶段只定义 policy。
