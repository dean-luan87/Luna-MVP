"""
场景描述引擎（Scene Description Engine）
提供主动和被动场景描述能力
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SceneDescriptionEngine:
    """
    场景描述引擎
    输入摄像头帧 → 返回可读场景描述
    """

    def __init__(self, yolo_parser=None, env_detector=None):
        """
        初始化场景描述引擎
        
        Args:
            yolo_parser: YOLO目标检测器（可选）
            env_detector: 环境检测器（可选）
        """
        self.yolo = yolo_parser
        self.env = env_detector

    def describe(self, frame, vision_result: Optional[Dict] = None) -> Dict[str, Any]:
        """
        输入摄像头帧 → 返回可读场景描述
        
        Args:
            frame: 图像帧（numpy array或PIL Image）
            vision_result: 视觉识别结果（可选，如果已调用过视觉模块）
        
        Returns:
            场景描述字典
        """
        try:
            # 1. 获取物体检测结果
            objects = []
            if vision_result:
                objects = self._parse_vision_result(vision_result)
            elif self.yolo:
                # 如果提供了yolo_parser，使用它
                objects = self.yolo.parse(frame) if hasattr(self.yolo, 'parse') else []
            else:
                # 从vision_result中提取
                objects = vision_result.get("detections", []) if vision_result else []

            # 2. 获取环境信息
            env = {}
            if vision_result:
                env = self._parse_environment(vision_result)
            elif self.env:
                env = self.env.analyze(frame) if hasattr(self.env, 'analyze') else {}
            else:
                env = self._default_environment()

            # 3. 场景分类
            scene = self._classify_scene(objects, env)

            # 4. 生成自然语言描述
            text = self._build_description(scene, objects, env)

            # 5. 提取危险信息
            hazards = self._extract_hazards(env, objects)

            return {
                "scene": scene,
                "summary": text,
                "objects": objects,
                "environment": env,
                "hazards": hazards,
                "raw": {
                    "detections": objects,
                    "environment": env
                }
            }
        except Exception as e:
            logger.error(f"[SceneDescriptionEngine] describe error: {e}", exc_info=True)
            return {
                "scene": "unknown",
                "summary": "场景识别失败，请稍后重试。",
                "objects": [],
                "environment": {},
                "hazards": [],
                "raw": {}
            }

    def query(self, question: str, frame=None, vision_result: Optional[Dict] = None) -> Dict[str, Any]:
        """
        问答式场景理解
        
        Args:
            question: 用户问题
            frame: 图像帧（可选）
            vision_result: 视觉识别结果（可选）
        
        Returns:
            回答字典
        """
        try:
            # 先获取场景描述
            description = self.describe(frame, vision_result)
            objects = description.get("objects", [])
            env = description.get("environment", {})
            scene = description.get("scene", "unknown")

            # 解析问题
            question_lower = question.lower().strip()

            # 问题匹配和回答生成
            answer = self._answer_question(question_lower, objects, env, scene)

            return {
                "answer": answer,
                "meta": {
                    "object_count": len(objects),
                    "scene": scene,
                    "hazard": "high" if description.get("hazards") else "none"
                }
            }
        except Exception as e:
            logger.error(f"[SceneDescriptionEngine] query error: {e}", exc_info=True)
            return {
                "answer": "抱歉，我暂时无法理解这个问题。",
                "meta": {}
            }

    def _parse_vision_result(self, vision_result: Dict) -> List[Dict]:
        """从视觉识别结果中解析物体"""
        objects = []
        
        # 从detections中提取
        detections = vision_result.get("detections", [])
        for det in detections:
            obj = {
                "label": det.get("class", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bbox": det.get("bbox", []),
            }
            
            # 估算距离（如果有）
            if "distance" in det:
                obj["distance"] = det["distance"]
            
            # 估算位置（根据bbox中心点）
            if "bbox" in det and len(det["bbox"]) >= 4:
                bbox = det["bbox"]
                center_x = (bbox[0] + bbox[2]) / 2
                img_width = 640  # 假设图像宽度
                if center_x < img_width * 0.33:
                    obj["position"] = "left"
                elif center_x > img_width * 0.67:
                    obj["position"] = "right"
                else:
                    obj["position"] = "front"
            
            objects.append(obj)
        
        return objects

    def _parse_environment(self, vision_result: Dict) -> Dict:
        """从视觉识别结果中解析环境信息"""
        env = {}
        
        # 从guidance结果中提取环境信息
        guidance = vision_result.get("guidance", {})
        if guidance:
            # 弱光检测
            if guidance.get("low_light"):
                env["light"] = "dark"
            elif guidance.get("brightness", 0) > 0.7:
                env["light"] = "bright"
            else:
                env["light"] = "normal"
            
            # 反射检测
            if guidance.get("reflective_surface"):
                env["reflection"] = "high"
            else:
                env["reflection"] = "low"
            
            # 暗区检测
            if guidance.get("dark_zone_ahead"):
                env["dark_zone"] = True
        else:
            env = self._default_environment()
        
        return env

    def _default_environment(self) -> Dict:
        """默认环境信息"""
        return {
            "light": "normal",
            "reflection": "low",
            "dark_zone": False,
            "crowd": "low"
        }

    def _classify_scene(self, objects: List[Dict], env: Dict) -> str:
        """场景分类"""
        object_labels = [obj.get("label", "").lower() for obj in objects]
        
        # 室内场景
        if any(label in ["escalator", "elevator", "cashier", "counter"] for label in object_labels):
            return "indoor_mall"
        
        if any(label in ["platform", "gate", "ticket"] for label in object_labels):
            return "subway"
        
        if any(label in ["hospital", "registration", "window"] for label in object_labels):
            return "hospital"
        
        # 根据光照判断
        if env.get("light") == "dark":
            return "dark_indoor"
        
        if env.get("light") == "bright":
            return "bright_indoor"
        
        return "unknown"

    def _build_description(self, scene: str, objects: List[Dict], env: Dict) -> str:
        """生成自然语言描述"""
        parts = []
        
        # 1. 场景类型
        scene_names = {
            "indoor_mall": "购物中心",
            "subway": "地铁站",
            "hospital": "医院",
            "dark_indoor": "室内暗光环境",
            "bright_indoor": "室内明亮环境",
            "unknown": "当前环境"
        }
        scene_name = scene_names.get(scene, "当前环境")
        
        # 2. 光照描述
        light_desc = ""
        if env.get("light") == "dark":
            light_desc = "光线较暗"
        elif env.get("light") == "bright":
            light_desc = "光线明亮"
        else:
            light_desc = "光线正常"
        
        parts.append(f"你现在位于{scene_name}，{light_desc}。")
        
        # 3. 物体描述
        obj_desc = self._describe_objects(objects)
        if obj_desc:
            parts.append(obj_desc)
        
        # 4. 危险环境描述
        hazard_desc = self._describe_hazards(env)
        if hazard_desc:
            parts.append(hazard_desc)
        
        return "".join(parts)

    def _describe_objects(self, objects: List[Dict]) -> str:
        """描述物体"""
        if not objects:
            return ""
        
        descs = []
        for obj in objects[:5]:  # 最多描述5个物体
            label = obj.get("label", "物体")
            distance = obj.get("distance")
            position = obj.get("position", "前方")
            
            # 位置翻译
            pos_map = {
                "left": "左侧",
                "right": "右侧",
                "front": "前方",
                "back": "后方"
            }
            pos_cn = pos_map.get(position, "前方")
            
            if distance:
                descs.append(f"{pos_cn}约{distance:.1f}米处有{label}")
            else:
                descs.append(f"{pos_cn}有{label}")
        
        return "。".join(descs) + "。" if descs else ""

    def _describe_hazards(self, env: Dict) -> str:
        """描述危险环境"""
        hazards = []
        
        if env.get("reflection") == "high":
            hazards.append("地面反光较强，请注意脚下")
        
        if env.get("dark_zone"):
            hazards.append("前方有光线突变区域")
        
        return "，".join(hazards) if hazards else ""

    def _extract_hazards(self, env: Dict, objects: List[Dict]) -> List[Dict]:
        """提取危险信息"""
        hazards = []
        
        if env.get("reflection") == "high":
            hazards.append({
                "type": "reflection",
                "severity": "medium",
                "note": "地面反光较强"
            })
        
        if env.get("dark_zone"):
            hazards.append({
                "type": "dark_zone",
                "severity": "high",
                "note": "前方有光线突变区域"
            })
        
        return hazards

    def _answer_question(self, question: str, objects: List[Dict], env: Dict, scene: str) -> str:
        """回答用户问题"""
        question_lower = question.lower()
        
        # 问题：有没有人？
        if "人" in question or "person" in question_lower or "people" in question_lower:
            persons = [obj for obj in objects if "person" in obj.get("label", "").lower() or "人" in obj.get("label", "")]
            if persons:
                p = persons[0]
                distance = p.get("distance", 0)
                position = p.get("position", "前方")
                pos_map = {"left": "左", "right": "右", "front": "前", "back": "后"}
                pos_cn = pos_map.get(position, "前")
                if distance:
                    return f"有，一位行人正在你{pos_cn}方约{distance:.1f}米处。"
                else:
                    return f"有，一位行人正在你{pos_cn}方。"
            else:
                return "目前没有检测到行人。"
        
        # 问题：有没有楼梯？
        if "楼梯" in question or "stair" in question_lower or "step" in question_lower:
            stairs = [obj for obj in objects if "stair" in obj.get("label", "").lower() or "楼梯" in obj.get("label", "")]
            if stairs:
                s = stairs[0]
                distance = s.get("distance", 0)
                position = s.get("position", "前方")
                pos_map = {"left": "左侧", "right": "右侧", "front": "前方", "back": "后方"}
                pos_cn = pos_map.get(position, "前方")
                if distance:
                    return f"有，{pos_cn}约{distance:.1f}米处有一段楼梯。"
                else:
                    return f"有，{pos_cn}有一段楼梯。"
            else:
                return "目前没有检测到楼梯。"
        
        # 问题：现在是什么场景？
        if "场景" in question or "地方" in question or "scene" in question_lower:
            scene_names = {
                "indoor_mall": "购物中心",
                "subway": "地铁站",
                "hospital": "医院",
                "dark_indoor": "室内暗光环境",
                "bright_indoor": "室内明亮环境",
                "unknown": "未知环境"
            }
            return f"你现在位于{scene_names.get(scene, '未知环境')}。"
        
        # 问题：室内还是室外？
        if "室内" in question or "室外" in question or "indoor" in question_lower or "outdoor" in question_lower:
            if scene in ["indoor_mall", "subway", "hospital", "dark_indoor", "bright_indoor"]:
                return "你现在在室内。"
            else:
                return "根据当前识别结果，可能是在室外。"
        
        # 问题：光线怎么样？
        if "光线" in question or "light" in question_lower:
            light = env.get("light", "normal")
            if light == "dark":
                return "当前光线较暗，请注意脚下。"
            elif light == "bright":
                return "当前光线明亮。"
            else:
                return "当前光线正常。"
        
        # 问题：有没有障碍物？
        if "障碍" in question or "obstacle" in question_lower:
            obstacles = [obj for obj in objects if obj.get("label", "") not in ["person", "人"]]
            if obstacles:
                return f"检测到{len(obstacles)}个物体，请注意避让。"
            else:
                return "目前没有检测到明显的障碍物。"
        
        # 问题：最近的门在哪里？
        if "门" in question or "door" in question_lower:
            doors = [obj for obj in objects if "door" in obj.get("label", "").lower() or "门" in obj.get("label", "")]
            if doors:
                d = doors[0]
                distance = d.get("distance", 0)
                position = d.get("position", "前方")
                pos_map = {"left": "左侧", "right": "右侧", "front": "前方", "back": "后方"}
                pos_cn = pos_map.get(position, "前方")
                if distance:
                    return f"{pos_cn}约{distance:.1f}米处有一扇门。"
                else:
                    return f"{pos_cn}有一扇门。"
            else:
                return "目前没有检测到门。"
        
        # 默认回答
        return "抱歉，我暂时无法理解这个问题。你可以问我'现在看到什么'、'有没有人'、'有没有楼梯'等问题。"



