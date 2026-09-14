# LUNA — PaddleOCR Pinned Partial Capability Boundary v0

## Phase

- **Phase-ModelOCR-003-Fix-004**
- **Purpose:** 将 **`weights_source=pinned_partial`**（det+rec 已固定，cls 未纳入）下的能力边界 **写死**，避免下游误用为全能力 OCR 或语义级输出。

## Scope prefix

本边界适用于：**PaddleOCR 权重已 pinned_partial**、且 manifest/readiness 标记为 **partial** 的阶段（含后续 004B skeleton，直至另行晋升）。

---

## Declared capabilities（明确声明为可用）

| 能力 | 声明 |
|------|------|
| 检测（det）权重 | **available**（已 pinned，见 `model_files_manifest_v0.json`） |
| 识别（rec）权重 | **available**（已 pinned） |
| 原文/raw text 管线（实现侧） | **仅允许**以 **raw text** 契约输出；见 OCR raw text 合同文档 |

---

## Explicit non-claims（明确不声明）

| 维度 | 声明 |
|------|------|
| 方向分类（cls） | **unavailable**（当前无 cls 权重目录） |
| `cls_available` | **false** |
| 旋转/倒置文本鲁棒性 | **not_claimed** |
| `orientation_support` | **false** |
| 朝向校正 / 自动转正 | **not_claimed** |
| `rotated_text_handling` | **not_claimed**（工程语义：**not_claimed**） |
| 语义理解、意图、结构化业务字段 | **禁止**（保持 raw-text-only 合同） |
| 导航、播报、执行 | **禁止**（与本 OCR 阶段边界一致） |

---

## Dependency boundary

- **权重与 manifest 成功**不隐含 **paddle/paddleocr/PIL** 已安装。
- 任何 **004B adapter**：须在依赖未满足时 **fail-closed**（不初始化、不伪造 ready），并单独记录 **dependency readiness**（不与 005 benchmark 混写）。

---

## First-phase raw text harness 允许假设

- 样本以 **正常朝向** 为主时，可使用 **det+rec** 进行原文抽取实验；记录中须保留 **`cls_available=false`** 与上表 non-claims。
- 若样本含大量旋转文本，须降低预期或先补 cls + 更新 manifest，再扩大声明范围。

---

## Version

- **v0** — 与 Phase-ModelOCR-003-Fix-004 收口一致；晋升 pinned_local 或补充 cls 后须修订版本或附录。
