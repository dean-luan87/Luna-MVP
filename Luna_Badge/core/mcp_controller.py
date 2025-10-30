#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge MCP设备控制协议
借鉴小智ESP32的MCP设计，实现统一设备控制接口
"""

import logging
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class DeviceType(Enum):
    """设备类型枚举"""
    VOLUME = "volume"           # 音量控制
    LED = "led"                 # LED灯光
    MOTOR = "motor"             # 电机
    GPIO = "gpio"               # GPIO控制
    DISPLAY = "display"         # 显示屏
    SENSOR = "sensor"           # 传感器
    CAMERA = "camera"           # 摄像头
    SPEAKER = "speaker"         # 扬声器
    MICROPHONE = "microphone"   # 麦克风

class DeviceAction(Enum):
    """设备操作枚举"""
    SET = "set"                 # 设置值
    GET = "get"                 # 获取值
    START = "start"             # 启动
    STOP = "stop"               # 停止
    RESET = "reset"             # 重置
    STATUS = "status"           # 获取状态

@dataclass
class DeviceCommand:
    """设备命令数据类"""
    device_type: DeviceType
    action: DeviceAction
    params: Dict[str, Any]
    timestamp: float = 0.0

@dataclass
class DeviceStatus:
    """设备状态数据类"""
    device_type: DeviceType
    status: str
    data: Dict[str, Any]
    timestamp: float = 0.0

class MCPDevice:
    """MCP设备基类"""
    
    def __init__(self, name: str, device_type: DeviceType):
        """
        初始化MCP设备
        
        Args:
            name: 设备名称
            device_type: 设备类型
        """
        self.name = name
        self.device_type = device_type
        self.enabled = True
        self.status = "idle"
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    async def control(self, action: DeviceAction, params: Dict[str, Any]) -> DeviceStatus:
        """
        控制设备
        
        Args:
            action: 操作类型
            params: 参数
            
        Returns:
            DeviceStatus: 设备状态
        """
        try:
            if action == DeviceAction.START:
                result = await self._start(params)
            elif action == DeviceAction.STOP:
                result = await self._stop(params)
            elif action == DeviceAction.SET:
                result = await self._set(params)
            elif action == DeviceAction.GET:
                result = await self._get(params)
            elif action == DeviceAction.RESET:
                result = await self._reset(params)
            elif action == DeviceAction.STATUS:
                result = await self._get_status(params)
            else:
                result = {"success": False, "error": f"Unknown action: {action.value}"}
            
            return DeviceStatus(
                device_type=self.device_type,
                status="success" if result.get("success", False) else "error",
                data=result
            )
        except Exception as e:
            self.logger.error(f"Device control error: {e}")
            return DeviceStatus(
                device_type=self.device_type,
                status="error",
                data={"success": False, "error": str(e)}
            )
    
    async def _start(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """启动设备"""
        self.status = "running"
        return {"success": True, "message": f"Device {self.name} started"}
    
    async def _stop(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """停止设备"""
        self.status = "stopped"
        return {"success": True, "message": f"Device {self.name} stopped"}
    
    async def _set(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """设置设备参数"""
        return {"success": True, "message": f"Device {self.name} settings updated"}
    
    async def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取设备参数"""
        return {"success": True, "data": {}}
    
    async def _reset(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """重置设备"""
        self.status = "idle"
        return {"success": True, "message": f"Device {self.name} reset"}
    
    async def _get_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取设备状态"""
        return {
            "success": True,
            "data": {
                "name": self.name,
                "type": self.device_type.value,
                "status": self.status,
                "enabled": self.enabled
            }
        }

class MCPController:
    """MCP设备控制器"""
    
    def __init__(self):
        """初始化MCP控制器"""
        self.devices: Dict[str, MCPDevice] = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("🎛️ MCP设备控制器初始化完成")
    
    def register_device(self, device: MCPDevice):
        """
        注册设备
        
        Args:
            device: MCP设备实例
        """
        self.devices[device.name] = device
        self.logger.info(f"✅ 注册设备: {device.name} ({device.device_type.value})")
    
    async def control_device(self, device_name: str, action: DeviceAction, 
                           params: Dict[str, Any] = None) -> DeviceStatus:
        """
        控制设备
        
        Args:
            device_name: 设备名称
            action: 操作类型
            params: 参数
            
        Returns:
            DeviceStatus: 设备状态
        """
        if params is None:
            params = {}
        
        if device_name not in self.devices:
            self.logger.error(f"❌ 设备未找到: {device_name}")
            return DeviceStatus(
                device_type=DeviceType.GPIO,
                status="error",
                data={"success": False, "error": f"Device not found: {device_name}"}
            )
        
        device = self.devices[device_name]
        if not device.enabled:
            self.logger.warning(f"⚠️ 设备已禁用: {device_name}")
            return DeviceStatus(
                device_type=device.device_type,
                status="error",
                data={"success": False, "error": f"Device disabled: {device_name}"}
            )
        
        self.logger.info(f"🎮 控制设备: {device_name} - {action.value}")
        return await device.control(action, params)
    
    async def control_device_by_type(self, device_type: DeviceType, action: DeviceAction,
                                    params: Dict[str, Any] = None) -> List[DeviceStatus]:
        """
        按类型控制设备
        
        Args:
            device_type: 设备类型
            action: 操作类型
            params: 参数
            
        Returns:
            List[DeviceStatus]: 设备状态列表
        """
        if params is None:
            params = {}
        
        results = []
        for device_name, device in self.devices.items():
            if device.device_type == device_type:
                result = await self.control_device(device_name, action, params)
                results.append(result)
        
        return results
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """获取所有设备列表"""
        devices = []
        for name, device in self.devices.items():
            devices.append({
                "name": name,
                "type": device.device_type.value,
                "status": device.status,
                "enabled": device.enabled
            })
        return devices
    
    def get_device_status(self, device_name: str) -> Optional[Dict[str, Any]]:
        """获取设备状态"""
        if device_name in self.devices:
            device = self.devices[device_name]
            return {
                "name": device.name,
                "type": device.device_type.value,
                "status": device.status,
                "enabled": device.enabled
            }
        return None


# 具体设备实现示例

class VolumeDevice(MCPDevice):
    """音量设备"""
    
    def __init__(self, name: str = "volume"):
        super().__init__(name, DeviceType.VOLUME)
        self.volume = 50  # 默认音量50%
    
    async def _set(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """设置音量"""
        if "volume" in params:
            volume = params["volume"]
            if 0 <= volume <= 100:
                self.volume = volume
                self.logger.info(f"🔊 设置音量: {self.volume}%")
                return {"success": True, "volume": self.volume}
            else:
                return {"success": False, "error": "Volume out of range (0-100)"}
        return {"success": False, "error": "Missing volume parameter"}
    
    async def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取音量"""
        return {"success": True, "volume": self.volume}

class LEDDevice(MCPDevice):
    """LED设备"""
    
    def __init__(self, name: str = "led"):
        super().__init__(name, DeviceType.LED)
        self.brightness = 0
        self.color = (255, 255, 255)  # RGB
        self.mode = "off"  # off, on, blink, rainbow
    
    async def _set(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """设置LED"""
        if "brightness" in params:
            self.brightness = params["brightness"]
        if "color" in params:
            self.color = params["color"]
        if "mode" in params:
            self.mode = params["mode"]
        
        self.logger.info(f"💡 LED设置: mode={self.mode}, brightness={self.brightness}, color={self.color}")
        return {"success": True, "mode": self.mode, "brightness": self.brightness, "color": self.color}
    
    async def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取LED状态"""
        return {
            "success": True,
            "mode": self.mode,
            "brightness": self.brightness,
            "color": self.color
        }

class MotorDevice(MCPDevice):
    """电机设备"""
    
    def __init__(self, name: str = "motor"):
        super().__init__(name, DeviceType.MOTOR)
        self.speed = 0  # 速度 0-100
        self.direction = "forward"  # forward, backward, stop
    
    async def _set(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """设置电机"""
        if "speed" in params:
            self.speed = params["speed"]
        if "direction" in params:
            self.direction = params["direction"]
        
        self.logger.info(f"⚙️ 电机设置: speed={self.speed}, direction={self.direction}")
        return {"success": True, "speed": self.speed, "direction": self.direction}
    
    async def _start(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """启动电机"""
        if "speed" in params:
            self.speed = params["speed"]
        if "direction" in params:
            self.direction = params["direction"]
        self.status = "running"
        self.logger.info(f"🚀 电机启动: speed={self.speed}, direction={self.direction}")
        return {"success": True, "speed": self.speed, "direction": self.direction}
    
    async def _stop(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """停止电机"""
        self.speed = 0
        self.status = "stopped"
        self.logger.info("🛑 电机停止")
        return {"success": True, "speed": 0}
    
    async def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取电机状态"""
        return {
            "success": True,
            "speed": self.speed,
            "direction": self.direction,
            "status": self.status
        }


# 全局MCP控制器实例
global_mcp_controller = MCPController()

def register_device(device: MCPDevice):
    """注册设备的便捷函数"""
    global_mcp_controller.register_device(device)

async def control_device(device_name: str, action: DeviceAction, params: Dict[str, Any] = None) -> DeviceStatus:
    """控制设备的便捷函数"""
    return await global_mcp_controller.control_device(device_name, action, params)

def get_devices() -> List[Dict[str, Any]]:
    """获取设备列表的便捷函数"""
    return global_mcp_controller.get_devices()


if __name__ == "__main__":
    # 测试MCP控制器
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    async def test_mcp_controller():
        """测试MCP控制器"""
        controller = MCPController()
        
        # 注册设备
        volume = VolumeDevice()
        led = LEDDevice()
        motor = MotorDevice()
        
        controller.register_device(volume)
        controller.register_device(led)
        controller.register_device(motor)
        
        # 控制设备
        await controller.control_device("volume", DeviceAction.SET, {"volume": 75})
        await controller.control_device("led", DeviceAction.SET, {"brightness": 100, "mode": "on"})
        await controller.control_device("motor", DeviceAction.START, {"speed": 50, "direction": "forward"})
        
        # 获取设备状态
        status = await controller.control_device("volume", DeviceAction.GET)
        print(f"Volume status: {status.data}")
        
        # 获取所有设备
        devices = controller.get_devices()
        print(f"Registered devices: {devices}")
    
    # 运行测试
    asyncio.run(test_mcp_controller())
