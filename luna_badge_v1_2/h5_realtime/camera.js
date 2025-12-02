// camera.js - 相机控制模块

const camera = document.getElementById("camera");
const captureCanvas = document.getElementById("captureCanvas");
let cameraStream = null;

/**
 * 启动相机
 */
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "environment",  // 后置摄像头
                width: { ideal: 1280 },
                height: { ideal: 720 }
            },
            audio: false
        });
        
        camera.srcObject = stream;
        cameraStream = stream;
        
        // 等待视频元数据加载
        await new Promise((resolve) => {
            camera.onloadedmetadata = resolve;
        });
        
        console.log(`相机启动成功: ${camera.videoWidth}x${camera.videoHeight}`);
        return true;
    } catch (err) {
        console.error("相机启动失败:", err);
        alert(`相机启动失败: ${err.message}\n\n请确保已授权相机权限。`);
        return false;
    }
}

/**
 * 停止相机
 */
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    camera.srcObject = null;
}

/**
 * 捕获当前帧
 * @returns {string} Base64 编码的 JPEG 图像
 */
function captureFrame() {
    if (!camera.videoWidth || !camera.videoHeight) {
        return null;
    }
    
    captureCanvas.width = camera.videoWidth;
    captureCanvas.height = camera.videoHeight;
    
    const ctx = captureCanvas.getContext("2d");
    ctx.drawImage(camera, 0, 0, captureCanvas.width, captureCanvas.height);
    
    // 转换为 JPEG，质量 0.6
    return captureCanvas.toDataURL("image/jpeg", 0.6);
}

/**
 * 获取相机分辨率
 */
function getCameraResolution() {
    return {
        width: camera.videoWidth || 640,
        height: camera.videoHeight || 480
    };
}

