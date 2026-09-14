# Luna 语音白名单短指令 v1

> 白名单由 `VoiceShortcutRegistry` 集中维护（`capabilities/voice/runtime/voice_shortcut_registry.py`）。  
> 每条条目包含：`shortcut_id`、`shortcut_type`、短语列表、`allowed_in_task_mode`、`allowed_in_normal_mode`、`requires_confirmation`、`mapped_route_type`。

## 1. 分类 A：设备控制类（device_control）

| shortcut_id | 短语（示例） | 任务态 | 普通态 | 需确认 | mapped_route_type |
|-------------|--------------|--------|--------|--------|-------------------|
| dev_pause | **暂停播报**、先暂停 | ✓ | ✓ | 否 | device_control |
| dev_stop | 停止 | ✓ | ✓ | 否 | device_control |
| dev_resume | **继续播报** | ✓ | ✓ | 否 | device_control |
| dev_cancel | 取消 | ✓ | ✓ | 否 | device_control |
| dev_shutdown | 关机 | ✓ | ✓ | **是** | device_control |
| dev_vol_up | 音量大一点、大声点 | ✓ | ✓ | 否 | device_control |
| dev_vol_down | 音量小一点 | ✓ | ✓ | 否 | device_control |

高风险动作（如 **关机**）在事件中标记 `requires_confirmation_candidate`，后续由确认路由承接；v1 不强做完整确认体系。

## 2. 分类 B：任务控制类（task_control）

| shortcut_id | 短语 | 任务态 | 普通态 | 需确认 | mapped_route_type |
|-------------|------|--------|--------|--------|-------------------|
| task_start_nav | 开始导航 | ✓ | ✓ | 否 | task_lifecycle |
| task_end | 结束任务 | ✓ | ✗ | 否 | task_lifecycle |
| task_switch | 切换任务 | ✓ | ✗ | 否 | task_lifecycle |
| task_pause | 暂停任务、**暂停** | ✓ | ✗ | 否 | task_lifecycle |
| task_resume | 继续任务、**继续** | ✓ | ✗ | 否 | task_lifecycle |

**任务态优先（v1 小补丁）**：当 **`is_task_mode=True`** 时，裸指令 **「暂停」「继续」** 映射到 **`task_pause` / `task_resume`**（任务生命周期），**不再**与设备 `dev_pause`/`dev_resume` 共用短词。设备侧使用显式短语 **「暂停播报」「继续播报」**（及「先暂停」）对应播报控制。

说明：「开始导航」等在普通态放行是为了支持 **唤醒后 + 窗口内** 通过白名单触发；若仅「开始导航」且无唤醒、无窗口且无任务态，由路由规则决定是否接受（见路由器实现）。

## 3. 分类 C：任务问询类（task_query）

| shortcut_id | 短语 | 任务态 | 普通态 | 需确认 | mapped_route_type |
|-------------|------|--------|--------|--------|-------------------|
| q_where | 现在到哪了、到哪了 | ✓ | ✗ | 否 | task_context_query |
| q_nearby | 附近有什么 | ✓ | ✗ | 否 | task_context_query |
| q_status | 当前状态 | ✓ | ✗ | 否 | task_context_query |
| q_ahead | 前面是什么 | ✓ | ✗ | 否 | task_context_query |
| q_distance | 还有多远 | ✓ | ✗ | 否 | task_context_query |

## 4. 分类 D：会话控制（session_control）

| shortcut_id | 短语 | 任务态 | 普通态 | 需确认 | mapped_route_type |
|-------------|------|--------|--------|--------|-------------------|
| session_end | 结束对话、不用了、退出 | ✓ | ✓ | 否 | session_end |

命中后由会话协调器 **清空会话窗口**（与「结束对话」语义一致）。

## 5. 分类 E：确认/反馈证据（confirmation_feedback）

用于待确认上下文下的 **是/否** 证据，**不是**直接执行命令（Bridge 走 `CONFIRMATION`）。

| shortcut_id | 短语 | 任务态 | 普通态 | 需确认 | mapped_route_type |
|-------------|------|--------|--------|--------|-------------------|
| cf_yes | 是、对 | ✓ | ✓ | 否 | confirmation |
| cf_no | 不是、不对 | ✓ | ✓ | 否 | confirmation |

**匹配规则**：单字短语（如「是」「对」）仅当 **整句与短语完全一致** 时命中，避免「这是一段…」中的「是」子串误匹配。多字短语仍使用包含匹配（最长短语优先）。

## 6. 任务态 vs 普通态小结

- **仅任务态**：任务问询类、部分任务控制类（见上表「普通态 ✗」）。
- **任务态 + 普通态（在允许列表内）**：设备控制、会话结束、部分条目如「开始导航」。
- **普通态未唤醒、无窗口且非白名单**：长句或自由说法 → **reject**（见输入主线文档）。

## 7. 后续扩展：大模型长语音拆解 → 关键词 → 任务动作

**本轮不实现**，仅作产品/架构预留：

1. **目标**：对长语音做 ASR 后，由 **大模型** 或专用解析器提炼 **关键词、槽位、任务动作**，并映射到任务链节点或 Bridge 的 proposal。
2. **位置**：属于 **语音输入扩展层**，在 `VoiceInputEvent` 与任务链之间增加 **结构化解析步骤**；**不**替代 v1 白名单捷径，而是与并存。
3. **原则**：扩展层仍须产出标准 `VoiceInputEvent` 或下游约定的结构化字段，**不**绕开治理与主链裁决。

---

主文档：[LUNA_VOICE_INPUT_MAINLINE_V1.md](./LUNA_VOICE_INPUT_MAINLINE_V1.md)
