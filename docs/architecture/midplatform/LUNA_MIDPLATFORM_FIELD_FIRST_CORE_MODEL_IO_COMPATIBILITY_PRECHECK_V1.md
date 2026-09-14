# Luna Midplatform — Model I/O Compatibility Precheck v1

## Phase

`Phase-Midplatform-Field-First-Core-Model-IO-Compatibility-Precheck-v1-001`

## 目标

在自研骨架实现之前，轻量检查模型文档中的 I/O 边界，校准 Field-First 骨架入口/出口，避免「房子建好、门窗尺寸不匹配」。

## 骨架必须兼容的字段

bbox | mask | track_id | text_region | recognized_text | segment_timestamp | word_timestamp | confidence | source_ref | frame_ref

## 六类 Common Payload

spatial | temporal | identity | confidence | graph | text/audio

## Next Phase

`Phase-Midplatform-Field-First-Self-Developed-Skeleton-Implementation-v1-001`
