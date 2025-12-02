# bridge/ws_server.py
"""
WebSocket 服务器：接收 JS 端的 YOLO + IMU 数据，转发给 NavigationRuntime
"""
import asyncio
import json
import logging
import sys
import os
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("⚠️ websockets 模块未安装，请运行: pip install websockets")

from core.navigation.navigation_runtime import NavigationRuntime

logger = logging.getLogger(__name__)


class WSNavigationBridge:
    """WebSocket 导航桥接器"""
    
    def __init__(self, ideal_heading_deg: Optional[float] = None):
        self.runtime = NavigationRuntime(
            ideal_heading_deg=ideal_heading_deg,
            on_result=self._on_result
        )
        self.clients = set()
    
    def _on_result(self, result: dict):
        """结果回调：推送给所有连接的客户端"""
        if not self.clients:
            return
        
        message = json.dumps(result, ensure_ascii=False)
        # 异步发送给所有客户端
        asyncio.create_task(self._broadcast(message))
    
    async def _broadcast(self, message: str):
        """广播消息给所有客户端"""
        if not self.clients:
            return
        
        disconnected = set()
        for ws in self.clients:
            try:
                await ws.send(message)
            except Exception as e:
                logger.warning(f"[WS Bridge] send error: {e}")
                disconnected.add(ws)
        
        # 清理断开的连接
        self.clients -= disconnected
    
    async def handle_client(self, ws, path):
        """处理单个客户端连接"""
        self.clients.add(ws)
        client_addr = ws.remote_address
        logger.info(f"[WS Bridge] Client connected: {client_addr}")
        
        try:
            async for msg in ws:
                try:
                    data = json.loads(msg)
                    logger.debug(f"[WS Bridge] Received data from {client_addr}: {data}")
                    
                    # 转发给 NavigationRuntime
                    result = self.runtime.feed(data)
                    
                    # 立即返回结果给客户端
                    await ws.send(json.dumps(result, ensure_ascii=False))
                    
                except json.JSONDecodeError as e:
                    logger.error(f"[WS Bridge] JSON decode error: {e}")
                    await ws.send(json.dumps({
                        "error": "Invalid JSON",
                        "message": str(e)
                    }))
                except Exception as e:
                    logger.error(f"[WS Bridge] Processing error: {e}")
                    await ws.send(json.dumps({
                        "error": "Processing failed",
                        "message": str(e)
                    }))
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"[WS Bridge] Client disconnected: {client_addr}")
        except Exception as e:
            logger.error(f"[WS Bridge] Connection error: {e}")
        finally:
            self.clients.discard(ws)
    
    async def start_server(self, host: str = "0.0.0.0", port: int = 8765):
        """启动 WebSocket 服务器"""
        logger.info(f"[WS Bridge] Starting server on ws://{host}:{port} ...")
        async with websockets.serve(self.handle_client, host, port):
            logger.info(f"[WS Bridge] Server listening on ws://{host}:{port}")
            await asyncio.Future()  # run forever


async def start_server(ideal_heading_deg: float = None, port: int = 8765):
    """便捷启动函数"""
    bridge = WSNavigationBridge(ideal_heading_deg=ideal_heading_deg)
    await bridge.start_server(port=port)


if __name__ == "__main__":
    if not WEBSOCKETS_AVAILABLE:
        print("❌ 请先安装 websockets: pip install websockets")
        sys.exit(1)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 从命令行参数读取理想方向（可选）
    ideal_heading = None
    if len(sys.argv) > 1:
        try:
            ideal_heading = float(sys.argv[1])
        except ValueError:
            print(f"⚠️ 无效的理想方向参数: {sys.argv[1]}")
    
    print("=" * 70)
    print("🚀 WebSocket 导航桥接服务器")
    print("=" * 70)
    print(f"  地址: ws://localhost:8765")
    print(f"  理想方向: {ideal_heading if ideal_heading is not None else '未设置'}")
    print("")
    print("  JS 端连接示例:")
    print("    const ws = new WebSocket('ws://localhost:8765');")
    print("    ws.send(JSON.stringify({")
    print("      heading_deg: 90,")
    print("      speed_mps: 0.8,")
    print("      yolo: [...],")
    print("      ocr: [...]")
    print("    }));")
    print("=" * 70)
    
    try:
        asyncio.run(start_server(ideal_heading_deg=ideal_heading))
    except KeyboardInterrupt:
        print("\n✅ 服务器已停止")

