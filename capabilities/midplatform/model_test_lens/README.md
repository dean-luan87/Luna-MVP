# Model Test Lens（模型测试镜头页）

**定位**：本地静态模型测试可视化页面，属于中台测试管理（`capabilities/midplatform/model_test_lens/`）。

## 固定本地测试页（以后就用这个）

| | |
|---|---|
| **URL** | **http://localhost:8765**（端口冻结，勿改） |
| **一次性启动** | `bash scripts/start_model_test_lens.sh` |
| **常驻服务（推荐）** | `bash scripts/install_model_test_lens_service.sh` |
| **HTML** | `capabilities/midplatform/model_test_lens/static_site/index.html` |

路径与端口已写入 `static_site/canonical_entry_v1.json`，后续开发不随意改动。

### 长期保持 8765 在线（macOS，登录自启）

只需安装一次，以后开机自动可用，不必每次 `bash scripts/start_model_test_lens.sh`：

```bash
bash scripts/install_model_test_lens_service.sh
```

浏览器书签固定：**http://localhost:8765**

```bash
bash scripts/status_model_test_lens_service.sh   # 查看是否在跑
bash scripts/uninstall_model_test_lens_service.sh # 取消常驻
```

日志：`~/Library/Logs/LunaModelTestLens/`

需要时对我说「启动 Model Test Lens」，我会在后台执行一次性启动脚本（若已安装常驻服务则通常已在运行）。

## 与白盒板块（未来合并）

| 分区 | 职责 |
|------|------|
| **Model Test Lens**（本页） | 模型测试：单模型能力、metrics、envelope、candidate 可视化 |
| **白盒** | 产品测试：链路、决策、参数、运行态解释 |

未来合并为统一本地测试台；合并后 **http://localhost:8765** 仍作为模型测试分区入口。

## 与白盒页面的区别

| | 白盒页面 | Model Test Lens |
|---|---|---|
| 目的 | 系统决策、参数变化、链路流转 | 单模型能力边界、研发测试 |
| 受众 | 产品/运行态解释 | 模型评估、质量复核 |
| 执行 | 可看 runtime 相关解释 | **不执行模型、不承载 runtime** |
| 输出 | 产品参数可视化 | candidate output、metrics、TestBoard refs |

## 核心流程（规划）

```
导入测试内容 → 选择单个模型 → 读取 phase/runner 产物 → 可视化 → 对照 TestBoard
```

真正跑模型仍走 **phase / runner / verifier / TestBoard**；页面第一版**只读**本地产物。

## 目录

```
model_test_lens/
├── static_site/          # 本地静态页（skeleton + SLAM/MobileSAM 示例）
├── standards/            # MUEP V1 统一评估标准 + SLAM 专用标准
│   ├── muep/             # 三层 metric、评分公式、failure taxonomy
│   └── slam/             # ATE / drift / stability 规范
├── adapters/             # 模型输出 → 统一 envelope
│   └── slam/             # SLAM Evaluation Adapter V1 + ATE 计算器
├── schemas/              # 统一 envelope / manifest / trace / layer schema
├── model_panels/         # 按模型类型分面板
├── examples/             # 示例 envelope（MobileSAM、SLAM）
├── review_*.py           # 治理 review
└── model_test_lens_static_site_plan_v1.md
```

## MUEP V1（统一评估协议）

所有模型共用最小评估协议：

- **输入**：`model_type` + `input` + `task`
- **输出**：`prediction` + `metrics`（三层）+ `failure_modes` + `confidence`
- **评分**：`0.6*task + 0.25*robustness + 0.15*structural`

详见 `standards/muep/README.md`。

## SLAM Diagnostic Engine V1

```bash
python3 -m capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1 --slim
python3 -m capabilities.midplatform.model_test_lens.review_model_test_lens_muep_slam_v1_standard_and_adapter_v1
```

诊断层：Procrustes 对齐、error curve、drift heatmap、failure timeline、V2 评分（含 diagnostic_penalty）。

静态页 SLAM 示例含 4 个诊断 panel（curve / heatmap / timeline / trajectory）。

## SLAM Adapter V1

```bash
# 生成 SLAM 示例 envelope（含 ATE / drift 自动计算）
python3 -m capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1
python3 -m capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1 --slim

# 验证 MUEP + SLAM adapter
python3 -m capabilities.midplatform.model_test_lens.review_model_test_lens_muep_slam_v1_standard_and_adapter_v1
```

静态页点击 **Load SLAM example** 可查看轨迹叠加与 MUEP 分数。

## 运行规划 review

## 读取来源（V1）

- `_tmp_eval_out/`
- `capabilities/test_board/`
- `capabilities/test_assets/`
- `capabilities/midplatform/model_test_lens/schemas/`

## 禁止（V1）

- 外部 URL、live camera、实时麦克风
- runtime server、自动下载 dataset
- 页面内直接 inference
- registry 写入、semantic/fact/navigation

## 运行规划 review

```bash
python3 -m capabilities.midplatform.model_test_lens.review_model_test_lens_static_site_planning_v1
```

## 下一阶段

- 接入真实 ORB-SLAM / VINS / Kimera 输出到 `slam_evaluation_adapter_v1`
- TUM RGB-D / KITTI Benchmark Pack 数据登记
- Data Adapter：`_tmp_eval_out` 自动转统一 envelope
