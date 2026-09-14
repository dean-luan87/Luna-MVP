# Luna Backend v1.2.0

Luna Badge 后端服务 - 工程化重构版本

## 📁 目录结构

```
luna_backend/
├── app.py              # Flask应用入口
├── wsgi.py             # WSGI入口（生产环境）
├── config/             # 配置模块
│   ├── settings.py    # 应用配置
│   ├── constants.py   # 常量定义
│   └── error_codes.py # 错误码体系
├── core/               # 核心模块
│   ├── logger.py      # 统一日志系统
│   ├── exceptions.py  # 异常体系
│   ├── response.py    # 统一响应格式
│   ├── error_manager.py # 错误管理器
│   └── utils.py       # 工具函数
├── routes/             # 路由层（API端点）
├── services/           # 业务逻辑层
│   ├── tts/           # TTS服务
│   ├── vision/        # 视觉服务
│   ├── navigation/    # 导航服务
│   ├── scene/         # 场景记忆服务
│   ├── event/         # 事件系统
│   └── system/        # 系统服务
└── static/            # 静态文件
```

## 🚀 快速开始

### 安装依赖

```bash
pip install flask flask-cors
```

### 运行开发服务器

```bash
python app.py
```

### 运行生产服务器

```bash
gunicorn wsgi:app
```

## 📖 开发规范

详见 `docs/ENGINEERING_STANDARDS.md`

## 🔧 错误码体系

详见 `config/error_codes.py`

## 📝 版本历史

- v1.2.0: 工程化重构，模块拆分，错误码体系



