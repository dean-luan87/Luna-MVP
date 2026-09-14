# Phase-Perception-001 — Industrial Grade Placeholder Register v0（工业级占位登记，不阻塞主线）

**目的**：对当前阶段暂时做不到的工业级要求做占位登记，并明确后续归属阶段。  
**硬规则（写死）**：
- 工业级要求分期进入  
- 当前做不了的只允许 placeholder / future hook  
- **每个占位必须标记 planned_phase**  
- **current_status=placeholder_only**  
- **blocking_current_phase=false**（不得阻塞当前阶段停止条件）  
- 不得被遗忘（必须可追踪、可复盘）  

---

## Placeholder Register（v0）

| placeholder_id | requirement_name | reason | planned_phase | current_status | blocking_current_phase |
|---|---|---|---|---|---|
| IG-001 | 弱光/逆光/雨天鲁棒性 | baseline 仅做 mock/fixture；先保证 schema 与保守性 | Phase-Device-001 | placeholder_only | false |
| IG-002 | 摄像头抖动鲁棒性 | 真机抖动与 IMU/稳像耦合不在 v0 | Phase-Device-001 | placeholder_only | false |
| IG-003 | 设备端性能/功耗/发热 | 本阶段不做真机性能总验收 | Phase-Device-001 | placeholder_only | false |
| IG-004 | 隐私与敏感场景处理 | 需要独立隐私策略与脱敏管线 | Phase-Model-004（future） | placeholder_only | false |
| IG-005 | 真机环境日志分级 | 当前只做结构化 baseline 输出与工具回放 | Phase-Device-001 | placeholder_only | false |
| IG-006 | 模型版本漂移监控 | 需要模型平台化/监控链路 | Phase-Model-004（future） | placeholder_only | false |
| IG-007 | 远程诊断与配置灰度 | 需要运维与灰度框架 | Phase-Device-002（future） | placeholder_only | false |
| IG-008 | 长时间连续运行稳定性 | 需要长时真机/现场测试 | Phase-Device-001 | placeholder_only | false |
| IG-009 | 地图数据更新与离线地图策略 | Fusion-001 仅 mock 地图约束；真实地图更新策略后置 | Phase-Fusion-002（future） | placeholder_only | false |
| IG-010 | 多源地图供应商适配 | 供应商适配不在 v0 | Phase-Fusion-002（future） | placeholder_only | false |
| IG-011 | 真实定位漂移鲁棒性（map×vision 对齐） | 真机定位/视觉同步误差校准后置 | Phase-Device-001 | placeholder_only | false |
| IG-012 | 长期记忆污染治理 | Memory 作为优化候选；污染治理需要单独策略 | Phase-Fusion-002（future） | placeholder_only | false |
| IG-013 | 跨设备记忆同步 | 同步与隐私约束后置 | Phase-Fusion-002（future） | placeholder_only | false |
| IG-014 | 隐私敏感路线处理 | 路线隐私策略后置 | Phase-Model-004（future） | placeholder_only | false |
| IG-015 | 真实 TTS 延迟实测 | Expression-001 只冻结输出候选与时效策略；不做真机 TTS 端到端延迟测量 | Phase-Device-001 | placeholder_only | false |
| IG-016 | 多语言/方言播报 | v0 不做多语言播报与本地化策略 | Phase-Voice-002（future） | placeholder_only | false |
| IG-017 | 用户个性化播报节奏 | v0 禁止人格化/个性化；节奏个性化后置 | Phase-Voice-003（future） | placeholder_only | false |
| IG-018 | 长时间导航疲劳度管理 | v0 不做长期导航疲劳度与提醒策略优化 | Phase-Expression-002（future） | placeholder_only | false |
| IG-019 | 不同硬件音量/噪声环境适配 | 真机麦克风/扬声器/噪声自适应后置 | Phase-Device-001 | placeholder_only | false |
| IG-020 | 紧急播报声学优先级 | 紧急提示的声学优先级与混音策略后置 | Phase-Device-001 | placeholder_only | false |
| IG-021 | 无网络时本地播报策略 | 离线播报与缓存策略后置 | Phase-Device-001 | placeholder_only | false |

---

## 备注

- 本表只做登记，不做实现。  
- planned_phase 为路线图归属建议；未来若调整必须保留迁移记录。  

