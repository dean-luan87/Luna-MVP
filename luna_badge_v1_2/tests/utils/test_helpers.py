"""
测试工具和 Mock 数据生成器
提供统一的测试辅助函数，用于所有测试模块
"""
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Mock 数据目录
MOCK_DATA_DIR = Path(__file__).parent.parent / "mock_data"


def load_frame(file_path: Optional[str] = None) -> np.ndarray:
    """
    加载测试用的图像帧
    
    Args:
        file_path: 图像文件路径，如果为 None 则生成随机图像
    
    Returns:
        numpy.ndarray: 图像数组 (H, W, 3)
    """
    if file_path:
        import cv2
        return cv2.imread(file_path)
    else:
        # 生成随机测试图像 (640x480x3)
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)


def mock_camera(width: int = 640, height: int = 480) -> Dict[str, Any]:
    """
    模拟摄像头对象
    
    Returns:
        dict: 包含摄像头配置和方法的字典
    """
    return {
        "width": width,
        "height": height,
        "fps": 30,
        "is_active": True,
        "capture": lambda: load_frame(),
    }


def mock_yolo_output(num_objects: int = 3) -> List[Dict[str, Any]]:
    """
    模拟 YOLO 检测输出
    
    Args:
        num_objects: 检测到的对象数量
    
    Returns:
        list: 检测结果列表
    """
    objects = []
    for i in range(num_objects):
        objects.append({
            "cls": f"object_{i}",
            "conf": 0.8 + i * 0.05,
            "bbox": [100 + i * 50, 100 + i * 50, 200 + i * 50, 200 + i * 50],
            "x1": 100 + i * 50,
            "y1": 100 + i * 50,
            "x2": 200 + i * 50,
            "y2": 200 + i * 50,
        })
    return objects


def mock_navigation_state(
    current_position: Optional[tuple] = None,
    target_position: Optional[tuple] = None,
    obstacles: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    模拟导航状态
    
    Args:
        current_position: 当前位置 (x, y)
        target_position: 目标位置 (x, y)
        obstacles: 障碍物列表
    
    Returns:
        dict: 导航状态字典
    """
    return {
        "current_position": current_position or (0.0, 0.0),
        "target_position": target_position or (10.0, 10.0),
        "obstacles": obstacles or [],
        "path": [],
        "status": "navigating",
        "confidence": 0.9,
    }


def mock_audio_response(text: str = "测试语音") -> Dict[str, Any]:
    """
    模拟音频响应
    
    Args:
        text: 语音文本
    
    Returns:
        dict: 音频响应字典
    """
    return {
        "text": text,
        "audio_file": None,
        "duration_ms": len(text) * 50,
        "status": "success",
    }


def save_mock_data(data: Any, filename: str, subdir: str = "") -> Path:
    """
    保存 Mock 数据到文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
        subdir: 子目录（sample_frames, sample_ocr, sample_yolo）
    
    Returns:
        Path: 保存的文件路径
    """
    if subdir:
        save_dir = MOCK_DATA_DIR / subdir
    else:
        save_dir = MOCK_DATA_DIR
    
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / filename
    
    if isinstance(data, np.ndarray):
        import cv2
        cv2.imwrite(str(file_path), data)
    elif isinstance(data, (dict, list)):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(data))
    
    return file_path


def load_mock_data(filename: str, subdir: str = "") -> Any:
    """
    加载 Mock 数据
    
    Args:
        filename: 文件名
        subdir: 子目录
    
    Returns:
        加载的数据
    """
    if subdir:
        load_dir = MOCK_DATA_DIR / subdir
    else:
        load_dir = MOCK_DATA_DIR
    
    file_path = load_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Mock data not found: {file_path}")
    
    if file_path.suffix in ['.jpg', '.jpeg', '.png']:
        import cv2
        return cv2.imread(str(file_path))
    elif file_path.suffix == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def create_test_config(**kwargs) -> Dict[str, Any]:
    """
    创建测试配置
    
    Args:
        **kwargs: 配置参数
    
    Returns:
        dict: 测试配置字典
    """
    default_config = {
        "model": "yolo11_tiny",
        "device": "cpu",
        "log_level": "DEBUG",
        "test_mode": True,
        "mock_camera": True,
        "mock_audio": True,
    }
    default_config.update(kwargs)
    return default_config
















