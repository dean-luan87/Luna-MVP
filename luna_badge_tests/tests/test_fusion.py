from core.fusion_engine import FusionEngine


def test_fusion_engine_basic():
    fusion = FusionEngine(window_size=3)
    result1 = {"detections": [{"class": "obstacle"}], "depth_map": None, "meta": {}}
    result2 = {"detections": [{"class": "person"}], "depth_map": None, "meta": {}}

    fusion.add_result(result1)
    fusion.add_result(result2)

    fused = fusion.get_fused_result()
    
    # 兼容新老字段：
    # - 老版本：result["detections"]
    # - 新版本：result["objects"]
    assert isinstance(fused, dict)
    detections = fused.get("detections") or fused.get("objects")
    assert isinstance(detections, list)








