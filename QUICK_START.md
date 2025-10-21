# 快速开始指南

## 30秒快速启动

### Web模式（推荐）

```bash
# 1. 安装依赖
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet

# 2. 启动服务器
python main.py --web

# 3. 打开浏览器访问
# http://localhost:5000/
```

就这么简单！浏览器会自动跳转到带UUID的地址。

### 桌面模式（原有功能）

```bash
# 1. 安装额外依赖
pip install pywebview[qt]

# 2. 启动应用
python main.py
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `python main.py --web` | 启动Web模式（默认端口5000） |
| `python main.py --web --port 8080` | 指定端口 |
| `python main.py --web --host 0.0.0.0` | 允许外网访问 |
| `python main.py` | 启动桌面模式 |
| `python main.py --autologin 学号 密码` | 桌面模式自动登录 |

## 首次使用流程

### Web模式

1. **启动服务器**
   ```bash
   python main.py --web
   ```
   
2. **看到提示**
   ```
   ============================================================
     跑步助手 Web 模式已启动
     访问地址: http://127.0.0.1:5000
     首次访问将自动分配UUID并重定向
   ============================================================
   ```

3. **打开浏览器**
   - 访问: `http://localhost:5000/`
   - 自动跳转到: `http://localhost:5000/uuid=xxxxxxxxxxxxxx`

4. **保存UUID链接**
   - 将带UUID的链接加入书签
   - 下次直接访问这个链接即可恢复会话

5. **开始使用**
   - 登录账号
   - 使用所有功能（与桌面版相同）

### 桌面模式

1. **启动应用**
   ```bash
   python main.py
   ```

2. **等待窗口打开**
   - 自动打开应用窗口
   - 选择账号或输入新账号
   - 登录使用

## 疑难解答

### 问题1: 端口已被占用

**错误信息:**
```
Address already in use
```

**解决方法:**
```bash
# 方法1: 使用其他端口
python main.py --web --port 5001

# 方法2: 查找并关闭占用端口的进程
lsof -ti:5000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :5000   # Windows
```

### 问题2: 依赖未安装

**错误信息:**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方法:**
```bash
# Web模式
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet

# 桌面模式（额外需要）
pip install pywebview[qt]
```

### 问题3: 无法访问

**检查清单:**
- [ ] 服务器是否正在运行？
- [ ] 端口号是否正确？
- [ ] 防火墙是否阻止？
- [ ] Host配置是否正确？

**测试命令:**
```bash
curl http://localhost:5000/health
# 应返回: {"status":"ok","sessions":0}
```

## 下一步

- 📖 查看 [README_WEB_MODE.md](README_WEB_MODE.md) 了解详细功能
- 💡 查看 [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) 查看使用场景
- 🔧 查看 [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) 了解技术细节

## 需要帮助？

1. 检查日志输出查看详细错误
2. 确认依赖版本兼容性
3. 查看文档寻找答案
4. 提交Issue报告问题

---

**提示:** 首次启动建议使用Web模式，更轻量且无需安装GUI相关依赖。
