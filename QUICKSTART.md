# 快速开始指南 (5分钟部署)

本指南帮助您在5分钟内完成Docker部署。

## 前提条件

- 已安装Docker和Docker Compose
- 有root或sudo权限（Linux）

## 🚀 三步部署

### 第一步：克隆项目

```bash
git clone https://github.com/liu23zhi/python_runing.git
cd python_runing
```

### 第二步：启动容器

```bash
docker-compose up -d
```

等待镜像构建和容器启动（首次运行需要几分钟）。

### 第三步：访问应用

在浏览器中打开：`http://服务器IP` 或 `http://localhost`

🎉 完成！

## 📋 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down

# 重启容器
docker-compose restart

# 查看容器状态
docker-compose ps
```

## 🔒 启用HTTPS（可选）

### 1. 准备证书

选择以下方式之一：

**方式A：使用Let's Encrypt（推荐）**
```bash
# 安装certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d yourdomain.com

# 复制证书
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/privkey.key
sudo chmod 644 ./ssl/*
```

**方式B：自签名证书（测试用）**
```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout ssl/privkey.key \
  -out ssl/fullchain.pem \
  -days 365 \
  -subj "/CN=localhost"
```

### 2. 配置SSL

编辑 `config.ini`：
```ini
[SSL]
ssl_enabled = true
ssl_cert_path = ssl/fullchain.pem
ssl_key_path = ssl/privkey.key
https_only = true
```

### 3. 重启容器

```bash
docker-compose restart
```

现在可以访问：
- HTTPS: `https://服务器IP`
- HTTP: `http://服务器IP` (自动跳转到HTTPS)

## 🔧 自定义端口

如果80/443端口被占用，编辑 `docker-compose.yml`：

```yaml
ports:
  - "8080:80"    # 使用8080端口
  - "8443:443"   # 使用8443端口
```

然后重启：
```bash
docker-compose down
docker-compose up -d
```

## ❓ 遇到问题？

运行测试脚本：
```bash
chmod +x docker-test.sh
./docker-test.sh
```

查看完整文档：
- [Docker部署详细指南](DOCKER_CN.md)
- [主README](README.md)

## 📊 检查运行状态

```bash
# 查看容器状态
docker-compose ps

# 查看资源使用
docker stats python-running-helper

# 查看最近日志
docker-compose logs --tail=100
```

## 🔄 更新应用

```bash
# 停止容器
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 🛑 卸载

```bash
# 停止并删除容器
docker-compose down

# 删除镜像（可选）
docker rmi python-running-helper

# 删除数据（谨慎！）
rm -rf data/ cache/ logs/
```

---

需要更多帮助？查看 [完整文档](DOCKER_CN.md)
