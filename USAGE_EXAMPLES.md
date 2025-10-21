# 使用示例

## 快速开始

### 1. Web模式（推荐用于服务器部署）

```bash
# 基本启动
python main.py --web

# 指定端口和地址
python main.py --web --host 0.0.0.0 --port 8080
```

然后在浏览器访问：
- 首次访问: `http://localhost:5000/`
- 自动跳转到: `http://localhost:5000/uuid=<your-unique-id>`
- 下次直接访问带UUID的链接即可恢复会话

### 2. 桌面模式（原有功能）

```bash
# 正常启动
python main.py

# 自动登录
python main.py --autologin 学号 密码
```

## 使用场景

### 场景1: 个人本地使用

**推荐：桌面模式**

优点：
- 独立窗口，不占用浏览器
- 无需配置网络
- 启动即用

```bash
python main.py
```

### 场景2: 服务器部署，多人使用

**推荐：Web模式**

优点：
- 支持多用户并发
- 浏览器访问，无需安装客户端
- 会话持久化

```bash
# 生产环境建议使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:start_web_server
```

### 场景3: 远程访问

**推荐：Web模式 + SSH隧道**

```bash
# 服务器端
python main.py --web --host 127.0.0.1 --port 5000

# 客户端（本地）
ssh -L 5000:localhost:5000 user@server

# 然后在本地浏览器访问 http://localhost:5000
```

## 高级用法

### 1. 配置反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 2. 使用Systemd守护进程（Linux）

创建 `/etc/systemd/system/running-helper.service`:

```ini
[Unit]
Description=Running Helper Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/python_runing
ExecStart=/usr/bin/python3 main.py --web --host 127.0.0.1 --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable running-helper
sudo systemctl start running-helper
```

### 3. Docker部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir Flask flask-cors requests openpyxl xlrd xlwt chardet

EXPOSE 5000

CMD ["python", "main.py", "--web", "--host", "0.0.0.0", "--port", "5000"]
```

构建和运行：
```bash
docker build -t running-helper .
docker run -d -p 5000:5000 running-helper
```

## 常见问题

### Q: Web模式下会话会丢失吗？

A: 会话存储在服务器内存中。重启服务器会清空所有会话。建议：
- 保存重要的UUID链接
- 生产环境可实现持久化存储（Redis/数据库）

### Q: 可以同时运行两种模式吗？

A: 可以，使用不同端口：
```bash
# 终端1: Web模式
python main.py --web --port 5000

# 终端2: 桌面模式（需要额外安装pywebview）
python main.py
```

### Q: Web模式安全吗？

A: 默认配置绑定127.0.0.1，仅本机可访问。如需公网访问：
1. 配置防火墙规则
2. 使用HTTPS（反向代理）
3. 添加身份验证
4. 定期更新依赖

### Q: 如何查看日志？

```bash
# Web模式
python main.py --web 2>&1 | tee server.log

# 桌面模式
# 查看控制台输出
```

## 性能建议

### Web模式优化

1. **使用生产WSGI服务器**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

2. **配置进程数**
   - CPU密集型任务：进程数 = CPU核心数
   - IO密集型任务：进程数 = CPU核心数 × 2

3. **内存管理**
   - 定期重启服务释放内存
   - 监控会话数量
   - 实现会话过期清理

### 桌面模式优化

1. **减少资源占用**
   - 关闭不需要的功能
   - 定期清理缓存

2. **提升响应速度**
   - 预加载地图资源
   - 使用本地缓存

## 故障排查

### 问题：端口被占用

```bash
# 查找占用端口的进程
lsof -i :5000

# 或使用其他端口
python main.py --web --port 5001
```

### 问题：无法访问Web界面

1. 检查防火墙设置
2. 确认服务器正在运行
3. 检查host配置是否正确

### 问题：会话无法保持

1. 检查浏览器Cookie设置
2. 确认使用相同的UUID链接
3. 检查会话是否过期（默认7天）

## 更多帮助

查看完整文档：
- [README_WEB_MODE.md](README_WEB_MODE.md) - Web模式详细说明
- [main.py](main.py) - 源代码注释
