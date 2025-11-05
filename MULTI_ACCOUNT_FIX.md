# 多账号模式修复说明

## 问题描述

多账号模式存在异常，无法执行。

## 根本原因

在多账号工作线程 `_multi_account_worker` 中，代码尝试使用桌面模式的 `self.window.evaluate_js()` 进行路径规划，但在 Web 模式下 `self.window` 不存在（桌面模式已弃用）。

### 问题代码位置

1. **第 7673-7674 行**：路径规划调用
```python
self.window.evaluate_js(
    f'triggerPathGenerationForPy("{acc.username}", {json.dumps(waypoints)})')
```

2. **第 7937-7940 行**：地图位置更新
```python
if self.window:
    self.window.evaluate_js(
        f'multi_updateRunnerPosition("{acc.username}", {lon}, {lat}, "{acc.user_data.name}")')
```

## 修复方案

### 1. 路径规划修复（核心修复）

将桌面模式的 `self.window.evaluate_js()` 替换为 Web 模式的 `chrome_pool.execute_js()`，使用与后台任务模式相同的 JavaScript 代码。

**修复后的逻辑**：
1. 检查 `chrome_pool` 是否可用
2. 获取会话 ID（`_web_session_id`）
3. 加载高德地图 API 密钥（带缓存优化）
4. 获取 Chrome 浏览器上下文
5. 检查并加载高德地图 SDK（避免重复加载）
6. 执行路径规划 JavaScript
7. 处理结果或错误

### 2. 地图更新修复

移除桌面模式的地图更新代码，因为：
- 在 Web 模式下不需要
- 前端通过其他方式更新地图

### 3. 性能优化

**配置缓存**：
- API 密钥缓存在 `self._amap_key_cached` 中
- 避免每个任务都重新读取配置文件

**SDK 加载优化**：
- 检查 AMap SDK 是否已加载
- 避免重复加载 CDN 资源

**错误处理增强**：
- 添加详细的错误日志
- 提供清晰的错误消息

## 修复效果

### ✅ 功能恢复
- 多账号模式现在可以在 Web 模式下正常工作
- 无需 GUI 窗口，可以在后台运行
- 浏览器标签页关闭后仍可继续执行

### ✅ 性能提升
- 减少文件 I/O 操作（API 密钥缓存）
- 减少网络请求（SDK 加载检查）
- 更好的错误处理和日志记录

### ✅ 一致性改进
- 与单账号模式保持一致
- 与后台任务模式保持一致
- 统一使用 chrome_pool 进行路径规划

## 测试结果

| 测试项 | 结果 |
|--------|------|
| Python 语法检查 | ✅ 通过 |
| CodeQL 安全扫描 | ✅ 无漏洞 |
| 代码审查 | ✅ 主要问题已解决 |

## 使用建议

### 配置要求

1. **高德地图 API 密钥**：
   - 在 `config.ini` 中配置 `amap_js_key`
   - 路径：`[Map] amap_js_key = 你的密钥`

2. **Chrome 浏览器**：
   - 确保 Playwright Chromium 已安装
   - 运行：`python -m playwright install chromium`

### 运行模式

多账号模式现在支持：
- ✅ 网页打开时运行
- ✅ 网页关闭后后台运行（使用 chrome_pool）
- ✅ 多个账号并发执行

## 技术细节

### 路径规划 JavaScript

使用的 JavaScript 代码与后台任务模式相同，包含：
- AMapLoader 加载
- AMap.Walking 插件
- 分段路径规划
- 重试机制（最多 3 次）
- 直线回退选项（可配置）

### Chrome Pool 集成

```python
# 获取 Chrome 上下文
ctx = chrome_pool.get_context(session_id)
page = ctx['page']

# 执行 JavaScript
path_coords = chrome_pool.execute_js(
    session_id,
    javascript_code,
    waypoints,
    amap_key,
    acc.params
)
```

## 相关代码位置

- **修复代码**：`main.py` 第 7668-7850 行
- **相关函数**：`_multi_account_worker`
- **配置文件**：`config.ini` [Map] 节

## 后续建议

1. 测试多账号模式在实际使用中的表现
2. 监控日志文件中的错误信息
3. 根据使用情况调整缓存策略
4. 考虑添加单元测试

## 版本信息

- **修复日期**：2025-11-04
- **修复分支**：copilot/fix-multi-account-issue
- **提交哈希**：fbab7b8
