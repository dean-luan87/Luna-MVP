// test_panel.js
// Luna Badge v1.2.0 测试面板核心逻辑

(function() {
    'use strict';

    let cameraStream = null;
    let videoElement = null;
    let overlayCanvas = null;
    let ctx = null;
    let fpsCounter = 0;
    let lastFpsTime = Date.now();

    // ==================== 初始化 ====================
    function init() {
        videoElement = document.getElementById('testVideo');
        overlayCanvas = document.getElementById('overlayCanvas');
        if (overlayCanvas) {
            ctx = overlayCanvas.getContext('2d');
        }

        // 启动FPS监控
        setInterval(updateFPS, 1000);

        // 监听NavigationFSM状态变化
        if (window.NavigationFSM) {
            setInterval(updateNavState, 500);
        }

        // 监听EventDispatcher事件
        if (window.EventDispatcher) {
            setupEventListeners();
        }

        console.log('✅ 测试面板已初始化');
    }

    // ==================== FPS监控 ====================
    function updateFPS() {
        const now = Date.now();
        const elapsed = (now - lastFpsTime) / 1000;
        const fps = Math.round(fpsCounter / elapsed);
        
        const fpsElement = document.getElementById('fpsValue');
        if (fpsElement) {
            fpsElement.textContent = fps;
        }
        
        fpsCounter = 0;
        lastFpsTime = now;
    }

    // ==================== 导航状态更新 ====================
    function updateNavState() {
        if (!window.NavigationFSM) return;

        try {
            const state = window.NavigationFSM.getState ? window.NavigationFSM.getState() : 'IDLE';
            const stateElement = document.getElementById('navState');
            if (stateElement) {
                stateElement.textContent = state;
            }
        } catch (e) {
            // 忽略错误
        }
    }

    // ==================== 事件监听 ====================
    function setupEventListeners() {
        // 监听场景描述事件
        if (window.EventDispatcher && window.EventDispatcher.subscribe) {
            window.EventDispatcher.subscribe('SCENE_DESCRIPTION', (data) => {
                addLog('eventLog', `场景描述: ${data.summary || '无'}`, 'info');
            });

            window.EventDispatcher.subscribe('NAV_GUIDANCE', (data) => {
                addLog('eventLog', `导航指引: ${JSON.stringify(data)}`, 'info');
            });

            window.EventDispatcher.subscribe('NAV_ERROR', (data) => {
                addLog('errorCodeLog', `错误码: ${data.code || 'unknown'} - ${data.message || ''}`, 'error');
            });
        }
    }

    // ==================== 摄像头控制 ====================
    window.startCamera = async function() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: true,
                audio: false 
            });
            cameraStream = stream;
            if (videoElement) {
                videoElement.srcObject = stream;
            }
            
            const statusElement = document.getElementById('cameraStatus');
            if (statusElement) {
                statusElement.textContent = '运行中';
                statusElement.className = 'status-value status-ready';
            }

            addLog('eventLog', '摄像头已启动', 'success');
        } catch (error) {
            addLog('eventLog', `摄像头启动失败: ${error.message}`, 'error');
        }
    };

    window.stopCamera = function() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        if (videoElement) {
            videoElement.srcObject = null;
        }

        const statusElement = document.getElementById('cameraStatus');
        if (statusElement) {
            statusElement.textContent = '未启动';
            statusElement.className = 'status-value status-off';
        }

        addLog('eventLog', '摄像头已停止', 'info');
    };

    // ==================== 捕获帧 ====================
    window.captureFrame = async function() {
        if (!videoElement || !videoElement.videoWidth) {
            addLog('eventLog', '请先启动摄像头', 'warning');
            return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0);

        canvas.toBlob(async (blob) => {
            // 转换为base64
            const reader = new FileReader();
            reader.onloadend = async () => {
                const base64 = reader.result.split(',')[1];
                
                // 调用场景描述API
                if (window.VisionBridge && window.VisionBridge.describeScene) {
                    try {
                        const result = await window.VisionBridge.describeScene(base64);
                        if (result && result.success) {
                            updateSceneDescription(result.data);
                            drawDetections(result.data.objects || []);
                        }
                    } catch (error) {
                        addLog('eventLog', `场景描述失败: ${error.message}`, 'error');
                    }
                }
            };
            reader.readAsDataURL(blob);
        });

        fpsCounter++;
    };

    // ==================== 更新场景描述 ====================
    function updateSceneDescription(data) {
        const box = document.getElementById('sceneDescriptionBox');
        if (box) {
            box.innerHTML = `
                <div class="summary">${data.summary || '无描述'}</div>
                <pre class="objects">${JSON.stringify(data.objects || [], null, 2)}</pre>
            `;
        }

        const jsonOutput = document.getElementById('jsonOutput');
        if (jsonOutput) {
            jsonOutput.textContent = JSON.stringify(data, null, 2);
        }
    }

    // ==================== 绘制检测框 ====================
    function drawDetections(objects) {
        if (!overlayCanvas || !ctx || !videoElement) return;

        overlayCanvas.width = videoElement.videoWidth;
        overlayCanvas.height = videoElement.videoHeight;

        ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

        objects.forEach(obj => {
            const bbox = obj.bbox || [];
            if (bbox.length >= 4) {
                ctx.strokeStyle = '#00ff00';
                ctx.lineWidth = 2;
                ctx.strokeRect(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]);
                
                ctx.fillStyle = '#00ff00';
                ctx.font = '14px Arial';
                ctx.fillText(obj.label || 'unknown', bbox[0], bbox[1] - 5);
            }
        });
    }

    // ==================== 导航事件触发 ====================
    window.triggerNavEvent = function(eventType) {
        if (!window.NavigationFSM) {
            addLog('eventLog', 'NavigationFSM未初始化', 'error');
            return;
        }

        try {
            if (window.NavigationFSM.handleEvent) {
                window.NavigationFSM.handleEvent({
                    type: eventType,
                    timestamp: Date.now()
                });
                addLog('eventLog', `触发导航事件: ${eventType}`, 'info');
            }
        } catch (error) {
            addLog('eventLog', `导航事件失败: ${error.message}`, 'error');
        }
    };

    // ==================== 串联测试 ====================
    window.runFullFlowTest = async function() {
        const progress = document.getElementById('testProgress');
        if (progress) {
            progress.textContent = '🚀 开始全流程测试...';
        }

        addLog('eventLog', '开始全流程测试', 'info');

        // 1. 启动摄像头
        await window.startCamera();
        await new Promise(resolve => setTimeout(resolve, 1000));

        // 2. 捕获帧并描述场景
        window.captureFrame();
        await new Promise(resolve => setTimeout(resolve, 2000));

        // 3. 触发导航事件
        window.triggerNavEvent('go_straight');
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (progress) {
            progress.textContent = '✅ 全流程测试完成';
        }
        addLog('eventLog', '全流程测试完成', 'success');
    };

    window.runHazardNavTest = async function() {
        const progress = document.getElementById('testProgress');
        if (progress) {
            progress.textContent = '⚠️ 开始危险检测测试...';
        }

        addLog('eventLog', '开始危险检测测试', 'info');

        // 1. 启动摄像头
        await window.startCamera();
        await new Promise(resolve => setTimeout(resolve, 1000));

        // 2. 捕获帧
        window.captureFrame();
        await new Promise(resolve => setTimeout(resolve, 2000));

        // 3. 触发危险响应
        window.triggerNavEvent('stop');
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (progress) {
            progress.textContent = '✅ 危险检测测试完成';
        }
        addLog('eventLog', '危险检测测试完成', 'success');
    };

    window.runQuickTest = async function() {
        const progress = document.getElementById('testProgress');
        if (progress) {
            progress.textContent = '⚡ 开始10秒快速测试...';
        }

        const startTime = Date.now();
        const interval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const remaining = 10 - elapsed;
            
            if (progress) {
                progress.textContent = `⚡ 快速测试进行中... (${remaining}秒)`;
            }

            if (remaining <= 0) {
                clearInterval(interval);
                if (progress) {
                    progress.textContent = '✅ 快速测试完成';
                }
                addLog('eventLog', '快速测试完成', 'success');
            }
        }, 1000);

        // 执行测试
        await window.startCamera();
        await new Promise(resolve => setTimeout(resolve, 2000));
        window.captureFrame();
    };

    // ==================== 日志工具 ====================
    function addLog(containerId, message, type = 'info') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        
        container.insertBefore(entry, container.firstChild);
        
        // 限制日志数量
        while (container.children.length > 50) {
            container.removeChild(container.lastChild);
        }
    }

    // ==================== 页面加载完成后初始化 ====================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // 导出全局函数
    window.testPanel = {
        addLog: addLog,
        updateSceneDescription: updateSceneDescription,
        drawDetections: drawDetections
    };

    console.log('✅ 测试面板脚本已加载');
})();



