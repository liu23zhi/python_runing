# 跑步助手 (Running Assistant)

一个功能强大的跑步任务管理工具，支持桌面应用和Web模式。

## 🌟 主要特性

### 桌面应用模式
- 🖥️ 原生桌面GUI界面
- 📍 实时GPS轨迹模拟
- 🗺️ 高德地图集成
- 📊 任务统计和历史记录
- 👥 多账号管理

### Web模式 (NEW!)
- 🌐 **浏览器访问，无需安装**
- 🔐 **UUID会话管理** - 每个用户独立空间
- 🔄 **自动重定向** - 首次访问自动分配UUID
- 💾 **会话持久化** - 关闭浏览器可恢复
- 🚫 **防卡顿隔离** - 多用户互不影响
- 🎯 **Chrome引擎支持** - 更稳定的JS执行

## 📦 安装

### 基础依赖
```bash
pip install -r requirements.txt
```

### 可选依赖（用于Web模式Chrome引擎）
```bash
pip install selenium
# 并安装 ChromeDriver: https://chromedriver.chromium.org/
```

## 🚀 快速开始

### 桌面模式（默认）
```bash
python main.py
```

### Web模式
```bash
# 基本使用
python main.py --mode web

# 使用Chrome引擎（推荐）
python main.py --mode web --use-chrome

# 自定义配置
python main.py --mode web --web-host 0.0.0.0 --web-port 8080 --use-chrome
```

然后在浏览器中访问显示的地址，例如：
```
http://127.0.0.1:5000
```

## 📖 文档

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | ⚡ 5分钟快速上手指南 |
| [README_WEB_MODE.md](README_WEB_MODE.md) | 📘 Web模式完整文档 |
| [CHANGELOG.md](CHANGELOG.md) | 📋 更新日志 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 🏗️ 系统架构图 |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | 📝 实现总结 |

## 💡 使用示例

### 示例1: 本地开发
```bash
python main.py --mode web
# 访问 http://localhost:5000
```

### 示例2: 团队协作
```bash
python main.py --mode web --web-host 0.0.0.0 --web-port 8080
# 团队成员通过 http://服务器IP:8080 访问
# 每人获得独立的UUID会话
```

### 示例3: 生产部署
```bash
python main.py --mode web --use-chrome
# 配合 Nginx 反向代理和 HTTPS
```

更多示例请运行：
```bash
python examples.py
```

## 🔧 命令行参数

```bash
usage: main.py [-h] [--autologin USERNAME PASSWORD] [--mode {app,web}]
               [--web-host WEB_HOST] [--web-port WEB_PORT] [--use-chrome]

options:
  --mode {app,web}      运行模式（默认: app）
  --web-host HOST       Web模式监听地址（默认: 127.0.0.1）
  --web-port PORT       Web模式端口（默认: 5000）
  --use-chrome          使用Chrome作为JS引擎（需要selenium）
  --autologin USER PASS 自动登录（仅app模式）
```

## 🧪 测试

运行自动化测试套件：
```bash
python test_web_mode.py
```

测试内容：
- ✅ Web服务器启动
- ✅ UUID自动分配
- ✅ 会话重定向
- ✅ 会话持久化
- ✅ 多会话隔离

## 🎯 Web模式工作原理

### UUID会话流程

```
用户首次访问
    ↓
http://localhost:5000/
    ↓
系统生成UUID: abc123...
    ↓
重定向到
    ↓
http://localhost:5000/uuid=abc123...
    ↓
用户操作，数据保存在该UUID会话
    ↓
关闭浏览器
    ↓
再次访问相同UUID URL
    ↓
恢复之前的会话数据
```

### 多用户隔离

- 每个UUID有独立的数据空间
- 多用户可同时使用，互不干扰
- 一个用户的浏览器卡顿不影响其他用户

详细架构请查看 [ARCHITECTURE.md](ARCHITECTURE.md)

## 🛠️ 项目结构

```
python_runing/
├── main.py                      # 主程序入口
├── web_mode.py                  # Web模式实现
├── index.html                   # 前端页面
├── requirements.txt             # 依赖列表
├── .gitignore                   # Git忽略规则
│
├── 文档/
│   ├── README_WEB_MODE.md       # Web模式详细文档
│   ├── QUICKSTART.md            # 快速开始指南
│   ├── IMPLEMENTATION_SUMMARY.md # 实现总结
│   ├── CHANGELOG.md             # 更新日志
│   └── ARCHITECTURE.md          # 系统架构
│
├── 工具/
│   ├── examples.py              # 使用示例
│   └── test_web_mode.py         # 测试套件
│
└── build.bat                    # Windows构建脚本
```

## 📋 依赖

### 必需依赖
- Python 3.7+
- pywebview[qt]
- requests
- openpyxl, xlrd, xlwt
- chardet
- flask (Web模式)

### 可选依赖
- selenium (Chrome引擎)

完整列表见 [requirements.txt](requirements.txt)

## 🔒 安全建议

在生产环境使用时：
1. ✅ 使用HTTPS
2. ✅ 配置防火墙
3. ✅ 添加用户认证
4. ✅ 实现会话超时
5. ✅ 启用速率限制

详细安全建议请查看 [README_WEB_MODE.md](README_WEB_MODE.md)

## 🚀 性能优化

### 生产环境推荐配置
```bash
# 使用 Gunicorn 作为 WSGI 服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'web_mode:create_app(api, event)'

# 配合 Nginx 反向代理
# 启用 HTTPS
# 配置缓存
```

详细优化建议请查看 [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 🐛 故障排除

### 常见问题

**Q: Flask导入错误**
```bash
pip install flask
```

**Q: Chrome启动失败**
```bash
# 安装selenium
pip install selenium
# 下载ChromeDriver
# 访问 https://chromedriver.chromium.org/
```

**Q: 端口被占用**
```bash
python main.py --mode web --web-port 8080
```

更多问题请查看 [QUICKSTART.md](QUICKSTART.md)

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解最新变更。

### 最近更新 (2025-10-21)
- ✨ 添加Web模式支持
- 🔐 实现UUID会话管理
- 🚀 支持Chrome/Chromium JS引擎
- 📚 完整的文档和示例
- 🧪 自动化测试套件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可

本项目仅供学习和研究使用。

## 📞 获取帮助

1. 📖 查看文档（特别是 [QUICKSTART.md](QUICKSTART.md)）
2. 🔍 查看示例代码 (`python examples.py`)
3. 🧪 运行测试 (`python test_web_mode.py`)
4. 💬 提交Issue

## 🎉 开始使用

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Web模式
python main.py --mode web

# 在浏览器中打开
# http://127.0.0.1:5000
```

享受使用！ 🎊
