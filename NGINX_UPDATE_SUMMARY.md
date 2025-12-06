# Nginx前端架构更新说明

## 更新概述

本次更新将应用的前端静态文件服务从Flask迁移到Nginx，以提高系统的稳定性和性能。端口保持不变（80和443）。

## 核心变更

### 1. 新增Nginx作为前端服务器
- Nginx处理所有静态文件（HTML、CSS、JS、图片等）
- Nginx作为反向代理，将API请求转发到Flask后端
- Flask专注于业务逻辑处理，监听127.0.0.1:5000（仅内部访问）

### 2. 使用Supervisor管理进程
- 统一管理Nginx和Flask两个进程
- 自动重启失败的进程
- 提供进程监控和日志管理

## 文件变更对比

### Dockerfile

**添加的依赖：**
```dockerfile
nginx \
supervisor \
```

**添加的步骤：**
```dockerfile
# 复制nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 创建nginx日志目录
RUN mkdir -p /var/log/nginx
```

### docker-entrypoint.sh

**原逻辑：**
- HTTP模式：Flask直接监听0.0.0.0:80
- HTTPS模式：后台运行HTTP重定向服务 + Flask监听0.0.0.0:443

**新逻辑：**
- 使用Supervisor管理Nginx和Flask
- Nginx监听80和443端口
- Flask监听127.0.0.1:5000
- SSL启用时，动态生成包含HTTP→HTTPS重定向的Nginx配置

### nginx.conf

新增文件，包含：
- HTTP服务器配置（端口80）
- HTTPS服务器配置（端口443）
- 静态文件缓存策略
- WebSocket支持（SocketIO）
- API代理规则

## 架构对比

### 之前：
```
客户端 ──(80/443)──> Flask ──> 所有请求处理
```

### 现在：
```
客户端 ──(80/443)──> Nginx ──> 静态文件（直接响应）
                           └──> API请求 ──(5000)──> Flask
```

## 优势

1. **稳定性**：Nginx是成熟的Web服务器，专为静态文件服务优化
2. **性能**：静态文件由Nginx直接服务，减少Python开销
3. **并发**：Nginx的异步I/O模型处理大量并发更高效
4. **缓存**：静态资源启用7天缓存，减少重复请求
5. **压缩**：启用gzip压缩，减少传输数据量
6. **监控**：Supervisor提供进程管理和监控

## 端口保持不变

- 外部访问端口：80（HTTP）、443（HTTPS）
- docker-compose端口映射：8080→80, 8443→443
- 用户体验完全一致

## 部署方法

```bash
# 重新构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 验证部署

```bash
# 检查服务状态
docker exec python-running-helper supervisorctl status

# 预期输出：
# flask-backend    RUNNING   pid xxx, uptime x:xx:xx
# nginx            RUNNING   pid xxx, uptime x:xx:xx
```

## 详细文档

完整的部署说明和故障排查指南，请参阅 [NGINX_DEPLOYMENT.md](NGINX_DEPLOYMENT.md)

## 兼容性

- ✅ 完全向后兼容
- ✅ 所有现有功能保持不变
- ✅ API端点不变
- ✅ WebSocket连接正常工作
- ✅ SSL/TLS配置兼容
