#!/bin/bash
# 生成自签名 SSL 证书（用于 HTTPS）

set -e

CERT_DIR="ssl_certs"
mkdir -p "$CERT_DIR"

echo "生成 SSL 证书..."
echo "目录: $CERT_DIR"

# 获取本机 IP（支持公司和家庭地址）
IP_ADDR=$(ipconfig getifaddr en0 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")

echo "检测到的 IP: $IP_ADDR"

# 生成证书（包含多个 IP 和 localhost）
openssl req -x509 -newkey rsa:4096 -keyout "$CERT_DIR/key.pem" \
  -out "$CERT_DIR/cert.pem" -days 365 -nodes \
  -subj "/C=CN/ST=State/L=City/O=Luna/CN=$IP_ADDR" \
  -addext "subjectAltName=IP:$IP_ADDR,IP:10.183.232.224,IP:192.168.3.57,IP:127.0.0.1,DNS:localhost,DNS:*.local"

echo ""
echo "✅ SSL 证书已生成："
echo "   密钥: $CERT_DIR/key.pem"
echo "   证书: $CERT_DIR/cert.pem"
echo ""
echo "📱 iPhone 访问时，需要："
echo "   1. 首次访问会提示证书不受信任"
echo "   2. 点击「显示详细信息」"
echo "   3. 点击「访问此网站」"
echo "   4. 之后就可以正常使用摄像头了"
