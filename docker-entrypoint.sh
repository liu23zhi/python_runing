#!/bin/bash
# Docker启动脚本 - 处理HTTP和HTTPS端口监听

set -e

# 打印启动信息
echo "================================================="
echo "  跑步助手 Docker 容器启动"
echo "================================================="

# 检查config.ini是否存在，如果不存在则创建
if [ ! -f "/app/config.ini" ]; then
    echo "配置文件不存在，将在首次运行时自动创建"
fi

# 从 /app/config.ini 读取 ssl_enabled 的值
ssl_enabled=$(sed -n 's/^[[:space:]]*ssl_enabled[[:space:]]*=[[:space:]]*\(.*\)/\1/p' /app/config.ini | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')

# 检查SSL证书
if [ -f "/app/ssl/fullchain.pem" ] && [ -f "/app/ssl/privkey.key" ] && [ "$ssl_enabled" = "true" ]; then
    echo "检测到SSL证书文件"
    echo "将在HTTPS模式（443端口）运行"
    echo "HTTP请求（80端口）将自动重定向到HTTPS"
    
    # 使用supervisord或类似工具运行双进程，或使用nginx反向代理
    # 这里我们使用简单的后台进程方式
    
    # 启动HTTP重定向服务（80端口）
    echo "启动HTTP重定向服务（80端口）..."
    python3 - <<'EOF' &
from flask import Flask, redirect, request
import sys
app = Flask(__name__)

# 允许的主机名（防止Host头注入攻击）
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_to_https(path):
    # 获取主机名（不含端口）
    host = request.host.split(':')[0]
    
    # 构建HTTPS URL（使用原始主机名，但使用443端口）
    # 注意：这里不再需要使用 \": 转义，直接使用 : 即可，因为 Heredoc 保护了内容
    https_url = f'https://{request.host.split(":")[0]}:443{request.full_path.rstrip("?")}'
    
    return redirect(https_url, code=301)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    except KeyboardInterrupt:
        sys.exit(0)
EOF
    HTTP_PID=$!
    echo "HTTP重定向服务已启动 (PID: $HTTP_PID)"
    
    # 等待HTTP服务启动
    sleep 2
    
    # 启动主HTTPS服务（443端口）
    echo "启动主HTTPS服务（443端口）..."
    python3 /app/main.py --host 0.0.0.0 --port 443
    
    # 如果主服务退出，优雅地清理HTTP重定向服务
    echo "主服务已退出，正在清理HTTP重定向服务..."
    kill -TERM $HTTP_PID 2>/dev/null && wait $HTTP_PID 2>/dev/null || true
else
    echo "未检测到SSL证书文件"
    echo "将在HTTP模式（80端口）运行"
    echo "如需启用HTTPS，请将证书文件放置在 ./ssl/ 目录下："
    echo "  - ./ssl/fullchain.pem (证书文件)"
    echo "  - ./ssl/privkey.key (私钥文件)"
    echo "并在config.ini中设置 ssl_enabled=true"
    
    # 仅启动HTTP服务
    exec python3 /app/main.py --host 0.0.0.0 --port 80
fi
