#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 手机端识路测试服务器
通过Web界面在手机上测试视觉识别和导航功能
"""

import os
import sys
import logging
import base64
import io
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入视觉引擎
from core.vision_ocr_engine import VisionOCREngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 全局视觉引擎
vision_engine = None

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Luna 识路测试</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .camera-section {
            margin-bottom: 30px;
        }
        .camera-preview {
            width: 100%;
            max-width: 100%;
            border-radius: 15px;
            margin-bottom: 15px;
            display: none;
        }
        .camera-preview.active {
            display: block;
        }
        video {
            width: 100%;
            border-radius: 15px;
            background: #000;
        }
        canvas {
            display: none;
        }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:active {
            transform: scale(0.98);
            opacity: 0.9;
        }
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        .file-input {
            display: none;
        }
        .result-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .result-section.active {
            display: block;
        }
        .result-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .result-item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .result-text {
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        }
        .result-confidence {
            font-size: 14px;
            color: #666;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .loading.active {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            display: none;
        }
        .error.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Luna 识路测试</h1>
        
        <div class="camera-section">
            <video id="video" autoplay playsinline></video>
            <canvas id="canvas"></canvas>
            <img id="preview" class="camera-preview" />
            
            <button class="btn btn-primary" onclick="startCamera()">📷 打开摄像头</button>
            <button class="btn btn-primary" onclick="capturePhoto()" id="captureBtn" style="display:none;">📸 拍照识别</button>
            <button class="btn btn-secondary" onclick="stopCamera()" id="stopBtn" style="display:none;">⏹️ 关闭摄像头</button>
            
            <label for="fileInput" class="btn btn-secondary" style="display:block;">
                📁 选择图片
            </label>
            <input type="file" id="fileInput" class="file-input" accept="image/*" onchange="handleFileSelect(event)">
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px;">正在识别中...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result-section" id="resultSection">
            <div class="result-title">识别结果</div>
            <div id="results"></div>
        </div>
    </div>

    <script>
        let stream = null;
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const preview = document.getElementById('preview');
        const captureBtn = document.getElementById('captureBtn');
        const stopBtn = document.getElementById('stopBtn');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const resultSection = document.getElementById('resultSection');
        const results = document.getElementById('results');

        async function startCamera() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' } // 后置摄像头
                });
                video.srcObject = stream;
                video.play();
                captureBtn.style.display = 'block';
                stopBtn.style.display = 'block';
                document.querySelector('.btn-primary').style.display = 'none';
            } catch (err) {
                showError('无法访问摄像头: ' + err.message);
            }
        }

        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            video.srcObject = null;
            captureBtn.style.display = 'none';
            stopBtn.style.display = 'none';
            preview.classList.remove('active');
            document.querySelector('.btn-primary').style.display = 'block';
        }

        function capturePhoto() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            canvas.toBlob(function(blob) {
                sendImage(blob);
            }, 'image/jpeg', 0.9);
        }

        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                sendImage(file);
            }
        }

        async function sendImage(imageBlob) {
            loading.classList.add('active');
            error.classList.remove('active');
            resultSection.classList.remove('active');
            
            const formData = new FormData();
            formData.append('image', imageBlob);
            
            try {
                const response = await fetch('/api/recognize', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                } else {
                    showError(data.error || '识别失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                loading.classList.remove('active');
            }
        }

        function displayResults(data) {
            results.innerHTML = '';
            
            // 显示OCR识别结果
            if (data.ocr_results && data.ocr_results.length > 0) {
                const ocrDiv = document.createElement('div');
                ocrDiv.innerHTML = '<div style="font-weight:bold; margin-bottom:10px; color:#667eea;">📝 识别的文字:</div>';
                data.ocr_results.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.text}</div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    ocrDiv.appendChild(itemDiv);
                });
                results.appendChild(ocrDiv);
            }
            
            // 显示物体检测结果
            if (data.detections && data.detections.length > 0) {
                const detDiv = document.createElement('div');
                detDiv.innerHTML = '<div style="font-weight:bold; margin-top:20px; margin-bottom:10px; color:#667eea;">🎯 检测到的物体:</div>';
                data.detections.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.class}</div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    detDiv.appendChild(itemDiv);
                });
                results.appendChild(detDiv);
            }
            
            // 显示导航信息
            if (data.navigation_info) {
                const navDiv = document.createElement('div');
                navDiv.innerHTML = '<div style="font-weight:bold; margin-top:20px; margin-bottom:10px; color:#667eea;">🧭 导航信息:</div>';
                const navItemDiv = document.createElement('div');
                navItemDiv.className = 'result-item';
                navItemDiv.innerHTML = `<div class="result-text">${data.navigation_info}</div>`;
                navDiv.appendChild(navItemDiv);
                results.appendChild(navDiv);
            }
            
            if (results.innerHTML === '') {
                results.innerHTML = '<div class="result-item">未识别到内容</div>';
            }
            
            resultSection.classList.add('active');
        }

        function showError(message) {
            error.textContent = message;
            error.classList.add('active');
        }
    </script>
</body>
</html>
"""

def init_vision_engine():
    """初始化视觉引擎"""
    global vision_engine
    try:
        logger.info("正在初始化视觉识别引擎...")
        vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if vision_engine.load_models():
            logger.info("✅ 视觉识别引擎初始化成功")
            return True
        else:
            logger.error("❌ 视觉识别引擎初始化失败")
            return False
    except Exception as e:
        logger.error(f"❌ 视觉识别引擎初始化异常: {e}")
        return False

def image_to_numpy(image_data):
    """将图片数据转换为numpy数组"""
    try:
        # 如果是base64编码
        if isinstance(image_data, str):
            image_data = base64.b64decode(image_data)
        
        # 转换为PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # 转换为RGB（如果需要）
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 转换为BGR（OpenCV格式）
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        return img_bgr
    except Exception as e:
        logger.error(f"图片转换失败: {e}")
        return None

def analyze_navigation_info(ocr_results, detections):
    """分析导航信息"""
    navigation_keywords = [
        "出口", "入口", "电梯", "楼梯", "厕所", "洗手间",
        "诊室", "病房", "挂号", "缴费", "室", "号",
        "左", "右", "前", "后", "上", "下"
    ]
    
    nav_info = []
    
    # 检查OCR结果中的导航关键词
    for ocr in ocr_results:
        text = ocr.get('text', '')
        for keyword in navigation_keywords:
            if keyword in text:
                nav_info.append(f"发现导航标识: {text}")
                break
    
    # 检查检测到的物体
    for det in detections:
        class_name = det.get('class', '')
        if class_name in ['door', 'stairs', 'elevator']:
            nav_info.append(f"检测到导航相关物体: {class_name}")
    
    return " | ".join(nav_info) if nav_info else "未发现明显的导航信息"

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """识别接口"""
    try:
        if vision_engine is None:
            return jsonify({
                'success': False,
                'error': '视觉引擎未初始化'
            }), 500
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': '未上传图片'
            }), 400
        
        # 读取图片
        file = request.files['image']
        image_data = file.read()
        
        # 转换为numpy数组
        image_np = image_to_numpy(image_data)
        if image_np is None:
            return jsonify({
                'success': False,
                'error': '图片格式错误'
            }), 400
        
        # 进行识别
        logger.info("开始识别图片...")
        results = vision_engine.detect_and_recognize(image_np)
        
        # 分析导航信息
        navigation_info = analyze_navigation_info(
            results.get('ocr_results', []),
            results.get('detections', [])
        )
        
        # 返回结果
        return jsonify({
            'success': True,
            'detections': results.get('detections', []),
            'ocr_results': results.get('ocr_results', []),
            'combined': results.get('combined', []),
            'navigation_info': navigation_info,
            'processing_time': results.get('processing_time', 0)
        })
        
    except Exception as e:
        logger.error(f"识别错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'vision_engine_loaded': vision_engine is not None
    })

if __name__ == '__main__':
    # 初始化视觉引擎
    if not init_vision_engine():
        logger.error("视觉引擎初始化失败，服务器无法启动")
        sys.exit(1)
    
    # 启动服务器
    # 使用0.0.0.0允许局域网访问，这样手机可以连接
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Luna 识路测试服务器启动中...")
    logger.info(f"📱 手机访问地址: http://<你的Mac IP>:{port}")
    logger.info(f"💻 本地访问地址: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

