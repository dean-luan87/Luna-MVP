# scene_classifier_v2.py

"""
场景分类器 V2（增强版）

输入：
- 三帧视觉
- OCR 文本
- YOLO 检测物体
- 运动模式（是否在乘车、乘电梯）
- 地图位置（可选）

输出场景类别：
- OutdoorStreet: 人行道、马路、街边
- MallIndoor: 商场、超市、便利店
- HospitalHall: 医院大厅、科室、挂号区
- SubwayStation: 地铁大厅、安检口、站台
- BusStation: 公交站、候车亭
- GovServiceHall: 政务大厅、服务窗口
"""

from typing import Optional, Dict, Any, List


class SceneClassifierV2:
    """
    场景分类器 V2：综合多模态信息判断场景类型
    """
    
    def __init__(self):
        # 场景关键词库
        self.scene_keywords = {
            "HospitalHall": [
                "医院", "挂号", "缴费", "候诊", "分诊", "科室",
                "Hospital", "Registration", "Pharmacy", "Department"
            ],
            "MallIndoor": [
                "商场", "超市", "便利店", "购物", "店铺",
                "Mall", "Store", "Shopping", "Floor"
            ],
            "SubwayStation": [
                "地铁", "站台", "安检", "换乘", "线路",
                "Subway", "Metro", "Platform", "Line", "Gate"
            ],
            "BusStation": [
                "公交", "站台", "候车", "Bus", "Platform", "Stop"
            ],
            "GovServiceHall": [
                "政务", "服务", "窗口", "办理", "Government", "Service", "Window"
            ],
            "OutdoorStreet": [
                "街道", "人行道", "路口", "Street", "Road", "Crosswalk"
            ]
        }
    
    def classify(
        self,
        ocr_text: str = "",
        yolo_objects: Optional[List[Dict]] = None,
        movement_mode: Optional[str] = None,
        map_location: Optional[str] = None
    ) -> str:
        """
        综合判断场景类型
        
        参数：
        - ocr_text: OCR 识别的文本
        - yolo_objects: YOLO 检测到的物体列表
        - movement_mode: 运动模式（"elevator", "escalator", "walking"等）
        - map_location: 地图位置信息（可选）
        
        返回：
        - 场景类型字符串
        """
        scores = {}
        
        # 1. OCR 关键词匹配
        ocr_text_lower = ocr_text.lower()
        for scene, keywords in self.scene_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in ocr_text_lower:
                    score += 1
            scores[scene] = scores.get(scene, 0) + score * 2  # OCR 权重较高
        
        # 2. YOLO 物体检测
        if yolo_objects:
            for obj in yolo_objects:
                obj_class = obj.get("class", "").lower()
                obj_label = obj.get("label", "").lower()
                
                # 医院相关物体
                if any(kw in obj_class or kw in obj_label for kw in ["hospital", "registration", "pharmacy"]):
                    scores["HospitalHall"] = scores.get("HospitalHall", 0) + 1
                
                # 商场相关物体
                if any(kw in obj_class or kw in obj_label for kw in ["mall", "store", "shopping"]):
                    scores["MallIndoor"] = scores.get("MallIndoor", 0) + 1
                
                # 地铁相关物体
                if any(kw in obj_class or kw in obj_label for kw in ["subway", "metro", "platform", "gate"]):
                    scores["SubwayStation"] = scores.get("SubwayStation", 0) + 1
        
        # 3. 运动模式推断
        if movement_mode:
            if movement_mode == "elevator":
                # 电梯中可能是医院/商场/办公楼
                scores["HospitalHall"] = scores.get("HospitalHall", 0) + 1
                scores["MallIndoor"] = scores.get("MallIndoor", 0) + 1
            elif movement_mode == "escalator":
                # 扶梯通常是商场/地铁
                scores["MallIndoor"] = scores.get("MallIndoor", 0) + 1
                scores["SubwayStation"] = scores.get("SubwayStation", 0) + 1
        
        # 4. 地图位置推断（如果有）
        if map_location:
            if "hospital" in map_location.lower():
                scores["HospitalHall"] = scores.get("HospitalHall", 0) + 3
            elif "mall" in map_location.lower():
                scores["MallIndoor"] = scores.get("MallIndoor", 0) + 3
        
        # 5. 选择得分最高的场景
        if scores:
            best_scene = max(scores.items(), key=lambda x: x[1])
            if best_scene[1] > 0:
                return best_scene[0]
        
        # 默认返回户外街道
        return "OutdoorStreet"










