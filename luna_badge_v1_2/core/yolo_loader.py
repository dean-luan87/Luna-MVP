# core/yolo_loader.py

import os
from typing import Any, Dict, Optional, Tuple

import yaml
from ultralytics import YOLO
from core.logging import get_logger



log = get_logger("yolo_loader")
class UnifiedYOLOLoader:
    """
    统一的 YOLO 模型加载器：
    - 从 configs/model_registry.yaml 读取配置
    - 当前只实现 PyTorch(.pt)，后续可扩 ONNX
    """

    def __init__(self, config_path: str = "configs/model_registry.yaml") -> None:
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.current_model_key: Optional[str] = None
        self.model: Any = None
        self.framework: str = "pytorch"
        self.input_size: Tuple[int, int] = (640, 640)
        self.model_path: str = ""

    # ---------- 配置 ----------
    def load_config(self) -> None:
        # 支持从不同目录运行，自动查找配置文件
        from pathlib import Path
        config_file = Path(self.config_path)
        if not config_file.exists():
            # 尝试从 core 目录查找
            core_dir = Path(__file__).parent
            config_file = core_dir.parent / self.config_path
            if not config_file.exists():
                raise FileNotFoundError(f"[YOLO_LOADER] config not found: {self.config_path}")

        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}

        self.current_model_key = self.config.get("current_nav_model")
        if not self.current_model_key:
            raise ValueError("[YOLO_LOADER] current_nav_model not set in config")

        models_cfg = self.config.get("models", {})
        model_cfg = models_cfg.get(self.current_model_key)
        if not model_cfg:
            raise ValueError(f"[YOLO_LOADER] model config not found: {self.current_model_key}")

        self.framework = model_cfg.get("framework", "pytorch")
        size = model_cfg.get("input_size", [640, 640])
        self.input_size = (int(size[0]), int(size[1]))
        self.model_path = model_cfg.get("path")

        if not self.model_path:
            raise ValueError(f"[YOLO_LOADER] model path missing for: {self.current_model_key}")

        # 支持相对路径（从项目根目录）
        if not os.path.isabs(self.model_path):
            project_root = Path(__file__).parent.parent
            model_file = project_root / self.model_path
            if model_file.exists():
                self.model_path = str(model_file)
            elif not os.path.exists(self.model_path):
                raise FileNotFoundError(f"[YOLO_LOADER] model file not found: {self.model_path}")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"[YOLO_LOADER] model file not found: {self.model_path}")

        print(
            f"[YOLO_LOADER] config loaded: "
            f"key={self.current_model_key}, path={self.model_path}, "
            f"framework={self.framework}, input_size={self.input_size}"
        )

    # ---------- 加载 ----------
    def load_model(self) -> Any:
        if not self.config:
            self.load_config()

        log.info(f"[YOLO_LOADER] loading model from {self.model_path} ...")

        if self.framework == "pytorch":
            self.model = YOLO(self.model_path)
            log.info("[YOLO_LOADER] ✅ model loaded via ultralytics.YOLO (pytorch)")
        else:
            raise ValueError(f"[YOLO_LOADER] unknown framework: {self.framework}")

        return self.model

    # ---------- 推理 ----------
    def infer(self, image) -> Any:
        """
        image: np.ndarray / PIL / torch tensor
        """
        if self.model is None:
            self.load_model()

        if self.framework != "pytorch":
            raise RuntimeError("[YOLO_LOADER] infer called but framework is not pytorch")

        results = self.model(image, imgsz=self.input_size, verbose=False)
        return results
