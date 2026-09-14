# Luna 内部任务指令映射表 v1（系统规格基线 · 定稿）

> **状态**：本文与 [LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md](./LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md)、[LUNA_TASK_PLAN_V1_V2_FINAL_V1.md](./LUNA_TASK_PLAN_V1_V2_FINAL_V1.md) 共同构成 **接模型前的系统规格基线**。  
> **总序**：[LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md](./LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md)。  
> **原则**：模型 **不能发明新命令**，只能映射到本表 **白名单系统指令**；指令必须 **可审查、可确认、可拒绝**。  
> **工程**：`InstructionMappingRecord`（`shared/schemas/instruction_mapping.py`）、指令 id（`shared/schemas/internal_task_instructions_v1.py`）。

---

## 2.1 设计目标

将 **人类语义** 映射为 Luna **系统层唯一合法任务语言**。

---

## 2.2 映射总表

### A. 导航类（navigation.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 去某地 | `navigation.start` | `destination` | `constraints`, `waypoints` |
| 暂停导航 | `navigation.pause` | 无 | 无 |
| 继续导航 | `navigation.resume` | 无 | 无 |
| 停止导航 | `navigation.stop` | 无 | `reason` |
| 切换目的地 | `navigation.switch_destination` | `destination` | `constraints` |
| 加中途点 | `navigation.add_waypoint` | `waypoint` | `position_hint` |
| 移除中途点 | `navigation.remove_waypoint` | `waypoint` | 无 |
| 重新规划 | `navigation.reroute` | 无 | `constraints` |
| 查询进度 | `navigation.query_progress` | 无 | 无 |
| 查询 ETA | `navigation.query_eta` | 无 | 无 |
| 查询当前位置 | `navigation.query_location` | 无 | 无 |
| 查询路线状态 | `navigation.query_route_status` | 无 | 无 |

---

### B. 观察类（observation.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 看前面 | `observation.query_front` | 无 | `scope` |
| 看左边 | `observation.query_left` | 无 | `scope` |
| 看右边 | `observation.query_right` | 无 | `scope` |
| 查附近 | `observation.query_nearby` | 无 | `target_type` |
| 找物品 | `observation.find_object` | `target_type` | `target_features` |
| 找地点 | `observation.find_place` | `target_type` | `constraints` |
| 找标志 | `observation.find_sign` | `target_type` | `text_hint` |
| 持续扫描 | `observation.scan_continuous` | `scan_scope` | `duration_mode` |
| 停止扫描 | `observation.stop_scan` | 无 | 无 |
| 描述场景 | `observation.describe_scene` | 无 | `scope` |

---

### C. 任务控制类（task.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 开始任务 | `task.start` | `task_target` | `constraints` |
| 暂停任务 | `task.pause` | 无 | `target_task_id` |
| 继续任务 | `task.resume` | 无 | `target_task_id` |
| 停止任务 | `task.stop` | 无 | `target_task_id`, `reason` |
| 取消任务 | `task.cancel` | 无 | `target_task_id` |
| 切换任务 | `task.switch` | `task_target` | `constraints` |
| 插入临时任务 | `task.insert_temporary` | `task_target` | `restore_after_finish` |
| 恢复上个任务 | `task.restore_previous` | 无 | `target_task_id` |
| 查询当前任务 | `task.query_current` | 无 | 无 |
| 查询下一步 | `task.query_next_step` | 无 | 无 |

> **与 task_query 域**：问询类（到哪了/下一步…）走 **导航/任务问询映射**，**不得**用 `task.switch` 等控制类指令替代（见 §2.4 规则 2）。

---

### D. 设备控制类（device.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 音量大 | `device.volume_up` | 无 | `step` |
| 音量小 | `device.volume_down` | 无 | `step` |
| 静音 | `device.mute` | 无 | 无 |
| 取消静音 | `device.unmute` | 无 | 无 |
| 休眠 | `device.sleep` | 无 | 无 |
| 关机 | `device.shutdown` | 无 | 无 |
| 设备状态 | `device.status_query` | 无 | 无 |
| 更新状态 | `device.update_query` | 无 | 无 |

---

### E. 确认 / 反馈类（confirmation.* / feedback.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 接受确认 | `confirmation.accept` | `confirmation_target_id` | 无 |
| 拒绝确认 | `confirmation.reject` | `confirmation_target_id` | 无 |
| 修正确认 | `confirmation.modify` | `confirmation_target_id` | `modification_payload` |
| 结束当前对话 | `feedback.stop_current_dialogue` | 无 | 无 |
| 表示没听懂 | `feedback.not_understood` | 无 | 无 |
| 请求重试 | `feedback.retry` | 无 | 无 |

---

### F. 无任务观察类（casual_observation.*）

| 语义动作 | 系统映射 | 必填参数 | 可选参数 |
|----------|----------|----------|----------|
| 一次性前方观察 | `casual_observation.query_once` | 无 | `scope` |
| 一次性附近观察 | `casual_observation.query_nearby` | 无 | `target_type` |
| 场景描述 | `casual_observation.describe_current_scene` | 无 | `scope` |

---

## 2.3 每条映射都必须带治理属性

```json
{
  "system_mapping_candidate": "navigation.start",
  "required_params": ["destination"],
  "optional_params": ["constraints", "waypoints"],
  "requires_confirmation_default": false,
  "task_chain_impact_level": "high",
  "supports_temporary_insertion": true,
  "allowed_in_no_task_mode": true,
  "allowed_in_task_mode": true
}
```

| 字段 | 说明 |
|------|------|
| `required_params` | 没有则不能执行 |
| `optional_params` | 可补充 |
| `requires_confirmation_default` | 默认是否确认 |
| `task_chain_impact_level` | `low` / `medium` / `high` |
| `supports_temporary_insertion` | 是否可作为插入任务 |
| `allowed_in_no_task_mode` | 无主任务时是否允许 |
| `allowed_in_task_mode` | 有主任务时是否允许 |

工程侧：`InstructionMappingRecord`。

---

## 2.4 治理硬规则

| 规则 | 内容 |
|------|------|
| **1** | **高影响动作**默认不能自动执行：`task.switch`、`task.stop`、`device.shutdown`、高影响重排序等。 |
| **2** | **查询类不得伪装成控制类**：例如「现在到哪了」**永远**不是 `task.switch`。 |
| **3** | **无任务观察**默认不升级长期任务；须用户明确要求才升级。 |
| **4** | **确认/反馈类**无待确认上下文时 **不得强行落执行**：例如单独「是」若无 `confirmation_target_id` 对应对象，**不得**直接执行任何业务动作。 |

---

## 2.5 与 Voice 白名单

Voice 短指令仍按 [LUNA_VOICE_SHORTCUT_WHITELIST_V1.md](../voice/LUNA_VOICE_SHORTCUT_WHITELIST_V1.md)；**长语音/文本解析**输出应归一到本表 **system_mapping** 与 `InstructionMappingRecord`。
