"""
Qwen Model Loader (v1.3.0)

Qwen 模型加载器（含日志）

功能：
- 加载 L1 模型（0.5B / 1.5B）- 小模型，设备侧/边缘执行
- 加载 L2 模型（3B）- 主模型，近端服务器执行
- 提供统一的模型接口
- 完整的日志记录和性能监控

注意：
- L1 用于：实时安全判断 / 命令词 / 简易导航 / 任务链状态转移
- L2 用于：自然对话、复杂语义、任务链生成、场景解释
"""

import logging
import time
from typing import Optional, Callable, Dict, Any

from .error_codes import ErrorCode, create_error_response, create_success_response
from .tracking import TrackingSystem

logger = logging.getLogger(__name__)


class QwenModelLoader:
    """
    Qwen 模型加载器

    负责加载和管理 L1 和 L2 模型
    """

    # 支持的模型列表
    L1_MODELS = {
        "0.5B": "Qwen/Qwen2.5-0.5B-Instruct",
        "1.5B": "Qwen/Qwen2.5-1.5B-Instruct",
    }

    L2_MODELS = {
        "3B": "Qwen/Qwen2.5-3B-Instruct",
    }

    def __init__(self, tracking: Optional[TrackingSystem] = None):
        """
        初始化模型加载器

        Args:
            tracking: 埋点系统实例（可选）
        """
        self.l1_model = None
        self.l1_tokenizer = None
        self.l2_model = None
        self.l2_tokenizer = None
        self.tracking = tracking

        logger.info("Qwen 模型加载器初始化完成")

    def load_l1(
        self,
        model_size: str = "0.5B",
        device_map: str = "auto",
        **kwargs
    ) -> bool:
        """
        加载 L1 模型（小模型）

        Args:
            model_size: 模型大小，"0.5B" 或 "1.5B"
            device_map: 设备映射，"auto" 表示自动分配
            **kwargs: 传递给 from_pretrained 的其他参数

        Returns:
            bool: 是否加载成功
        """
        start_time = time.time()

        if model_size not in self.L1_MODELS:
            error_msg = f"不支持的 L1 模型大小: {model_size}"
            logger.error(error_msg)
            if self.tracking:
                self.tracking.track_model_load(
                    model="L1",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False

        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model_name = self.L1_MODELS[model_size]
            logger.info(f"🚀 开始加载 L1 模型: {model_name}...")

            # 加载 tokenizer
            logger.debug(f"  加载 tokenizer...")
            self.l1_tokenizer = AutoTokenizer.from_pretrained(model_name)

            # 加载模型
            logger.debug(f"  加载模型...")
            self.l1_model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=device_map,
                **kwargs
            )

            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"✅ L1 模型加载成功: {model_name} (耗时: {latency_ms:.2f}ms)")

            # 记录埋点
            if self.tracking:
                self.tracking.track_model_load(
                    model="L1",
                    success=True,
                    latency_ms=latency_ms,
                )

            return True

        except ImportError:
            error_msg = "未安装 transformers 库，请运行: pip install transformers accelerate tiktoken"
            logger.error(f"❌ {error_msg}")
            if self.tracking:
                self.tracking.track_model_load(
                    model="L1",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ L1 模型加载失败: {error_msg}", exc_info=True)
            if self.tracking:
                self.tracking.track_model_load(
                    model="L1",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False

    def load_l2(
        self,
        model_size: str = "3B",
        device_map: str = "auto",
        **kwargs
    ) -> bool:
        """
        加载 L2 模型（主模型）

        Args:
            model_size: 模型大小，目前支持 "3B"
            device_map: 设备映射，"auto" 表示自动分配
            **kwargs: 传递给 from_pretrained 的其他参数

        Returns:
            bool: 是否加载成功
        """
        start_time = time.time()

        if model_size not in self.L2_MODELS:
            error_msg = f"不支持的 L2 模型大小: {model_size}"
            logger.error(error_msg)
            if self.tracking:
                self.tracking.track_model_load(
                    model="L2",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False

        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model_name = self.L2_MODELS[model_size]
            logger.info(f"🚀 开始加载 L2 模型: {model_name}...")

            # 加载 tokenizer
            logger.debug(f"  加载 tokenizer...")
            self.l2_tokenizer = AutoTokenizer.from_pretrained(model_name)

            # 加载模型
            logger.debug(f"  加载模型...")
            self.l2_model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=device_map,
                **kwargs
            )

            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"✅ L2 模型加载成功: {model_name} (耗时: {latency_ms:.2f}ms)")

            # 记录埋点
            if self.tracking:
                self.tracking.track_model_load(
                    model="L2",
                    success=True,
                    latency_ms=latency_ms,
                )

            return True

        except ImportError:
            error_msg = "未安装 transformers 库，请运行: pip install transformers accelerate tiktoken"
            logger.error(f"❌ {error_msg}")
            if self.tracking:
                self.tracking.track_model_load(
                    model="L2",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ L2 模型加载失败: {error_msg}", exc_info=True)
            if self.tracking:
                self.tracking.track_model_load(
                    model="L2",
                    success=False,
                    latency_ms=(time.time() - start_time) * 1000,
                    error_message=error_msg,
                )
            return False

    def get_l1_callable(self) -> Optional[Callable]:
        """
        获取 L1 模型的可调用对象

        Returns:
            Optional[Callable]: L1 模型的调用函数，如果未加载则返回 None
        """
        if self.l1_model is None or self.l1_tokenizer is None:
            return None

        def l1_call(text: str) -> Dict[str, Any]:
            """L1 模型调用函数"""
            try:
                # 构建输入
                messages = [
                    {"role": "user", "content": text}
                ]
                text_input = self.l1_tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                model_inputs = self.l1_tokenizer([text_input], return_tensors="pt").to(self.l1_model.device)

                # 生成响应
                generated_ids = self.l1_model.generate(
                    model_inputs.input_ids,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                )
                generated_ids = [
                    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
                ]

                response = self.l1_tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )[0]

                # 简单的意图分类（这里可以扩展为更复杂的分类逻辑）
                intent = self._classify_intent(text, response)

                return {
                    "text": response,
                    "intent": intent,
                    "confidence": 0.8,  # 默认置信度
                }
            except Exception as e:
                logger.error(f"L1 模型调用失败: {e}")
                return {"error": str(e)}

        return l1_call

    def get_l2_callable(self) -> Optional[Callable]:
        """
        获取 L2 模型的可调用对象

        Returns:
            Optional[Callable]: L2 模型的调用函数，如果未加载则返回 None
        """
        if self.l2_model is None or self.l2_tokenizer is None:
            return None

        def l2_call(text: str) -> Dict[str, Any]:
            """L2 模型调用函数"""
            try:
                # 构建输入
                messages = [
                    {"role": "user", "content": text}
                ]
                text_input = self.l2_tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                model_inputs = self.l2_tokenizer([text_input], return_tensors="pt").to(self.l2_model.device)

                # 生成响应
                generated_ids = self.l2_model.generate(
                    model_inputs.input_ids,
                    max_new_tokens=1024,
                    temperature=0.7,
                    do_sample=True,
                )
                generated_ids = [
                    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
                ]

                response = self.l2_tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )[0]

                return {
                    "text": response,
                }
            except Exception as e:
                logger.error(f"L2 模型调用失败: {e}")
                return {"error": str(e)}

        return l2_call

    @staticmethod
    def _classify_intent(text: str, response: str) -> str:
        """
        简单的意图分类（可以后续扩展为更复杂的分类器）

        Args:
            text: 用户输入文本
            response: 模型响应

        Returns:
            str: 意图类型
        """
        text_lower = text.lower()

        # 简单导航类意图
        if any(word in text_lower for word in ["往左", "往右", "向前", "向后", "继续", "停下"]):
            return "simple_nav"
        # 方向类意图
        if any(word in text_lower for word in ["方向", "哪里", "哪边"]):
            return "orientation"
        # 确认类意图
        if any(word in text_lower for word in ["是吗", "对吗", "是不是", "能不能"]):
            return "confirm"
        # 是/否类意图
        if any(word in text_lower for word in ["是的", "不是", "可以", "不行", "好", "不好"]):
            return "yes_no"

        # 默认复杂语义
        return "complex_semantic"


def load_l1(model_size: str = "0.5B", **kwargs) -> Optional[Callable]:
    """
    便捷函数：加载 L1 模型并返回可调用对象

    Args:
        model_size: 模型大小
        **kwargs: 传递给 load_l1 的其他参数

    Returns:
        Optional[Callable]: L1 模型调用函数，失败返回 None
    """
    loader = QwenModelLoader()
    if loader.load_l1(model_size, **kwargs):
        return loader.get_l1_callable()
    return None


def load_l2(model_size: str = "3B", **kwargs) -> Optional[Callable]:
    """
    便捷函数：加载 L2 模型并返回可调用对象

    Args:
        model_size: 模型大小
        **kwargs: 传递给 load_l2 的其他参数

    Returns:
        Optional[Callable]: L2 模型调用函数，失败返回 None
    """
    loader = QwenModelLoader()
    if loader.load_l2(model_size, **kwargs):
        return loader.get_l2_callable()
    return None

