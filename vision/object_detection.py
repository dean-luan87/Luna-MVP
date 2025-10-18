import cv2
import numpy as np
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # 加载YOLOv8模型
        self.model = YOLO(model_path)

    def detect_objects(self, frame):
        """
        输入一帧图像，返回检测结果
        """
        results = self.model(frame)
        
        output = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    output.append({
                        'label': self.model.names[class_id],
                        'confidence': confidence,
                        'box': [int(x1), int(y1), int(x2), int(y2)]
                    })
        return output

    def draw_boxes(self, frame, detections):
        """
        将检测结果画在图像上
        """
        for det in detections:
            x1, y1, x2, y2 = det['box']
            label = det['label']
            confidence = det['confidence']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame