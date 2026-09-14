# Luna Midplatform — Field-First Core Model Room & Interface Logic Definition v1

## Phase

`Phase-Midplatform-Field-First-Core-Model-Room-and-Interface-Logic-Definition-v1-001`

## 核心原则

1. **先建房间，再放模型** — 所有模型必须先归入岗位房间
2. **模型输出默认是 candidate** — 不得直接成为 fact / record / world model / authorization / action
3. **模型不能反向定义中台** — 开源模型只做能力资产和结构参考
4. **入口出口固定** — 每类模型必须有 adapter + metadata + traceability
5. **接口优先，接入延后** — 本阶段不做真实模型运行

## 9 类模型房间

| 房间 | 参考资产 | 输出 |
|------|----------|------|
| Source Intake Room | 视觉/OCR/语音/深度/IMU/地图 | ObservationCandidate |
| Visual Perception Room | SAM2, Grounded SAM2, ByteTrack | Object/Mask/Track ObservationCandidate |
| OCR / Text Perception Room | PaddleOCR, RapidOCR | TextObservationCandidate |
| Audio / Speech Perception Room | ASR, diarization, voiceprint | SpeechObservationCandidate |
| Spatial / SLAM / Scene Graph Room | Kimera, Hydra, HOV-SG, Open3DSG | Spatial/SceneGraph ReferenceCandidate |
| ECS / Entity Component Room | Esper, Flecs | EntityComponentCandidate (dataclass 先模拟) |
| Semantic / Event Graph Room | NetworkX, RDFLib, Neo4j | SemanticEventCandidate |
| Field Simulation Room | 规则/几何/状态机 | FieldSimulationResultCandidate |
| Midplatform Reasoning Room | LLM/VLM | MidplatformReasoningCandidate |

## Model Adapter Bus

```
Model Raw Output → Model Adapter → Candidate → Validator → Field Model / Reasoning Context
```

## 禁止直接输出

WorldModelFact, PersistentMemory, RealAction, Authorization, Grant, Record, FinalDecision

## Next Phase

`Phase-Midplatform-Field-First-Core-Work-Manual-and-Architecture-Definition-v1-001`
