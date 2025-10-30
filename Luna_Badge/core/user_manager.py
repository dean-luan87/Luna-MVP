#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 用户管理系统
借鉴小智ESP32的用户认证和设备绑定设计
"""

import logging
import hashlib
import time
import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import random

logger = logging.getLogger(__name__)

class UserStatus(Enum):
    """用户状态枚举"""
    ACTIVE = "active"           # 活跃
    INACTIVE = "inactive"       # 不活跃
    SUSPENDED = "suspended"     # 已暂停
    DELETED = "deleted"         # 已删除

class DeviceStatus(Enum):
    """设备状态枚举"""
    ONLINE = "online"           # 在线
    OFFLINE = "offline"         # 离线
    ERROR = "error"             # 错误

@dataclass
class User:
    """用户数据类"""
    user_id: str
    phone: str
    nickname: str
    email: str
    created_at: float
    last_login: float
    status: UserStatus
    devices: List[str]  # 绑定的设备ID列表
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "phone": self.phone,
            "nickname": self.nickname,
            "email": self.email,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "status": self.status.value,
            "devices": self.devices
        }

@dataclass
class Device:
    """设备数据类"""
    device_id: str
    device_name: str
    device_type: str
    user_id: str
    registered_at: float
    last_active: float
    status: DeviceStatus
    ip_address: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "user_id": self.user_id,
            "registered_at": self.registered_at,
            "last_active": self.last_active,
            "status": self.status.value,
            "ip_address": self.ip_address
        }

class UserManager:
    """用户管理器"""
    
    def __init__(self, storage_file: str = "data/users.json"):
        """
        初始化用户管理器
        
        Args:
            storage_file: 用户数据存储文件
        """
        self.storage_file = storage_file
        self.users: Dict[str, User] = {}
        self.devices: Dict[str, Device] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}  # token -> session
        
        # 验证码存储 (phone -> code)
        self.verification_codes: Dict[str, Dict[str, Any]] = {}
        
        # 验证码配置
        self.code_expire_time = 300  # 5分钟过期
        self.max_attempts = 5       # 最大尝试次数
        self.rate_limit = 60        # 频率限制（秒）
        self.sms_service = None     # 预留真实短信服务接口
        
        self.logger = logging.getLogger(__name__)
        self._load_data()
        self.logger.info("👤 用户管理器初始化完成")
    
    def _load_data(self):
        """加载数据"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 加载用户
                    for user_data in data.get('users', []):
                        user = User(
                            user_id=user_data['user_id'],
                            phone=user_data['phone'],
                            nickname=user_data['nickname'],
                            email=user_data['email'],
                            created_at=user_data['created_at'],
                            last_login=user_data['last_login'],
                            status=UserStatus(user_data['status']),
                            devices=user_data.get('devices', [])
                        )
                        self.users[user.user_id] = user
                    
                    # 加载设备
                    for device_data in data.get('devices', []):
                        device = Device(
                            device_id=device_data['device_id'],
                            device_name=device_data['device_name'],
                            device_type=device_data['device_type'],
                            user_id=device_data['user_id'],
                            registered_at=device_data['registered_at'],
                            last_active=device_data['last_active'],
                            status=DeviceStatus(device_data['status']),
                            ip_address=device_data.get('ip_address', '')
                        )
                        self.devices[device.device_id] = device
                    
                    self.logger.info(f"📂 加载数据: {len(self.users)}个用户, {len(self.devices)}个设备")
        except Exception as e:
            self.logger.error(f"❌ 加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                'users': [user.to_dict() for user in self.users.values()],
                'devices': [device.to_dict() for device in self.devices.values()]
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info("💾 数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存数据失败: {e}")
    
    def send_verification_code(self, phone: str) -> bool:
        """
        发送验证码
        
        Args:
            phone: 手机号
            
        Returns:
            bool: 是否发送成功
        """
        # 检查频率限制
        if phone in self.verification_codes:
            vc = self.verification_codes[phone]
            if time.time() - vc.get('sent_at', 0) < self.rate_limit:
                self.logger.warning(f"⚠️ 请求过于频繁: {phone}")
                return False
        
        # 生成验证码
        code = str(random.randint(100000, 999999))
        
        # 存储验证码
        self.verification_codes[phone] = {
            'code': code,
            'expires_at': time.time() + self.code_expire_time,
            'sent_at': time.time(),
            'attempts': 0  # 尝试次数
        }
        
        self.logger.info(f"📱 发送验证码到 {phone}: {code}")
        
        # TODO: 调用真实短信服务
        if self.sms_service:
            # 预留接口
            # result = self.sms_service.send(phone, f"您的验证码是：{code}，5分钟内有效")
            pass
        
        return True
    
    def verify_code(self, phone: str, code: str) -> bool:
        """
        验证验证码
        
        Args:
            phone: 手机号
            code: 验证码
            
        Returns:
            bool: 验证是否成功
        """
        if phone not in self.verification_codes:
            self.logger.warning(f"⚠️ 验证码不存在: {phone}")
            return False
        
        vc = self.verification_codes[phone]
        
        # 检查是否过期
        if time.time() > vc['expires_at']:
            self.logger.warning(f"⚠️ 验证码已过期: {phone}")
            del self.verification_codes[phone]
            return False
        
        # 检查尝试次数
        if vc['attempts'] >= self.max_attempts:
            self.logger.warning(f"⚠️ 验证码尝试次数过多: {phone}")
            del self.verification_codes[phone]
            return False
        
        vc['attempts'] += 1
        
        if vc['code'] == code:
            # 验证成功，删除验证码
            del self.verification_codes[phone]
            self.logger.info(f"✅ 验证码验证成功: {phone}")
            return True
        
        self.logger.warning(f"⚠️ 验证码错误: {phone}, 剩余尝试次数: {self.max_attempts - vc['attempts']}")
        return False
    
    def register_user(self, phone: str, nickname: str = None, email: str = None) -> Optional[User]:
        """
        注册用户
        
        Args:
            phone: 手机号
            nickname: 昵称
            email: 邮箱
            
        Returns:
            User: 用户对象，如果注册失败返回None
        """
        # 检查手机号是否已存在
        for user in self.users.values():
            if user.phone == phone:
                self.logger.warning(f"⚠️ 手机号已注册: {phone}")
                return None
        
        # 创建新用户
        user = User(
            user_id=f"user_{int(time.time())}",
            phone=phone,
            nickname=nickname or f"用户{phone[-4:]}",
            email=email or "",
            created_at=time.time(),
            last_login=time.time(),
            status=UserStatus.ACTIVE,
            devices=[]
        )
        
        self.users[user.user_id] = user
        self._save_data()
        
        self.logger.info(f"✅ 用户注册成功: {user.user_id} - {phone}")
        return user
    
    def login(self, phone: str, verification_code: str) -> Optional[str]:
        """
        用户登录
        
        Args:
            phone: 手机号
            verification_code: 验证码
            
        Returns:
            str: 访问令牌，如果登录失败返回None
        """
        # 验证验证码
        if not self.verify_code(phone, verification_code):
            self.logger.warning(f"⚠️ 验证码错误: {phone}")
            return None
        
        # 查找用户
        user = None
        for u in self.users.values():
            if u.phone == phone:
                user = u
                break
        
        # 如果用户不存在，自动注册
        if user is None:
            user = self.register_user(phone)
        
        if user is None:
            return None
        
        # 更新登录时间
        user.last_login = time.time()
        self._save_data()
        
        # 生成访问令牌
        token = self._generate_token(user.user_id)
        
        # 保存会话
        self.sessions[token] = {
            'user_id': user.user_id,
            'created_at': time.time(),
            'expires_at': time.time() + 86400 * 7  # 7天过期
        }
        
        self.logger.info(f"✅ 用户登录成功: {user.user_id} - {phone}")
        return token
    
    def register_device(self, device_id: str, device_name: str, device_type: str,
                       user_id: str, ip_address: str = "") -> Optional[Device]:
        """
        注册设备
        
        Args:
            device_id: 设备ID
            device_name: 设备名称
            device_type: 设备类型
            user_id: 用户ID
            ip_address: IP地址
            
        Returns:
            Device: 设备对象，如果注册失败返回None
        """
        # 检查用户是否存在
        if user_id not in self.users:
            self.logger.error(f"❌ 用户不存在: {user_id}")
            return None
        
        # 创建设备
        device = Device(
            device_id=device_id,
            device_name=device_name,
            device_type=device_type,
            user_id=user_id,
            registered_at=time.time(),
            last_active=time.time(),
            status=DeviceStatus.ONLINE,
            ip_address=ip_address
        )
        
        self.devices[device.device_id] = device
        
        # 添加到用户设备列表
        user = self.users[user_id]
        if device_id not in user.devices:
            user.devices.append(device_id)
        
        self._save_data()
        
        self.logger.info(f"✅ 设备注册成功: {device_id} - {device_name}")
        return device
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return self.users.get(user_id)
    
    def get_device(self, device_id: str) -> Optional[Device]:
        """获取设备"""
        return self.devices.get(device_id)
    
    def get_user_devices(self, user_id: str) -> List[Device]:
        """获取用户的设备列表"""
        user = self.get_user(user_id)
        if user is None:
            return []
        
        devices = []
        for device_id in user.devices:
            device = self.get_device(device_id)
            if device:
                devices.append(device)
        
        return devices
    
    def _generate_token(self, user_id: str) -> str:
        """生成访问令牌"""
        data = f"{user_id}{time.time()}{random.random()}"
        token = hashlib.sha256(data.encode()).hexdigest()
        return token
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        验证令牌
        
        Args:
            token: 访问令牌
            
        Returns:
            str: 用户ID，如果验证失败返回None
        """
        if token not in self.sessions:
            return None
        
        session = self.sessions[token]
        
        # 检查是否过期
        if time.time() > session['expires_at']:
            del self.sessions[token]
            return None
        
        return session['user_id']
    
    def update_device_status(self, device_id: str, status: DeviceStatus):
        """更新设备状态"""
        if device_id in self.devices:
            device = self.devices[device_id]
            device.status = status
            device.last_active = time.time()
            self._save_data()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        active_users = len([u for u in self.users.values() if u.status == UserStatus.ACTIVE])
        online_devices = len([d for d in self.devices.values() if d.status == DeviceStatus.ONLINE])
        
        return {
            "total_users": len(self.users),
            "active_users": active_users,
            "total_devices": len(self.devices),
            "online_devices": online_devices,
            "active_sessions": len(self.sessions)
        }


# 全局用户管理器实例
global_user_manager = UserManager()

def send_verification_code(phone: str) -> bool:
    """发送验证码的便捷函数"""
    return global_user_manager.send_verification_code(phone)

def verify_code(phone: str, code: str) -> bool:
    """验证验证码的便捷函数"""
    return global_user_manager.verify_code(phone, code)

def register_user(phone: str, nickname: str = None, email: str = None) -> Optional[User]:
    """注册用户的便捷函数"""
    return global_user_manager.register_user(phone, nickname, email)

def login(phone: str, verification_code: str) -> Optional[str]:
    """用户登录的便捷函数"""
    return global_user_manager.login(phone, verification_code)

def verify_token(token: str) -> Optional[str]:
    """验证令牌的便捷函数"""
    return global_user_manager.verify_token(token)


if __name__ == "__main__":
    # 测试用户管理
    logging.basicConfig(level=logging.INFO)
    
    def test_user_manager():
        """测试用户管理器"""
        manager = UserManager()
        
        # 发送验证码
        phone = "13800138000"
        manager.send_verification_code(phone)
        
        # 模拟验证码
        # 在实际测试中需要从日志中获取验证码
        # code = "123456"  # 从日志中获取
        
        # 注册用户
        user = manager.register_user(phone, "测试用户")
        print(f"注册用户: {user}")
        
        # 注册设备
        device = manager.register_device("device_001", "Luna Badge", "badge", user.user_id)
        print(f"注册设备: {device}")
        
        # 获取统计信息
        stats = manager.get_statistics()
        print(f"统计信息: {stats}")
    
    # 运行测试
    test_user_manager()
