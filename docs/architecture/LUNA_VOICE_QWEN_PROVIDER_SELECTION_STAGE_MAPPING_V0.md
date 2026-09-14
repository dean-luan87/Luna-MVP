# LUNA Voice — Provider Selection Stage Mapping v0（Phase-Voice-Qianwen-003）

**Stage**：`request_trace.stage.output.voice.qwen_entry.provider_selection`

**语义**：承载 **dry-run** 下的 **`provider_order` / `selected_provider` / `selection_reason`**（来自 Phase-002 `provider_selection`），并与 **`provider_mode`**（`online_prefer_qwen` vs `offline_only`）对照。

---

## 映射规则（观测）

| governance_final_action（同源 governance） | online_prefer_qwen（dry-run） | offline_only（dry-run） |
|-----------------------------------------------|-------------------------------|-------------------------|
| accepted_dry_run | `selected_provider=qwen`，order `[qwen,piper]` | `selected_provider=piper`，order `[piper]` |
| fallback_candidate | `selected_provider=piper`，order `[qwen,piper]` | `selected_provider=piper`，order `[piper]` |
| suppressed / cancelled / 其它阻断 | `selected_provider=none` | `selected_provider=none` |

**离线观测结论**：**offline 路径永不出现 `qwen`**；**online** 仅在策略允许且样本为 **accepted** 时首选 **qwen**。

---

## 表产物

- **`voice_qwen_provider_selection_stage_table.json`**：逐 **request_id × provider_mode** 展开。
