#!/bin/bash
# Docker启动脚本 - 使用nginx作为前端服务器，supervisor管理进程

set -e

# 打印启动信息
echo "================================================="
echo "  跑步助手 Docker 容器启动 (Nginx前端模式)"
echo "================================================="

# 检查config.ini是否存在，如果不存在则创建
if [ ! -f "/app/config.ini" ]; then
    echo "配置文件不存在，将在首次运行时自动创建"
fi

# 从 /app/config.ini 读取 ssl_enabled 的值
ssl_enabled=$(sed -n 's/^[[:space:]]*ssl_enabled[[:space:]]*=[[:space:]]*\(.*\)/\1/p' /app/config.ini | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')

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

# 检查SSL证书
if [ -f "/app/ssl/fullchain.pem" ] && [ -f "/app/ssl/privkey.key" ] && [ "$ssl_enabled" = "true" ]; then
    echo "检测到SSL证书文件"
    echo "将同时启用HTTP（80端口）和HTTPS（443端口）"
    echo "Nginx将处理HTTP到HTTPS的重定向"
    
    # 修改nginx配置，添加HTTP到HTTPS的重定向
    cat > /etc/nginx/nginx.conf <<'NGINX_EOF'
user  www-data;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    types_hash_max_size 2048;

    gzip  on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

    # HTTP服务器 - 重定向到HTTPS
    server {
        listen 80;
        server_name _;

        # 重定向所有HTTP请求到HTTPS
        return 301 https://$host$request_uri;
    }

    # HTTPS服务器 - 端口443
    server {
        listen 443 ssl http2;
        server_name _;

        # SSL证书配置
        ssl_certificate /app/ssl/fullchain.pem;
        ssl_certificate_key /app/ssl/privkey.key;

        # SSL安全配置
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # 静态文件根目录
        root /app;

        # 默认首页
        index index.html;

        # 客户端最大上传大小
        client_max_body_size 100M;

        # 静态文件缓存设置
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
            expires 7d;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # WebSocket支持 - SocketIO
        location /socket.io/ {
            proxy_pass http://127.0.0.1:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_read_timeout 86400;
        }

        # API请求代理到Flask后端
        location ~ ^/(api|auth|logs|cdn-cache|avatar|system-announcement)/ {
            proxy_pass http://127.0.0.1:5000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_read_timeout 300;
            proxy_connect_timeout 300;
            proxy_send_timeout 300;
        }

        # UUID会话路径 - 代理到Flask
        location ~ ^/uuid= {
            proxy_pass http://127.0.0.1:5000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 首页 - 优先尝试静态文件，如果不存在则代理到Flask
        location = / {
            try_files /index.html @backend;
        }

        # 其他请求 - 先尝试静态文件，不存在则代理到Flask
        location / {
            try_files $uri $uri/ @backend;
        }

        # 后端代理fallback
        location @backend {
            proxy_pass http://127.0.0.1:5000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
NGINX_EOF
    
    echo "已配置HTTPS模式的nginx"
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
