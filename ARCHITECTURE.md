# 架构文档 - 服务器端Chrome渲染

## 概述

本应用已完全弃用桌面模式和tkinter，采用纯Web架构，通过Playwright在服务器端运行Chrome进行所有JavaScript计算。

## 架构图

```
┌─────────────────┐
│  用户浏览器      │  ← 仅作为显示界面
│  (任意浏览器)    │     接收用户输入，显示结果
└────────┬────────┘
         │ HTTP请求
         ↓
┌─────────────────────┐
│  Flask Web服务器    │
│  ┌───────────────┐  │
│  │ UUID会话管理  │  │  ← 每个用户一个独立会话
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ API路由       │  │  ← /api/<method>, /execute_js
│  └───────────────┘  │
└────────┬────────────┘
         │
         ↓
┌─────────────────────┐
│  Python后端 (Api类) │
│  - 业务逻辑         │
│  - 数据处理         │
│  - 网络请求         │
└────────┬────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Playwright + Chrome浏览器池 │
│  ┌─────────────────────┐    │
│  │ 会话1 → Chrome上下文 │    │  ← 独立的浏览器上下文
│  ├─────────────────────┤    │
│  │ 会话2 → Chrome上下文 │    │
│  ├─────────────────────┤    │
│  │ 会话N → Chrome上下文 │    │
│  └─────────────────────┘    │
│  - 执行JavaScript代码       │
│  - 地图API调用             │
│  - 路径计算                │
└─────────────────────────────┘
```

## 关键组件

### 1. ChromeBrowserPool

**职责**: 管理服务器端Chrome浏览器实例

**功能**:
- 初始化Playwright和Chromium浏览器
- 为每个会话创建独立的浏览器上下文
- 在Chrome中执行JavaScript代码
- 清理过期的浏览器上下文

**代码位置**: `main.py` 中的 `ChromeBrowserPool` 类

```python
class ChromeBrowserPool:
    def __init__(self, headless=True, max_instances=5)
    def get_context(self, session_id)
    def execute_js(self, session_id, script, *args)
    def close_context(self, session_id)
    def cleanup(self)
```

### 2. Flask Web服务器

**路由**:
- `/` - 首页，自动分配UUID并重定向
- `/uuid=<uuid>` - 会话页面，显示应用界面
- `/api/<method>` - Python API调用端点
- `/execute_js` - 在服务器端Chrome中执行JS
- `/health` - 健康检查

### 3. 前端API层

**JavaScript函数**:
- `callPythonAPI(method, ...args)` - 调用Python后端API
- `executeServerJS(script, ...args)` - 在服务器端Chrome执行JS

## 数据流

### 用户登录流程

```
1. 用户访问 http://localhost:5000/
   ↓
2. Flask: 生成UUID，创建session
   ↓
3. 重定向到 /uuid=<generated-uuid>
   ↓
4. 返回HTML界面给用户浏览器
   ↓
5. 用户输入账号密码，点击登录
   ↓
6. 前端: callPythonAPI('login', username, password)
   ↓
7. Flask: 转发到Api.login()
   ↓
8. Python后端: 验证用户，返回结果
   ↓
9. 前端: 接收结果，更新UI
```

### JS计算流程

```
1. 前端需要执行JS计算
   ↓
2. 调用: executeServerJS('function() { ... }', args)
   ↓
3. 发送POST请求到 /execute_js
   ↓
4. Flask接收请求
   ↓
5. 调用: chrome_pool.execute_js(session_id, script, args)
   ↓
6. Playwright在服务器端Chrome中执行JS
   ↓
7. 返回执行结果
   ↓
8. 前端接收结果并处理
```

## 安全性

### 优势

1. **JS逻辑隐藏**: 所有计算逻辑在服务器端，用户无法查看或修改
2. **防篡改**: 用户浏览器无法修改计算逻辑
3. **沙箱隔离**: 每个会话有独立的Chrome上下文
4. **代码保护**: 核心算法不暴露给客户端

### 安全措施

- 会话ID使用UUID4生成，24位随机字符
- 会话有效期7天（可配置）
- 服务器端Chrome运行在无头模式
- API端点需要有效的session_id
- 错误信息不暴露内部细节

## 性能特性

### 资源管理

- **浏览器复用**: Chrome浏览器进程在服务器启动时创建，多个会话共享
- **上下文隔离**: 每个会话独立的浏览器上下文，互不干扰
- **按需创建**: 浏览器上下文在首次需要时创建
- **自动清理**: 定期清理过期的上下文

### 并发支持

- Flask使用线程模式 (`threaded=True`)
- 支持多个用户同时访问
- 每个会话独立处理，不会相互阻塞

## 部署要求

### 服务器环境

**必需**:
- Python 3.8+
- Chromium浏览器（通过Playwright安装）
- 足够的内存（每个Chrome上下文约100-200MB）

**推荐配置**:
- CPU: 2核心以上
- 内存: 2GB以上（支持10个并发会话）
- 存储: 500MB以上（Chromium浏览器约300MB）

### 安装步骤

```bash
# 1. 安装Python依赖
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet playwright

# 2. 安装Chromium浏览器
python -m playwright install chromium

# 3. 启动服务器
python main.py
```

### 生产部署

使用Gunicorn提升性能：

```bash
# 安装Gunicorn
pip install gunicorn

# 启动（4个worker进程）
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

配合Nginx反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_timeout 300s;  # 增加超时时间支持长时间计算
    }
}
```

## 与旧架构对比

| 特性 | 旧架构（桌面模式） | 新架构（纯Web） |
|------|-------------------|----------------|
| GUI框架 | tkinter/PyWebView | 无（纯Web） |
| JS执行位置 | 用户浏览器 | 服务器端Chrome |
| 客户端要求 | 安装Python+依赖 | 仅需浏览器 |
| 多用户支持 | 否 | 是（UUID会话） |
| 安全性 | 中等 | 高 |
| 部署难度 | 需要GUI环境 | 仅需服务器 |
| 资源占用 | 每用户独立进程 | 共享Chrome进程 |

## 故障排除

### Chromium未安装

**症状**:
```
ERROR: Executable doesn't exist at .../chromium.../chrome-linux/headless_shell
```

**解决**:
```bash
python -m playwright install chromium
```

### 端口已占用

**症状**:
```
Address already in use
```

**解决**:
```bash
# 方法1: 使用其他端口
python main.py --port 8080

# 方法2: 结束占用进程
lsof -ti:5000 | xargs kill -9
```

### Chrome上下文过多

**症状**: 内存占用过高

**解决**: 实现会话过期清理逻辑，定期关闭不活跃的上下文

## 未来优化

1. **会话持久化**: 使用Redis存储会话状态
2. **负载均衡**: 多服务器部署，共享会话
3. **资源限制**: 限制每个会话的资源使用
4. **WebSocket**: 实时通信，减少轮询
5. **缓存机制**: 缓存常用的JS计算结果

## 许可证

（与主项目一致）
