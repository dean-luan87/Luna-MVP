# Luna Badge 服务器启动问题排查指南

## 🔴 "连接被拒绝" 问题

### 问题现象
浏览器访问测试地址时显示"连接被拒绝"或"无法访问此网站"

### 排查步骤

#### 1. 检查服务器是否启动

```bash
# 检查是否有Python进程在运行
ps aux | grep web_test_server

# 检查端口是否被占用
lsof -ti:9000
```

**解决方案**:
- 如果没有进程，需要启动服务器
- 如果端口被占用，使用其他端口

#### 2. 启动服务器

```bash
cd Luna_Badge
python3 web_test_server.py
```

**注意**: 
- 确保在 `Luna_Badge` 目录下执行
- 查看启动日志，确认端口号
- 如果看到错误信息，记录下来

#### 3. 检查端口可用性

```bash
# 检查9000端口
lsof -ti:9000

# 如果被占用，查找可用端口
python3 -c "
import socket
for port in range(9000, 9100):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result != 0:
        print(f'可用端口: {port}')
        break
"
```

#### 4. 使用指定端口启动

如果9000端口不可用，使用其他端口：

```bash
# 使用9001端口
PORT=9001 python3 web_test_server.py

# 或使用9999端口
PORT=9999 python3 web_test_server.py
```

#### 5. 检查防火墙设置

macOS 防火墙可能阻止连接：

```bash
# 检查防火墙状态
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 临时关闭防火墙（测试用）
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

**注意**: 测试完成后记得重新开启防火墙

#### 6. 检查Python依赖

```bash
# 检查Flask是否安装
python3 -c "import flask; print(flask.__version__)"

# 如果没有安装
pip3 install flask flask-cors

# 如果使用虚拟环境
source venv/bin/activate
pip install flask flask-cors
```

#### 7. 检查文件权限

```bash
# 确保web_test_server.py有执行权限
chmod +x web_test_server.py

# 或直接使用python3运行
python3 web_test_server.py
```

#### 8. 查看详细错误日志

启动服务器时，查看控制台输出的错误信息：

```bash
# 启动并查看所有输出
python3 web_test_server.py 2>&1 | tee server.log
```

常见错误：
- `Address already in use` → 端口被占用
- `ModuleNotFoundError` → 缺少Python依赖
- `Permission denied` → 权限问题
- `SyntaxError` → 代码语法错误

---

## 🟡 其他常见问题

### 问题1: 端口5000/8080/9000都被占用

**解决方案**:
```bash
# 查找并杀死占用端口的进程
lsof -ti:9000 | xargs kill -9

# 或使用其他端口
PORT=9999 python3 web_test_server.py
```

### 问题2: 模块导入错误

**解决方案**:
```bash
# 确保在正确的目录
cd Luna_Badge

# 检查Python路径
python3 -c "import sys; print(sys.path)"

# 添加当前目录到Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 web_test_server.py
```

### 问题3: SSL证书问题（HTTPS模式）

**解决方案**:
```bash
# 生成SSL证书
python3 generate_ssl_cert.py

# 或使用HTTP模式（删除SSL证书）
rm -rf ssl/
python3 web_test_server.py
```

### 问题4: 浏览器无法访问

**检查清单**:
- ✅ 服务器是否正常启动（查看控制台输出）
- ✅ 端口号是否正确（查看启动日志）
- ✅ 使用正确的URL格式：`http://127.0.0.1:端口号/`
- ✅ 浏览器控制台是否有错误（F12查看）
- ✅ 防火墙是否阻止连接

---

## ✅ 快速诊断脚本

创建并运行以下脚本进行快速诊断：

```bash
#!/bin/bash
# quick_check.sh

echo "=== Luna Badge 服务器诊断 ==="

# 检查Python
echo -n "Python版本: "
python3 --version

# 检查依赖
echo -n "Flask: "
python3 -c "import flask; print('OK')" 2>/dev/null || echo "未安装"

# 检查端口
echo -n "端口9000: "
lsof -ti:9000 > /dev/null && echo "被占用" || echo "可用"

# 检查文件
echo -n "web_test_server.py: "
[ -f "web_test_server.py" ] && echo "存在" || echo "不存在"

# 查找可用端口
echo "查找可用端口..."
for port in 9000 9001 9999; do
    if ! lsof -ti:$port > /dev/null 2>&1; then
        echo "  可用端口: $port"
    fi
done
```

---

## 📞 获取帮助

如果以上方法都无法解决问题，请提供以下信息：

1. **错误信息**: 完整的错误日志
2. **系统信息**: 
   ```bash
   python3 --version
   uname -a
   ```
3. **端口状态**:
   ```bash
   lsof -ti:9000
   netstat -an | grep 9000
   ```
4. **启动日志**: 服务器启动时的完整输出

---

**最后更新**: 2025-01-18



