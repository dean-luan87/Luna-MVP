# unified env shadow metadata snapshot 实现说明（V1）

## 实现了什么

- 在主线 `dispatch_voice_final_text` 中新增一条**可开关**的 JSONL 观测写入：
  - **事件类型**：`unified_env_shadow_snapshot`
  - **写入时机**：`sidewalk_env_summary_v1` / `retail_env_summary_v1` 稳定化之后、`unified_env_summary_shadow_v1` 写入之后、旁路编排（orchestrator）之前
  - **写入内容**：只包含 analyzer 需要的最小字段与 metadata 白名单（不整包落盘）

该 snapshot **只做观测落盘**：不改变主线决策、不回写任何 summary、不驱动任何行为；失败吞掉。

## 写入点在哪

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `_unified_env_shadow_snapshot_enabled_v1()`
  - `_maybe_emit_unified_env_shadow_snapshot_v1(...)`
  - `dispatch_voice_final_text` 内：紧接 `_maybe_attach_unified_env_shadow_v1(...)` 之后调用

## 开关与路径

- **开关**：`LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1`
  - 默认关闭；仅当值为 `1` / `true` / `yes` 时写入
- **输出路径**：`LUNA_UNIFIED_ENV_SHADOW_SNAPSHOT_V1_JSONL`
  - 默认：`logs/unified_env_shadow_snapshot_v1.jsonl`

## 最小事件形态（JSONL）

每行 JSON：

```json
{
  "type": "unified_env_shadow_snapshot",
  "data": {
    "timestamp": 0.0,
    "event_timestamp": 0.0,
    "related_request_id": "rid",
    "source": "voice_final_text_dispatcher_v1",
    "metadata": {
      "sidewalk_env_summary_v1": {},
      "retail_env_summary_v1": {},
      "unified_env_summary_shadow_v1": {}
    }
  }
}
```

其中 `metadata` 采用白名单，仅保留：
- `sidewalk_env_summary_v1`（若存在且为 dict）
- `retail_env_summary_v1`（若存在且为 dict）
- `unified_env_summary_shadow_v1`（若不存在会在 payload 内补齐一份，不回写 runtime_context）

## 怎么验证

```bash
python3 tools/test_unified_env_shadow_snapshot_v1.py
```

覆盖：
- 开关关闭不写入
- 开关开启写入一条 snapshot
- snapshot 字段满足 analyzer 最小契约
- metadata 白名单不包含 risk/intent/OCR
- 写入失败吞掉、不影响调用返回

## 仍未做什么（按边界）

- 不做一致率统计（由 `tools/analyze_unified_env_shadow_v1.py` 负责）
- 不做主线接线 / 派生替换
- 不做自动评审 / 行为驱动

## 一句话收束

先把真实窗口的 `unified_env_shadow_snapshot` JSONL 产出来，再用 analyzer 跑第二观察窗口，最后再讨论是否值得进入最小接线评审。

