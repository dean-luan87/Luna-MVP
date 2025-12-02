
        // 全局错误处理 - 确保错误不会阻止页面运行
        window.addEventListener('error', function(e) {
            console.error('全局JavaScript错误:', e.error, e.message, e.filename, e.lineno);
            // 显示错误到页面
            try {
                const errorDiv = document.getElementById('error');
                if (errorDiv) {
                    errorDiv.textContent = 'JavaScript错误: ' + (e.message || '未知错误');
                    errorDiv.classList.add('active');
                }
            } catch (err) {
                console.error('无法显示错误:', err);
            }
        });
        
        // 确保页面加载完成
        console.log('✅ JavaScript开始执行');
        
        let stream = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let currentImageBlob = null;
        let visualNavigationInterval = null;  // 视觉导航定时器
        let productModeActive = false;  // 产品模式状态
        let voiceListeningInterval = null;  // 语音监听定时器
        
        // 全局音频上下文和音量控制
        let globalAudioContext = null;
        let currentAudioVolume = 1.0;  // 当前音量（0.0-1.0）
        let audioUnlocked = false;  // 音频是否已解锁（通过用户交互）
        
        // 初始化音频上下文（用于解锁音频播放）
        function initAudioContext() {
            try {
                if (!globalAudioContext) {
                    globalAudioContext = new (window.AudioContext || window.webkitAudioContext)();
                }
                return globalAudioContext;
            } catch (e) {
                console.warn('音频上下文初始化失败:', e);
                return null;
            }
        }
        
        // 解锁音频播放（需要在用户交互时调用）
        async function unlockAudio() {
            if (audioUnlocked) return true;
            
            try {
                const ctx = initAudioContext();
                if (!ctx) return false;
                
                // 创建静音音频并播放，用于解锁音频权限
                const buffer = ctx.createBuffer(1, 1, 22050);
                const source = ctx.createBufferSource();
                source.buffer = buffer;
                source.connect(ctx.destination);
                source.start(0);
                
                // 等待一小段时间确保音频已解锁
                await new Promise(resolve => setTimeout(resolve, 100));
                
                audioUnlocked = true;
                console.log('✅ 音频已解锁');
                return true;
            } catch (e) {
                console.warn('音频解锁失败:', e);
                return false;
            }
        }
        
        // 调整音量（全局函数，供按钮调用）- 必须先定义
        function adjustVolume(delta) {
            try {
                currentAudioVolume = Math.max(0.0, Math.min(1.0, currentAudioVolume + delta));
                
                // 更新所有正在播放的音频音量
                if (window.currentPlayingAudios) {
                    window.currentPlayingAudios.forEach(audio => {
                        if (audio && !audio.paused) {
                            audio.volume = currentAudioVolume;
                        }
                    });
                }
                
                // 更新音量显示
                const volumeDisplay = document.getElementById('volumeDisplay');
                if (volumeDisplay) {
                    volumeDisplay.textContent = Math.round(currentAudioVolume * 100) + '%';
                }
                
                // 显示音量提示
                if (typeof showVolumeIndicator === 'function') {
                    showVolumeIndicator(currentAudioVolume);
                }
                console.log(`🔊 音量: ${Math.round(currentAudioVolume * 100)}%`);
            } catch (e) {
                console.error('调整音量失败:', e);
            }
        }
        
        // 音量键事件监听（移动端）
        function setupVolumeControls() {
            try {
                // 监听音量键（通过媒体键事件）
                document.addEventListener('keydown', (e) => {
                    try {
                        // 音量上键（某些浏览器）
                        if (e.key === 'VolumeUp' || e.code === 'VolumeUp') {
                            e.preventDefault();
                            if (typeof adjustVolume === 'function') {
                                adjustVolume(0.1);
                            }
                        }
                        // 音量下键
                        else if (e.key === 'VolumeDown' || e.code === 'VolumeDown') {
                            e.preventDefault();
                            if (typeof adjustVolume === 'function') {
                                adjustVolume(-0.1);
                            }
                        }
                    } catch (err) {
                        console.error('音量键处理错误:', err);
                    }
                });
                
                // 注意：Media Session API 不支持音量控制动作（volumeup/volumedown）
                // 音量控制已通过键盘事件监听实现（见 setupVolumeControls 函数）
                // 如果需要媒体控制，可以使用支持的标准动作：'play', 'pause', 'nexttrack', 'previoustrack', 'seekbackward', 'seekforward'
                // if ('mediaSession' in navigator) {
                //     try {
                //         // 只设置支持的标准媒体动作
                //         // navigator.mediaSession.setActionHandler('play', () => { ... });
                //         // navigator.mediaSession.setActionHandler('pause', () => { ... });
                //     } catch (err) {
                //         console.warn('媒体会话API不支持:', err);
                //     }
                // }
                // 注意：不监听touchstart事件，避免干扰页面正常操作
            } catch (e) {
                console.error('设置音量控制失败:', e);
            }
        }
        
        // 显示音量指示器
        function showVolumeIndicator(volume) {
            const indicator = document.getElementById('volumeIndicator') || createVolumeIndicator();
            const percentage = Math.round(volume * 100);
            indicator.textContent = `🔊 ${percentage}%`;
            indicator.style.display = 'block';
            indicator.style.opacity = '1';
            
            setTimeout(() => {
                indicator.style.opacity = '0';
                setTimeout(() => {
                    indicator.style.display = 'none';
                }, 300);
            }, 1500);
        }
        
        // 创建音量指示器
        function createVolumeIndicator() {
            const indicator = document.createElement('div');
            indicator.id = 'volumeIndicator';
            indicator.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 20px 40px;
                border-radius: 10px;
                font-size: 24px;
                font-weight: bold;
                z-index: 10000;
                display: none;
                transition: opacity 0.3s;
                pointer-events: none;
            `;
            document.body.appendChild(indicator);
            return indicator;
        }
        
        // 初始化音频功能（延迟执行，避免阻塞页面）
        function initAudioFeatures() {
            try {
                // 延迟初始化，确保所有函数都已定义
                setTimeout(() => {
                    try {
                        if (typeof initAudioContext === 'function') {
                            initAudioContext();
                        }
                        if (typeof setupVolumeControls === 'function') {
                            setupVolumeControls();
                        }
                        
                        // 在用户首次交互时解锁音频
                        const unlockOnInteraction = () => {
                            try {
                                if (typeof unlockAudio === 'function') {
                                    unlockAudio();
                                }
                                document.removeEventListener('click', unlockOnInteraction);
                                document.removeEventListener('touchstart', unlockOnInteraction);
                            } catch (e) {
                                console.error('解锁音频失败:', e);
                            }
                        };
                        document.addEventListener('click', unlockOnInteraction, { once: true });
                        document.addEventListener('touchstart', unlockOnInteraction, { once: true });
                    } catch (e) {
                        console.error('初始化音频功能失败:', e);
                    }
                }, 200);
            } catch (e) {
                console.error('音频功能初始化失败:', e);
            }
        }
        
        // 在页面加载时初始化（简化版，避免阻塞页面）
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAudioFeatures);
        } else {
            // DOM已经加载完成
            setTimeout(initAudioFeatures, 100);
        }
        
        // 全局音频元素追踪
        window.currentPlayingAudios = window.currentPlayingAudios || [];
        let lastVoiceRecognitionTime = 0;  // 上次语音识别时间
        let realtimeLogsInterval = null;  // 实时日志定时器
        let lastLogTimestamp = null;  // 上次获取的日志时间戳
        
        // 获取DOM元素的辅助函数（延迟获取，避免在元素创建前访问）
        function getVideo() {
            return document.getElementById('video');
        }
        
        function getCanvas() {
            return document.getElementById('canvas');
        }
        
        // 为了兼容旧代码，保留变量引用（延迟初始化）
        let video = null;
        let canvas = null;
        
        function initDOMElements() {
            if (!video) video = getVideo();
            if (!canvas) canvas = getCanvas();
        }
        
        // 在DOM加载后初始化元素引用
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initDOMElements);
        } else {
            initDOMElements();
        }
        
        // 在使用video和canvas的函数中，确保它们已初始化
        function ensureDOMElements() {
            if (!video) video = getVideo();
            if (!canvas) canvas = getCanvas();
        }
        
        function switchTab(tabName, event) {
            // 确保函数暴露到全局作用域
            window.switchTab = switchTab;
            console.log('switchTab被调用:', tabName, event);
            // 防止默认行为
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
            try {
                // 移除所有标签的active状态
                const tabs = document.querySelectorAll('.tab');
                const contents = document.querySelectorAll('.tab-content');
                console.log('找到标签数:', tabs.length, '内容数:', contents.length);
                
                tabs.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                
                // 添加当前标签的active状态
                let clickedTab = null;
                if (event && event.target) {
                    clickedTab = event.target;
                    console.log('使用event.target');
                } else {
                    // 如果没有event对象，通过tabName查找对应的按钮
                    clickedTab = document.querySelector(`.tab[onclick*="${tabName}"]`);
                    console.log('通过选择器查找:', clickedTab);
                }
                
                if (clickedTab) {
                    clickedTab.classList.add('active');
                    console.log('标签已激活');
                } else {
                    console.warn('未找到对应的标签按钮');
                }
                
                // 显示对应的内容
                const contentId = tabName + '-tab';
                const content = document.getElementById(contentId);
                console.log('查找内容:', contentId, content);
                if (content) {
                    content.classList.add('active');
                    console.log('内容已显示');
                } else {
                    console.error('未找到内容区域:', contentId);
                }
            } catch (e) {
                console.error('切换标签页失败:', e, e.stack);
                // 即使出错也尝试显示内容
                try {
                    const contentId = tabName + '-tab';
                    const content = document.getElementById(contentId);
                    if (content) {
                        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                        content.classList.add('active');
                    }
                } catch (err) {
                    console.error('恢复失败:', err);
                }
            }
        }
        
        async function startCamera() {
            try {
                ensureDOMElements();
                const videoEl = getVideo();
                if (!videoEl) {
                    showError('无法找到视频元素');
                    return;
                }
                
                // 检测Safari浏览器
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                const isSecureContext = window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                
                // Safari特殊检查
                if ((isSafari || isIOS) && !isSecureContext) {
                    showError(`⚠️ Safari浏览器需要HTTPS才能访问摄像头。\n\n解决方案：\n1. 使用"选择图片"功能代替摄像头\n2. 或配置HTTPS访问`);
                    return;
                }
                
                // 检查浏览器支持
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    showError(`您的浏览器不支持摄像头访问。\n\n建议：使用"选择图片"功能上传照片进行识别。`);
                    return;
                }
                
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        facingMode: 'environment',
                        width: { ideal: 1280 },
                        height: { ideal: 720 }
                    }
                });
                videoEl.srcObject = stream;
                video = videoEl;  // 更新引用
                videoEl.setAttribute('playsinline', 'true');
                videoEl.setAttribute('webkit-playsinline', 'true');
                await videoEl.play();
                document.getElementById('captureBtn').style.display = 'block';
                document.getElementById('stopBtn').style.display = 'block';
                document.querySelector('#vision-tab .btn-primary').style.display = 'none';
                
                // 如果产品模式已激活，自动启动视觉导航和语音监听
                if (productModeActive) {
                    setTimeout(() => {
                        startVisualNavigation();
                        startVoiceListening();
                    }, 1000);
                }
            } catch (err) {
                let errorMsg = '无法访问摄像头: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问摄像头权限（在Safari设置中允许）';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到摄像头设备';
                } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
                    errorMsg += '摄像头被其他应用占用，请关闭其他应用后重试';
                } else if (err.name === 'OverconstrainedError') {
                    errorMsg += '摄像头不支持请求的配置';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                errorMsg += '\\n\\n💡 提示：可以使用"选择图片"功能上传照片';
                showError(errorMsg);
            }
        }
        
        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            ensureDOMElements();
            const videoEl = getVideo();
            if (videoEl) {
                videoEl.srcObject = null;
            }
            document.getElementById('captureBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'none';
            document.querySelector('#vision-tab .btn-primary').style.display = 'block';
        }
        
        function capturePhoto() {
            ensureDOMElements();
            const videoEl = getVideo();
            const canvasEl = getCanvas();
            if (!videoEl || !canvasEl) {
                showError('无法找到视频或画布元素');
                return;
            }
            canvasEl.width = videoEl.videoWidth;
            canvasEl.height = videoEl.videoHeight;
            const ctx = canvasEl.getContext('2d');
            ctx.drawImage(videoEl, 0, 0);
            canvasEl.toBlob(function(blob) {
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
        
        function testFacilityDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/facility');
        }
        
        function testTrafficLightDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/traffic_light');
        }
        
        function testCrowdDensityDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/crowd_density');
        }
        
        function testQueueDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/queue');
        }
        
        function testDoorplateDetection() {
            if (!currentImageBlob) {
                showError('请先拍照或选择图片');
                return;
            }
            sendImage(currentImageBlob, '/api/detect/doorplate');
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
                // 检测Safari浏览器
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                const isSecureContext = window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                
                // Safari特殊检查
                if ((isSafari || isIOS) && !isSecureContext) {
                    showError(`⚠️ Safari浏览器需要HTTPS才能访问麦克风。\n\n当前功能受限，建议使用桌面浏览器测试。`);
                    return;
                }
                
                // 检查浏览器支持
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    showError(`您的浏览器不支持麦克风访问。\n\nSafari在iOS上可能需要HTTPS。`);
                    return;
                }
                
                const audioStream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        sampleRate: 16000
                    }
                });
                audioChunks = [];
                
                // 检查MediaRecorder支持（Safari支持有限）
                if (!window.MediaRecorder) {
                    showError(`您的浏览器不支持录音功能。\n\nSafari的MediaRecorder支持有限，建议使用Chrome浏览器。`);
                    return;
                }
                
                // Safari需要指定MIME类型
                let options = {};
                if (MediaRecorder.isTypeSupported('audio/webm')) {
                    options = { mimeType: 'audio/webm' };
                } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                    options = { mimeType: 'audio/mp4' };
                } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
                    options = { mimeType: 'audio/ogg' };
                }
                
                mediaRecorder = new MediaRecorder(audioStream, options);
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data && event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                mediaRecorder.onstop = async () => {
                    const mimeType = mediaRecorder.mimeType || 'audio/webm';
                    const audioBlob = new Blob(audioChunks, { type: mimeType });
                    await sendAudio(audioBlob);
                };
                
                mediaRecorder.onerror = (event) => {
                    showError('录音过程中出错: ' + (event.error?.message || '未知错误'));
                };
                
                mediaRecorder.start();
                document.getElementById('stopRecordBtn').style.display = 'block';
                document.getElementById('recordingStatus').style.display = 'block';
            } catch (err) {
                let errorMsg = '无法访问麦克风: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问麦克风权限（在Safari设置 > 网站设置中允许）';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到麦克风设备';
                } else if (err.name === 'NotReadableError') {
                    errorMsg += '麦克风被其他应用占用';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                if (isIOS || isSafari) {
                    errorMsg += '\\n\\n💡 Safari在iOS上需要HTTPS才能使用麦克风';
                }
                showError(errorMsg);
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
                
                if (step.detected === false || !step.direction) {
                    // 未检测到台阶
                    itemDiv.innerHTML = `
                        <div class="result-text" style="color: #666;">${step.message || '未检测到台阶'}</div>
                        <div style="margin-top: 10px; font-size: 12px; color: #999;">
                            可能原因：<br>
                            • 图片中没有台阶/楼梯<br>
                            • YOLO模型未加载或加载失败<br>
                            • 台阶特征不明显
                        </div>
                    `;
                } else {
                    // 检测到台阶
                    itemDiv.innerHTML = `
                        <div class="result-text">方向: ${step.direction || '未知'}</div>
                        <div class="result-confidence">置信度: ${(step.confidence * 100).toFixed(1)}%</div>
                        ${step.steps_count ? `<div style="margin-top: 5px;">台阶数量: ${step.steps_count}</div>` : ''}
                        ${step.height_cm ? `<div style="margin-top: 5px;">高度: ${step.height_cm}cm</div>` : ''}
                    `;
                }
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
                
                const voiceData = data.voice_result;
                const confidence = voiceData.details?.confidence || 0;
                const confidencePercent = (confidence * 100).toFixed(1);
                const confidenceColor = confidence > 0.7 ? '#51cf66' : confidence > 0.5 ? '#ffd43b' : '#ff6b6b';
                
                itemDiv.innerHTML = `
                    <div class="result-text">${voiceData.text || '未识别到语音'}</div>
                    <div style="margin-top: 8px;">
                        <span style="font-size: 13px; color: #666;">置信度: </span>
                        <span style="font-size: 14px; font-weight: bold; color: ${confidenceColor};">
                            ${confidencePercent}%
                        </span>
                        ${voiceData.details?.language ? `<span style="font-size: 12px; color: #999; margin-left: 10px;">语言: ${voiceData.details.language}</span>` : ''}
                    </div>
                    ${confidence < 0.5 ? '<div style="margin-top: 5px; font-size: 12px; color: #ff6b6b;">⚠️ 识别置信度较低，建议在安静环境下清晰说话</div>' : ''}
                `;
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
            console.log('showError被调用:', message);
            try {
                const error = document.getElementById('error');
                if (!error) {
                    console.error('未找到error元素');
                    alert('错误: ' + message);  // 备用方案
                    return;
                }
                error.textContent = message;
                error.classList.add('active');
                setTimeout(() => error.classList.remove('active'), 5000);
            } catch (e) {
                console.error('showError失败:', e);
                alert('错误: ' + message);  // 备用方案
            }
        }
        
        // 字符计数
        document.addEventListener('DOMContentLoaded', function() {
            const ttsText = document.getElementById('ttsText');
            const charCount = document.getElementById('charCount');
            if (ttsText && charCount) {
                ttsText.addEventListener('input', function() {
                    const length = this.value.length;
                    charCount.textContent = length;
                    if (length > 5000) {
                        charCount.style.color = '#ff6b6b';
                    } else if (length > 4500) {
                        charCount.style.color = '#ffd43b';
                    } else {
                        charCount.style.color = '#666';
                    }
                });
            }
        });
        
        // 导航相关函数
        async function planRoute() {
            const start = document.getElementById('navStart').value.trim();
            const destinationsStr = document.getElementById('navDestinations').value.trim();
            
            if (!start || !destinationsStr) {
                showError('请填写起点和目的地');
                return;
            }
            
            const destinations = destinationsStr.split(',').map(d => d.trim()).filter(d => d);
            
            showLoading();
            try {
                const response = await fetch('/api/navigation/plan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ start, destinations })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    // 保存路径规划结果，供导航使用
                    window.lastRouteResult = data.route;
                    displayNavigationResult('路径规划结果', data.route);
                } else {
                    showError('路径规划失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('路径规划错误: ' + err.message);
            }
        }
        
        async function loadAvailablePaths() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/paths');
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('可用路径列表', data.paths);
                } else {
                    showError('获取路径列表失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取路径列表错误: ' + err.message);
            }
        }
        
        async function startNavigation() {
            const destination = document.getElementById('navDestination').value.trim();
            
            if (!destination) {
                showError('请填写目的地');
                return;
            }
            
            // 如果之前有路径规划结果，使用路径段
            let routeSegments = null;
            const lastRouteResult = window.lastRouteResult;
            if (lastRouteResult && lastRouteResult.segments) {
                routeSegments = lastRouteResult.segments;
            }
            
            showLoading();
            try {
                const response = await fetch('/api/navigation/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        destination,
                        route_segments: routeSegments
                    })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已启动', data.status);
                    // 如果TTS可用，会自动播报开始导航
                } else {
                    showError('启动导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('启动导航错误: ' + err.message);
            }
        }
        
        async function pauseNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/pause', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: '用户暂停' })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已暂停', data.status);
                } else {
                    showError('暂停导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('暂停导航错误: ' + err.message);
            }
        }
        
        async function resumeNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/resume', {
                    method: 'POST'
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已恢复', data.status);
                } else {
                    showError('恢复导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('恢复导航错误: ' + err.message);
            }
        }
        
        async function cancelNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/cancel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason: '用户取消' })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已取消', data.status);
                } else {
                    showError('取消导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('取消导航错误: ' + err.message);
            }
        }
        
        async function completeNavigation() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/complete', {
                    method: 'POST'
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航已完成', data.status);
                } else {
                    showError('完成导航失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('完成导航错误: ' + err.message);
            }
        }
        
        async function getNavigationStatus() {
            showLoading();
            try {
                const response = await fetch('/api/navigation/status');
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('导航状态', data.status || '当前没有进行中的导航');
                } else {
                    showError('获取导航状态失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取导航状态错误: ' + err.message);
            }
        }
        
        async function updatePosition() {
            const lat = parseFloat(document.getElementById('navLat').value);
            const lng = parseFloat(document.getElementById('navLng').value);
            
            if (isNaN(lat) || isNaN(lng)) {
                showError('请填写有效的经纬度');
                return;
            }
            
            // 尝试获取当前摄像头画面进行障碍检测
            let imageData = null;
            ensureDOMElements();
            const videoEl = getVideo();
            const canvasEl = getCanvas();
            if (videoEl && videoEl.srcObject) {
                try {
                    canvasEl.width = videoEl.videoWidth;
                    canvasEl.height = videoEl.videoHeight;
                    const ctx = canvasEl.getContext('2d');
                    ctx.drawImage(videoEl, 0, 0);
                    imageData = canvasEl.toDataURL('image/jpeg', 0.8);
                } catch (e) {
                    console.log('无法获取摄像头画面:', e);
                }
            }
            
            showLoading();
            try {
                const requestBody = { lat, lng };
                if (imageData) {
                    requestBody.image = imageData;
                }
                
                const response = await fetch('/api/navigation/update_position', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    const result = {
                        status: data.status,
                        is_idle: data.is_idle ? '是（静止）' : '否（移动中）'
                    };
                    if (data.detected_hazards && data.detected_hazards.length > 0) {
                        result.detected_hazards = data.detected_hazards;
                        result.message = '检测到障碍，已自动播报提示';
                    }
                    displayNavigationResult('位置已更新', result);
                } else {
                    showError('更新位置失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('更新位置错误: ' + err.message);
            }
        }
        
        function getCurrentLocation() {
            if (!navigator.geolocation) {
                showError('您的浏览器不支持GPS定位');
                return;
            }
            
            showLoading();
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    document.getElementById('navLat').value = lat.toFixed(6);
                    document.getElementById('navLng').value = lng.toFixed(6);
                    hideLoading();
                    showSuccess('已获取当前位置: ' + lat.toFixed(6) + ', ' + lng.toFixed(6));
                },
                (error) => {
                    hideLoading();
                    let errorMsg = '获取位置失败: ';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMsg += '用户拒绝了位置权限';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMsg += '位置信息不可用';
                            break;
                        case error.TIMEOUT:
                            errorMsg += '获取位置超时';
                            break;
                        default:
                            errorMsg += '未知错误';
                    }
                    showError(errorMsg);
                }
            );
        }
        
        function displayNavigationResult(title, data) {
            const results = document.getElementById('results');
            results.innerHTML = '';
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'result-title';
            titleDiv.textContent = title;
            results.appendChild(titleDiv);
            
            const dataDiv = document.createElement('div');
            dataDiv.className = 'result-item';
            dataDiv.innerHTML = '<pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 13px;">' + JSON.stringify(data, null, 2) + '</pre>';
            results.appendChild(dataDiv);
            
            document.getElementById('resultSection').classList.add('active');
        }
        
        function showSuccess(message) {
            const error = document.getElementById('error');
            error.style.background = '#d4edda';
            error.style.color = '#155724';
            error.textContent = '✅ ' + message;
            error.classList.add('active');
            setTimeout(() => {
                error.classList.remove('active');
                error.style.background = '#fee';
                error.style.color = '#c33';
            }, 3000);
        }
        
        // 实时日志功能
        async function startRealtimeLogs() {
            if (realtimeLogsInterval) {
                return; // 已在运行
            }
            
            document.getElementById('startRealtimeLogsBtn').style.display = 'none';
            document.getElementById('stopRealtimeLogsBtn').style.display = 'block';
            document.getElementById('realtimeLogsContainer').style.display = 'block';
            
            const logsContent = document.getElementById('realtimeLogsContent');
            logsContent.innerHTML = '<div style="color:#666;">正在加载实时日志...</div>';
            
            // 先获取一次日志，获取最后的时间戳
            try {
                const response = await fetch('/api/logs/view?limit=10');
                const data = await response.json();
                if (data.success && data.logs && data.logs.length > 0) {
                    lastLogTimestamp = data.logs[data.logs.length - 1].timestamp;
                    displayRealtimeLogs(data.logs);
                }
            } catch (err) {
                logsContent.innerHTML = `<div style="color:#F44336;">加载失败: ${err.message}</div>`;
            }
            
            // 每2秒轮询一次新日志
            realtimeLogsInterval = setInterval(async () => {
                try {
                    let url = '/api/logs/realtime';
                    if (lastLogTimestamp) {
                        url += `?since=${lastLogTimestamp}`;
                    }
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (data.success && data.logs && data.logs.length > 0) {
                        // 更新最后的时间戳
                        lastLogTimestamp = data.logs[data.logs.length - 1].timestamp;
                        // 追加新日志
                        appendRealtimeLogs(data.logs);
                    }
                } catch (err) {
                    console.error('实时日志获取失败:', err);
                }
            }, 2000); // 每2秒更新一次
        }
        
        function stopRealtimeLogs() {
            if (realtimeLogsInterval) {
                clearInterval(realtimeLogsInterval);
                realtimeLogsInterval = null;
            }
            document.getElementById('startRealtimeLogsBtn').style.display = 'block';
            document.getElementById('stopRealtimeLogsBtn').style.display = 'none';
        }
        
        function displayRealtimeLogs(logs) {
            const logsContent = document.getElementById('realtimeLogsContent');
            logsContent.innerHTML = '';
            logs.forEach(log => {
                appendLogEntry(log);
            });
            // 滚动到底部
            const container = document.getElementById('realtimeLogsContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        function appendRealtimeLogs(logs) {
            logs.forEach(log => {
                appendLogEntry(log);
            });
            // 滚动到底部
            const container = document.getElementById('realtimeLogsContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        function appendLogEntry(log) {
            const logsContent = document.getElementById('realtimeLogsContent');
            const time = new Date(log.timestamp).toLocaleTimeString();
            const levelColor = log.level === 'error' ? '#F44336' : log.level === 'warning' ? '#FF9800' : '#2196F3';
            const levelIcon = log.level === 'error' ? '❌' : log.level === 'warning' ? '⚠️' : 'ℹ️';
            
            const entry = document.createElement('div');
            entry.style.cssText = `margin-bottom:5px; padding:5px; border-left:3px solid ${levelColor}; padding-left:10px;`;
            entry.innerHTML = `
                <span style="color:#666; font-size:11px;">[${time}]</span>
                <span style="color:${levelColor}; font-weight:bold;">${levelIcon} ${log.level.toUpperCase()}</span>
                <span style="color:#333;">${log.content || log.source || ''}</span>
                ${log.metadata ? `<span style="color:#999; font-size:11px;">(${JSON.stringify(log.metadata).substring(0, 50)}...)</span>` : ''}
            `;
            logsContent.appendChild(entry);
        }
        
        // 日志管理相关函数
        async function viewLogs() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                let url = '/api/logs/view';
                if (date) {
                    url += `?date=${date}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult(`日志列表（${data.count} 条）`, {
                        date: data.date,
                        count: data.count,
                        logs: data.logs
                    });
                } else {
                    showError('查看日志失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('查看日志错误: ' + err.message);
            }
        }
        
        async function getLogStatistics() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                let url = '/api/logs/statistics';
                if (date) {
                    url += `?date=${date}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    displayNavigationResult('日志统计信息', {
                        date: data.date,
                        statistics: data.statistics
                    });
                } else {
                    showError('获取统计信息失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('获取统计信息错误: ' + err.message);
            }
        }
        
        async function uploadLogs() {
            const date = document.getElementById('logDate').value;
            
            showLoading();
            try {
                const response = await fetch('/api/logs/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ date: date || null })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    showSuccess(data.message + (data.upload_file ? `\\n文件: ${data.upload_file}` : ''));
                } else {
                    showError('上传日志失败: ' + (data.error || '未知错误'));
                }
            } catch (err) {
                hideLoading();
                showError('上传日志错误: ' + err.message);
            }
        }
        
        function downloadLogs() {
            const date = document.getElementById('logDate').value;
            
            let url = '/api/logs/download';
            if (date) {
                url += `?date=${date}`;
            }
            
            // 直接下载文件
            window.location.href = url;
        }
        
        // 实时视觉导航功能
        function startVisualNavigation() {
            // 确保函数暴露到全局作用域
            window.startVisualNavigation = startVisualNavigation;
            // 优先使用产品模式的摄像头流（如果已开启）
            const productVideo = document.getElementById('productVideo');
            let videoToUse = video;
            
            // 如果产品模式已开启摄像头，共享使用
            if (productVideo && productVideo.srcObject && productVideo.readyState >= 2) {
                console.log('使用产品模式的摄像头流');
                // 将产品模式的流也赋值给普通模式的video
                ensureDOMElements();
                const videoEl = getVideo();
                if (videoEl && !videoEl.srcObject) {
                    videoEl.srcObject = productVideo.srcObject;
                    videoEl.play().then(() => {
                        video = videoEl;  // 更新引用
                        continueStartVisualNavigation();
                    }).catch((err) => {
                        console.error('视频播放失败:', err);
                        continueStartVisualNavigation();
                    });
                    return;
                }
            }
            
            continueStartVisualNavigation();
            
            function continueStartVisualNavigation() {
                // 检查摄像头是否开启
                ensureDOMElements();
                const videoEl = getVideo();
                if (!videoEl || !videoEl.srcObject) {
                    showError('请先开启摄像头');
                    return;
                }
                
                // 检查视频是否已播放
                if (videoEl.readyState < 2) {
                    showError('摄像头未就绪，请稍候再试');
                    return;
                }
                
                // 显示结果区域
                document.getElementById('visualGuidanceResult').style.display = 'block';
                document.getElementById('guidanceMessages').innerHTML = '<div style="color:#4CAF50;">🎥 视觉导航已启动，正在分析画面...</div>';
                
                // 开始定时分析画面（每1.5秒一次，提高响应速度）
                visualNavigationInterval = setInterval(() => {
                    analyzeVisualGuidance().catch((err) => {
                        console.error('视觉导航分析失败:', err);
                    });
                }, 1500);
                
                // 立即执行一次
                analyzeVisualGuidance().then(() => {
                    showSuccess('实时视觉导航已启动');
                }).catch((err) => {
                    console.error('视觉导航分析失败:', err);
                    showSuccess('实时视觉导航已启动');
                });
            }
        }
        
        function stopVisualNavigation() {
            if (visualNavigationInterval) {
                clearInterval(visualNavigationInterval);
                visualNavigationInterval = null;
            }
            document.getElementById('visualGuidanceResult').style.display = 'none';
            document.getElementById('guidanceMessages').innerHTML = '';
            showSuccess('视觉导航已停止');
        }
        
        async function analyzeVisualGuidance() {
            try {
                // 从视频获取当前帧
                ensureDOMElements();
                const videoEl = getVideo();
                const canvasEl = getCanvas();
                if (!videoEl || !canvasEl) {
                    showError('无法找到视频或画布元素');
                    return;
                }
                canvasEl.width = videoEl.videoWidth;
                canvasEl.height = videoEl.videoHeight;
                const ctx = canvasEl.getContext('2d');
                ctx.drawImage(videoEl, 0, 0);
                
                // 转换为Blob
                canvasEl.toBlob(async (blob) => {
                    if (!blob) {
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('image', blob, 'frame.jpg');
                    
                    try {
                        const response = await fetch('/api/navigation/visual_guidance', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            // 产品模式使用专用显示函数
                            if (productModeActive) {
                                displayVisualGuidanceForProduct(data.guidance, data.vision_summary);
                            } else {
                                displayVisualGuidance(data.guidance, data.vision_summary);
                            }
                        } else {
                            console.error('视觉导航分析失败:', data.error);
                        }
                    } catch (err) {
                        console.error('视觉导航请求错误:', err);
                    }
                }, 'image/jpeg', 0.8);
            } catch (err) {
                console.error('获取视频帧失败:', err);
            }
        }
        
        function displayVisualGuidance(guidance, visionSummary) {
            const messagesDiv = document.getElementById('guidanceMessages');
            let html = '';
            
            // 方向指示
            const directionIcons = {
                'forward': '⬆️',
                'left': '⬅️',
                'right': '➡️',
                'stop': '⛔'
            };
            
            const directionColors = {
                'forward': '#4CAF50',
                'left': '#2196F3',
                'right': '#FF9800',
                'stop': '#F44336'
            };
            
            const direction = guidance.direction || 'forward';
            const icon = directionIcons[direction] || '➡️';
            const color = directionColors[direction] || '#666';
            
            html += `<div style="font-size:24px; text-align:center; margin-bottom:15px; color:${color}; font-weight:bold;">
                ${icon} ${direction.toUpperCase()}
            </div>`;
            
            // 指引消息
            if (guidance.messages && guidance.messages.length > 0) {
                html += '<div style="margin-bottom:10px;">';
                guidance.messages.forEach(msg => {
                    html += `<div style="padding:8px; margin:5px 0; background:#f5f5f5; border-radius:5px; font-size:14px;">${msg}</div>`;
                });
                html += '</div>';
            }
            
            // 房间号
            if (guidance.room_numbers && guidance.room_numbers.length > 0) {
                html += `<div style="margin-top:10px; padding:8px; background:#e3f2fd; border-radius:5px;">
                    <strong>房间号：</strong>${guidance.room_numbers.join(', ')}
                </div>`;
            }
            
            // 检测摘要
            html += '<div style="margin-top:15px; padding:10px; background:#f9f9f9; border-radius:5px; font-size:12px; color:#666;">';
            html += `<div>检测到 ${visionSummary.objects_detected || 0} 个物体，${visionSummary.texts_detected || 0} 段文字</div>`;
            if (guidance.signboards && guidance.signboards.length > 0) {
                html += `<div>标识牌：${guidance.signboards.length} 个</div>`;
            }
            if (guidance.step_detected) {
                html += `<div style="color:#F44336;">⚠️ 检测到台阶</div>`;
            }
            if (guidance.hazards_count > 0) {
                html += `<div style="color:#F44336;">⚠️ 检测到 ${guidance.hazards_count} 个危险区域</div>`;
            }
            html += '</div>';
            
            messagesDiv.innerHTML = html;
        }
        
        // 完整产品模式功能
        function startProductMode() {
            // 确保函数暴露到全局作用域
            window.startProductMode = startProductMode;
            // 检查必要模块
            const productVideo = document.getElementById('productVideo');
            if (!productVideo) {
                showError('视频元素未找到');
                return;
            }
            
            // 显示状态
            document.getElementById('productModeStatus').style.display = 'block';
            document.getElementById('productGuidance').style.display = 'block';
            document.getElementById('productVoiceStatus').style.display = 'block';
            document.getElementById('startProductModeBtn').style.display = 'none';
            document.getElementById('stopProductModeBtn').style.display = 'block';
            
            productModeActive = true;
            
            // 更新状态
            updateProductStatus('正在启动...');
            
            // 1. 自动开启摄像头（如果未开启）
            if (!productVideo.srcObject) {
                updateProductStatus('正在开启摄像头...');
                startCameraForProduct().then((cameraStarted) => {
                    if (!cameraStarted) {
                        showError('摄像头启动失败，请检查权限设置');
                        productModeActive = false;
                        document.getElementById('startProductModeBtn').style.display = 'block';
                        document.getElementById('stopProductModeBtn').style.display = 'none';
                        return;
                    }
                    // 摄像头启动后，继续后续步骤
                    continueAfterCameraReady();
                }).catch((err) => {
                    console.error('摄像头启动失败:', err);
                    showError('摄像头启动失败，请检查权限设置');
                    productModeActive = false;
                    document.getElementById('startProductModeBtn').style.display = 'block';
                    document.getElementById('stopProductModeBtn').style.display = 'none';
                });
            } else {
                // 摄像头已开启，直接继续
                continueAfterCameraReady();
            }
            
            // 继续后续步骤的函数
            function continueAfterCameraReady() {
                // 等待摄像头就绪（增加超时保护）
                new Promise((resolve, reject) => {
                    let checkCount = 0;
                    const maxChecks = 50; // 最多等待5秒
                    const checkReady = () => {
                        checkCount++;
                        if (productVideo.readyState >= 2) {
                            console.log('✅ 摄像头已就绪');
                            resolve();
                        } else if (checkCount >= maxChecks) {
                            console.warn('⚠️ 摄像头就绪超时');
                            reject(new Error('摄像头就绪超时'));
                        } else {
                            setTimeout(checkReady, 100);
                        }
                    };
                    checkReady();
                }).then(() => {
                    // 2. 立即启动视觉导航（自动环境扫描，不阻塞）
                    updateProductStatus('启动环境扫描...');
                    console.log('🎥 启动视觉导航...');
                    // 不等待，立即开始（异步），自动开始扫描
                    startVisualNavigationForProduct();
                    
                    // 3. 启动语音监听
                    updateProductStatus('启动语音监听...');
                    console.log('🎤 启动语音监听...');
                    return startVoiceListening();
                }).then(() => {
                    // 启动完成
                    console.log('✅ 产品模式启动完成');
                }).catch((err) => {
                    console.error('摄像头就绪失败:', err);
                    showError('摄像头就绪失败，请刷新页面重试');
                    productModeActive = false;
                    document.getElementById('startProductModeBtn').style.display = 'block';
                    document.getElementById('stopProductModeBtn').style.display = 'none';
                });
            }
            
            // 更新状态显示
            const voiceStatusDiv = document.getElementById('voiceStatusText');
            if (voiceStatusDiv) {
                voiceStatusDiv.innerHTML = '<span style="color:#4CAF50;">✅ 正在监听语音...</span>';
            }
            
            // 4. 播放欢迎语音（立即播放，不等待用户交互）
            // 注意：Mac上摄像头启动后可以立即播放，不需要等待用户交互
            updateProductStatus('产品模式运行中 - 自动环境扫描已开启');
            showSuccess('完整产品模式已启动，环境扫描和语音提示已自动开启');
            
            // 立即尝试播放欢迎语音（不阻塞）
            // 注意：由于用户已经点击了按钮，这个点击事件可以用于触发音频播放
            setTimeout(async () => {
                try {
                    debugLog('准备播放欢迎语音...', 'info');
                    await speakText('Luna已启动，开始环境扫描，我将主动为您提示周围环境', 'calm', false);
                    debugLog('✅ 欢迎语音已发送到播放队列', 'info');
                } catch (err) {
                    debugLog(`⚠️ 欢迎语音播放失败: ${err.message}`, 'warn');
                    console.error('欢迎语音播放错误:', err);
                    // 如果自动播放失败，等待用户交互
                    const playWelcomeOnce = async () => {
                        try {
                            debugLog('用户交互后尝试播放欢迎语音...', 'info');
                            await speakText('Luna已启动，开始环境扫描，我将主动为您提示周围环境', 'calm', false);
                            debugLog('✅ 用户交互后欢迎语音已播放', 'info');
                        } catch (e) {
                            debugLog(`❌ 用户交互后播放也失败: ${e.message}`, 'error');
                            console.error('用户交互后播放错误:', e);
                        }
                        document.removeEventListener('click', playWelcomeOnce);
                        document.removeEventListener('touchstart', playWelcomeOnce);
                    };
                    document.addEventListener('click', playWelcomeOnce, { once: true });
                    document.addEventListener('touchstart', playWelcomeOnce, { once: true });
                }
            }, 1000); // 延迟1秒确保摄像头已启动
        }
        
        function stopProductMode() {
            productModeActive = false;
            
            // 停止视觉导航
            stopVisualNavigation();
            
            // 停止语音监听
            stopVoiceListening();
            
            // 停止摄像头
            stopCameraForProduct();
            
            // 隐藏状态
            document.getElementById('productModeStatus').style.display = 'none';
            document.getElementById('productGuidance').style.display = 'none';
            document.getElementById('productVoiceStatus').style.display = 'none';
            document.getElementById('startProductModeBtn').style.display = 'block';
            document.getElementById('stopProductModeBtn').style.display = 'none';
            
            showSuccess('产品模式已停止');
        }
        
        async function startCameraForProduct() {
            try {
                const productVideo = document.getElementById('productVideo');
                if (!productVideo) {
                    showError('视频元素未找到');
                    return false;
                }
                
                const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                // 修复：更准确的HTTPS检测（包括IP地址访问）
                const isSecureContext = window.location.protocol === 'https:' || 
                                       window.location.hostname === 'localhost' || 
                                       window.location.hostname === '127.0.0.1' ||
                                       window.isSecureContext === true; // 使用浏览器原生API
                
                console.log('🔍 摄像头启动检查:', {
                    isSafari, isIOS, isSecureContext,
                    protocol: window.location.protocol,
                    hostname: window.location.hostname,
                    href: window.location.href,
                    isSecureContext_native: window.isSecureContext,
                    userAgent: navigator.userAgent,
                    hasMediaDevices: !!navigator.mediaDevices,
                    hasGetUserMedia: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
                });
                
                // 在页面上显示调试信息（iPhone Safari无法使用控制台）
                debugLog(`协议: ${window.location.protocol}`, 'info');
                debugLog(`地址: ${window.location.href}`, 'info');
                debugLog(`安全上下文: ${window.isSecureContext ? '是' : '否'}`, window.isSecureContext ? 'info' : 'warn');
                debugLog(`iOS: ${isIOS}, Safari: ${isSafari}`, 'info');
                
                // iOS Safari 在HTTP模式下无法使用摄像头（修复：使用原生isSecureContext）
                const actuallySecure = window.isSecureContext !== undefined ? window.isSecureContext : isSecureContext;
                
                if (isIOS && !actuallySecure) {
                    const errorMsg = `⚠️ iOS Safari浏览器需要HTTPS才能访问摄像头\n\n当前协议: ${window.location.protocol}\n当前地址: ${window.location.href}\n\n解决方案：\n1. 确保使用 https:// 访问\n2. 信任自签名证书\n3. 或使用Chrome浏览器`;
                    showError(errorMsg);
                    updateProductStatus('❌ iOS Safari需要HTTPS（当前: ' + window.location.protocol + '）');
                    
                    // 显示更详细的提示
                    const statusDiv = document.getElementById('productStatusDetails');
                    if (statusDiv) {
                        statusDiv.innerHTML = `
                            <div style="color:#F44336; font-weight:bold; margin-bottom:10px;">⚠️ iOS Safari限制</div>
                            <div style="font-size:13px; line-height:1.6; color:#666;">
                                当前协议: <strong>${window.location.protocol}</strong><br>
                                当前地址: <strong>${window.location.href}</strong><br>
                                安全上下文: <strong>${window.isSecureContext ? '是' : '否'}</strong><br><br>
                                iOS Safari浏览器出于安全考虑，在HTTP模式下无法使用摄像头和麦克风。<br><br>
                                <strong>解决方案：</strong><br>
                                1. 📱 确保使用 <code>https://</code> 访问（不是 http://）<br>
                                2. 🔒 信任自签名证书（点击"访问此网站"）<br>
                                3. 🌐 或使用Chrome浏览器访问
                            </div>
                        `;
                    }
                    return false;
                }
                
                // Safari桌面版也需要HTTPS
                if (isSafari && !isIOS && !actuallySecure) {
                    const errorMsg = `⚠️ Safari浏览器需要HTTPS才能访问摄像头\n\n当前协议: ${window.location.protocol}\n建议：\n1. 使用 https:// 访问\n2. 或使用Chrome浏览器测试`;
                    showError(errorMsg);
                    updateProductStatus('摄像头启动失败：需要HTTPS（当前: ' + window.location.protocol + '）');
                    return false;
                }
                
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    const errorMsg = `您的浏览器不支持摄像头访问\n\n建议使用Chrome、Edge或Firefox浏览器`;
                    showError(errorMsg);
                    updateProductStatus('摄像头启动失败：浏览器不支持');
                    return false;
                }
                
                updateProductStatus('正在请求摄像头权限...');
                console.log('📹 正在请求摄像头权限...');
                debugLog('正在请求摄像头权限...', 'info');
                
                // 简化摄像头请求参数，提高兼容性
                let stream = null;
                try {
                    // 先尝试后置摄像头（environment）
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: { 
                            facingMode: 'environment',
                            width: { ideal: 640 },
                            height: { ideal: 480 }
                        }
                    });
                    console.log('✅ 后置摄像头获取成功');
                    debugLog('✅ 后置摄像头获取成功', 'info');
                } catch (err1) {
                    console.warn('⚠️ 后置摄像头获取失败，尝试前置摄像头:', err1);
                    debugLog(`⚠️ 后置摄像头失败: ${err1.name} - ${err1.message}`, 'warn');
                    try {
                        // 如果后置摄像头失败，尝试前置摄像头
                        stream = await navigator.mediaDevices.getUserMedia({ 
                            video: { 
                                facingMode: 'user',
                                width: { ideal: 640 },
                                height: { ideal: 480 }
                            }
                        });
                        console.log('✅ 前置摄像头获取成功');
                        debugLog('✅ 前置摄像头获取成功', 'info');
                    } catch (err2) {
                        console.warn('⚠️ 前置摄像头也失败，尝试最简单配置:', err2);
                        debugLog(`⚠️ 前置摄像头也失败: ${err2.name} - ${err2.message}`, 'warn');
                        // 最后尝试最简单的配置
                        stream = await navigator.mediaDevices.getUserMedia({ 
                            video: true
                        });
                        console.log('✅ 默认摄像头配置获取成功');
                        debugLog('✅ 默认摄像头配置获取成功', 'info');
                    }
                }
                
                if (!stream) {
                    throw new Error('无法获取摄像头流');
                }
                
                console.log('✅ 摄像头权限已授予，流已获取');
                debugLog('✅ 摄像头权限已授予', 'info');
                console.log('📹 流信息:', {
                    active: stream.active,
                    id: stream.id,
                    tracks: stream.getTracks().map(t => ({
                        kind: t.kind,
                        enabled: t.enabled,
                        readyState: t.readyState,
                        settings: t.getSettings()
                    }))
                });
                
                updateProductStatus('正在设置视频流...');
                
                // 停止之前的流（如果有）
                if (productVideo.srcObject) {
                    const oldStream = productVideo.srcObject;
                    oldStream.getTracks().forEach(track => track.stop());
                }
                
                productVideo.srcObject = stream;
                productVideo.setAttribute('playsinline', 'true');
                productVideo.setAttribute('webkit-playsinline', 'true');
                productVideo.setAttribute('autoplay', 'true');
                productVideo.muted = false; // 确保不是静音状态
                
                // 等待视频元数据加载（增加超时）
                updateProductStatus('正在加载视频元数据...');
                await new Promise((resolve, reject) => {
                    let resolved = false;
                    const timeout = setTimeout(() => {
                        if (!resolved) {
                            resolved = true;
                            console.error('❌ 视频元数据加载超时');
                            reject(new Error('视频元数据加载超时'));
                        }
                    }, 10000); // 10秒超时
                    
                    productVideo.onloadedmetadata = () => {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.log('✅ 视频元数据已加载:', {
                                videoWidth: productVideo.videoWidth,
                                videoHeight: productVideo.videoHeight,
                                readyState: productVideo.readyState
                            });
                            resolve();
                        }
                    };
                    
                    productVideo.onerror = (err) => {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.error('❌ 视频加载错误:', err);
                            reject(err);
                        }
                    };
                    
                    // 如果已经加载完成，立即resolve
                    if (productVideo.readyState >= 1) {
                        if (!resolved) {
                            resolved = true;
                            clearTimeout(timeout);
                            console.log('✅ 视频已就绪（readyState=' + productVideo.readyState + '）');
                            resolve();
                        }
                    }
                });
                
                updateProductStatus('正在播放视频...');
                console.log('📹 准备播放视频...');
                
                // 尝试播放视频
                try {
                    await productVideo.play();
                    console.log('✅ 视频播放已启动');
                } catch (playErr) {
                    console.warn('⚠️ 自动播放失败，尝试用户交互后播放:', playErr);
                    // 如果自动播放失败，等待用户交互
                    updateProductStatus('请点击页面以启用摄像头画面');
                    // 添加点击事件来触发播放
                    const playOnClick = async () => {
                        try {
                            await productVideo.play();
                            console.log('✅ 用户交互后视频播放成功');
                            updateProductStatus('✅ 摄像头已开启并运行中');
                        } catch (e) {
                            console.error('❌ 用户交互后播放也失败:', e);
                        }
                        document.removeEventListener('click', playOnClick);
                        document.removeEventListener('touchstart', playOnClick);
                    };
                    document.addEventListener('click', playOnClick, { once: true });
                    document.addEventListener('touchstart', playOnClick, { once: true });
                }
                
                // 保存stream引用以便后续停止
                window.productVideoStream = stream;
                
                // 添加视频事件监听
                productVideo.onplay = () => {
                    console.log('✅ 视频正在播放');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.onloadeddata = () => {
                    console.log('✅ 视频数据已加载');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.oncanplay = () => {
                    console.log('✅ 视频可以播放');
                    updateProductStatus('✅ 摄像头已开启并运行中');
                };
                
                productVideo.onerror = (err) => {
                    console.error('❌ 视频播放错误:', err);
                    updateProductStatus('❌ 摄像头播放失败');
                    showError('摄像头播放失败，请刷新页面重试');
                };
                
                // 检查视频是否真的在播放
                setTimeout(() => {
                    if (productVideo.readyState >= 2 && productVideo.videoWidth > 0) {
                        console.log('✅ 摄像头确认运行中:', {
                            readyState: productVideo.readyState,
                            videoWidth: productVideo.videoWidth,
                            videoHeight: productVideo.videoHeight,
                            paused: productVideo.paused,
                            ended: productVideo.ended
                        });
                        updateProductStatus('✅ 摄像头已开启并运行中');
                    } else {
                        console.warn('⚠️ 摄像头可能未正常启动:', {
                            readyState: productVideo.readyState,
                            videoWidth: productVideo.videoWidth,
                            videoHeight: productVideo.videoHeight,
                            paused: productVideo.paused
                        });
                        updateProductStatus('⚠️ 摄像头启动中，请稍候...');
                    }
                }, 2000);
                
                return true;
            } catch (err) {
                console.error('❌ 摄像头启动失败:', err);
                debugLog(`❌ 摄像头启动失败: ${err.name} - ${err.message}`, 'error');
                let errorMsg = '无法访问摄像头: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问摄像头权限\\n\\n请在浏览器设置中允许摄像头访问';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到摄像头设备\\n\\n请检查摄像头是否已连接';
                } else if (err.name === 'NotReadableError') {
                    errorMsg += '摄像头被其他程序占用\\n\\n请关闭其他使用摄像头的应用';
                } else {
                    errorMsg += (err.message || '未知错误');
                }
                showError(errorMsg);
                updateProductStatus('❌ 摄像头启动失败: ' + err.name);
                return false;
            }
        }
        
        function stopCameraForProduct() {
            const productVideo = document.getElementById('productVideo');
            if (productVideo && productVideo.srcObject) {
                const stream = productVideo.srcObject;
                stream.getTracks().forEach(track => track.stop());
                productVideo.srcObject = null;
            }
            if (window.productVideoStream) {
                window.productVideoStream.getTracks().forEach(track => track.stop());
                window.productVideoStream = null;
            }
        }
        
        async function startVisualNavigationForProduct() {
            const productVideo = document.getElementById('productVideo');
            const productCanvas = document.getElementById('productCanvas');
            
            if (!productVideo || !productVideo.srcObject) {
                console.warn('摄像头未就绪，等待中...');
                // 等待摄像头就绪
                await new Promise(resolve => {
                    const checkReady = () => {
                        if (productVideo && productVideo.srcObject && productVideo.readyState >= 2) {
                            resolve();
                        } else {
                            setTimeout(checkReady, 100);
                        }
                    };
                    checkReady();
                });
            }
            
            // 显示结果区域
            document.getElementById('productGuidance').style.display = 'block';
            document.getElementById('guidanceMessages').innerHTML = '<div style="color:#4CAF50;">🎥 环境扫描已启动，正在分析周围环境...</div>';
            
            // 优化：降低检测频率到1-2秒，提高响应速度
            let lastFrameTime = 0;
            let frameSkipCount = 0;
            // 每3帧检测一次(约0.5-1秒,假设30fps)
            // 优化:提高检测频率
            const FRAME_SKIP = 3;
            // 最小间隔0.8秒(优化:提高响应速度,目标<1秒)
            const MIN_INTERVAL = 800;
            let isAnalyzing = false; // 防止并发分析
            
            function analyzeFrame() {
                if (!productModeActive) return;
                
                const now = Date.now();
                frameSkipCount++;
                
                // 如果正在分析中，跳过本次
                if (isAnalyzing) {
                    requestAnimationFrame(analyzeFrame);
                    return;
                }
                
                // 检查时间间隔和帧数
                if (now - lastFrameTime < MIN_INTERVAL || frameSkipCount < FRAME_SKIP) {
                    requestAnimationFrame(analyzeFrame);
                    return;
                }
                
                frameSkipCount = 0;
                lastFrameTime = now;
                
                // 执行检测（异步，不阻塞）
                analyzeVisualGuidanceForProduct().finally(() => {
                    isAnalyzing = false;
                });
                
                // 继续下一帧
                requestAnimationFrame(analyzeFrame);
            }
            
            // 开始检测循环
            requestAnimationFrame(analyzeFrame);
            
            // 立即执行一次（不等待）
            analyzeVisualGuidanceForProduct();
        }
        
        async function analyzeVisualGuidanceForProduct() {
            try {
                const productVideo = document.getElementById('productVideo');
                const productCanvas = document.getElementById('productCanvas');
                
                if (!productVideo || !productVideo.srcObject) {
                    console.warn('⚠️ 摄像头未就绪，跳过本次分析');
                    window.isAnalyzingVision = false;
                    return;
                }
                
                if (productVideo.readyState < 2) {
                    console.warn('⚠️ 视频未就绪（readyState=' + productVideo.readyState + '），跳过本次分析');
                    window.isAnalyzingVision = false;
                    return;
                }
                
                // 设置分析标志
                if (window.isAnalyzingVision) {
                    return; // 如果正在分析，跳过
                }
                window.isAnalyzingVision = true;
                
                // 更新状态：显示正在扫描
                const guidanceMessages = document.getElementById('guidanceMessages');
                if (guidanceMessages) {
                    guidanceMessages.innerHTML = '<div style="color:#FF9800;">🔍 正在扫描环境...</div>';
                }
                
                // 从视频获取当前帧（确保尺寸有效）
                if (productVideo.videoWidth === 0 || productVideo.videoHeight === 0) {
                    console.warn('⚠️ 视频尺寸无效，等待中...');
                    window.isAnalyzingVision = false;
                    return;
                }
                
                productCanvas.width = productVideo.videoWidth;
                productCanvas.height = productVideo.videoHeight;
                const ctx = productCanvas.getContext('2d');
                
                // 确保canvas尺寸有效
                if (productCanvas.width === 0 || productCanvas.height === 0) {
                    console.warn('⚠️ Canvas尺寸无效');
                    window.isAnalyzingVision = false;
                    return;
                }
                
                ctx.drawImage(productVideo, 0, 0);
                
                // ========== 镜头运动检测（ChatGPT建议）==========
                // 获取当前帧数据用于运动检测
                const frameData = productCanvas.toDataURL('image/jpeg', 0.1); // 低质量用于快速比较
                detectCameraMotion(frameData);
                
                // 转换为Blob（提高质量到70%以确保图片有效，平衡质量和速度）
                productCanvas.toBlob(async (blob) => {
                    window.isAnalyzingVision = false; // 重置标志
                    
                    if (!blob || blob.size === 0) {
                        console.warn('⚠️ Blob为空或无效');
                        return;
                    }
                    
                    console.log('📸 准备发送图片: 大小=' + blob.size + '字节, 类型=' + blob.type);
                    
                    const formData = new FormData();
                    formData.append('image', blob, 'frame.jpg');
                    
                    try {
                        const startTime = Date.now();
                        const response = await fetch('/api/navigation/visual_guidance', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        const processingTime = Date.now() - startTime;
                        
                        if (data.success) {
                            displayVisualGuidanceForProduct(data.guidance, data.vision_summary);
                            
                            // 显示处理时间
                            if (guidanceMessages && data.vision_summary) {
                                const timeInfo = `<div style="font-size:11px; color:#999; margin-top:5px;">处理时间: ${processingTime}ms</div>`;
                                if (guidanceMessages.innerHTML.indexOf('处理时间') === -1) {
                                    guidanceMessages.innerHTML += timeInfo;
                                }
                            }
                        } else {
                            console.error('❌ 视觉导航分析失败:', data.error);
                            if (guidanceMessages) {
                                guidanceMessages.innerHTML = '<div style="color:#F44336;">❌ 扫描失败: ' + (data.error || '未知错误') + '</div>';
                            }
                        }
                    } catch (err) {
                        window.isAnalyzingVision = false;
                        console.error('❌ 视觉导航请求错误:', err);
                        if (guidanceMessages) {
                            guidanceMessages.innerHTML = '<div style="color:#F44336;">❌ 网络错误，请检查连接</div>';
                        }
                    }
                }, 'image/jpeg', 0.7); // 提高质量到70%以确保图片有效
            } catch (err) {
                window.isAnalyzingVision = false;
                console.error('视觉导航分析错误:', err);
            }
        }
        
        // 调试日志函数（在页面上显示，方便iPhone Safari调试）
        function debugLog(message, type = 'info') {
            const debugDiv = document.getElementById('debugInfo');
            const debugLogDiv = document.getElementById('debugLog');
            if (debugDiv && debugLogDiv) {
                debugDiv.style.display = 'block';
                const time = new Date().toLocaleTimeString();
                const color = type === 'error' ? '#F44336' : type === 'warn' ? '#FF9800' : '#2196F3';
                const icon = type === 'error' ? '❌' : type === 'warn' ? '⚠️' : 'ℹ️';
                debugLogDiv.innerHTML += `<div style="color:${color}; margin-bottom:3px;">[${time}] ${icon} ${message}</div>`;
                // 自动滚动到底部
                debugDiv.scrollTop = debugDiv.scrollHeight;
            }
            // 同时输出到控制台（如果可用）
            if (console && console.log) {
                console.log(message);
            }
        }
        
        function updateProductStatus(text) {
            const statusDiv = document.getElementById('productStatusDetails');
            if (statusDiv) {
                statusDiv.innerHTML = `<div>${new Date().toLocaleTimeString()}</div><div>${text}</div>`;
            }
        }
        
        // 持续语音监听模式（优化版：实时检测）
        function startVoiceListening() {
            // 确保函数暴露到全局作用域
            window.startVoiceListening = startVoiceListening;
            if (voiceListeningInterval) {
                console.log('⚠️ 语音监听已在运行中');
                return Promise.resolve(); // 已在运行
            }
            
            // 保持音频流持续开启，避免重复请求权限
            let continuousAudioStream = null;
            let isRecording = false;
            
            console.log('🎤 开始启动语音监听...');
            updateProductStatus('正在请求麦克风权限...');
            
            return navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
                continuousAudioStream = stream;
                console.log('✅ 麦克风权限已授予');
                updateProductStatus('✅ 麦克风已开启，正在监听...');
                return stream;
            }).catch((err) => {
                console.error('❌ 无法获取音频流:', err);
                let errorMsg = '无法访问麦克风: ';
                if (err.name === 'NotAllowedError') {
                    errorMsg += '请允许浏览器访问麦克风权限';
                } else if (err.name === 'NotFoundError') {
                    errorMsg += '未找到麦克风设备';
                } else {
                    errorMsg += err.message || '未知错误';
                }
                showError(errorMsg);
                updateProductStatus('❌ 麦克风启动失败: ' + err.name);
                throw err;
            }).then((stream) => {
                if (!stream) return;
                
                // 使用AudioContext进行实时语音检测
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const analyser = audioContext.createAnalyser();
                const microphone = audioContext.createMediaStreamSource(continuousAudioStream);
                microphone.connect(analyser);
                
                analyser.fftSize = 128; // 优化：降低FFT大小减少计算量
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);
                
                // 语音活动检测参数
                const SILENCE_THRESHOLD = 30; // 静音阈值
                const SPEECH_THRESHOLD = 50;  // 语音阈值
                let silenceCount = 0;
                let speechCount = 0;
                let recordingStartTime = null;
                const MIN_RECORDING_TIME = 0.5; // 最小录音时间（秒）
                const MAX_RECORDING_TIME = 2.0;  // 最大录音时间（秒）
                
                let audioChunksForVAD = [];
                let mediaRecorderForVAD = null;
                
                // 开始录音
                function startRecording() {
                    if (isRecording) return;
                    
                    isRecording = true;
                    recordingStartTime = Date.now();
                    audioChunksForVAD = [];
                    
                    let options = {};
                    if (MediaRecorder.isTypeSupported('audio/webm')) {
                        options = { mimeType: 'audio/webm' };
                    } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                        options = { mimeType: 'audio/mp4' };
                    }
                    
                    mediaRecorderForVAD = new MediaRecorder(continuousAudioStream, options);
                    
                    mediaRecorderForVAD.ondataavailable = (event) => {
                        if (event.data && event.data.size > 0) {
                            audioChunksForVAD.push(event.data);
                        }
                    };
                    
                    mediaRecorderForVAD.onstop = () => {
                        if (audioChunksForVAD.length > 0) {
                            const audioBlob = new Blob(audioChunksForVAD, { type: mediaRecorderForVAD.mimeType || 'audio/webm' });
                            recognizeAndRespond(audioBlob).catch((err) => {
                                console.error('语音识别失败:', err);
                            });
                        }
                        isRecording = false;
                    };
                    
                    mediaRecorderForVAD.start();
                    
                    // 更新状态
                    const voiceStatusDiv = document.getElementById('voiceStatusText');
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#F44336;">🔴 正在录音...</span>';
                    }
                }
                
                // 停止录音
                function stopRecording() {
                    if (!isRecording || !mediaRecorderForVAD) return;
                    
                    const recordingDuration = (Date.now() - recordingStartTime) / 1000;
                    
                    // 如果录音时间太短，忽略
                    if (recordingDuration < MIN_RECORDING_TIME) {
                        isRecording = false;
                        return;
                    }
                    
                    if (mediaRecorderForVAD.state !== 'inactive') {
                        mediaRecorderForVAD.stop();
                    }
                    
                    // 更新状态：显示正在识别
                    const voiceStatusDiv = document.getElementById('voiceStatusText');
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#FF9800;">🟡 正在识别...</span>';
                    }
                }
                
                // 实时检测循环（优化：降低检测频率到200ms）
                function detectVoiceActivity() {
                    if (!productModeActive) {
                        if (isRecording) {
                            stopRecording();
                        }
                        return;
                    }
                    
                    analyser.getByteFrequencyData(dataArray);
                    
                    // 计算平均音量
                    let sum = 0;
                    for (let i = 0; i < bufferLength; i++) {
                        sum += dataArray[i];
                    }
                    const average = sum / bufferLength;
                    
                    if (average > SPEECH_THRESHOLD) {
                        // 检测到语音
                        speechCount++;
                        silenceCount = 0;
                        
                        if (!isRecording && speechCount > 2) {
                            // 连续2次检测到语音，开始录音
                            startRecording();
                        }
                    } else if (average < SILENCE_THRESHOLD) {
                        // 检测到静音
                        silenceCount++;
                        speechCount = 0;
                        
                        if (isRecording) {
                            const recordingDuration = (Date.now() - recordingStartTime) / 1000;
                            
                            // 如果静音超过0.5秒或录音超过最大时间，停止录音
                            if (silenceCount > 5 || recordingDuration >= MAX_RECORDING_TIME) {
                                stopRecording();
                            }
                        }
                    } else {
                        // 中间状态，重置计数
                        speechCount = Math.max(0, speechCount - 1);
                        silenceCount = Math.max(0, silenceCount - 1);
                    }
                    
                    // 优化：200ms检测一次（而不是每帧）
                    setTimeout(detectVoiceActivity, 200);
                }
                
                // 开始检测
                console.log('✅ 语音活动检测已启动');
                detectVoiceActivity();
                
                // 保存引用以便停止
                voiceListeningInterval = {
                    stop: () => {
                        console.log('🛑 停止语音监听...');
                        if (continuousAudioStream) {
                            continuousAudioStream.getTracks().forEach(track => track.stop());
                        }
                        if (audioContext) {
                            audioContext.close();
                        }
                        if (mediaRecorderForVAD && mediaRecorderForVAD.state !== 'inactive') {
                            mediaRecorderForVAD.stop();
                        }
                        voiceListeningInterval = null;
                        const voiceStatusDiv = document.getElementById('voiceStatusText');
                        if (voiceStatusDiv) {
                            voiceStatusDiv.innerHTML = '<span style="color:#999;">已停止监听</span>';
                        }
                    }
                };
            });
        }
        
        function stopVoiceListening() {
            if (voiceListeningInterval) {
                if (typeof voiceListeningInterval.stop === 'function') {
                    voiceListeningInterval.stop();
                } else {
                    clearInterval(voiceListeningInterval);
                }
                voiceListeningInterval = null;
            }
            const voiceStatusDiv = document.getElementById('voiceStatusText');
            if (voiceStatusDiv) {
                voiceStatusDiv.textContent = '语音监听已停止';
            }
            const voiceResultDiv = document.getElementById('voiceRecognitionResult');
            if (voiceResultDiv) {
                voiceResultDiv.style.display = 'none';
            }
        }
        
        async function captureAndRecognizeVoice() {
            try {
                // 更新状态：显示正在录音
                const voiceStatusDiv = document.getElementById('voiceStatusText');
                if (voiceStatusDiv) {
                    voiceStatusDiv.innerHTML = '<span style="color:#F44336;">🔴 正在录音...</span>';
                }
                
                const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];
                
                let options = {};
                if (MediaRecorder.isTypeSupported('audio/webm')) {
                    options = { mimeType: 'audio/webm' };
                } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                    options = { mimeType: 'audio/mp4' };
                }
                
                const recorder = new MediaRecorder(audioStream, options);
                
                recorder.ondataavailable = (event) => {
                    if (event.data && event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                recorder.onstop = async () => {
                    // 更新状态：显示正在识别
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#FF9800;">🟡 正在识别...</span>';
                    }
                    
                    const audioBlob = new Blob(audioChunks, { type: recorder.mimeType || 'audio/webm' });
                    await recognizeAndRespond(audioBlob);
                    
                    // 更新状态：显示监听中
                    if (voiceStatusDiv) {
                        voiceStatusDiv.innerHTML = '<span style="color:#1976D2;">🎤 正在监听...</span>';
                    }
                    
                    audioStream.getTracks().forEach(track => track.stop());
                };
                
                recorder.start();
                
                // 录音1.5秒
                setTimeout(() => {
                    if (recorder.state !== 'inactive') {
                        recorder.stop();
                    }
                }, 1500);
            } catch (err) {
                console.error('启动录音失败:', err);
                const voiceStatusDiv = document.getElementById('voiceStatusText');
                if (voiceStatusDiv) {
                    voiceStatusDiv.innerHTML = '<span style="color:#F44336;">❌ 录音失败: ' + (err.message || '未知错误') + '</span>';
                }
            }
        }
        
        async function recognizeAndRespond(audioBlob) {
            try {
                const formData = new FormData();
                formData.append('audio', audioBlob);
                
                const response = await fetch('/api/recognize/voice', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                // 显示识别结果（无论成功与否）
                const voiceResultDiv = document.getElementById('voiceRecognitionResult');
                if (voiceResultDiv) {
                    voiceResultDiv.style.display = 'block';
                }
                
                if (data.success && data.text && data.text.trim()) {
                    const recognizedText = data.text.trim();
                    const now = Date.now();
                    
                    // 避免重复识别（3秒内相同文本）
                    if (now - lastVoiceRecognitionTime < 3000) {
                        if (voiceResultDiv) {
                            voiceResultDiv.innerHTML = '<div style="color:#999;">识别中（避免重复）...</div>';
                        }
                        return;
                    }
                    lastVoiceRecognitionTime = now;
                    
                    // 显示识别结果
                    if (voiceResultDiv) {
                        voiceResultDiv.innerHTML = 
                            `<div style="color:#1976D2;"><strong>识别：</strong>${recognizedText}</div>`;
                    }
                    
                    // 处理语音指令
                    await processVoiceCommand(recognizedText);
                } else {
                    // 识别失败或没有识别到内容
                    if (voiceResultDiv) {
                        const errorMsg = data.error || '未识别到语音内容';
                        voiceResultDiv.innerHTML = `<div style="color:#999;">${errorMsg}</div>`;
                    }
                    console.log('语音识别结果:', data);
                }
            } catch (err) {
                console.error('语音识别错误:', err);
                const voiceResultDiv = document.getElementById('voiceRecognitionResult');
                if (voiceResultDiv) {
                    voiceResultDiv.style.display = 'block';
                    voiceResultDiv.innerHTML = `<div style="color:#F44336;">识别错误: ${err.message}</div>`;
                }
            }
        }
        
        async function processVoiceCommand(text) {
            const lowerText = text.toLowerCase();
            
            // 导航相关指令
            if (lowerText.includes('导航') || lowerText.includes('去') || lowerText.includes('到')) {
                // 提取目的地
                const destinationMatch = text.match(/(?:去|到|导航)(.+)/);
                if (destinationMatch) {
                    const destination = destinationMatch[1].trim();
                    await speakText(`好的，我将为您导航到${destination}`, 'cheerful');
                    // 这里可以调用导航API
                }
            }
            // 停止指令
            else if (lowerText.includes('停止') || lowerText.includes('暂停')) {
                await speakText('好的，已暂停', 'calm');
            }
            // 继续指令
            else if (lowerText.includes('继续') || lowerText.includes('恢复')) {
                await speakText('好的，继续导航', 'cheerful');
            }
            // 帮助指令
            else if (lowerText.includes('帮助') || lowerText.includes('怎么用')) {
                await speakText('我可以帮您导航、识别物体、检测障碍。请告诉我您要去哪里', 'calm');
            }
            // 默认响应
            else {
                await speakText('我听到了，请告诉我您需要什么帮助', 'calm');
            }
        }
        
        // ========== 优先级TTS播放队列管理器（ChatGPT建议优化）==========
        class PriorityTTSQueue {
            constructor() {
                this.currentAudio = null;
                this.currentPriority = 999; // 当前播放的优先级（数字越小优先级越高）
                this.queue = [];
                this.priorityLevels = {
                    'critical': 0,  // 台阶、危险（最高优先级）
                    'high': 1,      // 转向提示
                    'medium': 2,    // 标识牌
                    'low': 3        // 普通提示
                };
                this.stats = {
                    totalPlayed: 0,
                    totalInterrupted: 0,
                    latencyHistory: []
                };
            }
            
            getPriorityLevel(style, message) {
                // 根据消息内容和风格确定优先级
                if (message.includes('台阶') || message.includes('危险')) {
                    return this.priorityLevels.critical;
                } else if (message.includes('左转') || message.includes('右转')) {
                    return this.priorityLevels.high;
                } else if (message.includes('洗手间') || message.includes('电梯')) {
                    return this.priorityLevels.medium;
                } else {
                    return this.priorityLevels.low;
                }
            }
            
            async play(text, style = 'calm', priorityLevel = null) {
                const priority = priorityLevel !== null ? priorityLevel : this.getPriorityLevel(style, text);
                const triggerTime = Date.now();
                
                // 如果当前播放的优先级更低，中断它
                if (this.currentAudio && this.currentPriority > priority) {
                    console.log(`🔊 中断低优先级播放（优先级: ${this.currentPriority} -> ${priority}）`);
                    this.currentAudio.pause();
                    this.currentAudio.currentTime = 0;
                    this.currentAudio = null;
                    this.currentPriority = 999;
                    this.stats.totalInterrupted++;
                }
                
                // 如果正在播放且优先级相同或更高，加入队列
                if (this.currentAudio && this.currentPriority <= priority) {
                    this.queue.push({ text, style, priority, triggerTime });
                    console.log(`📋 加入队列（优先级: ${priority}）: ${text.substring(0, 20)}...`);
                    return;
                }
                
                // 立即播放
                this.currentAudio = await this._playAudio(text, style, priority, triggerTime);
                this.currentPriority = priority;
            }
            
            async _playAudio(text, style, priority, triggerTime) {
                const audio = await _playTTS(text, style);
                
                if (audio) {
                    // 记录播放开始时间
                    audio.onplay = () => {
                        const playTime = Date.now();
                        const latency = playTime - triggerTime;
                        this.stats.latencyHistory.push({
                            text: text.substring(0, 30),
                            latency: latency,
                            priority: priority,
                            timestamp: Date.now()
                        });
                        
                        // 只保留最近100条记录
                        if (this.stats.latencyHistory.length > 100) {
                            this.stats.latencyHistory.shift();
                        }
                        
                        // 如果延迟过大，记录警告
                        if (latency > 500) {
                            console.warn(`⚠️ 滞后提示: ${text.substring(0, 20)}..., 延迟: ${latency}ms`);
                        }
                    };
                    
                    // 播放结束
                    audio.onended = () => {
                        this.currentAudio = null;
                        this.currentPriority = 999;
                        this.stats.totalPlayed++;
                        
                        // 播放队列中的下一个（按优先级排序）
                        if (this.queue.length > 0) {
                            this.queue.sort((a, b) => a.priority - b.priority);
                            const next = this.queue.shift();
                            this.play(next.text, next.style, next.priority);
                        }
                    };
                }
                
                return audio;
            }
            
            getStats() {
                const latencies = this.stats.latencyHistory.map(h => h.latency);
                const avgLatency = latencies.length > 0 
                    ? latencies.reduce((a, b) => a + b, 0) / latencies.length 
                    : 0;
                const maxLatency = latencies.length > 0 ? Math.max(...latencies) : 0;
                
                return {
                    totalPlayed: this.stats.totalPlayed,
                    totalInterrupted: this.stats.totalInterrupted,
                    avgLatency: Math.round(avgLatency),
                    maxLatency: maxLatency,
                    queueLength: this.queue.length
                };
            }
        }
        
        // 创建全局优先级队列管理器
        const priorityTTSQueue = new PriorityTTSQueue();
        
        // TTS播放队列（保留兼容性）
        let ttsQueue = [];
        let isPlayingTTS = false;
        
        async function speakText(text, style = 'calm', priority = false) {
            // 使用新的优先级队列管理器
            const priorityLevel = priority ? priorityTTSQueue.priorityLevels.critical : priorityTTSQueue.priorityLevels.low;
            await priorityTTSQueue.play(text, style, priorityLevel);
        }
        
        async function _playTTS(text, style = 'calm') {
            isPlayingTTS = true;
            let audioElement = null;
            try {
                // 显示播放状态
                const playbackDiv = document.getElementById('voicePlaybackStatus');
                const playbackTextDiv = document.getElementById('playbackText');
                if (playbackDiv) {
                    playbackDiv.style.display = 'block';
                    playbackDiv.style.background = '#fff3cd';
                    if (playbackTextDiv) {
                        playbackTextDiv.textContent = text;
                    }
                }
                
                const startTime = Date.now();
                const response = await fetch('/api/tts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, style })
                });
                
                const data = await response.json();
                
                const ttsTime = Date.now() - startTime;
                console.log(`TTS生成时间: ${ttsTime}ms${data.cached ? ' ⚡(缓存)' : ''}`);
                
                if (data.success && data.audio) {
                    // 直接使用base64数据创建Blob，避免额外请求
                    const base64Data = data.audio;
                    const byteCharacters = atob(base64Data);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const audioBlob = new Blob([byteArray], { type: 'audio/mp3' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    audioElement = audio; // 保存引用，用于优先级队列管理
                    
                    // 设置初始音量
                    audio.volume = currentAudioVolume;
                    
                    // 添加到全局音频列表
                    if (!window.currentPlayingAudios) {
                        window.currentPlayingAudios = [];
                    }
                    window.currentPlayingAudios.push(audio);
                    
                    // 播放结束后从列表中移除
                    audio.onended = () => {
                        const index = window.currentPlayingAudios.indexOf(audio);
                        if (index > -1) {
                            window.currentPlayingAudios.splice(index, 1);
                        }
                    };
                    
                    // 播放开始
                    audio.onplay = () => {
                        const playTime = Date.now() - startTime;
                        console.log(`TTS总延迟: ${playTime}ms${data.cached ? ' ⚡(缓存)' : ''}`);
                        if (playbackDiv) {
                            playbackDiv.style.display = 'block';
                            playbackDiv.style.background = '#d4edda';
                            playbackDiv.innerHTML = '<div style="color:#155724;">🔊 正在播放语音...</div><div style="margin-top:5px; color:#666;">' + text + '</div>';
                        }
                    };
                    
                    // 播放结束
                    audio.onended = () => {
                        isPlayingTTS = false;
                        if (playbackDiv) {
                            playbackDiv.style.display = 'none';
                        }
                        URL.revokeObjectURL(audioUrl);
                        
                        // 播放队列中的下一个
                        if (ttsQueue.length > 0) {
                            const next = ttsQueue.shift();
                            _playTTS(next.text, next.style);
                        }
                    };
                    
                    // 播放错误
                    audio.onerror = (err) => {
                        isPlayingTTS = false;
                        console.error('音频播放错误:', err);
                        if (playbackDiv) {
                            playbackDiv.style.display = 'none';
                        }
                        URL.revokeObjectURL(audioUrl);
                        showError('语音播报失败，请检查音频权限');
                        
                        // 继续播放队列
                        if (ttsQueue.length > 0) {
                            const next = ttsQueue.shift();
                            _playTTS(next.text, next.style);
                        }
                    };
                    
                    // 尝试播放（添加用户交互检查和音量设置）
                    try {
                        // 确保音频已解锁
                        await unlockAudio();
                        
                        // 设置音量（使用当前音量设置）
                        audio.volume = currentAudioVolume;
                        
                        // 检查是否需要用户交互
                        const playPromise = audio.play();
                        
                        if (playPromise !== undefined) {
                            playPromise
                                .then(() => {
                                    console.log('✅ 音频播放成功');
                                })
                                .catch((playError) => {
                                    isPlayingTTS = false;
                                    console.error('播放失败:', playError);
                                    
                                    if (playError.name === 'NotAllowedError' || playError.name === 'NotSupportedError') {
                                        // 浏览器阻止自动播放，需要用户交互
                                        const errorMsg = '需要用户交互才能播放音频。请点击页面任意位置后，音频将自动播放。如果问题持续，请检查浏览器音频权限设置。';
                                        showError(errorMsg);
                                        
                                        // 尝试解锁音频（使用Promise链式调用，不使用await）
                                        unlockAudio().then(() => {
                                            // 添加点击事件监听，用户点击后重试播放
                                            const retryPlay = async () => {
                                                try {
                                                    await unlockAudio();
                                                    audio.volume = currentAudioVolume;
                                                    await audio.play();
                                                    console.log('✅ 用户交互后播放成功');
                                                    document.removeEventListener('click', retryPlay);
                                                    document.removeEventListener('touchstart', retryPlay);
                                                } catch (e) {
                                                    console.error('重试播放失败:', e);
                                                    showError('播放失败: ' + (e.message || '请检查浏览器音频权限设置'));
                                                }
                                            };
                                            
                                            document.addEventListener('click', retryPlay, { once: true });
                                            document.addEventListener('touchstart', retryPlay, { once: true });
                                        }).catch((err) => {
                                            console.error('解锁音频失败:', err);
                                        });
                                    } else {
                                        showError(`语音播报失败: ${playError.message || '未知错误'}\n\n错误类型: ${playError.name}`);
                                    }
                                    
                                    if (playbackDiv) {
                                        playbackDiv.style.display = 'none';
                                    }
                                    URL.revokeObjectURL(audioUrl);
                                    
                                    // 继续播放队列
                                    if (ttsQueue.length > 0) {
                                        const next = ttsQueue.shift();
                                        _playTTS(next.text, next.style);
                                    }
                                });
                        }
                    } catch (playError) {
                        isPlayingTTS = false;
                        console.error('播放异常:', playError);
                        showError('语音播报失败: ' + (playError.message || '未知错误'));
                        if (playbackDiv) {
                            playbackDiv.style.display = 'none';
                        }
                        URL.revokeObjectURL(audioUrl);
                        
                        // 继续播放队列
                        if (ttsQueue.length > 0) {
                            const next = ttsQueue.shift();
                            _playTTS(next.text, next.style);
                        }
                    }
                } else {
                    isPlayingTTS = false;
                    console.error('TTS API返回失败:', data);
                    if (playbackDiv) {
                        playbackDiv.style.display = 'none';
                    }
                }
            } catch (err) {
                isPlayingTTS = false;
                console.error('语音播报错误:', err);
                const playbackDiv = document.getElementById('voicePlaybackStatus');
                if (playbackDiv) {
                    playbackDiv.style.display = 'none';
                }
            }
            
            return audioElement; // 返回audio元素，用于优先级队列管理
        }
        
        // ========== 镜头运动检测（ChatGPT建议优化）==========
        const cameraMotionState = {
            lastFrame: null,
            motionDetected: false,
            lastMotionTime: 0,
            motionThreshold: 0.15,  // 运动阈值（帧差百分比）
            stabilityThreshold: 300  // 稳定阈值（ms）
        };
        
        function detectCameraMotion(currentFrameData) {
            if (!cameraMotionState.lastFrame) {
                cameraMotionState.lastFrame = currentFrameData;
                return false;
            }
            
            // 计算帧差（简化版：比较图像数据哈希）
            const currentHash = simpleHash(currentFrameData);
            const lastHash = cameraMotionState.lastFrame;
            
            // 如果哈希差异超过阈值，认为有运动
            const diff = Math.abs(currentHash - lastHash) / Math.max(currentHash, lastHash);
            
            if (diff > cameraMotionState.motionThreshold) {
                cameraMotionState.motionDetected = true;
                cameraMotionState.lastMotionTime = Date.now();
            } else {
                // 如果超过稳定阈值，认为镜头已稳定
                if (Date.now() - cameraMotionState.lastMotionTime > cameraMotionState.stabilityThreshold) {
                    cameraMotionState.motionDetected = false;
                }
            }
            
            cameraMotionState.lastFrame = currentHash;
            return cameraMotionState.motionDetected;
        }
        
        function simpleHash(data) {
            // 简单的哈希函数（用于快速比较）
            if (typeof data === 'string') {
                let hash = 0;
                for (let i = 0; i < data.length; i++) {
                    hash = ((hash << 5) - hash) + data.charCodeAt(i);
                    hash = hash & hash;
                }
                return hash;
            }
            return data;
        }
        
        // ========== 冷却时间配置（ChatGPT建议优化）==========
        const COOL_DOWN_MS = {
            'step': 3000,        // 台阶：3秒
            'hazard': 3000,      // 危险：3秒
            'direction': 2000,   // 转向：2秒
            'signboard': 5000,   // 标识牌：5秒
            'room': 3000,        // 房间号：3秒
            'default': 3000
        };
        
        function getCooldownTime(message) {
            if (message.includes('台阶')) return COOL_DOWN_MS.step;
            if (message.includes('危险')) return COOL_DOWN_MS.hazard;
            if (message.includes('左转') || message.includes('右转')) return COOL_DOWN_MS.direction;
            if (message.includes('洗手间') || message.includes('电梯') || message.includes('出口')) return COOL_DOWN_MS.signboard;
            if (message.includes('房间号')) return COOL_DOWN_MS.room;
            return COOL_DOWN_MS.default;
        }
        
        // 增强的视觉导航显示（产品模式专用）- 主动提示版（ChatGPT优化）
        let lastSpokenGuidance = {};
        const CAMERA_MOTION_THRESHOLD = 300; // 300ms（ChatGPT建议）
        
        function displayVisualGuidanceForProduct(guidance, visionSummary) {
            // 更新方向指示
            const directionIcons = {
                'forward': '⬆️',
                'left': '⬅️',
                'right': '➡️',
                'stop': '⛔'
            };
            
            const directionColors = {
                'forward': '#4CAF50',
                'left': '#2196F3',
                'right': '#FF9800',
                'stop': '#F44336'
            };
            
            const direction = guidance.direction || 'forward';
            const icon = directionIcons[direction] || '➡️';
            const color = directionColors[direction] || '#666';
            
            const directionDiv = document.getElementById('guidanceDirection');
            if (directionDiv) {
                directionDiv.innerHTML = `<span style="color:${color}; font-size:24px;">${icon}</span> <span style="color:${color};">${direction.toUpperCase()}</span>`;
            }
            
            // 更新指引消息
            let html = '';
            if (guidance.messages && guidance.messages.length > 0) {
                guidance.messages.forEach(msg => {
                    html += `<div style="padding:8px; margin:5px 0; background:#f5f5f5; border-radius:5px;">${msg}</div>`;
                });
            } else {
                html = '<div style="color:#999;">环境扫描中，未检测到特殊提示</div>';
            }
            const messagesDiv = document.getElementById('guidanceMessages');
            if (messagesDiv) {
                // 保留处理时间信息
                const existingTimeInfo = messagesDiv.innerHTML.match(/处理时间:.*?ms/);
                messagesDiv.innerHTML = html;
                if (existingTimeInfo && visionSummary && visionSummary.processing_time_ms) {
                    messagesDiv.innerHTML += `<div style="margin-top:10px; padding:5px; background:#e8f5e9; border-radius:5px; font-size:11px; color:#2E7D32;">
                        处理时间: ${visionSummary.processing_time_ms}ms | 物体: ${visionSummary.objects_detected || 0} | 文字: ${visionSummary.texts_detected || 0}
                    </div>`;
                }
            }
            
            // ========== 主动语音播报（ChatGPT优化版）==========
            if (guidance.messages && guidance.messages.length > 0) {
                const now = Date.now();
                
                // 筛选重要消息（台阶、危险、方向、标识牌）
                const importantMessages = guidance.messages.filter(msg => 
                    msg.includes('台阶') || 
                    msg.includes('危险') || 
                    msg.includes('左转') || 
                    msg.includes('右转') || 
                    msg.includes('直行') ||
                    msg.includes('洗手间') ||
                    msg.includes('电梯') ||
                    msg.includes('出口') ||
                    msg.includes('房间号')
                );
                
                if (importantMessages.length > 0) {
                    const currentMessage = importantMessages[0];
                    const messageKey = currentMessage.substring(0, 20); // 使用前20个字符作为唯一标识
                    
                    // 1. 镜头状态检查（ChatGPT建议）
                    if (cameraMotionState.motionDetected && 
                        (now - cameraMotionState.lastMotionTime) < CAMERA_MOTION_THRESHOLD) {
                        // 镜头未稳定，延迟提示或跳过
                        console.log(`📹 镜头运动中，延迟提示: ${currentMessage.substring(0, 20)}...`);
                        return;
                    }
                    
                    // 2. 冷却时间检查（ChatGPT优化：不同事件类型不同冷却时间）
                    const cooldownTime = getCooldownTime(currentMessage);
                    const lastSpokenTime = lastSpokenGuidance[messageKey] || 0;
                    
                    if ((now - lastSpokenTime) < cooldownTime) {
                        console.log(`⏱️ 冷却中，跳过提示: ${currentMessage.substring(0, 20)}... (剩余: ${cooldownTime - (now - lastSpokenTime)}ms)`);
                        return;
                    }
                    
                    // 3. 更新冷却时间记录
                    lastSpokenGuidance[messageKey] = now;
                    
                    // 4. 根据消息类型选择语音风格和优先级
                    let style = 'calm';
                    let priority = false;
                    
                    if (currentMessage.includes('台阶') || currentMessage.includes('危险')) {
                        style = 'urgent'; // 紧急提示
                        priority = true;   // 高优先级（critical）
                    } else if (currentMessage.includes('左转') || currentMessage.includes('右转')) {
                        style = 'cheerful'; // 导航提示
                        priority = true;    // 高优先级（high）
                    } else {
                        priority = false;   // 普通优先级（medium/low）
                    }
                    
                    // 5. 播放（使用优先级队列管理器）
                    // 修复：移除hasFocus检查，直接播放（Mac上摄像头启动后可以播放）
                    debugLog(`准备播放语音: ${currentMessage.substring(0, 30)}...`, 'info');
                    console.log(`🔊 [语音播报] 准备播放: ${currentMessage.substring(0, 30)}...`);
                    // 使用Promise链式调用，不使用await
                    speakText(currentMessage, style, priority)
                        .then(() => {
                            debugLog('✅ 语音已发送到播放队列', 'info');
                            console.log(`✅ [语音播报] 已发送到播放队列`);
                        })
                        .catch((err) => {
                            debugLog(`❌ 语音播放失败: ${err.message}`, 'error');
                            console.error(`❌ [语音播报] 失败:`, err);
                            // 如果失败，尝试用户交互后播放
                            const playWhenReady = () => {
                                speakText(currentMessage, style, priority)
                                    .then(() => {
                                        debugLog('✅ 用户交互后语音已播放', 'info');
                                        console.log(`✅ [语音播报] 用户交互后已播放`);
                                    })
                                    .catch((e) => {
                                        debugLog(`❌ 用户交互后播放也失败: ${e.message}`, 'error');
                                        console.error(`❌ [语音播报] 用户交互后也失败:`, e);
                                    });
                                document.removeEventListener('click', playWhenReady);
                                document.removeEventListener('touchstart', playWhenReady);
                            };
                            document.addEventListener('click', playWhenReady, { once: true });
                            document.addEventListener('touchstart', playWhenReady, { once: true });
                        });
                }
            }
        }
    