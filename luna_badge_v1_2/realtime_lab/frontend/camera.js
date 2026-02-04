const camera = document.getElementById("camera");
const captureCanvas = document.getElementById("captureCanvas");

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment", width: 640, height: 480 },
      audio: false,
    });
    camera.srcObject = stream;
    console.log("✅ 相机启动成功");
  } catch (err) {
    console.error("startCamera error:", err);
    
    // 详细的错误提示
    let errorMsg = "无法打开摄像头。\n\n";
    
    if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
      errorMsg += "原因：相机权限被拒绝\n";
      errorMsg += "解决：请在 iPhone 设置 > Safari > 相机 中允许访问";
    } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
      errorMsg += "原因：未找到摄像头设备";
    } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
      errorMsg += "原因：摄像头被其他应用占用";
    } else if (location.protocol === "http:" && location.hostname !== "localhost" && location.hostname !== "127.0.0.1") {
      errorMsg += "原因：iOS Safari 需要 HTTPS 才能访问摄像头\n";
      errorMsg += "解决：请使用 HTTPS 访问，或使用 localhost\n";
      errorMsg += "\n当前地址：" + location.href;
    } else {
      errorMsg += "错误：" + err.message;
    }
    
    alert(errorMsg);
  }
}

function captureFrame() {
  if (!camera.videoWidth || !camera.videoHeight) {
    return null;
  }

  captureCanvas.width = camera.videoWidth;
  captureCanvas.height = camera.videoHeight;

  const ctx = captureCanvas.getContext("2d");
  ctx.drawImage(camera, 0, 0, captureCanvas.width, captureCanvas.height);

  // 质量可调节，0.5 是比较折中
  return captureCanvas.toDataURL("image/jpeg", 0.5);
}

window.addEventListener("load", startCamera);

