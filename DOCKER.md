# Docker 部署指南

## 简介

本应用已支持 Docker 容器化部署，可以同时监听 80 端口（HTTP）和 443 端口（HTTPS）。当 SSL 启用后，访问 80 端口会自动重定向到 443 端口的 HTTPS 服务。

## 快速开始

### 1. HTTP 模式（仅 80 端口）

如果您不需要 HTTPS，可以直接运行：

```bash
# 使用 Docker Compose
docker-compose up -d

# 或使用 Docker 命令
docker build -t python-running-helper .
docker run -d -p 80:80 --name python-running-helper python-running-helper
```

访问地址：`http://your-server-ip`

### 2. HTTPS 模式（同时监听 80 和 443 端口）

#### 准备 SSL 证书

将您的 SSL 证书文件放置在 `ssl` 目录下：
- `ssl/fullchain.pem` - SSL 证书文件
- `ssl/privkey.key` - SSL 私钥文件

#### 配置文件设置

在 `config.ini` 文件中启用 SSL（如果文件不存在，首次运行会自动创建）：

```ini
[SSL]
# 是否启用SSL（true/false）
ssl_enabled = true

# SSL证书文件路径
ssl_cert_path = ssl/fullchain.pem

# SSL私钥文件路径
ssl_key_path = ssl/privkey.key

# 是否强制HTTPS（true表示HTTP请求会被重定向到HTTPS）
https_only = true
```

#### 启动容器

```bash
# 使用 Docker Compose（推荐）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

访问地址：
- HTTP: `http://your-server-ip` （自动重定向到 HTTPS）
- HTTPS: `https://your-server-ip`

## Docker Compose 配置说明

`docker-compose.yml` 文件中的关键配置：

```yaml
services:
  python-running-helper:
    ports:
      - "80:80"    # HTTP 端口
      - "443:443"  # HTTPS 端口
    volumes:
      - ./ssl:/app/ssl:ro              # SSL 证书目录（只读）
      - ./config.ini:/app/config.ini   # 配置文件
      - ./data:/app/data               # 数据持久化
      - ./cache:/app/cache             # 缓存目录
      - ./logs:/app/logs               # 日志目录
```

## 手动构建和运行

如果您不使用 Docker Compose：

```bash
# 构建镜像
docker build -t python-running-helper .

# 运行容器（HTTP 模式）
docker run -d \
  -p 80:80 \
  -v $(pwd)/config.ini:/app/config.ini \
  -v $(pwd)/data:/app/data \
  --name python-running-helper \
  python-running-helper

# 运行容器（HTTPS 模式）
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -v $(pwd)/ssl:/app/ssl:ro \
  -v $(pwd)/config.ini:/app/config.ini \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/logs:/app/logs \
  --name python-running-helper \
  python-running-helper
```

## 获取 SSL 证书

### 使用 Let's Encrypt（免费）

```bash
# 安装 certbot
sudo apt-get update
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d your-domain.com

# 证书文件位置
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem

# 复制到项目目录
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/privkey.key
sudo chmod 644 ./ssl/*.pem ./ssl/*.key
```

### 使用自签名证书（测试用）

```bash
# 创建自签名证书
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout ssl/privkey.key \
  -out ssl/fullchain.pem \
  -days 365 \
  -subj "/CN=localhost"
```

注意：自签名证书会在浏览器中显示安全警告。

## 常见问题

### 1. 端口被占用

如果 80 或 443 端口已被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:80"    # 将容器的 80 端口映射到主机的 8080 端口
  - "8443:443"   # 将容器的 443 端口映射到主机的 8443 端口
```

### 2. SSL 证书权限问题

确保证书文件的权限正确：

```bash
chmod 644 ssl/fullchain.pem
chmod 644 ssl/privkey.key
```

### 3. 查看容器日志

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f python-running-helper
```

### 4. 重启容器

```bash
# Docker Compose
docker-compose restart

# Docker
docker restart python-running-helper
```

## 更新应用

```bash
# 停止容器
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 数据备份

重要数据存储在挂载的卷中：
- `./data/` - 应用数据
- `./cache/` - 缓存文件
- `./logs/` - 日志文件
- `./config.ini` - 配置文件

定期备份这些目录以防数据丢失。

## 安全建议

1. **不要在生产环境使用默认配置** - 修改 config.ini 中的安全相关配置
2. **使用强密码** - 为管理员账户设置强密码
3. **定期更新证书** - Let's Encrypt 证书有效期为 90 天，需要定期更新
4. **限制访问** - 使用防火墙规则限制访问来源
5. **启用日志审计** - 定期检查日志文件

## 技术支持

如有问题，请查看：
- 容器日志：`docker-compose logs -f`
- 应用日志：`./logs/` 目录
- GitHub Issues: [项目地址]

