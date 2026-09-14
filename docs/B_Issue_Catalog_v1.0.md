B 模块 IssueCode 目录规范

B_Issue_Catalog v1.0（Frozen）

---

一、IssueCode 总体设计规则（先写死）

1. 命名规则（不可变）

B-{DOMAIN}-{XXX}

- B：模块标识（B 模块）
- DOMAIN：问题域
- PROC    工作过程
- OUT     结果产出
- COLLAB  BC 协同
- XXX：三位递增编号（001 起）

IssueCode 一旦发布，语义永不变更。

---

2. 每个 IssueCode 必须绑定的元信息

IssueCodeMeta {
  domain,
  default_level,
  affects_sub_state,
  auto_action_hint,
  description
}

⚠️ 注意：
auto_action_hint 是 模块侧自治动作建议，
不是系统裁决指令。

---

二、B-PROC-*（工作过程监督 Issue）

判断的是：“B 还能不能正常干活”

---

B-PROC-001：推理流程连续超时
- 描述：连续 N 次推理超过允许时间窗口
- 默认等级：ERROR
- 影响子状态：InternalProcessState = DEGRADED
- 动作建议：降频 / 进入轻量模式

---

B-PROC-002：推理流程卡死 / 无进展
- 描述：心跳存在，但推理计数长时间无变化
- 默认等级：CRITICAL
- 影响子状态：InternalProcessState = FAILED
- 动作建议：停止预测，等待恢复

---

B-PROC-003：连续内部异常（非输入导致）
- 描述：连续抛出内部异常（OOM、非法状态等）
- 默认等级：ERROR
- 影响子状态：InternalProcessState = DEGRADED
- 动作建议：禁用高风险路径

---

B-PROC-004：内部状态不一致
- 描述：检测到非法状态组合或重复初始化
- 默认等级：CRITICAL
- 影响子状态：InternalProcessState = FAILED
- 动作建议：强制进入 UNAVAILABLE

---

B-PROC-005：自检失败
- 描述：启动或恢复时未通过最小自检
- 默认等级：CRITICAL
- 影响子状态：InternalProcessState = FAILED
- 动作建议：禁止预测，仅允许恢复流程

---

三、B-OUT-*（结果产出监督 Issue）

判断的是：“B 说出来的话靠不靠谱”

---

B-OUT-001：输出字段缺失
- 描述：必要字段为空或缺失
- 默认等级：ERROR
- 影响子状态：OutputQualityState = INVALID
- 动作建议：暂停该类输出

---

B-OUT-002：输出数值非法
- 描述：NaN / Inf / 越界数值
- 默认等级：CRITICAL
- 影响子状态：OutputQualityState = INVALID
- 动作建议：立即停止预测

---

B-OUT-003：输出置信度异常塌陷
- 描述：置信度长期接近 0 或固定值
- 默认等级：WARNING
- 影响子状态：OutputQualityState = SUSPICIOUS
- 动作建议：提高不确定性标注

---

B-OUT-004：输出结果剧烈抖动
- 描述：短时间内结果变化超过合理范围
- 默认等级：WARNING
- 影响子状态：OutputQualityState = SUSPICIOUS
- 动作建议：降频输出

---

B-OUT-005：输出与输入明显不匹配
- 描述：输出语义与当前输入上下文严重冲突
- 默认等级：ERROR
- 影响子状态：OutputQualityState = INVALID
- 动作建议：暂停当前预测路径

---

四、B-COLLAB-*（BC 协同监督 Issue）

判断的是：“B 还能不能安全地参与协同”

---

B-COLLAB-001：Reference / 坐标不一致
- 描述：与 C 或系统使用的 Reference 不一致
- 默认等级：ERROR
- 影响子状态：CollaborationState = COLLAB_DEGRADED
- 动作建议：退出协同，等待重新校准

---

B-COLLAB-002：时间戳漂移超限
- 描述：B 输出时间与协同窗口不一致
- 默认等级：ERROR
- 影响子状态：CollaborationState = COLLAB_DEGRADED
- 动作建议：暂停协同

---

B-COLLAB-003：协同返回值结构异常
- 描述：来自 C 的反馈缺失字段或非法
- 默认等级：WARNING
- 影响子状态：CollaborationState = COLLAB_DEGRADED
- 动作建议：降级协同参与

---

B-COLLAB-004：协同链路中断
- 描述：无法发送或接收协同信息
- 默认等级：CRITICAL
- 影响子状态：CollaborationState = COLLAB_SUSPENDED
- 动作建议：主动退出协同

---

B-COLLAB-005：协同反馈逻辑冲突
- 描述：协同返回值与当前上下文严重冲突
- 默认等级：ERROR
- 影响子状态：CollaborationState = COLLAB_DEGRADED
- 动作建议：暂停当前协同会话

---

五、IssueCode 与自治状态的关系回顾（闭环）

IssueCode
 → SubState（PROC / OUT / COLLAB）
   → B_AutonomyState
     → State → Action 表

任何 Issue 都不能直接触发行为，只能影响状态。

---

六、为什么这套目录“够用又不过度”
- 覆盖：
- 活着吗？
- 说话靠谱吗？
- 能一起干活吗？
- 但不涉及：
- 业务语义
- 决策逻辑
- 用户安全裁决

这是 B 模块自治的“最小完备集合”。

---

七、下一步自然衔接（不推进）

现在 B 模块自治已经具备：
- Issue 语言
- 状态机
- 动作表

剩下的两步都是“工程接口”：
1. Autonomy Heartbeat Monitor 接口规范
2. B 模块自治 Snapshot / 上报接口（给后台）

你点一个，我直接写成规范文档。
