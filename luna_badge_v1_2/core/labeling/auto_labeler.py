# auto_labeler.py


class AutoLabeler:
    """
    自动标签器
    
    融合 YOLO + OCR + 场景分类 → 推理标签
    
    优先级：OCR > YOLO > 场景分类
    """
    
    KEYWORDS = {
        "厕所": "Toilet",
        "洗手间": "Toilet",
        "卫生间": "Toilet",
        "电梯": "Elevator",
        "Entrance": "Entrance",
        "Exit": "Exit",
        "出口": "Exit",
        "挂号": "Registration",
        "缴费": "Payment",
        "收费": "Payment",
        "扶梯": "Escalator",
        "楼梯": "Stair",
        "地铁": "Subway",
        "站台": "Platform",
        "咨询台": "Information",
        "服务台": "Information",
        "候诊": "Waiting",
        "分诊": "Triage",
    }
    
    def __init__(self, scene_classifier=None):
        self.scene_classifier = scene_classifier
    
    def label(self, yolo_results=None, ocr_text="", image=None):
        """
        自动标签推理
        
        输入：
        - yolo_results: YOLO检测结果列表，每个元素为 {"class": str, "confidence": float, "label": str}
        - ocr_text: OCR识别的文本
        - image: 图像帧（可选，用于场景分类）
        
        输出：
        - label: 标签字符串，如果无法识别则返回 None
        """
        # 1. OCR 优先（最高优先级）
        if ocr_text:
            ocr_text_lower = ocr_text.lower()
            for word, label in self.KEYWORDS.items():
                if word.lower() in ocr_text_lower or word in ocr_text:
                    return label
        
        # 2. YOLO 检测（中等优先级）
        if yolo_results:
            for obj in yolo_results:
                if isinstance(obj, dict):
                    confidence = obj.get("confidence", 0.0)
                    if confidence > 0.5:
                        # 检查是否是已知的结构性节点
                        obj_class = obj.get("class", "").lower()
                        obj_label = obj.get("label", "")
                        
                        # 映射 YOLO 类别到标签
                        if "elevator" in obj_class or "电梯" in obj_label:
                            return "Elevator"
                        elif "stair" in obj_class or "楼梯" in obj_label:
                            return "Stair"
                        elif "toilet" in obj_class or "厕所" in obj_label:
                            return "Toilet"
                        elif "escalator" in obj_class or "扶梯" in obj_label:
                            return "Escalator"
                        elif "entrance" in obj_class or "入口" in obj_label:
                            return "Entrance"
                        elif "exit" in obj_class or "出口" in obj_label:
                            return "Exit"
        
        # 3. 场景推断（最低优先级）
        if self.scene_classifier and image is not None:
            scene = self.scene_classifier.classify(image)
            if scene == "subway":
                return "SubwayArea"
            elif scene == "hospital":
                return "HospitalHall"
            elif scene == "indoor_mall":
                return "MallArea"
            elif scene == "bus_station":
                return "BusStation"
        
        return None
    
    def label_with_confidence(self, yolo_results=None, ocr_text="", image=None):
        """
        带置信度的标签推理
        
        返回：
        - {"label": str, "confidence": float, "source": str} 或 None
        """
        # OCR 优先
        if ocr_text:
            ocr_text_lower = ocr_text.lower()
            for word, label in self.KEYWORDS.items():
                if word.lower() in ocr_text_lower or word in ocr_text:
                    return {
                        "label": label,
                        "confidence": 0.9,  # OCR 置信度较高
                        "source": "OCR"
                    }
        
        # YOLO 检测
        if yolo_results:
            best_obj = None
            best_conf = 0.0
            for obj in yolo_results:
                if isinstance(obj, dict):
                    confidence = obj.get("confidence", 0.0)
                    if confidence > 0.5 and confidence > best_conf:
                        best_conf = confidence
                        best_obj = obj
            
            if best_obj:
                obj_class = best_obj.get("class", "").lower()
                obj_label = best_obj.get("label", "")
                
                # 映射到标签
                label = None
                if "elevator" in obj_class or "电梯" in obj_label:
                    label = "Elevator"
                elif "stair" in obj_class or "楼梯" in obj_label:
                    label = "Stair"
                elif "toilet" in obj_class or "厕所" in obj_label:
                    label = "Toilet"
                elif "escalator" in obj_class or "扶梯" in obj_label:
                    label = "Escalator"
                elif "entrance" in obj_class or "入口" in obj_label:
                    label = "Entrance"
                elif "exit" in obj_class or "出口" in obj_label:
                    label = "Exit"
                
                if label:
                    return {
                        "label": label,
                        "confidence": best_conf,
                        "source": "YOLO"
                    }
        
        # 场景推断
        if self.scene_classifier and image is not None:
            scene = self.scene_classifier.classify(image)
            scene_labels = {
                "subway": "SubwayArea",
                "hospital": "HospitalHall",
                "indoor_mall": "MallArea",
                "bus_station": "BusStation"
            }
            if scene in scene_labels:
                return {
                    "label": scene_labels[scene],
                    "confidence": 0.6,  # 场景推断置信度较低
                    "source": "Scene"
                }
        
        return None

























