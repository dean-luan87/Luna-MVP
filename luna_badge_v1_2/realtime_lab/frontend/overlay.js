const overlay = document.getElementById("overlay");
const overlayCtx = overlay.getContext("2d");

function drawDetections(objects) {
  if (!camera.videoWidth || !camera.videoHeight) {
    return;
  }

  overlay.width = camera.videoWidth;
  overlay.height = camera.videoHeight;

  overlayCtx.clearRect(0, 0, overlay.width, overlay.height);

  overlayCtx.lineWidth = 2;
  overlayCtx.font = "14px Arial";

  objects.forEach((obj) => {
    overlayCtx.strokeStyle = "lime";
    overlayCtx.strokeRect(
      obj.x1,
      obj.y1,
      obj.x2 - obj.x1,
      obj.y2 - obj.y1
    );

    overlayCtx.fillStyle = "lime";
    const label = `${obj.cls} ${Math.round(obj.conf * 100)}%`;
    overlayCtx.fillText(label, obj.x1 + 2, obj.y1 - 4);
  });
}





