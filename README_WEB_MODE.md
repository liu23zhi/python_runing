# 跑步助手 - Web模式使用说明

## 概述

本程序采用纯Web模式架构（已弃用桌面模式和tkinter）：

- **Web模式** - 使用Flask创建Web服务器，支持多用户浏览器访问
- **服务器端渲染** - 使用Playwright在服务器端运行Chrome处理JS计算
- **零客户端依赖** - 用户只需浏览器，无需安装任何额外软件

## Web模式特性

### 核心功能

- **自动UUID分配**: 首次访问根URL时自动生成唯一会话ID
- **会话持久化**: 关闭浏览器后重新访问同一UUID链接，会话状态保持不变
- **服务器端JS执行**: 所有JS计算在服务器端Chrome中执行，客户端浏览器仅作为显示界面
- **增强安全性**: 用户浏览器无法访问或篡改JS计算逻辑
- **防浏览器卡顿**: 会话独立于浏览器进程，浏览器崩溃不影响后台任务

### 访问流程示例

1. 首次访问: `http://localhost:5000/`
2. 自动重定向到: `http://localhost:5000/uuid=a1b2c3d4e5f6789012345678`
3. 关闭浏览器后，可直接访问: `http://localhost:5000/uuid=a1b2c3d4e5f6789012345678`
4. 会话状态完整保留，继续之前的工作

## 安装依赖

### 必需依赖
```bash
# 安装Python依赖
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet playwright

# 安装Playwright的Chromium浏览器
python -m playwright install chromium
```

## 使用方法

### 启动服务器

基本启动（本地访问，默认端口5000）:
```bash
python main.py
```

指定端口:
```bash
python main.py --port 8080
```

允许外网访问:
```bash
python main.py --host 0.0.0.0 --port 5000
```

使用可见的Chrome窗口（调试用）:
```bash
python main.py --headless=False
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--port` | Web服务器端口 | 5000 |
| `--host` | Web服务器地址 | 127.0.0.1 |
| `--headless` | 使用无头Chrome模式 | True |

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

### 新架构（纯Web模式）
```
用户浏览器（仅显示） → Flask服务器 → Python后端
                          ↓
                    会话管理（UUID）
                          ↓
                  服务器端Chrome（JS执行）
```

### 关键特性

- **客户端浏览器**: 仅负责UI显示和用户交互
- **Flask服务器**: 处理HTTP请求，管理会话
- **Python后端**: 执行所有业务逻辑
- **服务器端Chrome**: 使用Playwright控制，执行所有JS计算

### API调用

前端调用流程:
1. `callPythonAPI()` - 调用Python后端API
2. `executeServerJS()` - 在服务器端Chrome中执行JS代码

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
