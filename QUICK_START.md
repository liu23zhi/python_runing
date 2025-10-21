# 快速开始指南

## 30秒快速启动

### 安装和启动

```bash
# 1. 安装依赖
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet playwright

# 2. 安装Chromium浏览器
python -m playwright install chromium

# 3. 启动服务器
python main.py

# 4. 打开浏览器访问
# http://localhost:5000/
```

就这么简单！浏览器会自动跳转到带UUID的地址。

**注意**: 本程序已完全采用Web模式，弃用了桌面模式和tkinter。所有JS计算在服务器端Chrome中执行。

## 常用命令

| 命令 | 说明 |
|------|------|
| `python main.py` | 启动服务器（默认端口5000） |
| `python main.py --port 8080` | 指定端口 |
| `python main.py --host 0.0.0.0` | 允许外网访问 |
| `python main.py --headless False` | 使用可见Chrome窗口（调试用） |

## 首次使用流程

1. **启动服务器**
   ```bash
   python main.py
   ```
   
2. **看到提示**
   ```
   ============================================================
     跑步助手 Web 模式已启动（服务器端Chrome渲染）
     访问地址: http://127.0.0.1:5000
     首次访问将自动分配UUID并重定向
     JS计算在服务器端Chrome中执行，提升安全性
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
   - 所有JS计算在服务器端Chrome中执行
   - 客户端浏览器仅用于显示和交互

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
# 安装所有依赖
pip install Flask flask-cors requests openpyxl xlrd xlwt chardet playwright

# 安装Chromium浏览器
python -m playwright install chromium
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

**重要提示:** 
- 本程序已完全弃用桌面模式和tkinter
- 所有JS计算在服务器端Chrome中执行，提升安全性
- 用户浏览器仅作为显示界面，无需任何客户端依赖
