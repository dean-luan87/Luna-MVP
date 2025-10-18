#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸识别模块
识别熟人和身份提示
"""

import cv2
import numpy as np
import argparse
import os
import pickle
from datetime import datetime

class FaceRecognizer:
    def __init__(self, db_path='faces_db/', notify=True, speech_notify=True):
        self.db_path = db_path
        self.notify = notify
        self.speech_notify = speech_notify
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_database = {}
        
        # 创建数据库目录
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            
        self.load_database()
    
    def load_database(self):
        """加载人脸数据库"""
        try:
            if os.path.exists(os.path.join(self.db_path, 'faces.pkl')):
                with open(os.path.join(self.db_path, 'faces.pkl'), 'rb') as f:
                    self.face_database = pickle.load(f)
                print(f"✅ 加载了 {len(self.face_database)} 个已知人脸")
            else:
                print("📁 人脸数据库为空")
        except Exception as e:
            print(f"❌ 加载数据库失败: {e}")
    
    def save_database(self):
        """保存人脸数据库"""
        try:
            with open(os.path.join(self.db_path, 'faces.pkl'), 'wb') as f:
                pickle.dump(self.face_database, f)
            print("✅ 人脸数据库已保存")
        except Exception as e:
            print(f"❌ 保存数据库失败: {e}")
    
    def detect_faces(self, frame):
        """检测人脸"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            
            # 简单的相似度检测（实际应用中需要更复杂的算法）
            identity = self.recognize_face(face_roi)
            
            results.append({
                'bbox': (x, y, w, h),
                'identity': identity,
                'confidence': 0.8  # 简化版本
            })
            
        return results
    
    def recognize_face(self, face_roi):
        """识别人脸身份"""
        # 这里是简化版本，实际应用需要训练好的模型
        # 返回 "Unknown" 或已知身份
        return "Unknown"
    
    def run_recognition(self):
        print("👤 人脸识别模式启动")
        print(f"📁 数据库路径: {self.db_path}")
        print(f"🔔 通知: {'开启' if self.notify else '关闭'}")
        print(f"🔊 语音通知: {'开启' if self.speech_notify else '关闭'}")
        
        cap = cv2.VideoCapture(0)
        last_recognition_time = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 检测人脸
            faces = self.detect_faces(frame)
            
            # 绘制检测结果
            for face in faces:
                x, y, w, h = face['bbox']
                identity = face['identity']
                confidence = face['confidence']
                
                # 绘制边界框
                color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # 绘制标签
                label = f"{identity}: {confidence:.2f}"
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # 通知逻辑
                current_time = time.time()
                if identity != "Unknown" and current_time - last_recognition_time > 5:
                    if self.notify:
                        print(f"👋 识别到: {identity}")
                    last_recognition_time = current_time
            
            # 显示信息
            cv2.putText(frame, f"Face Recognition - Detected: {len(faces)}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("👤 Luna Face Recognition", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        self.save_database()

def main():
    parser = argparse.ArgumentParser(description='Luna 人脸识别工具')
    parser.add_argument('--db', type=str, default='faces_db/', help='人脸数据库路径')
    parser.add_argument('--notify', type=str, default='yes', help='是否启用通知')
    parser.add_argument('--speech_notify', type=str, default='yes', help='是否启用语音通知')
    
    args = parser.parse_args()
    
    notify = args.notify.lower() == 'yes'
    speech_notify = args.speech_notify.lower() == 'yes'
    
    recognizer = FaceRecognizer(args.db, notify, speech_notify)
    recognizer.run_recognition()

if __name__ == "__main__":
    main()
