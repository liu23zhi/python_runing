# 快速开始指南

## 5分钟快速上手

### 步骤1: 安装依赖

```bash
# 安装基础依赖
pip install flask

# 可选：安装Chrome支持（推荐）
pip install selenium
```

### 步骤2: 启动服务器

```bash
# 方式1: 使用默认配置（推荐新手）
python main.py --mode web

# 方式2: 使用Chrome引擎（推荐生产环境）
python main.py --mode web --use-chrome
```

### 步骤3: 访问应用

打开浏览器，访问:
```
http://127.0.0.1:5000
```

你会看到URL自动变成类似这样:
```
http://127.0.0.1:5000/uuid=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**保存这个URL**，下次访问时可以恢复你的会话！

## 常见使用场景

### 场景1: 本地个人使用

```bash
python main.py --mode web
```

访问 http://127.0.0.1:5000

### 场景2: 局域网团队使用

```bash
python main.py --mode web --web-host 0.0.0.0 --web-port 8080
```

团队成员访问 http://你的电脑IP:8080

### 场景3: 服务器部署

```bash
# 使用Chrome引擎，更稳定
python main.py --mode web --use-chrome --web-host 127.0.0.1 --web-port 5000
```

配合Nginx反向代理使用。

## 第一次使用？

### 什么是UUID会话？

- 每个用户获得一个**唯一的32位ID**
- 这个ID对应一个**独立的数据空间**
- **关闭浏览器**后，再次访问相同的UUID URL，可以**恢复之前的状态**

### 为什么需要UUID？

1. **防止卡顿**: 多人使用时，一个人的浏览器卡了不影响其他人
2. **可以恢复**: 关闭浏览器不会丢失数据
3. **多人协作**: 每个人有自己的独立空间

### 如何保存我的会话？

1. 启动服务器
2. 访问根地址（如 http://localhost:5000）
3. 注意看地址栏，URL会变成 http://localhost:5000/uuid=...
4. **把这个完整的URL保存到书签**
5. 下次直接访问这个书签，就能恢复会话

## 命令行参数说明

```bash
python main.py [选项]

选项:
  --mode {app,web}      运行模式
                        app: 桌面应用（默认）
                        web: Web模式
  
  --web-host HOST       监听地址（默认: 127.0.0.1）
                        127.0.0.1: 仅本地访问
                        0.0.0.0: 允许外部访问
  
  --web-port PORT       端口号（默认: 5000）
  
  --use-chrome          使用Chrome作为JS引擎
                        需要安装selenium和chromedriver
  
  --autologin USER PASS 自动登录（仅app模式）
```

## 示例命令

```bash
# 1. 默认Web模式（本地，端口5000）
python main.py --mode web

# 2. 自定义端口
python main.py --mode web --web-port 8080

# 3. 允许外部访问
python main.py --mode web --web-host 0.0.0.0

# 4. 使用Chrome引擎
python main.py --mode web --use-chrome

# 5. 完整配置
python main.py --mode web --web-host 0.0.0.0 --web-port 8080 --use-chrome
```

## 检查安装

### 检查Flask是否安装
```bash
python -c "import flask; print('Flask已安装:', flask.__version__)"
```

### 检查Selenium是否安装（如果使用Chrome）
```bash
python -c "import selenium; print('Selenium已安装:', selenium.__version__)"
```

### 检查ChromeDriver（如果使用Chrome）
```bash
chromedriver --version
```

## 故障排除

### Q: 启动报错 "No module named 'flask'"
A: 
```bash
pip install flask
```

### Q: 使用 --use-chrome 报错
A: 
```bash
# 安装selenium
pip install selenium

# 下载并安装ChromeDriver
# 访问 https://chromedriver.chromium.org/
# 下载与你的Chrome版本匹配的驱动
```

### Q: 端口已被占用
A: 
```bash
# 使用其他端口
python main.py --mode web --web-port 8080
```

### Q: 无法从其他电脑访问
A: 
```bash
# 使用 0.0.0.0 监听所有接口
python main.py --mode web --web-host 0.0.0.0

# 检查防火墙设置
# Windows: 允许Python通过防火墙
# Linux: sudo ufw allow 5000
```

## 下一步

- 阅读 [README_WEB_MODE.md](README_WEB_MODE.md) 了解详细功能
- 查看 [examples.py](examples.py) 学习更多使用场景
- 运行 [test_web_mode.py](test_web_mode.py) 验证功能

## 获取帮助

- 查看文档: README_WEB_MODE.md
- 运行示例: python examples.py
- 查看实现总结: IMPLEMENTATION_SUMMARY.md

## 提示

1. **保存UUID URL到书签**: 这样可以快速恢复会话
2. **使用Chrome引擎**: 生产环境更推荐使用 --use-chrome
3. **外网访问**: 使用 --web-host 0.0.0.0 但注意安全
4. **定期重启**: 长时间运行建议定期重启清理内存

开始享受Web模式带来的便利吧！ 🚀
