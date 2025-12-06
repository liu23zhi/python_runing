# Docker 部署说明

本文档提供详细的中文部署指南，帮助您使用 Docker 快速部署跑步助手应用。

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [SSL/HTTPS配置](#sslhttps配置)
- [常见问题](#常见问题)
- [维护与更新](#维护与更新)

## 🖥️ 系统要求

- Docker Engine 20.10 或更高版本
- Docker Compose 1.29 或更高版本（可选，推荐使用）
- 至少 2GB 可用磁盘空间
- 至少 1GB 可用内存

## 🚀 快速开始

### 方式一：使用 Docker Compose（推荐）

这是最简单的部署方式，只需三步：

```bash
# 1. 克隆或下载项目
git clone https://github.com/liu23zhi/python_runing.git
cd python_runing

# 2. 启动容器
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

启动成功后，在浏览器中访问：`http://服务器IP` 或 `http://localhost`

### 方式二：使用 Docker 命令

```bash
# 1. 构建镜像
docker build -t python-running-helper .

# 2. 运行容器
docker run -d \
  --name python-running-helper \
  -p 80:80 \
  -v $(pwd)/config.ini:/app/config.ini \
  -v $(pwd)/data:/app/data \
  python-running-helper

# 3. 查看日志
docker logs -f python-running-helper
```

## ⚙️ 配置说明

### 基本配置

首次运行时，应用会自动创建 `config.ini` 配置文件。您可以停止容器后修改配置：

```bash
# 停止容器
docker-compose down

# 编辑配置文件
nano config.ini

# 重新启动
docker-compose up -d
```

### 端口配置

默认配置同时监听两个端口：
- **80 端口**：HTTP 服务
- **443 端口**：HTTPS 服务（需要SSL证书）

如果这些端口已被占用，可以修改 `docker-compose.yml`：

```yaml
ports:
  - "8080:80"    # 将容器80端口映射到主机8080端口
  - "8443:443"   # 将容器443端口映射到主机8443端口
```

### 数据持久化

以下目录会被挂载到宿主机，确保数据持久化：

- `./data/` - 应用数据和会话信息
- `./cache/` - 缓存文件
- `./logs/` - 运行日志
- `./config.ini` - 配置文件
- `./ssl/` - SSL证书（如果使用HTTPS）

## 🔒 SSL/HTTPS配置

### 第一步：准备SSL证书

您可以通过以下方式获取SSL证书：

#### 选项A：使用 Let's Encrypt 免费证书（推荐）

```bash
# 安装 certbot
sudo apt-get update
sudo apt-get install certbot

# 获取证书（需要停止正在运行的Web服务）
sudo certbot certonly --standalone -d yourdomain.com

# 证书文件位置
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# 复制证书到项目目录
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/privkey.key
sudo chmod 644 ./ssl/*
```

#### 选项B：使用自签名证书（仅测试用）

```bash
# 创建SSL目录
mkdir -p ssl

# 生成自签名证书
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout ssl/privkey.key \
  -out ssl/fullchain.pem \
  -days 365 \
  -subj "/CN=localhost"
```

⚠️ **注意**：自签名证书会在浏览器中显示安全警告。

### 第二步：配置文件设置

编辑 `config.ini` 文件，启用SSL：

```ini
[SSL]
# 启用SSL/HTTPS
ssl_enabled = true

# SSL证书文件路径（相对于应用根目录）
ssl_cert_path = ssl/fullchain.pem

# SSL私钥文件路径
ssl_key_path = ssl/privkey.key

# 强制HTTPS（HTTP请求自动重定向到HTTPS）
https_only = true
```

### 第三步：重启容器

```bash
# 使用 Docker Compose
docker-compose down
docker-compose up -d

# 或使用 Docker 命令
docker restart python-running-helper
```

### SSL配置验证

启动后检查日志：

```bash
docker-compose logs | grep SSL
```

您应该看到类似的输出：
```
✓ SSL/HTTPS 已启用
  证书文件: ssl/fullchain.pem
  密钥文件: ssl/privkey.key
```

### 访问HTTPS服务

- **HTTPS访问**：`https://yourdomain.com` 或 `https://服务器IP`
- **HTTP访问**：`http://yourdomain.com` （自动重定向到HTTPS）

## 🛠️ 常见问题

### Q1: 端口被占用怎么办？

**现象**：启动失败，提示 "address already in use"

**解决方案**：

方法1 - 停止占用端口的服务：
```bash
# 查看占用80端口的进程
sudo lsof -i :80

# 停止Apache或Nginx
sudo systemctl stop apache2
# 或
sudo systemctl stop nginx
```

方法2 - 使用其他端口：
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"
  - "8443:443"
```

### Q2: SSL证书验证失败

**现象**：容器启动后立即退出，日志显示 "SSL证书验证失败"

**解决方案**：

1. 检查证书文件是否存在：
```bash
ls -lh ssl/
```

2. 检查证书文件权限：
```bash
chmod 644 ssl/fullchain.pem
chmod 644 ssl/privkey.key
```

3. 验证证书格式：
```bash
openssl x509 -in ssl/fullchain.pem -text -noout
```

### Q3: 容器启动后无法访问

**诊断步骤**：

1. 检查容器状态：
```bash
docker ps -a
```

2. 查看详细日志：
```bash
docker-compose logs -f
```

3. 检查防火墙：
```bash
# Ubuntu/Debian
sudo ufw status
sudo ufw allow 80
sudo ufw allow 443

# CentOS/RHEL
sudo firewall-cmd --list-ports
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --add-port=443/tcp --permanent
sudo firewall-cmd --reload
```

4. 检查容器网络：
```bash
docker network inspect python_runing_app-network
```

### Q4: 数据丢失问题

**预防措施**：

1. 确保使用卷挂载保存数据：
```yaml
volumes:
  - ./data:/app/data         # 应用数据
  - ./config.ini:/app/config.ini  # 配置
```

2. 定期备份：
```bash
# 创建备份目录
mkdir -p backup/$(date +%Y%m%d)

# 备份数据
cp -r data backup/$(date +%Y%m%d)/
cp config.ini backup/$(date +%Y%m%d)/
```

### Q5: Chrome浏览器相关错误

**现象**：日志中出现 "Chrome浏览器池初始化失败"

**解决方案**：

这通常是因为容器中缺少必要的依赖。Dockerfile已包含所有需要的依赖，如果仍有问题：

```bash
# 重新构建镜像
docker-compose build --no-cache

# 或清理后重建
docker-compose down
docker system prune -a
docker-compose up -d --build
```

## 🔄 维护与更新

### 查看运行状态

```bash
# 查看容器状态
docker-compose ps

# 查看资源使用情况
docker stats python-running-helper
```

### 查看日志

```bash
# 实时查看所有日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100

# 查看应用内部日志文件
docker-compose exec python-running-helper tail -f /app/logs/app.log
```

### 更新应用

```bash
# 1. 停止容器
docker-compose down

# 2. 备份数据（重要！）
tar -czf backup_$(date +%Y%m%d).tar.gz data/ config.ini

# 3. 拉取最新代码
git pull

# 4. 重新构建并启动
docker-compose up -d --build

# 5. 查看启动日志
docker-compose logs -f
```

### 清理和重置

```bash
# 停止并删除容器
docker-compose down

# 清理所有数据（谨慎操作！）
rm -rf data/ cache/ logs/

# 重新启动
docker-compose up -d
```

### SSL证书续期（Let's Encrypt）

Let's Encrypt 证书有效期为90天，需要定期续期：

```bash
# 停止容器（certbot需要使用80端口）
docker-compose down

# 续期证书
sudo certbot renew

# 复制新证书
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/privkey.key

# 重启容器
docker-compose up -d
```

建议设置自动续期：
```bash
# 编辑crontab
sudo crontab -e

# 添加以下行（每月1号凌晨2点检查并续期）
0 2 1 * * certbot renew --quiet && docker-compose -f /path/to/docker-compose.yml restart
```

## 📊 性能优化

### 调整资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  python-running-helper:
    # ... 其他配置 ...
    deploy:
      resources:
        limits:
          cpus: '2.0'      # 最多使用2个CPU核心
          memory: 2G       # 最多使用2GB内存
        reservations:
          cpus: '0.5'      # 至少保证0.5个CPU核心
          memory: 512M     # 至少保证512MB内存
```

### 日志轮转

防止日志文件过大：

```bash
# 在宿主机上设置日志轮转
sudo nano /etc/logrotate.d/python-running-helper
```

添加以下内容：
```
/path/to/python_runing/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
```

## 🔐 安全建议

1. **修改默认端口**：不要使用标准的80/443端口，使用非标准端口可以减少自动扫描攻击
2. **使用强密码**：为管理员账户设置复杂密码
3. **启用防火墙**：只开放必要的端口
4. **定期更新**：及时更新应用和系统补丁
5. **监控日志**：定期检查访问日志，发现异常活动
6. **备份数据**：定期备份重要数据

## 📞 获取帮助

如遇到问题：

1. 查看日志：`docker-compose logs -f`
2. 检查配置文件：`cat config.ini`
3. 查看容器状态：`docker-compose ps`
4. 提交 Issue：[GitHub Issues](https://github.com/liu23zhi/python_runing/issues)

## 📝 附录：完整的docker-compose.yml示例

```yaml
version: '3.8'

services:
  python-running-helper:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: python-running-helper
    ports:
      - "80:80"      # HTTP端口
      - "443:443"    # HTTPS端口
    volumes:
      # SSL证书（只读）
      - ./ssl:/app/ssl:ro
      # 配置文件
      - ./config.ini:/app/config.ini
      # 数据持久化
      - ./data:/app/data
      - ./cache:/app/cache
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - app-network
    # 可选：资源限制
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

networks:
  app-network:
    driver: bridge
```

---

**祝您部署顺利！** 🎉
