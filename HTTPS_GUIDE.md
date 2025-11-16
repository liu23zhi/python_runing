# HTTPS/SSL 功能使用指南

本文档介绍如何为跑步助手应用启用和配置HTTPS支持。

## 功能概述

新增的HTTPS/SSL功能提供以下特性：

1. **SSL/TLS加密**：保护客户端与服务器之间的通信安全
2. **证书管理**：通过Web管理界面上传和管理SSL证书
3. **仅HTTPS模式**：自动将HTTP请求重定向到HTTPS
4. **Nginx兼容**：正确处理反向代理转发的请求
5. **安全增强**：自动添加HSTS等安全响应头

## 快速开始

### 1. 准备SSL证书

您需要准备两个文件：

- **证书文件**（.pem或.crt格式）：包含服务器公钥和证书链
- **私钥文件**（.key或.pem格式）：证书对应的私钥

#### 获取SSL证书的方式：

**方式1：使用Let's Encrypt（免费）**
```bash
# 安装certbot
sudo apt-get install certbot

# 获取证书（需要域名和80端口）
sudo certbot certonly --standalone -d yourdomain.com

# 证书位置：
# 证书：/etc/letsencrypt/live/yourdomain.com/fullchain.pem
# 私钥：/etc/letsencrypt/live/yourdomain.com/privkey.pem
```

**方式2：使用自签名证书（仅测试用）**
```bash
# 生成自签名证书（有效期365天）
openssl req -x509 -newkey rsa:4096 -keyout privkey.key -out fullchain.pem -days 365 -nodes
```

**方式3：购买商业证书**
从SSL证书提供商（如DigiCert、GeoTrust等）购买证书。

### 2. 配置SSL

#### 方式A：通过配置文件（推荐）

1. 复制示例配置文件：
```bash
cp config.ini.example config.ini
```

2. 编辑`config.ini`文件：
```ini
[SSL]
# 启用SSL/HTTPS
ssl_enabled = true

# 证书文件路径（相对或绝对路径）
ssl_cert_path = ssl/fullchain.pem

# 私钥文件路径
ssl_key_path = ssl/privkey.key

# 是否仅允许HTTPS访问（HTTP自动重定向）
https_only = false
```

3. 将证书文件复制到ssl目录：
```bash
cp /path/to/your/fullchain.pem ssl/
cp /path/to/your/privkey.key ssl/
chmod 644 ssl/fullchain.pem
chmod 600 ssl/privkey.key  # 私钥文件应设置严格权限
```

4. 重启服务器：
```bash
python main.py
```

#### 方式B：通过Web管理界面

1. 以管理员身份登录应用

2. 打开管理面板，切换到"HTTPS设置"标签

3. 上传证书文件：
   - 点击"证书文件"选择您的.pem或.crt文件
   - 点击"私钥文件"选择您的.key文件
   - 点击"上传证书"按钮

4. 配置选项：
   - 勾选"启用 HTTPS"开关
   - 如需强制HTTPS，勾选"仅 HTTPS 模式"
   - 点击"保存配置"

5. 重启服务器使配置生效

### 3. 验证HTTPS是否正常工作

1. 使用HTTPS访问应用：
```
https://your-domain.com:port
```

2. 检查浏览器地址栏是否显示锁图标

3. 检查证书信息（点击锁图标 → 证书）

## 高级配置

### 使用Nginx反向代理

如果使用Nginx作为反向代理，推荐在Nginx层面配置SSL：

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL证书配置
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.key;
    
    # SSL安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # 代理到Flask应用
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# HTTP自动重定向到HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

在这种配置下，应用本身不需要启用SSL（`ssl_enabled = false`），Nginx会处理SSL连接。应用会通过`X-Forwarded-Proto`头正确识别HTTPS请求。

### 证书自动续期

如果使用Let's Encrypt，设置自动续期：

```bash
# 添加cron任务（每天检查一次）
sudo crontab -e

# 添加以下行
0 0 * * * certbot renew --quiet && systemctl restart your-app-service
```

### 安全最佳实践

1. **使用强密码和密钥**：确保私钥文件权限为600
2. **及时更新证书**：证书过期前续期
3. **启用HSTS**：强制浏览器使用HTTPS（已自动启用）
4. **定期安全审计**：检查SSL配置和证书有效性
5. **备份证书**：定期备份证书和私钥文件

## 故障排查

### 问题1：证书验证失败

**症状**：启动时提示"证书验证失败"

**解决方法**：
1. 检查证书文件格式是否为PEM格式
2. 确认证书和私钥是否匹配
3. 检查文件权限（证书644，私钥600）
4. 验证证书是否过期

### 问题2：浏览器显示不安全

**症状**：HTTPS已启用但浏览器显示连接不安全

**原因**：
- 使用自签名证书
- 证书域名与访问域名不匹配
- 证书链不完整

**解决方法**：
- 使用受信任CA签发的证书
- 确保证书包含正确的域名
- 使用完整的证书链（fullchain.pem）

### 问题3：端口被占用

**症状**：启动时提示端口已被占用

**解决方法**：
```bash
# 查找占用端口的进程
sudo netstat -tulpn | grep :443
# 或使用其他端口
python main.py --port 8443
```

### 问题4：WebSocket连接失败

**症状**：启用HTTPS后WebSocket无法连接

**解决方法**：
- 确保客户端使用`wss://`而不是`ws://`
- 检查防火墙规则
- 如使用Nginx，确保正确配置WebSocket代理

## API端点说明

管理员可通过以下API端点管理SSL配置：

### GET /api/admin/ssl/info
获取当前SSL配置和证书信息

**响应示例**：
```json
{
  "success": true,
  "config": {
    "ssl_enabled": true,
    "https_only": false,
    "cert_path": "ssl/fullchain.pem",
    "key_path": "ssl/privkey.key"
  },
  "cert_info": {
    "subject": "CN=example.com",
    "issuer": "CN=Let's Encrypt Authority",
    "not_before": "2024-01-01T00:00:00",
    "not_after": "2024-04-01T00:00:00",
    "is_expired": false
  }
}
```

### POST /api/admin/ssl/upload
上传SSL证书文件

**请求**：multipart/form-data
- `cert_file`: 证书文件
- `key_file`: 私钥文件

### POST /api/admin/ssl/config
更新SSL配置

**请求体**：
```json
{
  "ssl_enabled": true,
  "https_only": false
}
```

### POST /api/admin/ssl/toggle
快速启用/禁用SSL

**请求体**：
```json
{
  "enabled": true
}
```

## 安全注意事项

1. **私钥保密**：私钥文件应严格保密，不要提交到版本控制系统
2. **文件权限**：确保私钥文件权限为600（仅所有者可读写）
3. **证书有效期**：定期检查证书有效期，提前续期
4. **配置文件**：`config.ini`已加入.gitignore，避免泄露配置信息
5. **仅HTTPS模式**：启用前确保证书配置正确，避免锁死访问

## 更多信息

- SSL/TLS协议：https://en.wikipedia.org/wiki/Transport_Layer_Security
- Let's Encrypt：https://letsencrypt.org/
- OWASP SSL/TLS指南：https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html
