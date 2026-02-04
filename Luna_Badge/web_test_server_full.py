#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 完整功能测试服务器
支持所有核心功能的手机端测试
"""

import os
import sys
import logging
import base64
import io
import tempfile
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List, Optional

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 全局模块
vision_engine = None
step_detector = None
signboard_detector = None
hazard_detector = None
whisper_recognizer = None
tts_manager = None

def init_all_modules():
    """初始化所有模块"""
    global vision_engine, step_detector, signboard_detector, hazard_detector
    global whisper_recognizer, tts_manager
    
    success_count = 0
    
    # 1. 视觉OCR引擎
    try:
        from core.vision_ocr_engine import VisionOCREngine
        logger.info("正在初始化视觉OCR引擎...")
        vision_engine = VisionOCREngine(use_yolo=True, use_ocr=True, yolo_imgsz=1280)
        if vision_engine.load_models():
            logger.info("✅ 视觉OCR引擎初始化成功")
            success_count += 1
        else:
            logger.warning("⚠️ 视觉OCR引擎初始化失败")
    except Exception as e:
        logger.warning(f"⚠️ 视觉OCR引擎初始化异常: {e}")
    
    # 2. 台阶检测器
    try:
        from core.step_detector import StepDetector
        logger.info("正在初始化台阶检测器...")
        step_detector = StepDetector()
        logger.info("✅ 台阶检测器初始化成功")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 台阶检测器初始化异常: {e}")
    
    # 3. 标识牌检测器
    try:
        from core.signboard_detector import SignboardDetector
        logger.info("正在初始化标识牌检测器...")
        signboard_detector = SignboardDetector()
        logger.info("✅ 标识牌检测器初始化成功")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 标识牌检测器初始化异常: {e}")
    
    # 4. 危险检测器
    try:
        from core.hazard_detector import HazardDetector
        logger.info("正在初始化危险检测器...")
        hazard_detector = HazardDetector()
        logger.info("✅ 危险检测器初始化成功")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 危险检测器初始化异常: {e}")
    
    # 5. 语音识别器（延迟加载）
    try:
        from core.whisper_recognizer import WhisperRecognizer
        logger.info("语音识别器将在首次使用时加载...")
        whisper_recognizer = WhisperRecognizer(model_name="base", language="zh")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ 语音识别器初始化异常: {e}")
    
    # 6. TTS管理器
    try:
        from core.tts_manager import TTSManager
        logger.info("正在初始化TTS管理器...")
        tts_manager = TTSManager()
        logger.info("✅ TTS管理器初始化成功")
        success_count += 1
    except Exception as e:
        logger.warning(f"⚠️ TTS管理器初始化异常: {e}")
    
    logger.info(f"✅ 模块初始化完成: {success_count}/6 个模块成功")
    return success_count > 0

def image_to_numpy(image_data):
    """将图片数据转换为numpy数组"""
    try:
        if isinstance(image_data, str):
            image_data = base64.b64decode(image_data)
        
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        return img_bgr
    except Exception as e:
        logger.error(f"图片转换失败: {e}")
        return None

# HTML模板（完整版）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Luna 完整功能测试</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
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
        h1 { text-align: center; color: #333; margin-bottom: 20px; font-size: 28px; }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            background: #f5f5f5;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .tab.active {
            background: #667eea;
            color: white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        video { width: 100%; border-radius: 15px; background: #000; }
        canvas { display: none; }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.3s;
        }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-secondary { background: #f0f0f0; color: #333; }
        .btn-danger { background: #ff6b6b; color: white; }
        .btn-success { background: #51cf66; color: white; }
        .btn:active { transform: scale(0.98); opacity: 0.9; }
        .file-input { display: none; }
        .result-section {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .result-section.active { display: block; }
        .result-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .result-item {
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .result-text { font-size: 15px; color: #333; margin-bottom: 5px; }
        .result-confidence { font-size: 13px; color: #666; }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }
        .badge-success { background: #51cf66; color: white; }
        .badge-warning { background: #ffd43b; color: #333; }
        .badge-danger { background: #ff6b6b; color: white; }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .loading.active { display: block; }
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
        .error.active { display: block; }
        .audio-controls {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .audio-controls button {
            flex: 1;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 Luna 完整功能测试</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('vision')">👁️ 视觉识别</button>
            <button class="tab" onclick="switchTab('voice')">🎤 语音功能</button>
            <button class="tab" onclick="switchTab('comprehensive')">🔍 综合检测</button>
        </div>
        
        <!-- 视觉识别标签页 -->
        <div id="vision-tab" class="tab-content active">
            <video id="video" autoplay playsinline></video>
            <canvas id="canvas"></canvas>
            
            <button class="btn btn-primary" onclick="startCamera()">📷 打开摄像头</button>
            <button class="btn btn-primary" onclick="capturePhoto()" id="captureBtn" style="display:none;">📸 拍照识别</button>
            <button class="btn btn-secondary" onclick="stopCamera()" id="stopBtn" style="display:none;">⏹️ 关闭摄像头</button>
            
            <label for="fileInput" class="btn btn-secondary">
                📁 选择图片
            </label>
            <input type="file" id="fileInput" class="file-input" accept="image/*" onchange="handleFileSelect(event)">
            
            <button class="btn btn-success" onclick="testStepDetection()">🪜 台阶检测</button>
            <button class="btn btn-success" onclick="testSignboardDetection()">🚏 标识牌检测</button>
            <button class="btn btn-danger" onclick="testHazardDetection()">⚠️ 危险检测</button>
        </div>
        
        <!-- 语音功能标签页 -->
        <div id="voice-tab" class="tab-content">
            <h3 style="margin-bottom: 15px;">语音识别</h3>
            <button class="btn btn-primary" onclick="startRecording()">🎤 开始录音</button>
            <button class="btn btn-secondary" onclick="stopRecording()" id="stopRecordBtn" style="display:none;">⏹️ 停止录音</button>
            
            <div id="recordingStatus" style="text-align:center; margin:15px 0; color:#667eea; font-weight:bold; display:none;">
                🔴 正在录音...
            </div>
            
            <h3 style="margin-top: 30px; margin-bottom: 15px;">语音合成</h3>
            <input type="text" id="ttsText" placeholder="输入要合成的文字" style="width:100%; padding:12px; border:2px solid #eee; border-radius:8px; margin-bottom:10px; font-size:16px;">
            <div class="audio-controls">
                <button class="btn btn-success" onclick="testTTS('cheerful')">😊 欢快</button>
                <button class="btn btn-success" onclick="testTTS('calm')">😌 平静</button>
                <button class="btn btn-success" onclick="testTTS('urgent')">⚡ 紧急</button>
            </div>
        </div>
        
        <!-- 综合检测标签页 -->
        <div id="comprehensive-tab" class="tab-content">
            <button class="btn btn-primary" onclick="comprehensiveDetection()">🔍 综合检测</button>
            <p style="margin-top: 15px; color: #666; font-size: 14px;">
                综合检测将同时运行所有视觉检测模块，生成完整的分析报告
            </p>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px;">正在处理中...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result-section" id="resultSection">
            <div class="result-title">检测结果</div>
            <div id="results"></div>
        </div>
    </div>

    <script>
        let stream = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let currentImageBlob = null;
        
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
        }
        
        async function startCamera() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' }
                });
                video.srcObject = stream;
                video.play();
                document.getElementById('captureBtn').style.display = 'block';
                document.getElementById('stopBtn').style.display = 'block';
                document.querySelector('#vision-tab .btn-primary').style.display = 'none';
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
            document.getElementById('captureBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'none';
            document.querySelector('#vision-tab .btn-primary').style.display = 'block';
        }
        
        function capturePhoto() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            canvas.toBlob(function(blob) {
                currentImageBlob = blob;
                sendImage(blob, '/api/recognize');
            }, 'image/jpeg', 0.9);
        }
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                currentImageBlob = file;
                sendImage(file, '/api/recognize');
            }
        }
        
        async function sendImage(imageBlob, endpoint) {
            showLoading();
            const formData = new FormData();
            formData.append('image', imageBlob);
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                } else {
                    showError(data.error || '处理失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        function testStepDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/step');
        }
        
        function testSignboardDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/signboard');
        }
        
        function testHazardDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/hazard');
        }
        
        function comprehensiveDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/comprehensive');
        }
        
        async function startRecording() {
            try {
                const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];
                mediaRecorder = new MediaRecorder(audioStream);
                
                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    await sendAudio(audioBlob);
                };
                
                mediaRecorder.start();
                document.getElementById('stopRecordBtn').style.display = 'block';
                document.getElementById('recordingStatus').style.display = 'block';
            } catch (err) {
                showError('无法访问麦克风: ' + err.message);
            }
        }
        
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                document.getElementById('stopRecordBtn').style.display = 'none';
                document.getElementById('recordingStatus').style.display = 'none';
            }
        }
        
        async function sendAudio(audioBlob) {
            showLoading();
            const formData = new FormData();
            formData.append('audio', audioBlob);
            
            try {
                const response = await fetch('/api/recognize/voice', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.success) {
                    displayResults({ voice_result: data });
                } else {
                    showError(data.error || '识别失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        async function testTTS(style) {
            const text = document.getElementById('ttsText').value;
            if (!text) {
                showError('请输入要合成的文字');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/api/tts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, style })
                });
                const data = await response.json();
                
                if (data.success) {
                    // Edge-TTS返回的是MP3格式
                    const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                    audio.play().catch(err => {
                        showError('播放失败: ' + err.message);
                    });
                } else {
                    showError(data.error || '合成失败');
                }
            } catch (err) {
                showError('网络错误: ' + err.message);
            } finally {
                hideLoading();
            }
        }
        
        function displayResults(data) {
            const results = document.getElementById('results');
            results.innerHTML = '';
            
            // 视觉识别结果
            if (data.detections || data.ocr_results) {
                if (data.ocr_results && data.ocr_results.length > 0) {
                    const div = document.createElement('div');
                    div.innerHTML = '<div class="result-title">📝 识别的文字</div>';
                    data.ocr_results.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'result-item';
                        itemDiv.innerHTML = `
                            <div class="result-text">${item.text}</div>
                            <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                        `;
                        div.appendChild(itemDiv);
                    });
                    results.appendChild(div);
                }
                
                if (data.detections && data.detections.length > 0) {
                    const div = document.createElement('div');
                    div.innerHTML = '<div class="result-title">🎯 检测到的物体</div>';
                    data.detections.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'result-item';
                        itemDiv.innerHTML = `
                            <div class="result-text">${item.class}</div>
                            <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                        `;
                        div.appendChild(itemDiv);
                    });
                    results.appendChild(div);
                }
            }
            
            // 台阶检测结果
            if (data.step_detection) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🪜 台阶检测</div>';
                const itemDiv = document.createElement('div');
                itemDiv.className = 'result-item';
                const step = data.step_detection;
                itemDiv.innerHTML = `
                    <div class="result-text">方向: ${step.direction || '未知'}</div>
                    <div class="result-confidence">置信度: ${(step.confidence * 100).toFixed(1)}%</div>
                `;
                div.appendChild(itemDiv);
                results.appendChild(div);
            }
            
            // 标识牌检测结果
            if (data.signboards && data.signboards.length > 0) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🚏 标识牌检测</div>';
                data.signboards.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.text} <span class="badge badge-success">${item.type}</span></div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    div.appendChild(itemDiv);
                });
                results.appendChild(div);
            }
            
            // 危险检测结果
            if (data.hazards && data.hazards.length > 0) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">⚠️ 危险检测</div>';
                data.hazards.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    const severityClass = item.severity === 'high' || item.severity === 'critical' ? 'badge-danger' : 'badge-warning';
                    itemDiv.innerHTML = `
                        <div class="result-text">${item.type} <span class="badge ${severityClass}">${item.severity}</span></div>
                        <div class="result-confidence">置信度: ${(item.confidence * 100).toFixed(1)}%</div>
                    `;
                    div.appendChild(itemDiv);
                });
                results.appendChild(div);
            }
            
            // 语音识别结果
            if (data.voice_result) {
                const div = document.createElement('div');
                div.innerHTML = '<div class="result-title">🎤 语音识别</div>';
                const itemDiv = document.createElement('div');
                itemDiv.className = 'result-item';
                itemDiv.innerHTML = `<div class="result-text">${data.voice_result.text || '未识别到语音'}</div>`;
                div.appendChild(itemDiv);
                results.appendChild(div);
            }
            
            if (results.innerHTML === '') {
                results.innerHTML = '<div class="result-item">未识别到内容</div>';
            }
            
            document.getElementById('resultSection').classList.add('active');
        }
        
        function showLoading() {
            document.getElementById('loading').classList.add('active');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('active');
        }
        
        function showError(message) {
            const error = document.getElementById('error');
            error.textContent = message;
            error.classList.add('active');
            setTimeout(() => error.classList.remove('active'), 5000);
        }
    </script>
</body>
</html>
"""

# API路由
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """基础视觉识别"""
    try:
        if vision_engine is None:
            return jsonify({'success': False, 'error': '视觉引擎未初始化'}), 500
        
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return jsonify({'success': False, 'error': '图片格式错误'}), 400
        
        results = vision_engine.detect_and_recognize(image_np)
        
        return jsonify({
            'success': True,
            'detections': results.get('detections', []),
            'ocr_results': results.get('ocr_results', []),
            'processing_time': results.get('processing_time', 0)
        })
    except Exception as e:
        logger.error(f"识别错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/detect/step', methods=['POST'])
def detect_step():
    """台阶检测"""
    try:
        if step_detector is None:
            return jsonify({'success': False, 'error': '台阶检测器未初始化'}), 500
        
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return jsonify({'success': False, 'error': '图片格式错误'}), 400
        
        result = step_detector.detect_step(image_np)
        
        return jsonify({
            'success': True,
            'step_detection': result if result else {'detected': False}
        })
    except Exception as e:
        logger.error(f"台阶检测错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/detect/signboard', methods=['POST'])
def detect_signboard():
    """标识牌检测"""
    try:
        if signboard_detector is None:
            return jsonify({'success': False, 'error': '标识牌检测器未初始化'}), 500
        
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return jsonify({'success': False, 'error': '图片格式错误'}), 400
        
        results = signboard_detector.detect_signboards(image_np)
        
        return jsonify({
            'success': True,
            'signboards': [r.to_dict() for r in results] if results else []
        })
    except Exception as e:
        logger.error(f"标识牌检测错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/detect/hazard', methods=['POST'])
def detect_hazard():
    """危险检测"""
    try:
        if hazard_detector is None:
            return jsonify({'success': False, 'error': '危险检测器未初始化'}), 500
        
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return jsonify({'success': False, 'error': '图片格式错误'}), 400
        
        results = hazard_detector.detect_hazards(image_np)
        
        return jsonify({
            'success': True,
            'hazards': [r.to_dict() for r in results] if results else []
        })
    except Exception as e:
        logger.error(f"危险检测错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/detect/comprehensive', methods=['POST'])
def comprehensive_detection():
    """综合检测"""
    try:
        file = request.files['image']
        image_np = image_to_numpy(file.read())
        if image_np is None:
            return jsonify({'success': False, 'error': '图片格式错误'}), 400
        
        results = {}
        
        # 基础视觉识别
        if vision_engine:
            vision_results = vision_engine.detect_and_recognize(image_np)
            results.update(vision_results)
        
        # 台阶检测
        if step_detector:
            step_result = step_detector.detect_step(image_np)
            if step_result:
                results['step_detection'] = step_result
        
        # 标识牌检测
        if signboard_detector:
            signboards = signboard_detector.detect_signboards(image_np)
            results['signboards'] = [r.to_dict() for r in signboards] if signboards else []
        
        # 危险检测
        if hazard_detector:
            hazards = hazard_detector.detect_hazards(image_np)
            results['hazards'] = [r.to_dict() for r in hazards] if hazards else []
        
        return jsonify({
            'success': True,
            **results
        })
    except Exception as e:
        logger.error(f"综合检测错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recognize/voice', methods=['POST'])
def recognize_voice():
    """语音识别"""
    try:
        if whisper_recognizer is None:
            return jsonify({'success': False, 'error': '语音识别器未初始化'}), 500
        
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': '未上传音频'}), 400
        
        # 保存临时文件
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # 加载模型（如果未加载）
            if not whisper_recognizer.is_loaded:
                whisper_recognizer.load_model()
            
            # 识别
            text, details = whisper_recognizer.recognize_from_file(tmp_path)
            
            return jsonify({
                'success': True,
                'text': text,
                'details': details
            })
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    except Exception as e:
        logger.error(f"语音识别错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """语音合成"""
    try:
        import asyncio
        import edge_tts
        
        data = request.json
        text = data.get('text', '')
        style_str = data.get('style', 'cheerful')
        
        if not text:
            return jsonify({'success': False, 'error': '未提供文本'}), 400
        
        # 风格映射
        style_map = {
            'cheerful': ('zh-CN-XiaoxiaoNeural', 1.2),
            'calm': ('zh-CN-XiaoyiNeural', 0.95),
            'urgent': ('zh-CN-XiaoxiaoNeural', 1.5),
            'empathetic': ('zh-CN-YunxiNeural', 0.9),
            'angry': ('zh-CN-YunjianNeural', 1.3),
            'gentle': ('zh-CN-YunxiNeural', 0.85)
        }
        
        voice, rate = style_map.get(style_str, style_map['cheerful'])
        
        # 生成语音
        async def generate_audio():
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        
        # 运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_data = loop.run_until_complete(generate_audio())
        loop.close()
        
        if audio_data:
            # 转换为base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            return jsonify({
                'success': True,
                'audio': audio_base64
            })
        else:
            return jsonify({'success': False, 'error': '语音合成失败'}), 500
    except Exception as e:
        logger.error(f"TTS错误: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'modules': {
            'vision_engine': vision_engine is not None,
            'step_detector': step_detector is not None,
            'signboard_detector': signboard_detector is not None,
            'hazard_detector': hazard_detector is not None,
            'whisper_recognizer': whisper_recognizer is not None,
            'tts_manager': tts_manager is not None
        }
    })

if __name__ == '__main__':
    # 初始化所有模块
    if not init_all_modules():
        logger.warning("部分模块初始化失败，但服务器仍会启动")
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Luna 完整功能测试服务器启动中...")
    logger.info(f"📱 手机访问地址: http://<你的Mac IP>:{port}")
    logger.info(f"💻 本地访问地址: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

