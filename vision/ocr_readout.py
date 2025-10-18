#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR文本识别模块
支持多语言文本识别和TTS朗读
"""

import cv2
import numpy as np
import argparse
import sys
import time
try:
    import pytesseract
    import pyttsx3
except ImportError:
    print("❌ 请安装所需依赖: pip install pytesseract pyttsx3")
    sys.exit(1)

class OCRReader:
    def __init__(self, lang='zh', speak=True, trigger_button='space'):
        """
        初始化OCR阅读器
        
        Args:
            lang: 识别语言 ('zh', 'en', 'zh+en')
            speak: 是否启用语音朗读
            trigger_button: 触发按钮
        """
        self.lang = lang
        self.speak = speak
        self.trigger_button = trigger_button
        self.cap = None
        self.tts_engine = None
        
        # 配置Tesseract语言
        self.tesseract_config = self._get_tesseract_config()
        
        if self.speak:
            self._init_tts()
    
    def _get_tesseract_config(self):
        """获取Tesseract配置"""
        lang_map = {
            'zh': 'chi_sim',
            'en': 'eng',
            'zh+en': 'chi_sim+eng'
        }
        return f'--oem 3 --psm 6 -l {lang_map.get(self.lang, "eng")}'
    
    def _init_tts(self):
        """初始化TTS引擎"""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # 语速
            self.tts_engine.setProperty('volume', 0.8)  # 音量
            print("✅ TTS引擎初始化成功")
        except Exception as e:
            print(f"❌ TTS引擎初始化失败: {e}")
            self.speak = False
    
    def initialize_camera(self):
        """初始化摄像头"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ 无法打开摄像头")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("✅ 摄像头初始化成功")
        return True
    
    def preprocess_image(self, image):
        """图像预处理"""
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 去噪
        denoised = cv2.medianBlur(gray, 3)
        
        # 自适应阈值
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        return thresh
    
    def extract_text(self, image):
        """提取文本"""
        try:
            # 预处理图像
            processed = self.preprocess_image(image)
            
            # OCR识别
            text = pytesseract.image_to_string(processed, config=self.tesseract_config)
            
            # 清理文本
            text = text.strip()
            
            return text
            
        except Exception as e:
            print(f"❌ OCR识别错误: {e}")
            return ""
    
    def speak_text(self, text):
        """语音朗读"""
        if not self.speak or not self.tts_engine or not text:
            return
        
        try:
            print(f"🔊 朗读: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ 语音朗读错误: {e}")
    
    def run_ocr(self):
        """运行OCR识别"""
        if not self.initialize_camera():
            return
        
        print("📖 开始OCR文本识别")
        print(f"🌐 识别语言: {self.lang}")
        print(f"🔊 语音朗读: {'开启' if self.speak else '关闭'}")
        print(f"⌨️ 触发按钮: {self.trigger_button}")
        print("按 'q' 退出程序")
        
        last_text = ""
        text_cooldown = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ 无法读取摄像头画面")
                    break
                
                # 显示提示信息
                cv2.putText(frame, f"OCR Ready - Language: {self.lang}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Press '{self.trigger_button}' to read text", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                cv2.putText(frame, "Press 'q' to quit", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # 显示上次识别的文本
                if last_text:
                    cv2.putText(frame, f"Last: {last_text[:50]}...", 
                               (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.5, (255, 255, 255), 1)
                
                cv2.imshow("📖 Luna OCR Reader", frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord(self.trigger_button) and text_cooldown <= 0:
                    print("🔍 正在识别文本...")
                    text = self.extract_text(frame)
                    
                    if text and text != last_text:
                        print(f"📝 识别结果: {text}")
                        last_text = text
                        self.speak_text(text)
                        text_cooldown = 30  # 防止重复识别
                    else:
                        print("❌ 未识别到新文本")
                
                if text_cooldown > 0:
                    text_cooldown -= 1
                    
        except KeyboardInterrupt:
            print("\n⚠️ 程序被用户中断")
        except Exception as e:
            print(f"❌ 程序出现错误: {e}")
        finally:
            self.release()
    
    def release(self):
        """释放资源"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 资源已释放")

def main():
    parser = argparse.ArgumentParser(description='Luna OCR文本识别工具')
    parser.add_argument('--lang', type=str, default='zh', help='识别语言 (zh/en/zh+en)')
    parser.add_argument('--speak', type=bool, default=True, help='是否启用语音朗读')
    parser.add_argument('--trigger_button', type=str, default='space', help='触发按钮')
    
    args = parser.parse_args()
    
    ocr_reader = OCRReader(args.lang, args.speak, args.trigger_button)
    ocr_reader.run_ocr()

if __name__ == "__main__":
    main()
