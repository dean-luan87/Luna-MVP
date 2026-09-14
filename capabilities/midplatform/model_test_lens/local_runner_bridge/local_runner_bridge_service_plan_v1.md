# Model Test Lens — Local Runner Bridge Service Plan V1

## 定位

**localhost 本地模型测试后端**，不是 runtime、不是 output adapter、不是商业后端。

| 组件 | 地址 | 职责 |
|------|------|------|
| Model Test Lens UI | `http://localhost:8765` | 选文件、提交 job、看状态、加载 envelope |
| Local Runner Bridge Service | `http://127.0.0.1:8787` | 登记资产、跑 runner、调 adapter、写 TestBoard |

## 架构

```
Model Test Lens UI (8765)
    ↓ HTTP localhost only
Local Runner Bridge API (8787, bind 127.0.0.1)
    ↓
Asset Store: capabilities/test_assets/model_test_lens/
    ↓
Runner: segmentation_mobile_sam / slam_video / ...
    ↓
Adapter → MUEP envelope
    ↓
_tmp_eval_out + TestBoard refs
    ↓
UI 展示（只读）
```

## Service 允许

- 绑定 `127.0.0.1:8787`（禁止 `0.0.0.0`）
- 本地文件登记到受控 test asset 目录
- 生成 manifest / job
- 审批后调用受控 runner 执行模型测试
- 调用 evaluation adapter 生成 envelope
- 写 `_tmp_eval_out` 与 TestBoard

## Service 禁止

- 外网绑定 / 外网 URL / dataset 下载
- live camera / microphone
- registry / fact / semantic / navigation / speech / output adapter
- 删除 TestBoard / 历史 evidence

## API（规划，本阶段不实现）

见 `schemas/local_runner_bridge_api_schema_v1.json`。

## Runner Registry

第一版 skeleton 建议实现：

1. `segmentation_mobile_sam_runner`
2. `slam_video_runner`（limited / placeholder route）

其余 runner 为 placeholder。

## Job 生命周期

`created` → `asset_registered` → `awaiting_approval` → `ready_to_run` → `running` → `adapter_processing` → `completed` | `failed_no_boundary_violation` | `blocked`

## SLAM 无 GT

- `no_gt_limited_mode = true`
- 不计算 ATE / 不与 GT benchmark 比较
- 仅 limited diagnostics

## MobileSAM

- 读 image manifest + prompt plan
- 输出 candidate masks + metrics → envelope
- 不写 fact / 不进 runtime

## 本阶段

**Planning only** — 不启动 HTTP、不执行模型、不上传真实文件。

## 下一步

`Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Skeleton-Execution-And-Post-Review-v1-001`
