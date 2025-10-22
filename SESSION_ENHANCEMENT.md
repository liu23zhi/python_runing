# 会话增强文档 - Session Enhancement

## 概述

本文档描述了对会话存储系统的全面增强，以支持离线模式任务数据的完整持久化，后台线程独立运行，以及完整状态恢复功能。

## 主要功能

### 1. 完整的任务数据持久化

会话现在保存以下完整的任务数据（兼容离线模式）：

- **target_points** - 打卡点坐标列表 `[(经度, 纬度), ...]`
- **target_point_names** - 打卡点名称，用'|'分隔
- **recommended_coords** - 服务器推荐路线坐标
- **draft_coords** - 用户绘制的草稿路径
- **run_coords** - 处理后用于模拟的最终路径（包含时间间隔）
- **errand_id** - 任务ID
- **errand_schedule** - 任务计划ID
- **任务基本信息** - 名称、状态、开始/结束时间等
- **运行时状态** - 当前打卡点序号、已跑距离、轨迹ID等

### 2. 后台线程独立运行

**关键特性**：
- 任务执行线程与浏览器完全独立
- 关闭浏览器后，任务继续在服务器端执行
- 每30秒自动保存运行状态到会话文件
- 任务完成时立即保存最终状态

**实现细节**：
```python
# 在任务执行线程中
if session_id and (time.time() - last_auto_save_time >= 30):
    save_session_state(session_id, web_sessions[session_id])
    last_auto_save_time = time.time()
```

### 3. 完整状态恢复

重新打开浏览器时，系统自动恢复以下状态：

- **登录状态** - login_success, user_info
- **用户配置** - params, device_ua
- **任务列表** - 所有已加载的任务及其完整数据
- **任务选择** - current_run_idx
- **运行进度** - GPS点、打卡点、距离、时间等
- **UI状态** - 可选的ui_state字段
- **用户设置** - 可选的user_settings字段

### 4. 自动同步机制

**触发保存的场景**：
- 用户登录/登出
- 加载任务列表
- 选择任务
- 开始/停止任务执行
- 导入/导出离线文件
- 录制/生成/处理/清除路径
- 更新参数
- 生成新UA
- 任务执行中（每30秒）
- 任务完成时

**防抖机制**：
- 最小保存间隔：2秒（避免过于频繁）
- 可使用 `force_save=True` 参数强制立即保存

### 5. 线程安全

**多级锁机制**：
1. **web_sessions_lock** - 保护全局会话字典
2. **session_file_locks** - 每个会话文件独立的文件锁
3. **session_file_locks_lock** - 保护锁字典本身

**使用示例**：
```python
# 获取或创建文件锁
with session_file_locks_lock:
    if session_hash not in session_file_locks:
        session_file_locks[session_hash] = threading.Lock()
    file_lock = session_file_locks[session_hash]

# 使用文件锁保护并发写入
with file_lock:
    # 安全地读写会话文件
    pass
```

## 工作流程

### 场景1：任务运行中关闭浏览器

```
1. 用户登录并开始任务
2. 任务开始执行，后台线程启动
3. 每30秒自动保存当前状态（进度、距离、打卡点等）
4. 用户关闭浏览器
5. 后台线程继续执行任务
6. 用户重新打开相同UUID链接
7. 系统自动从文件恢复会话状态
8. 前端显示实时进度（任务仍在运行）
```

### 场景2：服务器重启

```
1. 服务器启动时调用 load_all_sessions(args)
2. 扫描 sessions/ 目录下的所有会话文件
3. 验证会话未过期（7天有效期）
4. 恢复每个会话的完整状态
5. 用户访问时直接使用已恢复的会话
```

### 场景3：多设备访问

```
1. 用户A在设备1登录，获得UUID
2. 用户A复制UUID链接到设备2
3. 设备2访问相同UUID
4. 系统从文件加载会话状态
5. 两台设备共享相同的任务列表、进度等
```

## API变更

### 新增函数

#### `save_session_state(session_id, api_instance, force_save=False)`
保存会话状态到文件

**参数**：
- `session_id`: 会话UUID
- `api_instance`: Api实例
- `force_save`: 强制保存（忽略防抖）

#### `restore_session_to_api_instance(api_instance, state)`
从状态字典恢复Api实例

**参数**：
- `api_instance`: 要恢复的Api实例
- `state`: 从文件加载的状态字典

#### `load_session_state(session_id)`
从文件加载会话状态（线程安全）

**返回**：
- 成功：状态字典
- 失败：None

### 增强的函数

#### `load_all_sessions(args)`
现在会调用 `restore_session_to_api_instance` 恢复完整状态

#### API路由 `/api/<method>`
- 自动恢复过期会话
- 扩展自动保存的方法列表
- 所有状态改变操作后自动保存

#### `_run_submission_thread(...)`
- 新增 `session_id` 和 `last_auto_save_time` 变量
- 每30秒自动保存状态
- 任务完成时强制保存

## 文件结构

### 会话存储目录
```
sessions/
├── _index.json                          # UUID到哈希的映射索引
├── 927d9cc...651e1.json                # 会话文件（SHA256哈希命名）
└── abc1234...xyz789.json               # 其他会话文件
```

### 会话文件格式
```json
{
  "session_id": "完整的2048位UUID",
  "login_success": true,
  "user_info": {
    "username": "用户名",
    "id": "用户ID"
  },
  "created_at": 1234567890.0,
  "last_accessed": 1234567890.0,
  "params": {
    "interval_ms": 3000,
    "speed_mps": 1.5,
    ...
  },
  "device_ua": "User-Agent字符串",
  "user_data": {
    "name": "姓名",
    "student_id": "学号",
    ...
  },
  "current_run_idx": 0,
  "loaded_tasks": [
    {
      "run_name": "任务名称",
      "errand_id": "任务ID",
      "target_points": [[120.1, 30.2], [120.3, 30.4]],
      "target_point_names": "点1|点2",
      "recommended_coords": [[120.1, 30.2], ...],
      "draft_coords": [[120.1, 30.2, 1], ...],
      "run_coords": [[120.1, 30.2, 100], ...],
      "target_sequence": 1,
      "distance_covered_m": 1234.5,
      ...
    }
  ],
  "is_offline_mode": false,
  "stop_run_flag_set": false,
  "ui_state": {...},
  "user_settings": {...}
}
```

## 性能优化

### 防抖机制
- 最小保存间隔：2秒
- 避免过于频繁的文件写入

### 文件锁机制
- 每个会话文件独立锁
- 避免全局锁竞争
- 支持高并发读写

### 索引优化
- SHA256哈希索引避免频繁计算
- 索引文件加速会话查找

### 会话清理
- 启动时自动清理过期会话（7天）
- 定期清理机制可扩展

## 测试

### 单元测试
已通过的测试：
- ✅ 会话创建和保存
- ✅ 会话加载和恢复
- ✅ 任务数据完整性
- ✅ 登录状态恢复
- ✅ 参数恢复
- ✅ 线程安全（文件锁）

### 集成测试（待完成）
- [ ] 任务执行中关闭浏览器
- [ ] 服务器重启后恢复
- [ ] 多设备同UUID访问

## 安全性

### CodeQL分析结果
✅ **0个安全警告**

### 安全措施
1. 不暴露详细错误信息给前端
2. 会话文件使用SHA256哈希命名（防止路径遍历）
3. 会话有效期限制（7天）
4. 线程安全的文件访问
5. 异常处理完善

## 兼容性

### 向后兼容
- 旧的会话文件会自动清理或忽略
- 缺失字段使用默认值
- 不影响现有功能

### 离线模式
- 完全兼容离线任务导入
- 保存所有离线任务字段
- 恢复后可继续编辑/执行

## 故障排除

### 会话文件损坏
**症状**：无法加载会话
**解决**：删除对应的会话文件，系统会创建新会话

### 文件锁死锁
**症状**：保存或加载卡住
**解决**：重启服务器，锁会自动释放

### 内存占用过高
**症状**：服务器内存持续增长
**解决**：
1. 减少会话有效期（默认7天）
2. 实施定期清理机制
3. 限制最大会话数

## 未来优化

### 短期（1-2周）
- [ ] 添加会话数量限制
- [ ] 实现定期自动清理
- [ ] 添加会话统计API

### 中期（1-2月）
- [ ] 使用Redis替代文件存储
- [ ] 实现会话迁移工具
- [ ] 添加会话备份功能

### 长期（3-6月）
- [ ] 分布式会话存储
- [ ] 会话复制和故障转移
- [ ] 实时状态同步（WebSocket）

## 总结

本次增强实现了以下目标：

✅ **完整的离线任务数据持久化**
- 所有离线任务字段（target_points, run_coords等）完整保存

✅ **后台线程独立运行**
- 关闭浏览器后任务继续执行
- 每30秒自动保存状态

✅ **完整状态恢复**
- 登录状态、任务列表、运行进度全部恢复
- 刷新页面或重新打开均可恢复

✅ **自动同步机制**
- 所有状态改变操作自动保存
- 防抖机制避免过于频繁

✅ **线程安全**
- 多级锁保护并发访问
- 文件级锁避免竞争

✅ **安全性**
- CodeQL分析0警告
- 完善的异常处理

所有改动保持最小化原则，不影响现有功能，新增功能作为增强。
