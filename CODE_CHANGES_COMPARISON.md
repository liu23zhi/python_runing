# 代码变更对比 - Nginx前端架构更新

## 1. Dockerfile 变更

### 原代码：
```dockerfile
# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 复制应用程序文件
COPY . .

# 创建必要的目录
RUN mkdir -p /app/ssl /app/cache /app/logs
```

### 修改后代码：
```dockerfile
# 安装系统依赖（包括nginx）
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 复制应用程序文件
COPY . .

# 复制nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 创建必要的目录
RUN mkdir -p /app/ssl /app/cache /app/logs /var/log/nginx
```

**变更说明：**
- 添加`nginx`和`supervisor`到系统依赖
- 复制nginx配置文件到容器
- 创建nginx日志目录

---

## 2. docker-entrypoint.sh 变更

### 原代码（HTTP模式）：
```bash
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
```

### 修改后代码（HTTP模式）：
```bash
else
    echo "未检测到SSL证书文件或SSL未启用"
    echo "将在HTTP模式（80端口）运行"
    echo "如需启用HTTPS，请将证书文件放置在 ./ssl/ 目录下："
    echo "  - ./ssl/fullchain.pem (证书文件)"
    echo "  - ./ssl/privkey.key (私钥文件)"
    echo "并在config.ini中设置 ssl_enabled=true"
    
    # 使用HTTP模式的nginx配置（已经在/etc/nginx/nginx.conf中）
    echo "已配置HTTP模式的nginx"
fi

# 创建日志目录
mkdir -p /var/log/supervisor /var/log/nginx

# 测试nginx配置
echo "测试nginx配置..."
nginx -t

# 启动supervisor（管理nginx和flask后端）
echo "启动服务..."
echo "- Nginx将监听端口80和443（如果启用SSL）"
echo "- Flask后端将监听127.0.0.1:5000"
echo "================================================="
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/python-running.conf
```

### 原代码（HTTPS模式）：
```bash
if [ -f "/app/ssl/fullchain.pem" ] && [ -f "/app/ssl/privkey.key" ] && [ "$ssl_enabled" = "true" ]; then
    echo "检测到SSL证书文件"
    echo "将在HTTPS模式（443端口）运行"
    echo "HTTP请求（80端口）将自动重定向到HTTPS"
    
    # 启动HTTP重定向服务（80端口）
    echo "启动HTTP重定向服务（80端口）..."
    python3 - <<'EOF' &
from flask import Flask, redirect, request
import sys
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_to_https(path):
    host = request.host.split(':')[0]
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
fi
```

### 修改后代码（HTTPS模式）：
```bash
# 创建supervisor配置
cat > /etc/supervisor/conf.d/python-running.conf <<'SUPERVISOR_EOF'
[supervisord]
nodaemon=true
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/nginx-stdout.log
stderr_logfile=/var/log/supervisor/nginx-stderr.log
priority=1

[program:flask-backend]
command=python3 /app/main.py --host 127.0.0.1 --port 5000
directory=/app
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/flask-stdout.log
stderr_logfile=/var/log/supervisor/flask-stderr.log
priority=10
SUPERVISOR_EOF

if [ -f "/app/ssl/fullchain.pem" ] && [ -f "/app/ssl/privkey.key" ] && [ "$ssl_enabled" = "true" ]; then
    echo "检测到SSL证书文件"
    echo "将同时启用HTTP（80端口）和HTTPS（443端口）"
    echo "Nginx将处理HTTP到HTTPS的重定向"
    
    # 动态生成包含HTTP→HTTPS重定向的nginx配置
    cat > /etc/nginx/nginx.conf <<'NGINX_EOF'
user  www-data;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    # ... 省略中间配置 ...
    
    # HTTP服务器 - 重定向到HTTPS
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }
    
    # HTTPS服务器 - 端口443
    server {
        listen 443 ssl http2;
        server_name _;
        # ... SSL配置和代理规则 ...
    }
}
NGINX_EOF
fi
```

**变更说明：**
- 移除手动进程管理（后台Flask进程）
- 使用supervisor统一管理nginx和Flask
- Flask从监听0.0.0.0改为127.0.0.1（仅内部访问）
- Nginx处理所有外部请求

---

## 3. 新增文件

### nginx.conf
新增的nginx配置文件，包含：

1. **HTTP服务器（端口80）配置**
   - 静态文件缓存：7天缓存期
   - WebSocket代理：支持SocketIO
   - API代理：转发到127.0.0.1:5000
   - UUID会话代理
   - fallback到Flask后端

2. **HTTPS服务器（端口443）配置**
   - SSL/TLS配置
   - 与HTTP服务器相同的代理规则

**关键配置：**
```nginx
# 静态文件缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
    expires 7d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# WebSocket支持
location /socket.io/ {
    proxy_pass http://127.0.0.1:5000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}

# API代理
location ~ ^/(api|auth|logs|cdn-cache|avatar|system-announcement)/ {
    proxy_pass http://127.0.0.1:5000;
    ...
}
```

---

## 变更总结

### 端口保持不变
- ✅ HTTP端口：80
- ✅ HTTPS端口：443
- ✅ docker-compose端口映射：8080→80, 8443→443

### 架构变更
**之前：**
- Flask直接监听80/443端口
- Flask处理所有请求（静态+动态）

**现在：**
- Nginx监听80/443端口（对外）
- Flask监听127.0.0.1:5000（仅内部）
- Nginx处理静态文件，代理API到Flask

### 优势
1. 稳定性提升：Nginx专业处理Web请求
2. 性能优化：静态文件缓存和gzip压缩
3. 并发能力：Nginx异步I/O模型
4. 进程管理：Supervisor统一管理
5. 向后兼容：所有现有功能保持不变

### 部署影响
- 需要重新构建Docker镜像
- 首次启动时会下载nginx和supervisor包
- 无需修改任何配置文件（除非自定义）
