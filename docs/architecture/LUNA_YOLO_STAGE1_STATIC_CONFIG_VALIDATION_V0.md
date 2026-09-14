# LUNA YOLO Stage-1 Static Configuration Validation v0（Phase-Mainline-GuardedTrial-003）

**Phase**：Phase-Mainline-GuardedTrial-003  
**定位**：在 **不调用 detector、不打开摄像头、不开视频流** 的前提下，静态确认 YOLO Stage-1 所需的 **入口 / 帧来源 / 模型与 manifest / 输出 schema / TRW 写入合同 / 10-frame runbook**。

---

## 1. 模块与工具

| 组件 | 路径 |
|------|------|
| 静态校验 | `capabilities/guarded_trial/yolo_stage1_static_config_validator_v0.py` |
| CLI | `tools/validate_yolo_stage1_static_config_v0.py` |
| Verifier | `tools/verify_yolo_stage1_static_config_v0.py` |

输出目录：`logs/yolo_stage1_static_config_validation_003_<UTC>/`。

---

## 2. 与 Phase-002 的关系

- Phase-002：**试验按钮**安全（precheck + verifier）。  
- Phase-003：**试验材料**是否在仓库与合同层面 **可静态对齐**（仍 **不跑 10 frames**）。
