# GO / NO_GO — Static Reading Information Source Localization Policy v1

## GO

- WorldModel-first、scene fallback、task mapping、scene-source matrix、ranking、exclusion、human fallback、RRD handoff 齐全  
- 当前 case 缺 task/scene 时 `requires_task_and_scene_context`，不伪造场景  
- 禁止默认泛扫文字；无 runtime action；verifier=GO  

## NO_GO

- 默认全局找字、OCR/detector/camera、伪造场景、事实层写入  

## 一句话

先定位「该读哪里」的信息源，再进入可阅读区域发现；本阶段只定义 policy。
