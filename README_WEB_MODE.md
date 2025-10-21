# 跑步助手 - Web模式使用说明

## 概述

本程序现在支持两种运行模式：

1. **桌面模式**（原有功能）- 使用PyWebView创建桌面应用
2. **Web模式**（新增功能）- 使用Flask创建Web服务器，支持多用户浏览器访问

## Web模式特性

### 核心功能

- **自动UUID分配**: 首次访问根URL时自动生成唯一会话ID
- **会话持久化**: 关闭浏览器后重新访问同一UUID链接，会话状态保持不变
- **本地计算**: 所有计算在Python后端执行，提高安全性
- **防浏览器卡顿**: 会话独立于浏览器进程，浏览器崩溃不影响后台任务

### 访问流程示例

1. 首次访问: `http://localhost:5000/`
2. 自动重定向到: `http://localhost:5000/uuid=a1b2c3d4e5f6789012345678`
3. 关闭浏览器后，可直接访问: `http://localhost:5000/uuid=a1b2c3d4e5f6789012345678`
4. 会话状态完整保留，继续之前的工作

## 安装依赖

### Web模式必需依赖
```bash
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet
```

### 桌面模式额外依赖
```bash
pip install pywebview[qt]
```

## 使用方法

### 启动Web模式

基本启动（本地访问，默认端口5000）:
```bash
python main.py --web
```

指定端口:
```bash
python main.py --web --port 8080
```

允许外网访问:
```bash
python main.py --web --host 0.0.0.0 --port 5000
```

### 启动桌面模式（原有功能）

```bash
python main.py
```

带自动登录:
```bash
python main.py --autologin 用户名 密码
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--web` | 启动Web服务器模式 | False（桌面模式） |
| `--port` | Web服务器端口 | 5000 |
| `--host` | Web服务器地址 | 127.0.0.1 |
| `--autologin` | 自动登录（仅桌面模式）| 无 |

## 安全建议

### Web模式安全配置

1. **仅本地使用**: 默认绑定127.0.0.1，仅本机可访问
2. **添加认证**: 生产环境建议添加身份验证
3. **使用HTTPS**: 公网部署时建议配置SSL证书
4. **防火墙规则**: 限制访问IP范围

### 会话管理

- 会话ID长度: 24字符
- 会话有效期: 7天（可在代码中调整）
- 会话存储: 内存存储（重启服务器会丢失）
- 会话清理: 每小时自动检查过期会话

## 架构说明

### 桌面模式
```
用户 → PyWebView窗口 → Python后端
```

### Web模式
```
用户 → 浏览器 → Flask服务器 → Python后端
                    ↓
              会话管理（UUID）
```

### API调用统一

前端使用统一的 `callPythonAPI()` 函数:
- **桌面模式**: 直接调用 `window.pywebview.api.*`
- **Web模式**: 通过HTTP POST调用 `/api/*` 端点

## 故障排除

### Web模式无法启动

1. 检查端口是否被占用:
```bash
netstat -an | grep 5000
```

2. 检查依赖是否安装:
```bash
pip list | grep -i "flask\|requests"
```

### 桌面模式无法启动

1. 安装PyWebView:
```bash
pip install pywebview[qt]
```

2. Linux系统可能需要额外的Qt依赖:
```bash
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine
```

### 会话丢失

- Web模式重启服务器会清空所有会话
- 建议使用持久化存储（如Redis）保存会话状态

## 性能优化

### Web模式性能提示

1. **并发处理**: Flask使用线程处理请求，支持多用户并发
2. **会话隔离**: 每个UUID对应独立的Api实例，互不干扰
3. **资源清理**: 定期清理过期会话释放内存

### 生产部署建议

使用生产级WSGI服务器（如Gunicorn）:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 开发说明

### 添加新的API端点

在 `Api` 类中添加方法后，前端自动可以通过 `callPythonAPI('method_name', args)` 调用。

### 调试模式

查看详细日志:
```bash
python main.py --web 2>&1 | tee server.log
```

## 更新日志

### v2.0 - Web模式支持
- ✅ 添加Flask Web服务器模式
- ✅ UUID自动分配和会话管理
- ✅ 统一API调用接口
- ✅ 可选依赖支持
- ✅ 本地计算提升安全性

## 许可证

（保持与原项目一致）
