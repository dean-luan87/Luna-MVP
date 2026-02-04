# bridge/yolo_python_bridge.py
"""
Python YOLO 直接接入桥接层
支持 ultralytics YOLO 和直接接入 NavigationRuntime
"""
import logging
import sys
import os
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.navigation.navigation_runtime import NavigationRuntime

logger = logging.getLogger(__name__)

# 尝试导入 YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("⚠️ ultralytics YOLO 未安装，请运行: pip install ultralytics")


class YOLONavigationBridge:
    """
    YOLO Python 桥接器
    将 ultralytics YOLO 输出直接接入 NavigationRuntime
    """
    
    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        ideal_heading_deg: Optional[float] = None,
        on_result: Optional[callable] = None
    ):
        """
        Args:
            model_path: YOLO 模型路径
            ideal_heading_deg: 理想方向（度）
            on_result: 结果回调函数
        """
        self.runtime = NavigationRuntime(
            ideal_heading_deg=ideal_heading_deg,
            on_result=on_result
        )
        
        if YOLO_AVAILABLE:
            try:
                self.model = YOLO(model_path)
                logger.info(f"✅ YOLO 模型加载成功: {model_path}")
            except Exception as e:
                logger.error(f"❌ YOLO 模型加载失败: {e}")
                self.model = None
        else:
            self.model = None
            logger.warning("⚠️ YOLO 不可用，将使用模拟数据")
    
    def process_frame(
        self,
        frame,
        heading_deg: float = 0.0,
        speed_mps: float = 0.0,
        turn_rate_deg_s: float = 0.0,
        ocr_results: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        处理单帧图像
        
        Args:
            frame: 图像（numpy array 或 PIL Image）
            heading_deg: 当前朝向（度）
            speed_mps: 速度（米/秒）
            turn_rate_deg_s: 转向角速度（度/秒）
            ocr_results: OCR 结果列表（可选）
        
        Returns:
            导航分析结果
        """
        yolo_data = []
        
        if self.model:
            try:
                results = self.model(frame, verbose=False)[0]
                H, W = frame.shape[:2] if hasattr(frame, 'shape') else (480, 640)
                
                for box in results.boxes:
                    cls = int(box.cls[0])
                    label = results.names[cls]
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    
                    # 归一化 bbox 到 [0,1]
                    yolo_data.append({
                        "label": label,
                        "bbox": [x1/W, y1/H, x2/W, y2/H],
                        "confidence": conf,
                        # distance_m 需要额外的深度估计，这里先留空
                    })
                
                logger.debug(f"[YOLO Bridge] 检测到 {len(yolo_data)} 个对象")
            
            except Exception as e:
                logger.error(f"[YOLO Bridge] YOLO 推理错误: {e}")
        else:
            # 模拟数据（用于测试）
            logger.debug("[YOLO Bridge] 使用模拟数据")
            yolo_data = [
                {
                    "label": "person",
                    "bbox": [0.3, 0.4, 0.5, 0.8],
                    "confidence": 0.85,
                }
            ]
        
        # 构造输入数据
        data = {
            "heading_deg": heading_deg,
            "speed_mps": speed_mps,
            "turn_rate_deg_s": turn_rate_deg_s,
            "yolo": yolo_data,
            "ocr": ocr_results or [],
        }
        
        # 转发给 NavigationRuntime
        result = self.runtime.feed(data)
        return result
    
    def process_video_stream(
        self,
        video_source,
        imu_reader: Optional[callable] = None,
        ocr_processor: Optional[callable] = None
    ):
        """
        处理视频流（生成器）
        
        Args:
            video_source: 视频源（cv2.VideoCapture 或图像生成器）
            imu_reader: IMU 读取函数，返回 {heading_deg, speed_mps, turn_rate_deg_s}
            ocr_processor: OCR 处理函数，接收 frame，返回 OCR 结果列表
        
        Yields:
            每帧的导航分析结果
        """
        import cv2
        
        if isinstance(video_source, cv2.VideoCapture):
            # cv2.VideoCapture 对象
            while True:
                ret, frame = video_source.read()
                if not ret:
                    break
                
                # 读取 IMU 数据
                imu_data = imu_reader() if imu_reader else {
                    "heading_deg": 0.0,
                    "speed_mps": 0.0,
                    "turn_rate_deg_s": 0.0,
                }
                
                # OCR 处理（可选）
                ocr_results = ocr_processor(frame) if ocr_processor else []
                
                # 处理帧
                result = self.process_frame(
                    frame,
                    heading_deg=imu_data.get("heading_deg", 0.0),
                    speed_mps=imu_data.get("speed_mps", 0.0),
                    turn_rate_deg_s=imu_data.get("turn_rate_deg_s", 0.0),
                    ocr_results=ocr_results
                )
                
                yield result
        else:
            # 图像生成器
            for frame in video_source:
                imu_data = imu_reader() if imu_reader else {
                    "heading_deg": 0.0,
                    "speed_mps": 0.0,
                    "turn_rate_deg_s": 0.0,
                }
                
                ocr_results = ocr_processor(frame) if ocr_processor else []
                
                result = self.process_frame(
                    frame,
                    heading_deg=imu_data.get("heading_deg", 0.0),
                    speed_mps=imu_data.get("speed_mps", 0.0),
                    turn_rate_deg_s=imu_data.get("turn_rate_deg_s", 0.0),
                    ocr_results=ocr_results
                )
                
                yield result


# ============================================================
# 使用示例（可直接运行）
# ============================================================

def example_usage():
    """使用示例"""
    
    # 示例 1: 单帧处理
    bridge = YOLONavigationBridge(
        model_path="yolov8n.pt",
        ideal_heading_deg=90.0
    )
    
    # 假设有一个 frame（numpy array）
    # import cv2
    # frame = cv2.imread("test.jpg")
    # result = bridge.process_frame(
    #     frame,
    #     heading_deg=92.5,
    #     speed_mps=0.8,
    #     turn_rate_deg_s=1.5
    # )
    # print(result)
    
    # 示例 2: 视频流处理
    # import cv2
    # cap = cv2.VideoCapture(0)  # 摄像头
    # 
    # def read_imu():
    #     # 你的 IMU 读取逻辑
    #     return {
    #         "heading_deg": 90.0,
    #         "speed_mps": 0.8,
    #         "turn_rate_deg_s": 0.0
    #     }
    # 
    # for result in bridge.process_video_stream(cap, imu_reader=read_imu):
    #     print(f"方向: {result['primary_direction']}, 建议: {result['recommended_action']}")
    
    print("✅ YOLO Python 桥接器已初始化")
    print("   使用 bridge.process_frame() 处理单帧")
    print("   使用 bridge.process_video_stream() 处理视频流")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    example_usage()

