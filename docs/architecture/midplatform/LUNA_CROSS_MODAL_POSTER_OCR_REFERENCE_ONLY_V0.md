# CrossModal Poster OCR ReferenceOnly v0

**Phase**：`Phase-CrossModal-Poster-OCR-ReferenceOnly-001`  
**定位**：将 **Poster text OCR plan** 与 **VisualSymbolEvidence** **并列** 为 reference-only 索引；**不是 fusion**。

**严禁**：运行 OCR；解码 QR；确认品牌；语义融合；写事实层 / Scene Delta / WorldModel；自动批准；改 runtime routing。

**Simulation Lab**：仅只读附着 `developer_full` 的 `simulation_summary.json`；**不** 触发模型。

**后续**：Track B 四阶段 closure 见 [LUNA_POSTER_TESTBOARD_TRACK_B_CLOSURE_V0.md](./LUNA_POSTER_TESTBOARD_TRACK_B_CLOSURE_V0.md)（`Phase-Poster-TestBoard-Closure-001`）。

**Real OCR reference 更新**（plan + real OCR + visual 并列）：见 [LUNA_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md](./LUNA_POSTER_REAL_OCR_REFERENCE_UPDATE_V0.md)（`Phase-Poster-Real-OCR-Reference-Update-001`）。
