# LUNA YOLO Guarded Trial Hook-In v0

**Phase**：Phase-Mainline-RuntimeReadiness-004  \n
**Hook wrapper**：`capabilities/runtime_readiness/yolo_guarded_trial_hook_v0.py`  \n
**候选挂接点**：`capabilities/model_perception/yolo_shadow_adapter_v0.py::run_yolo_shadow_adapter_on_sample_v0`

---

## 目标

在 YOLO 候选入口处加入 guarded trial gate 评估，但 **默认短路 no-op**，不得触发额外 detector/provider 路径。

---

## 默认行为（必须）

- gate decision 默认 `disabled`
- hook result `enabled=false`、`no_op=true`
- 不改变 `yolo_shadow_adapter_v0` 的 fallback/disable 边界逻辑

---

## 禁止项

- 不新增真实 detector 调用路径
- 不进入下游 SceneTask/Fusion/Output
- 不导航、不世界模型写入

