# 跑步助手 (Running Helper)

一个基于Flask的Web应用，用于跑步任务管理和自动化。

## ✨ 特性

- 🌐 Web界面管理
- 🔐 用户认证和会话管理
- 🔒 SSL/HTTPS支持
- 🐳 Docker容器化部署
- 📱 移动端适配
- 🔄 实时WebSocket通信
- 🎨 现代化UI设计

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

最简单的部署方式，只需三步：

```bash
# 1. 克隆项目
git clone https://github.com/liu23zhi/python_runing.git
cd python_runing

# 2. 使用Docker Compose启动
docker-compose up -d

# 3. 访问应用
# 浏览器打开: http://localhost
```

详细的Docker部署文档：
- [Docker部署指南（中文）](DOCKER_CN.md)
- [Docker Deployment Guide (English)](DOCKER.md)

### 方式二：传统部署

#### 环境要求

- Python 3.8+
- Chrome/Chromium 浏览器

#### 安装步骤

**Linux/macOS:**

```bash
# 使用启动脚本
chmod +x start.sh
./start.sh
```

**Windows:**

```bash
# 使用批处理文件
start.bat
```

**手动安装:**

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 运行应用
python main.py
```

## 📖 使用说明

### 基本使用

启动应用后，在浏览器中访问：
- HTTP: `http://localhost:5000`
- HTTPS: `https://localhost:443` (需要配置SSL证书)

### 配置文件

首次运行会自动创建 `config.ini` 配置文件，包含：
- 数据库配置
- SSL/HTTPS设置
- 第三方服务配置
- 其他系统配置

### 命令行参数

```bash
python main.py [选项]

选项:
  --port PORT          指定端口号 (默认: 5000)
  --host HOST          指定监听地址 (默认: 127.0.0.1)
  --headless           使用无头模式运行Chrome (默认: True)
  --log-level LEVEL    设置日志级别 (debug/info/warning/error)
  --debug              启用调试模式
```

示例：
```bash
# 在8080端口运行
python main.py --port 8080

# 允许外部访问
python main.py --host 0.0.0.0

# 启用调试日志
python main.py --log-level debug
```

## 🔒 SSL/HTTPS 配置

### Docker环境

查看 [Docker部署指南](DOCKER_CN.md) 中的SSL配置章节。

### 传统环境

1. 准备SSL证书文件：
   - `ssl/fullchain.pem` - 证书文件
   - `ssl/privkey.key` - 私钥文件

2. 编辑 `config.ini`：
   ```ini
   [SSL]
   ssl_enabled = true
   ssl_cert_path = ssl/fullchain.pem
   ssl_key_path = ssl/privkey.key
   https_only = true
   ```

3. 重启应用

## 🐳 Docker 部署详解

### 标准HTTP部署

```bash
docker-compose up -d
```

访问: `http://服务器IP`

### HTTPS部署

```bash
# 1. 准备SSL证书到 ssl/ 目录
# 2. 配置 config.ini 启用SSL
# 3. 启动容器
docker-compose up -d
```

访问: `https://服务器IP`

Docker会同时监听80和443端口：
- 80端口: HTTP (自动重定向到HTTPS)
- 443端口: HTTPS

### Nginx反向代理（可选）

如果您需要更高级的功能（如负载均衡、缓存等），可以使用Nginx作为反向代理：

1. 参考 `nginx.conf.example` 配置示例
2. 修改Docker容器只监听本地端口
3. 配置Nginx代理到容器

详见: [nginx.conf.example](nginx.conf.example)

## 📁 项目结构

```
python_runing/
├── main.py                 # 主程序入口
├── index.html             # Web前端界面
├── requirements.txt       # Python依赖
├── config.ini            # 配置文件（自动生成）
├── Dockerfile            # Docker镜像构建文件
├── docker-compose.yml    # Docker Compose配置
├── docker-entrypoint.sh  # Docker启动脚本
├── start.sh              # Linux启动脚本
├── start.bat             # Windows启动脚本
├── ssl/                  # SSL证书目录
├── data/                 # 数据存储目录
├── cache/                # 缓存目录
└── logs/                 # 日志目录
```

## 🛠️ 开发

### 本地开发环境设置

```bash
# 克隆项目
git clone https://github.com/liu23zhi/python_runing.git
cd python_runing

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装Playwright
playwright install chromium

# 运行应用（开发模式）
python main.py --debug
```

### 代码结构

- `main.py`: Flask应用主文件，包含所有路由和业务逻辑
- `index.html`: 前端单页应用，包含所有UI和JavaScript逻辑
- API端点遵循RESTful设计

## 📝 更新日志

### v1.1.0 (2024-12-06)
- ✨ 新增Docker支持
- ✨ 支持同时监听80和443端口
- ✨ HTTP自动重定向到HTTPS
- 📝 完善文档

### v1.0.0
- 🎉 初始版本发布

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本项目仅供学习和研究使用，请勿用于违反相关法律法规的用途。使用本项目所产生的一切后果由使用者自行承担。

## 📞 支持

如有问题，请：
1. 查看文档：[DOCKER_CN.md](DOCKER_CN.md)
2. 提交Issue: [GitHub Issues](https://github.com/liu23zhi/python_runing/issues)
3. 查看日志文件排查问题

---

**Made with ❤️ by the community**
