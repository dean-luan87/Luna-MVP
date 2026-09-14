from core.yolo_detector import YoloDetector


def test_yolo_detector_infer_structure():
    detector = YoloDetector({"model_name": "yolov8n"})
    detector.load_model()

    fake_frame = {"timestamp": 0, "data": None}
    results = detector.infer(fake_frame)

    # 修复断言：infer 返回的是字典，不是列表
    assert isinstance(results, dict)
    assert "objects" in results or "detections" in results
    detections = results.get("objects") or results.get("detections")
    assert isinstance(detections, list)
    if detections:
        r0 = detections[0]
        assert "class" in r0
        assert "bbox" in r0
        assert "confidence" in r0








