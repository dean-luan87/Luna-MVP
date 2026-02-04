class VisualNodeDetector:
    """
    YOLO + OCR → NodeCandidate
    NodeCandidate: {bbox, type, text, confidence}
    """
    def __init__(self, yolo_model=None, ocr_engine=None):
        self.yolo = yolo_model
        self.ocr = ocr_engine

    def detect(self, frame):
        # TODO: integrate YOLO + OCR
        return []

