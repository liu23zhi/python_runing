# Nginx前端部署说明

## 概述

本次更新将前端静态文件的服务从Flask迁移到Nginx，以提高稳定性和性能。Nginx将作为反向代理处理静态文件请求，并将API请求转发到后端Flask应用。

## 架构变更

### 之前的架构
```
客户端 → Flask (端口80/443) → 处理所有请求（静态文件 + API）
```

### 现在的架构
```
客户端 → Nginx (端口80/443) → 静态文件直接响应
                              ↓
                              → Flask (127.0.0.1:5000) → 处理API请求
```

## 主要变更内容

### 1. 新增文件

#### `nginx.conf`
- Nginx主配置文件
- 配置HTTP（80端口）和HTTPS（443端口）服务器
- 静态文件缓存策略
- WebSocket支持（用于SocketIO）
- API请求代理规则

### 2. 修改的文件

#### `Dockerfile`
**变更内容：**
- 添加nginx和supervisor到系统依赖安装列表
- 复制nginx.conf到容器的/etc/nginx/nginx.conf
- 创建nginx日志目录

**原代码：**
```dockerfile
# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    ...
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*
```

**修改后代码：**
```dockerfile
# 安装系统依赖（包括nginx）
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    ...
    xdg-utils \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*
```

**原代码：**
```dockerfile
# 复制应用程序文件
COPY . .

# 创建必要的目录
RUN mkdir -p /app/ssl /app/cache /app/logs
```

**修改后代码：**
```dockerfile
# 复制应用程序文件
COPY . .

# 复制nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 创建必要的目录
RUN mkdir -p /app/ssl /app/cache /app/logs /var/log/nginx
```

#### `docker-entrypoint.sh`
完全重写了启动脚本，使用supervisor管理进程。

**原架构：**
- HTTP模式：直接运行Flask on 0.0.0.0:80
- HTTPS模式：后台运行HTTP重定向服务 + 前台运行Flask on 0.0.0.0:443

**新架构：**
- 使用supervisor同时管理nginx和Flask后端
- Nginx监听80和443端口（对外）
- Flask监听127.0.0.1:5000（仅内部访问）
- SSL启用时，nginx自动处理HTTP到HTTPS的重定向

**主要变更：**
1. 创建supervisor配置文件，管理两个进程：
   - nginx（优先级1）
   - flask-backend（优先级10）

2. 根据SSL配置动态生成nginx配置：
   - SSL启用：HTTP重定向到HTTPS，HTTPS服务所有内容
   - SSL未启用：HTTP服务所有内容

3. 使用supervisor作为主进程（exec /usr/bin/supervisord）

## Nginx配置详解

### 静态文件处理
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
    expires 7d;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```
- 静态资源缓存7天
- 关闭访问日志以提高性能

### WebSocket支持
```nginx
location /socket.io/ {
    proxy_pass http://127.0.0.1:5000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}
```
- 支持SocketIO实时通信
- 保持长连接（proxy_read_timeout 86400）

### API代理
```nginx
location ~ ^/(api|auth|logs|cdn-cache|avatar|system-announcement)/ {
    proxy_pass http://127.0.0.1:5000;
    ...
}
```
- 所有API请求转发到Flask后端
- 超时设置300秒

### 路由优先级
1. 静态文件（图片、CSS、JS等）：直接由nginx响应
2. API路径：代理到Flask
3. UUID会话路径：代理到Flask
4. 其他路径：先尝试静态文件，不存在则代理到Flask

## 端口说明

**保持不变：**
- 容器外部端口：80（HTTP）和443（HTTPS）
- docker-compose.yml中的端口映射保持不变（8080→80, 8443→443）

**内部变更：**
- Nginx：监听80和443（对外）
- Flask：监听127.0.0.1:5000（仅内部，不对外暴露）

## 优势

1. **稳定性提升**
   - Nginx是成熟的Web服务器，处理静态文件更稳定
   - 进程隔离：nginx和Flask分别管理，互不影响

2. **性能优化**
   - 静态文件由nginx直接服务，无需Python处理
   - 启用gzip压缩
   - 静态资源缓存

3. **更好的并发处理**
   - Nginx的异步I/O模型处理大量并发连接更高效
   - Flask专注于API业务逻辑

4. **易于维护**
   - supervisor统一管理进程
   - 更容易监控和重启单个服务

## 部署步骤

### 使用Docker Compose部署（推荐）

```bash
# 1. 停止现有容器
docker-compose down

# 2. 重新构建镜像
docker-compose build

# 3. 启动容器
docker-compose up -d

# 4. 查看日志
docker-compose logs -f
```

### 验证部署

```bash
# 检查nginx状态
docker exec python-running-helper supervisorctl status nginx

# 检查Flask后端状态
docker exec python-running-helper supervisorctl status flask-backend

# 查看nginx日志
docker exec python-running-helper tail -f /var/log/nginx/access.log

# 查看Flask日志
docker exec python-running-helper tail -f /var/log/supervisor/flask-stdout.log
```

## 故障排查

### Nginx配置测试
```bash
docker exec python-running-helper nginx -t
```

### 重启服务
```bash
# 重启nginx
docker exec python-running-helper supervisorctl restart nginx

# 重启Flask后端
docker exec python-running-helper supervisorctl restart flask-backend

# 重启所有服务
docker exec python-running-helper supervisorctl restart all
```

### 查看进程状态
```bash
docker exec python-running-helper supervisorctl status
```

## 回滚说明

如果需要回滚到之前的版本：

```bash
# 1. 切换到之前的commit
git checkout <previous-commit-hash>

# 2. 重新构建和部署
docker-compose down
docker-compose build
docker-compose up -d
```

## 注意事项

1. **首次部署**：需要重新构建Docker镜像
2. **SSL证书**：确保证书文件放在`./ssl/`目录下
3. **配置文件**：config.ini的ssl_enabled配置会影响nginx的行为
4. **端口占用**：确保宿主机的8080和8443端口未被占用

## 技术支持

如有问题，请检查以下日志：
- Nginx访问日志：`/var/log/nginx/access.log`
- Nginx错误日志：`/var/log/nginx/error.log`
- Flask日志：`/var/log/supervisor/flask-stdout.log`
- Supervisor日志：`/var/log/supervisor/supervisord.log`
