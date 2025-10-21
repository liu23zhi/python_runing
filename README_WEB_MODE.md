# Web模式使用说明

## 概述

本应用现在支持两种运行模式：
1. **桌面应用模式（默认）**：传统的GUI桌面应用
2. **Web模式**：基于Flask的Web服务器，支持浏览器访问

## Web模式的特性

### UUID会话管理
- 首次访问时，系统会自动生成一个唯一的UUID
- 自动重定向到 `http://域名/uuid=<32位UUID>`
- 每个UUID对应一个独立的会话，互不干扰
- 关闭浏览器后再次访问相同的UUID地址，可以恢复到之前的程序状态
- 防止浏览器卡顿影响其他用户的使用

### JS执行引擎选项
支持两种JS执行方式：

1. **Pywebview（默认）**：使用隐藏的pywebview窗口作为JS引擎
2. **Chrome/Chromium**：使用真实的Chrome浏览器执行JS（推荐用于生产环境）

## 安装依赖

### 基础依赖
```bash
pip install flask
```

### 使用Chrome引擎（可选）
```bash
pip install selenium
```

还需要安装ChromeDriver：
- 访问 https://chromedriver.chromium.org/
- 下载与你的Chrome版本匹配的ChromeDriver
- 将ChromeDriver添加到系统PATH中

## 使用方法

### 启动Web模式（使用Pywebview作为JS引擎）
```bash
python main.py --mode web
```

### 启动Web模式（使用Chrome作为JS引擎）
```bash
python main.py --mode web --use-chrome
```

### 自定义端口和地址
```bash
python main.py --mode web --web-host 0.0.0.0 --web-port 8080
```

### 启动桌面应用模式（默认）
```bash
python main.py
# 或
python main.py --mode app
```

## 访问Web应用

启动后，在浏览器中访问显示的地址，例如：
```
http://127.0.0.1:5000
```

首次访问会自动重定向到类似这样的地址：
```
http://127.0.0.1:5000/uuid=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

## 工作原理

### 会话隔离
1. 用户首次访问根URL（如 `http://localhost:5000/`）
2. 系统生成一个32位的UUID（如 `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`）
3. 将UUID保存在Flask session中
4. 重定向到 `/uuid=<UUID>` 路径
5. 该UUID对应一个独立的数据会话
6. 关闭浏览器后，只要访问相同的UUID URL，就能恢复会话

### JS执行隔离
- **Pywebview模式**：在后台运行一个隐藏的webview窗口，所有JS计算在这个窗口中执行
- **Chrome模式**：启动无头Chrome浏览器，使用Selenium WebDriver执行JS代码

### 优势
- **防卡顿**：每个用户有独立的会话，一个用户的浏览器卡顿不会影响其他用户
- **可恢复**：通过UUID URL，用户可以在任何时间恢复到之前的状态
- **可扩展**：可以部署到服务器上，多人通过浏览器同时使用
- **跨平台**：只需要浏览器，不需要安装桌面应用

## API端点

### 用户端点
- `GET /` - 首页，自动分配UUID并重定向
- `GET /uuid=<uuid>` - 带UUID的会话页面

### 管理端点
- `GET /health` - 健康检查
- `GET /sessions` - 查看活跃会话列表（调试用）

### API代理端点
- `GET/POST /api/<method>` - 代理到Python后端的API方法

## 安全注意事项

1. **生产环境部署**：
   - 修改 `app.secret_key` 为更安全的密钥
   - 使用HTTPS
   - 配置防火墙规则
   - 禁用 `/sessions` 调试端点

2. **会话清理**：
   - 当前版本的会话不会自动过期
   - 建议添加会话超时机制
   - 定期清理不活跃的会话

3. **资源限制**：
   - 限制同时活跃的会话数量
   - 添加速率限制
   - 监控内存使用

## 故障排除

### Chrome启动失败
- 确保已安装Chrome/Chromium浏览器
- 确保ChromeDriver版本与Chrome版本匹配
- 检查ChromeDriver是否在系统PATH中

### 端口被占用
```bash
# 使用其他端口
python main.py --mode web --web-port 8080
```

### Flask导入错误
```bash
pip install flask
```

### Selenium导入错误
```bash
pip install selenium
```

## 开发建议

### 扩展会话数据
在 `web_mode.py` 中的 `active_sessions` 字典可以存储每个会话的自定义数据：

```python
active_sessions[session_uuid] = {
    'api': api_instance,
    'data': {
        'user_preferences': {},
        'cached_results': {},
        # 添加更多自定义字段
    }
}
```

### 添加会话过期
可以在 `active_sessions` 中添加 `last_access` 时间戳，并实现定期清理：

```python
import time

# 在会话创建时
active_sessions[session_uuid] = {
    'api': api_instance,
    'last_access': time.time(),
    'data': {}
}

# 添加清理函数
def cleanup_expired_sessions(max_age_seconds=3600):
    now = time.time()
    with sessions_lock:
        expired = [
            uuid for uuid, sess in active_sessions.items()
            if now - sess.get('last_access', 0) > max_age_seconds
        ]
        for uuid in expired:
            del active_sessions[uuid]
```

## 版本信息

- 首次实现：2025-10-21
- 支持的Python版本：3.7+
- 依赖的主要库：Flask, Pywebview, Selenium（可选）
