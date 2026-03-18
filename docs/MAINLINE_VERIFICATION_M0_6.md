# 主线验证 M0.6：去噪与价值分层

在 M0.5「接入链通、观测链通」基础上，解决**假活跃**问题：把「在场」与「出力」分开、给软动作加真实触发门槛、按有效值做价值排序。

## 目标

- **observed vs effective**：消费拆成「被读/汇总」与「真正影响决策」两层。
- **软动作门槛**：look_forward / shift_view_* / recheck_* 等仅在「有 reason 或 target」等条件成立时记入；arbitration_summary_ready / object_search_prompt_ready 仅在非默认时记入。
- **价值有效**：search / recheck / arbitration / bundle / experience 按「有效值」（非默认占位）统计，分析脚本输出「4b. 价值排序（有效）」。

## 1. 消费分层

| 字段 | 含义 |
|------|------|
| `integration_observed_modules` | 被读到、被汇总到 summary 的模块（原 consumed 语义） |
| `integration_effective_modules` | 真正影响 soft/blocked/foreground/state 的模块 |

有效判定（满足任一即计为 effective）：

- **task_chain_bridge**：tc_state 非 active 或 bundle_state 非 none
- **task_arbitration**：arb_action ≠ continue_current
- **task_bundle**：有 bundle_id 且 status 为 proposed/active
- **object_search_interaction**：search_state 非纯 searching/target_unclear 或 waiting/terminal
- **recheck_planner**：有 action 且 (reason 或 target) 非空
- **experience_evolution**：有 group/repeated/contradiction 或 status 非 candidate

## 2. 软动作真实触发门槛

- **look_forward / shift_view_* / recheck_environment / recheck_close_range**：仅当 recheck 有明确 reason 或 target（`recheck_meaningful`）时加入 soft_actions。
- **arbitration_summary_ready**：仅当 arb_action ≠ continue_current 时加入。
- **object_search_prompt_ready**：仅当 search_state 为「有意义」状态（非纯占位）时加入。

其余软动作（如 bundle_summary_ready 等）保持原逻辑。

## 3. 价值有效（integration_pillar_effective）

每帧输出 dict：`search / recheck / arbitration / bundle / experience` 是否**非默认占位**。

- **search**：非默认 prompt、非空 target、非纯占位 state。
- **recheck**：非默认 look_forward 占位，有明确目标/原因/未阻断动作。
- **experience**：非默认 candidate 占位，有非空 group/repeated/contradiction 或 status 差异。
- **arbitration**：非永远 continue_current，有可区分仲裁或维度变化。
- **bundle**：有 bundle 相关状态或合并场景。

分析脚本聚合 `integration_pillar_effective`，输出「1b. 模块有效率」和「4b. 价值排序（有效）」。

## 4. 单帧观察备注（M0.6）

`integration_observation_frame_note` 增加 `eff_mod=N`（本帧 effective 模块数），便于 grep/统计。

## 使用方式

### 跑主流程并写新 JSONL（无注释，可直接复制）

```bash
cd /Users/luanlei/Desktop/Luna-Core
DECISION_MONITOR_ENABLED=1 DECISION_MONITOR_JSONL_PATH=logs/decision_monitor_fresh.jsonl DECISION_MONITOR_CONSOLE=1 DECISION_MONITOR_CONSOLE_INTERVAL=10 python3 main.py
```

跑一段时间后按 `q` 退出。

### 只分析本次产出的新文件

```bash
python3 tools/analyze_mainline_integration.py logs/decision_monitor_fresh.jsonl
```

可选：`--max-frames 5000`、`--json-out report.json`。

### 报告解读

- **1. 模块消费率**：observed 出现次数（原 consumed）。
- **1b. 模块有效率**：effective 出现次数；明显低于 100% 才说明分层生效。
- **2. 软动作命中率**：经门槛过滤后，look_forward 等不应再 100%。
- **4. 价值排序**：有内容帧数（原逻辑）。
- **4b. 价值排序（有效）**：非默认占位帧数；用于判断谁真值钱。

## 修改与新增

| 项 | 说明 |
|----|------|
| `decision_monitor/mainline_integration.py` | 增加 observed/effective、pillar_effective、软动作门槛、eff_mod 备注 |
| `tools/analyze_mainline_integration.py` | 聚合 effective_modules、pillar_effective；输出 1b、4b |
| Viewer 主线接入卡片 | 展示 observed / effective / pillar有效 |
| `docs/MAINLINE_VERIFICATION_M0_6.md` | 本文档 |

## 测试素材

- **M0.6 桌面静态寻物测试图 001**：根目录 `find_test.jpg`。图中目标为：手机、维生素药瓶、牙签盒、纸巾、**杯子**（非“被子”）。适合 A 类静态寻物，不适合 B 类容器/遮挡流。详见 `docs/M0_6_FIND_TEST_SCENE_001.md`。

## 建议的下一步测试

- **场景 A**：对象寻物（桌上明显物体或使用 `find_test.jpg`），看 object search / recheck 有效是否上升。
- **场景 B**：容器/遮挡（盒子、抽屉），看 recheck/experience 有效。
- **场景 C**：双任务注入，看 arbitration / bundle 有效与阻断。

这样可从「空转稳定」过渡到「认知价值」验证。
