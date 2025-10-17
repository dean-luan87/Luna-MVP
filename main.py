# -*- coding: utf-8 -*-
"""
Luna 实体徽章 MVP - 主程序
实现"看得见、说得出、记得下"的完整流程
"""

import cv2
import time
import json
import numpy as np
from datetime import datetime
import argparse
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置和工具模块
from config import MODEL_PATHS, CAMERA_CONFIG, PROCESSING_CONFIG, OUTPUT_CONFIG
from utils import (
    YOLODetector, OCRProcessor, QwenVLProcessor, 
    WhisperProcessor, TTSProcessor, CameraHandler, setup_logger, JSONLogger
)
from utils.system_voice_recognition import SystemVoiceRecognition, listen_and_recognize
from modules.voice import Voice


class LunaBadgeMVP:
    """Luna 实体徽章 MVP 主类"""
    
    def __init__(self):
        """初始化Luna徽章系统"""
        # 设置日志
        self.logger = setup_logger('luna_badge')
        self.json_logger = JSONLogger()
        
        # 初始化语音播报模块
        self.logger.info("正在初始化语音播报模块...")
        try:
            self.voice = Voice()
            if self.voice.is_available:
                self.logger.info("语音播报模块初始化成功")
                # 播放启动提示音
                self.voice.speak("Luna 已启动")
            else:
                self.logger.warning("语音播报模块不可用，将静默运行")
        except Exception as e:
            self.logger.error(f"语音播报模块初始化失败: {e}")
            self.voice = None
        
        # 初始化各个处理器
        self.logger.info("正在初始化摄像头...")
        self.camera = CameraHandler()
        
        # 检查摄像头状态
        if not self.camera.is_opened():
            self.logger.error("摄像头初始化失败，程序可能无法正常运行")
            self.logger.info("请检查:")
            self.logger.info("1. 摄像头是否已连接")
            self.logger.info("2. 摄像头是否被其他程序占用")
            self.logger.info("3. 系统权限设置（Mac需要摄像头权限）")
            # 语音提示摄像头问题
            self._speak_safely("摄像头初始化失败，请检查摄像头连接")
        else:
            self.logger.info("摄像头初始化成功")
            # 语音提示摄像头正常
            self._speak_safely("摄像头初始化成功")
        
        self.logger.info("正在初始化AI模型...")
        self.yolo_detector = YOLODetector()
        self.ocr_processor = OCRProcessor()
        self.qwen_processor = QwenVLProcessor()
        self.whisper_processor = WhisperProcessor()
        self.tts_processor = TTSProcessor()
        
        # 初始化语音识别模块
        self.logger.info("正在初始化系统语音识别模块...")
        try:
            self.voice_recognition = SystemVoiceRecognition()
            if self.voice_recognition.is_available:
                self.logger.info("系统语音识别模块初始化成功")
                # 测试麦克风
                if self.voice_recognition.test_microphone():
                    self.logger.info("麦克风测试成功")
                else:
                    self.logger.warning("麦克风测试失败")
            else:
                self.logger.warning("语音识别模块不可用")
        except Exception as e:
            self.logger.error(f"语音识别模块初始化失败: {e}")
            self.voice_recognition = None
        
        # 处理状态
        self.is_running = False
        self.last_process_time = 0
        
        self.logger.info("Luna 实体徽章 MVP 初始化完成")
        # 语音提示系统就绪
        self._speak_safely("系统初始化完成，开始运行")
    
    def _speak_safely(self, text: str):
        """
        安全的语音播报方法，包含错误处理
        
        Args:
            text: 要播报的文本
        """
        try:
            if not text or not text.strip():
                return
            
            if not self.voice:
                self.logger.warning("语音模块未初始化")
                return
                
            if not self.voice.is_available:
                self.logger.warning("语音模块不可用")
                return
            
            # 检查是否正在播报
            if self.voice.is_speaking():
                self.logger.warning("语音模块正在播报中，跳过新的播报请求")
                return
            
            # 开始播报
            success = self.voice.speak(text)
            if success:
                self.logger.debug(f"语音播报已启动: {text[:50]}...")
            else:
                self.logger.warning("语音播报启动失败")
                
        except Exception as e:
            self.logger.warning(f"语音播报异常: {e}")
            # 尝试重新初始化语音模块
            try:
                if self.voice:
                    self.voice.stop()
                from modules.voice import Voice
                self.voice = Voice()
                self.logger.info("语音模块重新初始化完成")
            except Exception as reinit_error:
                self.logger.warning(f"语音模块重新初始化失败: {reinit_error}")
    
    def _build_voice_text(self, result: dict) -> str:
        """
        构建语音播报内容
        
        Args:
            result: 识别结果字典
            
        Returns:
            构建的语音文本
        """
        try:
            voice_parts = []
            
            # 添加检测到的物体信息
            if result['objects']:
                object_names = [obj['label'] for obj in result['objects']]
                if len(object_names) == 1:
                    voice_parts.append(f"检测到{object_names[0]}")
                else:
                    voice_parts.append(f"检测到{len(object_names)}个物体：{', '.join(object_names)}")
            
            # 添加识别的文字信息
            if result['texts']:
                text_contents = [text['text'] for text in result['texts']]
                if len(text_contents) == 1:
                    voice_parts.append(f"识别到文字：{text_contents[0]}")
                else:
                    voice_parts.append(f"识别到{len(text_contents)}个文字：{', '.join(text_contents)}")
            
            # 添加AI描述
            if result['description']:
                voice_parts.append(result['description'])
            
            # 如果没有检测到任何内容
            if not voice_parts:
                voice_parts.append("当前场景较为空旷，未检测到特殊物体或文字")
            
            return "。".join(voice_parts) + "。"
            
        except Exception as e:
            self.logger.warning(f"构建语音文本失败: {e}")
            return result.get('description', '')
    
    def _start_voice_conversation(self):
        """启动语音对话功能"""
        try:
            if not self.voice_recognition or not self.voice_recognition.is_available:
                self.logger.warning("语音识别模块不可用，跳过语音对话")
                return
            
            # 语音提示用户开始说话
            self._speak_safely("请开始说话")
            
            # 在新线程中启动语音识别
            import threading
            voice_thread = threading.Thread(target=self._voice_conversation_loop, daemon=True)
            voice_thread.start()
            
            self.logger.info("语音对话功能已启动")
            
        except Exception as e:
            self.logger.error(f"启动语音对话失败: {e}")
    
    def _voice_conversation_loop(self):
        """语音对话循环"""
        try:
            while self.is_running:
                # 等待语音输入
                self.logger.info("等待语音输入...")
                recognized_text = self.voice_recognition.listen_and_recognize(timeout=5)
                
                if recognized_text and recognized_text.strip():
                    # 识别到语音
                    self.logger.info(f"识别到语音: {recognized_text}")
                    
                    # 语音回应
                    response = f"你刚才说的是：{recognized_text}"
                    self._speak_safely(response)
                    
                    # 等待语音播报完成
                    time.sleep(2)
                    
                else:
                    # 没有识别到语音
                    self.logger.warning("5秒内无声音输入")
                    self._speak_safely("我没有听清，再说一遍？")
                    
                    # 短暂等待后继续
                    time.sleep(1)
                    
        except Exception as e:
            self.logger.error(f"语音对话循环出错: {e}")
    
    def process_frame(self, frame: np.ndarray) -> dict:
        """
        处理单帧图像，执行完整的识别流程
        
        Args:
            frame: 输入图像帧
            
        Returns:
            处理结果字典
        """
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        
        try:
            # 1. YOLO目标检测
            self.logger.info("开始YOLO目标检测...")
            objects = self.yolo_detector.detect(frame)
            
            # 2. OCR文字识别
            self.logger.info("开始OCR文字识别...")
            texts = self.ocr_processor.extract_text(frame)
            
            # 3. Qwen2-VL生成场景描述
            self.logger.info("开始生成场景描述...")
            description = self.qwen_processor.generate_description(frame, objects, texts)
            
            # 4. 语音输入处理（模拟）
            audio_input = self.whisper_processor.transcribe(np.array([]))  # 模拟音频数据
            
            processing_time = time.time() - start_time
            
            # 构建结果
            result = {
                'timestamp': timestamp,
                'objects': objects,
                'texts': texts,
                'description': description,
                'audio_input': audio_input,
                'processing_time': processing_time
            }
            
            # 5. 输出结果
            self._output_results(result)
            
            # 6. 记录日志
            self.json_logger.log_recognition_result(
                timestamp=timestamp,
                objects=objects,
                texts=texts,
                description=description,
                audio_input=audio_input,
                processing_time=processing_time
            )
            
            return result
            
        except Exception as e:
            error_msg = f"帧处理失败: {e}"
            self.logger.error(error_msg)
            self.json_logger.log_error(timestamp, error_msg, "processing_error")
            return None
    
    def _output_results(self, result: dict):
        """
        输出处理结果
        
        Args:
            result: 处理结果字典
        """
        if not result:
            return
        
        # 打印识别结果
        if OUTPUT_CONFIG['print_results']:
            print("\n" + "="*50)
            print(f"时间: {result['timestamp']}")
            print(f"处理时间: {result['processing_time']:.2f}秒")
            
            # 打印检测到的物体
            if result['objects']:
                print("\n检测到的物体:")
                for obj in result['objects']:
                    print(f"  - {obj['label']}: {obj['confidence']:.2f}")
            else:
                print("\n未检测到物体")
            
            # 打印识别的文字
            if result['texts']:
                print("\n识别的文字:")
                for text in result['texts']:
                    print(f"  - {text['text']}: {text['confidence']:.2f}")
            else:
                print("\n未识别到文字")
            
            # 打印AI描述
            print(f"\nAI场景描述: {result['description']}")
            
            if result['audio_input']:
                print(f"语音输入: {result['audio_input']}")
            
            print("="*50)
        
        # 语音播报识别结果
        if result['description']:
            # 构建语音播报内容
            voice_text = self._build_voice_text(result)
            if voice_text:
                self.logger.info("开始语音播报识别结果...")
                self._speak_safely(voice_text)
        
        # 兼容原有的TTS处理器（如果配置启用）
        if OUTPUT_CONFIG['play_audio'] and result['description']:
            try:
                self.tts_processor.speak(result['description'])
            except Exception as e:
                self.logger.warning(f"原有TTS播报失败: {e}")
    
    def run(self, show_camera: bool = True):
        """
        运行主循环
        
        Args:
            show_camera: 是否显示摄像头画面
        """
        if not self.camera.is_opened():
            self.logger.error("摄像头未打开，无法运行")
            return
        
        self.is_running = True
        self.logger.info("开始运行Luna徽章系统...")
        
        # 启动语音对话
        self._start_voice_conversation()
        
        try:
            while self.is_running:
                # 读取摄像头帧
                frame = self.camera.read_frame()
                if frame is None:
                    self.logger.warning("无法读取摄像头帧，跳过")
                    continue
                
                # 显示摄像头画面
                if show_camera and OUTPUT_CONFIG['show_camera_feed']:
                    cv2.imshow('Luna Badge MVP - 摄像头画面', frame)
                    
                    # 检查按键
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        self.logger.info("用户按下'q'键，退出程序")
                        break
                    elif key == ord('s'):
                        self.logger.info("用户按下's'键，立即处理当前帧")
                        self.process_frame(frame)
                        continue
                
                # 按间隔处理帧
                current_time = time.time()
                if current_time - self.last_process_time >= PROCESSING_CONFIG['process_interval']:
                    self.logger.info("开始处理当前帧...")
                    self.process_frame(frame)
                    self.last_process_time = current_time
                
        except KeyboardInterrupt:
            self.logger.info("用户中断程序")
        except Exception as e:
            self.logger.error(f"运行过程中发生错误: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("开始清理资源...")
        self.is_running = False
        
        # 停止语音播报
        if self.voice:
            try:
                self.voice.stop()
            except Exception as e:
                self.logger.warning(f"停止语音播报失败: {e}")
        
        # 停止语音识别
        if self.voice_recognition:
            try:
                # 语音识别模块会自动停止
                self.logger.info("语音识别模块已停止")
            except Exception as e:
                self.logger.warning(f"停止语音识别失败: {e}")
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        self.logger.info("资源清理完成")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Luna 实体徽章 MVP')
    parser.add_argument('--no-camera', action='store_true', help='不显示摄像头画面')
    parser.add_argument('--interval', type=float, default=PROCESSING_CONFIG['process_interval'], 
                       help='处理间隔（秒）')
    parser.add_argument('--camera-index', type=int, default=CAMERA_CONFIG['camera_index'],
                       help='摄像头索引')
    
    args = parser.parse_args()
    
    # 更新配置
    PROCESSING_CONFIG['process_interval'] = args.interval
    CAMERA_CONFIG['camera_index'] = args.camera_index
    
    print("Luna 实体徽章 MVP 启动中...")
    print("="*50)
    print("功能说明:")
    print("- 摄像头识别：检测人、车、障碍物、标志牌")
    print("- 文字识别：识别画面中的文字内容")
    print("- 场景描述：AI生成自然语言描述")
    print("- 语音播报：TTS语音输出")
    print("- 日志记录：JSON格式记录所有结果")
    print("="*50)
    print("操作说明:")
    print("- 按 'q' 键退出程序")
    print("- 按 's' 键立即处理当前帧")
    print("="*50)
    
    # 创建并运行Luna徽章系统
    luna_badge = LunaBadgeMVP()
    luna_badge.run(show_camera=not args.no_camera)


if __name__ == "__main__":
    main()
