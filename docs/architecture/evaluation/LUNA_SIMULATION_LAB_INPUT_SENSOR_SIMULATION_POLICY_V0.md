# Luna Simulation Lab — Input & Sensor Simulation Policy v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**定位**：**Sensor/Input Simulation** 层：在无完整物理传感器时，用 **文件、序列流与 mock 状态** 驱动 OCR / Vision / Voice / Map 与 STCM 输入面。

---

## 1. 输入源类型（与 profile `input_sources` 对齐）

| 类型 | 示例 | 用途 |
|------|------|------|
| 摄像头替代 | 视频文件、图片序列、mock frame stream | Vision、OCR 帧率与缓冲 |
| OCR | ROI 图、海报/标签 manifest（labeled set） | 质量与 batch recovery |
| 语音 | WAV、ASR 文本 mock | Voice pipeline 与 notice |
| 位置/地图 | GPS trace、map node trace | 导航相关 deadline |
| 视觉锚点 | visual anchor trace | STCM 空间重验证 |
| 传感器状态 mock | battery、thermal、network、memory 标志 | 降级与 interrupt |

---

## 2. 与 Test Board 的结合

标准输入包应 **版本化**（manifest + checksum + 许可证说明），并在 `simulation_summary.json` 中记录 **输入包 id**，以便 **跨 profile 复验**。

---

## 3. 限制声明

模拟帧 **不能** 完全替代 **镜头畸变、滚动快门、真实曝光路径**；结论限于 **算法与管线在受控输入下** 的行为。

**不等同真实硬件；真实硬件验证仍为后置必须环节。**
