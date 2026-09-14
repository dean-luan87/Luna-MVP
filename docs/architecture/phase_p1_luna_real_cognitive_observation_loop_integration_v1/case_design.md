# Case Design

## Case A — REAL_SINGLE_CYCLE_SUFFICIENT

Goal：观察公共交通场景中的 location text candidate。

Information Need：`information:station-location-text:v1`。

第一轮绑定既有真实输入：
`capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png`。

如果真实 RapidOCR 产生非空 native text candidates，该绑定提供所声明的
station-location information，Cognitive State 应为 `SUFFICIENT` 并由 canonical
Stop authority 结束；如果真实结果为空，必须保留 `EMPTY_SUCCESS` 语义并由
Verifier 失败该正向认知 Case，不能伪造文字或 sufficiency。

## Case B — REAL_REOBSERVATION_REQUIRED

Goal：在一个受限的公共交通文字观察集合中取得 station 与 platform 两类
location text candidates。

Required information：

- `information:station-location-text:v1`
- `information:platform-location-text:v1`

Cycle 1 绑定车站图片，只能在真实 native result 非空时提供 station requirement。
Cycle 1 不足时，canonical Gap 的 missing refs 应具体指出 platform requirement。
Cycle 2 的平台图片绑定只有在该 missing ref 与第二个 binding 相交时才会被请求。

案例定义只保存真实 source path、region binding 和 information refs；不保存 OCR
文字，不把 fixture 当作 Provider result，也不以 cycle 或 case 名称直接决定
sufficiency。
