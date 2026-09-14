# Luna Observation Lens — Static Site

默认界面为 **Luna 观察镜**（Luna Observation Lens），用户可见文案以中文为主；英文原始字段仅出现在开发者数据中。

### HUD 视觉策略 V1（默认）

- **默认关闭**整图半透明蒙版；原图保持清晰
- **默认显示**：语义色线框、中文标签、置信度、不确定提示
- **可选开启**：「显示区域填充」+ 透明度（仅影响局部填充）
- **颜色语义**：绿=任务相关 · 红=风险 · 黄=需复核 · 蓝=环境结构 · 紫=文字/OCR · 灰=弱相关
- **右侧观察面板**：事实 → 目标判断 → 风险 → 建议；推理过程默认折叠

### HUD 可读性与外部标注 V1（默认）

- **HiDPI Canvas**：按 `devicePixelRatio` 放大内部像素，线框与文字在 Retina 屏上保持清晰
- **图内极简化**：仅显示 `编号 + 短标签 + 置信度`（如 `① 前方车辆 70%`）
- **图外识别对象列表**：中央 HUD 下方展示每个对象的置信度、状态、说明与建议补测
- **右侧 Luna 观察面板**：只回答整体任务 / 总体观察 / 主要风险 / 下一步建议（对象细节在图外列表）
- **联动**：点击列表条目高亮图中线框；支持筛选（全部 / 任务相关 / 风险 / 不确定）

### 一屏观察台布局 V1（默认）

- **主画面优先**：中央 HUD 占最大面积；页面主体无长滚动
- **左侧能力抽屉**：默认窄栏（当前能力 + 状态），点击展开完整列表
- **顶部紧凑工具栏**：主操作单行显示；导入/高级/开发者/记录收入「更多」
- **对象胶囊条**：图下横向 chip（`① 路牌 · 80% · OCR`）；详情按需展开
- **右侧结论化**：任务 / 观察 / 风险 / 建议；选中对象显示简要详情
- **底部抽屉**：指标 / 对象 / 高级 / 开发者 / 白盒 / 记录 — 默认全部折叠；仅点击 tab 后以 **fixed overlay** 展开

### 左侧触发器与底部 Drawer 清理 V1

- **九宫格按钮**：左侧顶部 36×36 能力抽屉开关（非输入框 / 非 ☰ / 非 ✕）
- **收起态**：九宫格 + 纵向能力快捷入口（分割 / 检测 / OCR / SLAM …）
- **底部默认**：仅摘要栏 + tab（约 64–88px），**不出现空白 drawer 区域**
- **展开 drawer**：fixed overlay，有关闭按钮；空状态不超过 120px

### Human Correction Layer V1（人工指错层）

- **对象胶囊**：hover 显示「指错」按钮
- **HUD 选中对象**：详情区「标记问题」；画布点击选中对象
- **漏识别**：HUD 工具栏「标记漏识别」— 点选或框选区域
- **右侧观察面板**：各区块「指出问题」
- **底部 Drawer**：新增「纠错」tab（默认折叠）— 列表 / 筛选 / 导出 JSON
- **边界**：仅生成 correction candidate；不写 fact；不改 envelope；不自动训练

## Luna Observation Lens V1 Closure（已收口）

V1 已正式 Closure，UI 主体冻结。标准与路线见：

- `closure/luna_observation_lens_v1_closure_report.md`
- `standards/ui/luna_observation_lens_v1_template_standard.md`
- `closure/luna_observation_lens_v1_followup_routes.json`

后续模型接入（P0：Detection / OCR）在 V1 壳内扩展，不再大改布局。

---

## 固定本地入口（永久不变）

以后所有模型测试都用这个页面，路径和端口已冻结：

| 项 | 固定值 |
|----|--------|
| **推荐 URL** | **http://localhost:8765** |
| **HTML 文件** | `capabilities/midplatform/model_test_lens/static_site/index.html` |
| **端口** | `8765`（勿改） |
| **配置锚点** | `canonical_entry_v1.json`（本目录） |

### 启动（在项目根目录 `Luna-Workspace-Min` 执行）

**方式 A — 常驻服务（推荐，安装一次即可）**

```bash
bash scripts/install_model_test_lens_service.sh
```

登录后自动保持 **http://localhost:8765** 可用；无需每次手动启动。

**方式 B — 一次性启动（临时调试）**

```bash
bash scripts/start_model_test_lens.sh
```

浏览器打开：**http://localhost:8765**（端口冻结，勿改）

### 方式二：直接双击 / 打开 HTML 文件

```
capabilities/midplatform/model_test_lens/static_site/index.html
```

无需服务即可用内置示例；推荐仍用 `localhost:8765` 以便后续加载相对路径资源。

---

## 运行方式（详细）

### 方式一：直接打开 HTML

在浏览器中打开（与上表相同，勿记别的路径）：

```
capabilities/midplatform/model_test_lens/static_site/index.html
```

点击 **Load MobileSAM example** 或 **Load SLAM example** 加载内置示例（无需网络）。

也可通过 **Load local JSON envelope** 选择本地 `.json` 文件。

### 方式二：本地静态服务（推荐）

在项目根目录执行：

```bash
bash capabilities/midplatform/model_test_lens/static_site/serve.sh
```

或：

```bash
bash capabilities/midplatform/model_test_lens/static_site/serve.sh
```

浏览器访问：**http://localhost:8765**（固定，勿改端口）

### 本地 Runner Bridge（8787）

Model Test Lens 页面可通过 **127.0.0.1:8787** 提交测试 job（页面本身不执行模型）。

启动本地 Runner Bridge（手动，非 daemon）：

```bash
bash scripts/start_local_runner_bridge.sh
```

或：

```bash
python3 -m capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_server_v1 --host 127.0.0.1 --port 8787
```

- UI：`http://localhost:8765`
- API：`http://127.0.0.1:8787`
- 第一版 runner：`segmentation_mobile_sam`（图片）、`slam_video_limited`（占位，不跑真实 ORB-SLAM）

## Luna Observation Lens 布局（默认）

单屏仪表盘，不再使用纵向 5 屏报告流：

| 区域 | 内容 |
|------|------|
| 顶部任务栏 | 选择文件、开始观察、原图/对比/HUD 切换、高级/开发者 |
| 左侧能力栏 | 输入摘要、能力卡片（可测试/实验中/未接入）、示例入口 |
| 中央主画面 | 默认机器人视角 HUD；可切换原图、普通对比 |
| 右侧解释面板 | 当前任务、我看到了什么、不确定、可能漏掉、建议补测 |
| 底部摘要 + Drawer | 一行指标摘要；折叠：指标详情 / 高级流程 / 开发者数据 / 白盒 / 测试记录 |

模块：`luna_observation_compact_ui_v1.js`、`luna_observation_layout_v1.js`、`luna_observation_drawers_v1.js`

## Simple Mode（合并进观察台）

| 操作 | 说明 |
|------|------|
| 选择文件 | 顶栏或左侧；图片/视频（`test_assets` 内已知文件可自动定位路径） |
| 能力选择 | 左侧能力卡片（分割可测试、SLAM 实验中） |
| 开始观察 | 顶栏按钮；自动经 8787 完成本地测试 |
| 高级流程 | 底部 Drawer「高级流程」→ Manifest / Job / Runner Bridge |
| 开发者 | 底部 Drawer「开发者 JSON」或顶栏「开发者」 |

## 本地测试资产导入（UI Patch v1）

主内容区下方新增 **本地测试资产导入**：

1. 选择资产类型（image / video / frame_sequence / audio / text）与本地文件
2. **生成 Manifest** — 仅浏览器内 JSON preview，不上传、不跑模型
3. **创建 Test Job Request** / **Runner Bridge Request** — candidate-only
4. **Runner 输出状态占位** — `waiting_for_runner_output`，完成后用页头导入 envelope

专用脚本：`local_asset_import_ui_v1.js`、`runner_bridge_ui_v1.js`、`local_asset_import_examples_v1.js`

开发者模式下可查看 manifest / job / runner bridge 原始 JSON。

## 功能

- 10 类模型 panel 导航（Segmentation / SLAM 有内置示例，其余为 placeholder）
- 本地 JSON 文件导入
- **本地资产登记 + manifest / job / runner bridge 生成（不执行模型）**
- 内置 MobileSAM multi-image segmentation 示例 envelope
- 内置 SLAM ORB street scene 示例（MUEP + 轨迹可视化）
- Metrics / failure modes / boundary / readiness（只读）/ TestBoard refs

## 明确禁止

- 模型 inference 按钮或 API 调用
- runtime / output adapter
- registry 写入
- 外部 URL fetch
- camera / microphone
- 删除 TestBoard 或 eval artifact

## 相关文件

- 示例 envelope：`../examples/mobile_sam_multi_real_image_envelope_example_v1.json`
- Schema：`../schemas/model_test_result_envelope_schema_v1.json`
- 配置：`example_loader_config_v1.json`

## 治理说明

所有展示内容为 **candidate-only**。`readiness_effect` 仅反映 artifact 中的值，页面不会升级 registry 或写入 fact。
