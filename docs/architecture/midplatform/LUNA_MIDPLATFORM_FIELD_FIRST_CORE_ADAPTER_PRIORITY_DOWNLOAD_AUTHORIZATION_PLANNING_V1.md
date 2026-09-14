# Luna Midplatform — Adapter Priority & Download Authorization Planning v1

## Phase

`Phase-Midplatform-Field-First-Core-Adapter-Priority-and-Download-Authorization-Planning-v1-001`

## 核心原则

1. **先 adapter，后下载** — near-term 且 contract 清楚才可进入 owner review 候选
2. **先轻量链路，后重型模型** — 不先接 Kimera/Hydra/Neo4j
3. **先 ObservationCandidate，后 FieldSimulation**
4. **下载授权不自动打开** — `download_authorized` 保持 false
5. **自研骨架优先** — P0 五项无需权重

## Adapter 优先级

| 优先级 | 内容 |
|--------|------|
| **P0** | Luna Frontend Sensing, ECS, Event Graph, Geometry Simulator, Drive Layer |
| **P1** | PaddleOCR, RapidOCR, ByteTrack, YOLO, Whisper, faster-whisper, rule+LLM hybrid |
| **P2** | Grounded SAM2, SAM2, SenseVoice, pyannote, GroundingDINO, structured LLM |
| **P3** | Kimera/Hydra/HOV-SG/Open3DSG/Esper/Flecs/RDFLib + deferred |

## Skeleton 批次

- **Batch A：** 自研主链（无权重）
- **Batch B：** 轻量观测 adapter skeleton（不加载模型）
- **Batch C：** 重型 future placeholder（不下载不运行）

## Next Phase

`Phase-Midplatform-Field-First-Self-Developed-Skeleton-Implementation-v1-001`
