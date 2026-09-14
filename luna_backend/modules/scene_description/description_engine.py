# modules/scene_description/description_engine.py
# 场景描述引擎（SceneDescriptionEngine）
# 输入：视觉检测结果（物体、文字、危险、设施、人群等）
# 输出：结构化场景描述 + 自然语言描述 + 简单解释

from typing import List, Dict, Any, Optional
import math
import logging

logger = logging.getLogger(__name__)


class SceneDescriptionEngine:
    """
    场景描述引擎：
    - describe() 用来生成一段"当前环境描述"
    - explain() 用来给出"为什么这么判断"的解释（面向后续 Luna 问答）
    """

    def __init__(self):
        # 预留一些阈值和配置，将来可以从 config 加载
        self.near_distance = 1.0     # 1m 内算"很近"
        self.mid_distance = 3.0      # 3m 内算"前方"
        self.crowd_threshold = 5     # 5 人以上算人多
        self.reflection_threshold = 0.7  # 反光强度阈值（0~1 假定）
        self.dark_threshold = 0.3        # 亮度阈值（0~1 假定）

    # -----------------------------
    # 核心入口：生成场景描述
    # -----------------------------
    def describe(
        self,
        objects: List[Dict[str, Any]],
        texts: List[Dict[str, Any]] = None,
        hazards: List[Dict[str, Any]] = None,
        facilities: List[Dict[str, Any]] = None,
        crowd_density: Optional[Dict[str, Any]] = None,
        env_features: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        参数均为"结构化检测结果"，建议由 /api/navigation/describe_scene 路由做预处理后传入

        objects: [
          { "label": "person", "class": "person", "bbox": (x1,y1,x2,y2), "distance":1.2, "position":"leftFront" }
        ]
        texts:   OCR 结果列表（用来辅助场景判断，如"出口""电梯"等）
        hazards: 危险检测结果列表
        facilities: 公共设施检测结果列表（如厕所、楼梯、电梯、公交站）
        crowd_density: 人群密度分析结果
        env_features: 额外环境特征，如 {"brightness":0.6,"reflection":0.2}
        """
        texts = texts or []
        hazards = hazards or []
        facilities = facilities or []
        env_features = env_features or {}

        # 1. 推断环境标签
        scene_type = self._infer_scene_type(objects, texts, facilities)
        light_info = self._infer_light(env_features)
        crowd_info = self._infer_crowd(objects, crowd_density)
        hazard_info = self._summarize_hazards(hazards)
        important_objs = self._pick_key_objects(objects, facilities)

        # 2. 生成自然语言描述
        summary = self._build_summary(
            scene_type=scene_type,
            light_info=light_info,
            crowd_info=crowd_info,
            important_objs=important_objs,
            hazard_info=hazard_info,
        )

        # 3. 生成简要解释（留给"为什么这么判断"用）
        explanation = self._build_explanation(
            scene_type=scene_type,
            light_info=light_info,
            crowd_info=crowd_info,
            hazard_info=hazard_info,
            objects=objects,
            facilities=facilities,
            texts=texts,
        )

        return {
            "scene_type": scene_type,          # 场景类型：mall / subway / hospital / street / indoor / outdoor / unknown
            "summary": summary,                # 对用户说的话
            "environment": {
                "light": light_info.get("level"),
                "light_detail": light_info,
                "crowd": crowd_info.get("level"),
                "crowd_detail": crowd_info,
            },
            "objects": important_objs,         # 挑过一遍后的关键物体列表
            "hazards": hazard_info.get("hazards") or [],
            "explanation": explanation,        # 解释用文本（可不播报，只用来 debug 或问答）
        }

    # -----------------------------
    # 场景推断相关
    # -----------------------------
    def _infer_scene_type(
        self,
        objects: List[Dict[str, Any]],
        texts: List[Dict[str, Any]],
        facilities: List[Dict[str, Any]],
    ) -> str:
        labels = {obj.get("class") or obj.get("label") for obj in objects if obj}
        text_all = " ".join([t.get("text", "") for t in texts]) if texts else ""
        facility_types = {f.get("type") for f in facilities if f}

        text_all_lower = text_all.lower()

        # 简单规则，可后续改成模型或更复杂规则
        if "地铁" in text_all or "metro" in text_all_lower:
            return "subway"
        if "医院" in text_all or "门诊" in text_all or "clinic" in text_all_lower:
            return "hospital"
        if "出口" in text_all or "exit" in text_all_lower:
            # 出口可以是地铁 / 商场 / 公共建筑，不单独定类
            pass
        if {"escalator", "elevator"} & labels or "商场" in text_all:
            return "mall"

        if "toilet" in text_all_lower or "洗手间" in text_all or "卫生间" in text_all:
            return "near_restroom"

        if "bus_stop" in facility_types or "公交站" in text_all:
            return "bus_stop"

        # 根据物体粗分室内/室外
        if "sky" in labels or "tree" in labels or "car" in labels:
            return "street"
        if "door" in labels or "elevator" in labels or "stairs" in labels:
            return "indoor"

        return "unknown"

    def _infer_light(self, env_features: Dict[str, Any]) -> Dict[str, Any]:
        brightness = env_features.get("brightness")
        if brightness is None:
            # 如果没有亮度信息，给个默认
            return {"level": "unknown", "brightness": None}

        if brightness < self.dark_threshold:
            level = "dark"
        elif brightness > 0.7:
            level = "bright"
        else:
            level = "normal"

        reflection = env_features.get("reflection", 0.0)
        reflection_level = "high" if reflection > self.reflection_threshold else "normal"

        return {
            "level": level,
            "brightness": brightness,
            "reflection": reflection,
            "reflection_level": reflection_level,
        }

    def _infer_crowd(
        self,
        objects: List[Dict[str, Any]],
        crowd_density: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        person_count = sum(1 for o in objects if (o.get("class") or o.get("label")) == "person")

        density_level = crowd_density.get("level") if crowd_density else None
        density_value = crowd_density.get("value") if crowd_density else None

        if density_level:
            level = density_level
        else:
            if person_count == 0:
                level = "empty"
            elif person_count < self.crowd_threshold:
                level = "low"
            else:
                level = "high"

        return {
            "level": level,
            "person_count": person_count,
            "density_value": density_value,
        }

    def _summarize_hazards(self, hazards: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not hazards:
            return {"has_hazard": False, "hazards": []}

        # 这里只做简单归类，后面可以和 EventDispatcher 的 ENHANCED_HAZARD 统一
        summarized = []
        for h in hazards:
            summarized.append(
                {
                    "type": h.get("type"),
                    "severity": h.get("severity"),
                    "distance": h.get("distance"),
                    "position": h.get("position"),
                }
            )

        max_severity = max((h.get("severity") or 0) for h in hazards)

        return {
            "has_hazard": True,
            "max_severity": max_severity,
            "hazards": summarized,
        }

    def _pick_key_objects(
        self,
        objects: List[Dict[str, Any]],
        facilities: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        从一堆检测结果里挑出"对用户有用"的东西：
        - 门/楼梯/电梯
        - 公共设施（洗手间、出口、服务台、公交站等）
        - 最近的人
        """
        key_objs: List[Dict[str, Any]] = []

        # 1) 公共设施优先
        for f in facilities:
            key_objs.append(
                {
                    "kind": "facility",
                    "type": f.get("type"),
                    "label": f.get("label"),
                    "distance": f.get("distance"),
                    "position": f.get("position"),
                }
            )

        # 2) 门/楼梯/电梯
        for o in objects:
            cls = o.get("class") or o.get("label")
            if cls in {"door", "stairs", "step_down", "step_up", "elevator", "escalator"}:
                key_objs.append(
                    {
                        "kind": "structure",
                        "type": cls,
                        "distance": o.get("distance"),
                        "position": o.get("position"),
                    }
                )

        # 3) 最近的人（前方 3m 内）
        persons = [
            o for o in objects
            if (o.get("class") or o.get("label")) == "person"
        ]
        persons_with_dist = [
            (o, o.get("distance", 99))
            for o in persons
        ]
        persons_with_dist.sort(key=lambda x: x[1])

        if persons_with_dist:
            nearest, d = persons_with_dist[0]
            if d < self.mid_distance:
                key_objs.append(
                    {
                        "kind": "person",
                        "type": "person",
                        "distance": d,
                        "position": nearest.get("position", "front"),
                    }
                )

        return key_objs

    # -----------------------------
    # 自然语言描述 & 解释
    # -----------------------------
    def _build_summary(
        self,
        scene_type: str,
        light_info: Dict[str, Any],
        crowd_info: Dict[str, Any],
        important_objs: List[Dict[str, Any]],
        hazard_info: Dict[str, Any],
    ) -> str:
        parts = []

        # 场景类型
        scene_text = self._scene_type_to_text(scene_type)
        if scene_text:
            parts.append(scene_text)

        # 光照
        if light_info.get("level") == "dark":
            parts.append("当前光线较暗")
        elif light_info.get("level") == "bright":
            parts.append("光线比较明亮")

        # 人群
        if crowd_info.get("level") == "high":
            parts.append("周围人比较多")
        elif crowd_info.get("level") == "empty":
            parts.append("周围几乎没有人")

        # 关键物体
        obj_desc = self._build_object_sentence(important_objs)
        if obj_desc:
            parts.append(obj_desc)

        # 危险提示
        if hazard_info.get("has_hazard"):
            parts.append("前方存在潜在危险，请注意脚下和周围环境")

        if not parts:
            return "目前没有特别明显的环境特征。"

        # 组合句子
        return "，".join(parts) + "。"

    def _scene_type_to_text(self, scene_type: str) -> str:
        mapping = {
            "subway": "看起来像是地铁或站台区域",
            "hospital": "看起来像是在医院或门诊楼内",
            "mall": "看起来像是在商场或室内公共空间",
            "bus_stop": "附近可能是公交站或候车区域",
            "near_restroom": "附近可能有洗手间",
            "street": "你现在应该是在室外道路或街道附近",
            "indoor": "你现在应该在室内环境",
        }
        return mapping.get(scene_type, "")

    def _build_object_sentence(self, important_objs: List[Dict[str, Any]]) -> Optional[str]:
        if not important_objs:
            return None

        # 简单中文方向映射
        dir_map = {
            "leftFront": "左前方",
            "front": "正前方",
            "rightFront": "右前方",
            "left": "左侧",
            "right": "右侧",
        }

        segments = []
        for obj in important_objs:
            direction = dir_map.get(obj.get("position"), "前方")
            dist = obj.get("distance")
            if dist is not None:
                if dist < self.near_distance:
                    dist_text = "很近的位置"
                else:
                    dist_text = f"大约 {dist:.1f} 米处"
            else:
                dist_text = ""

            label = self._label_to_chinese(obj.get("type") or obj.get("label"))
            if dist_text:
                segments.append(f"{direction}{dist_text}有{label}")
            else:
                segments.append(f"{direction}有{label}")

        return "，".join(segments)

    def _label_to_chinese(self, label: str) -> str:
        mapping = {
            "door": "一扇门",
            "glass_door": "一扇玻璃门",
            "stairs": "楼梯",
            "step_down": "下台阶",
            "step_up": "上台阶",
            "elevator": "电梯",
            "escalator": "扶梯",
            "toilet": "洗手间",
            "person": "行人",
            "service_desk": "服务台",
        }
        return mapping.get(label, label or "未知物体")

    def _build_explanation(
        self,
        scene_type: str,
        light_info: Dict[str, Any],
        crowd_info: Dict[str, Any],
        hazard_info: Dict[str, Any],
        objects: List[Dict[str, Any]],
        facilities: List[Dict[str, Any]],
        texts: List[Dict[str, Any]],
    ) -> str:
        """
        解释文本：给开发和后期"Luna 解释能力"用，不一定要播报
        """
        reasons = []

        # 场景解释
        if scene_type != "unknown":
            reasons.append(f"场景类型推断为 {scene_type}，主要依据检测到的物体/文字信息。")

        # 光照解释
        brightness = light_info.get("brightness")
        if brightness is not None:
            reasons.append(f"亮度估计值为 {brightness:.2f}，光照等级为 {light_info.get('level')}。")

        # 人群解释
        person_count = crowd_info.get("person_count")
        if person_count is not None:
            reasons.append(f"识别到行人数为 {person_count}，人群密度水平为 {crowd_info.get('level')}。")

        # 文字信息
        if texts:
            sample = " | ".join([t.get("text", "") for t in texts[:3]])
            reasons.append(f"OCR 识别到的文字样本包括：{sample} ...")

        # 设施信息
        if facilities:
            f_types = {f.get("type") for f in facilities}
            reasons.append(f"检测到的公共设施类型包括：{', '.join(f_types)}。")

        if hazard_info.get("has_hazard"):
            reasons.append("存在危险检测结果，因此在描述中加入了安全提示。")

        if not reasons:
            return "当前没有足够的信息进行详细解释。"

        return " ".join(reasons)



