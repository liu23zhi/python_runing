# 认证和权限管理系统文档

## 概述

本文档描述完整的用户认证和权限管理系统实现，包括用户注册/登录、游客模式、权限组管理和管理面板。

## 功能特性

### 1. 用户认证

#### 用户注册
- 用户可以注册新账号（用户名3-20字符，密码至少6字符）
- 密码使用SHA256哈希存储
- 用户数据保存在`users/`目录，文件名为用户名的SHA256哈希
- 新用户默认分配到`user`权限组

#### 用户登录
- 使用用户名和密码登录
- 验证密码哈希
- 登录成功后会话关联认证信息
- 超级管理员用户名在`config.ini`中配置

#### 游客登录
- 可在`config.ini`中配置是否允许游客登录
- 游客无需注册即可使用系统
- 游客权限受限（详见权限系统）

### 2. 权限系统

#### 权限组

系统预定义4个权限组：

**游客 (guest)**
- ✅ 查看通知 (view_notifications)
- ✗ 标记通知已读 (mark_notifications_read)
- ✗ 执行多账号任务 (execute_multi_account)
- ✗ 使用签到功能 (use_attendance)
- ✅ 执行单个任务 (execute_single_task)
- ✅ 导入离线文件 (import_offline)
- ✅ 导出数据 (export_data)
- ✅ 修改参数 (modify_params)

**普通用户 (user)**
- ✅ 所有基础功能
- ✅ 标记通知已读
- ✅ 执行多账号任务
- ✅ 使用签到功能

**管理员 (admin)**
- ✅ 所有普通用户权限
- ✅ 管理用户 (manage_users)
- ✅ 管理权限组 (manage_permissions)

**超级管理员 (super_admin)**
- ✅ 所有管理员权限
- ✅ 管理系统 (manage_system)
- ✅ 创建和修改权限组

#### 权限检查

API调用会自动检查权限：
- `mark_notification_read` - 需要 `mark_notifications_read` 权限
- `mark_all_read` - 需要 `mark_notifications_read` 权限
- `trigger_attendance` - 需要 `use_attendance` 权限
- `multi_start_single_account` - 需要 `execute_multi_account` 权限
- `multi_start_all_accounts` - 需要 `execute_multi_account` 权限

权限不足时返回403错误。

### 3. 配置文件

#### config.ini
```ini
[Admin]
# 超级管理员用户名
super_admin = admin

[Guest]
# 是否允许游客登录（无需账号）
allow_guest_login = true

[System]
# 会话有效期（天）
session_expiry_days = 7
# 用户数据存储目录
users_dir = users
# 权限组存储文件
permissions_file = permissions.json
```

#### permissions.json

存储所有权限组配置和用户组分配：

```json
{
  "permission_groups": {
    "guest": {
      "name": "游客",
      "permissions": { ... }
    },
    ...
  },
  "user_groups": {
    "username1": "user",
    "username2": "admin"
  }
}
```

### 4. 管理面板

#### 访问要求
- 必须是`admin`或`super_admin`用户
- 主界面右上角显示"管理"按钮

#### 用户管理
- 查看所有注册用户
- 显示用户创建时间和最后登录时间
- 更改用户的权限组

#### 权限组管理
- 查看所有权限组
- 显示每个权限组的权限列表
- 超级管理员可创建/修改权限组（通过API）

## 用户界面

### 1. 认证登录页面

#### 位置
- Web模式启动时首先显示
- 认证成功后进入应用登录页面

#### 功能
- **登录标签**：用户名、密码输入框
- **注册标签**：用户名、密码、确认密码输入框
- **游客登录按钮**：允许游客时显示
- 错误和成功消息提示

### 2. 管理面板

#### 用户管理标签
- 用户列表（用户名、创建时间、最后登录、权限组）
- 下拉菜单切换用户权限组
- 实时更新

#### 权限组管理标签
- 权限组列表
- 每个权限的启用/禁用状态
- 仅查看（超级管理员可通过API修改）

## API端点

### 认证API

#### POST /auth/register
注册新用户

**请求体：**
```json
{
  "auth_username": "username",
  "auth_password": "password"
}
```

**响应：**
```json
{
  "success": true,
  "message": "注册成功"
}
```

#### POST /auth/login
用户登录

**请求头：** `X-Session-ID: <session_uuid>`

**请求体：**
```json
{
  "auth_username": "username",
  "auth_password": "password"
}
```

**响应：**
```json
{
  "success": true,
  "auth_username": "username",
  "group": "user",
  "is_guest": false
}
```

#### POST /auth/guest_login
游客登录

**请求头：** `X-Session-ID: <session_uuid>`

**响应：**
```json
{
  "success": true,
  "auth_username": "guest",
  "group": "guest",
  "is_guest": true
}
```

#### POST /auth/check_permission
检查权限

**请求头：** `X-Session-ID: <session_uuid>`

**请求体：**
```json
{
  "permission": "mark_notifications_read"
}
```

**响应：**
```json
{
  "success": true,
  "has_permission": false
}
```

### 管理API

所有管理API需要管理员权限。

#### GET /auth/admin/list_users
列出所有用户

**请求头：** `X-Session-ID: <session_uuid>`

**响应：**
```json
{
  "success": true,
  "users": [
    {
      "auth_username": "user1",
      "group": "user",
      "created_at": 1234567890.0,
      "last_login": 1234567900.0
    }
  ]
}
```

#### POST /auth/admin/update_user_group
更新用户权限组

**请求头：** `X-Session-ID: <session_uuid>`

**请求体：**
```json
{
  "target_username": "user1",
  "new_group": "admin"
}
```

**响应：**
```json
{
  "success": true,
  "message": "权限组已更新"
}
```

#### GET /auth/admin/list_groups
列出所有权限组

**请求头：** `X-Session-ID: <session_uuid>`

**响应：**
```json
{
  "success": true,
  "groups": {
    "guest": {
      "name": "游客",
      "permissions": { ... }
    }
  }
}
```

#### POST /auth/admin/create_group
创建权限组（仅超级管理员）

**请求体：**
```json
{
  "group_name": "custom_group",
  "display_name": "自定义组",
  "permissions": {
    "view_notifications": true,
    ...
  }
}
```

#### POST /auth/admin/update_group
更新权限组（仅超级管理员）

**请求体：**
```json
{
  "group_name": "custom_group",
  "permissions": {
    "view_notifications": true,
    ...
  }
}
```

#### GET /auth/get_config
获取认证配置

**响应：**
```json
{
  "success": true,
  "allow_guest_login": true
}
```

## 技术实现

### 后端 (Python)

#### AuthSystem类
- `_load_config()` - 加载config.ini
- `_load_permissions()` - 加载permissions.json
- `_save_permissions()` - 保存权限配置
- `register_user(username, password)` - 用户注册
- `authenticate(username, password)` - 用户认证
- `check_permission(username, permission)` - 权限检查
- `get_user_group(username)` - 获取用户组
- `update_user_group(username, group)` - 更新用户组
- `create_permission_group()` - 创建权限组
- `update_permission_group()` - 更新权限组
- `list_users()` - 列出所有用户
- `get_all_groups()` - 获取所有权限组

#### 会话集成
- 认证信息存储在会话：`auth_username`, `auth_group`, `is_guest`, `is_authenticated`
- 会话持久化包含认证状态
- 重新加载会话时恢复认证信息

#### 线程安全
- `AuthSystem`使用锁保护并发访问
- 文件操作线程安全

### 前端 (JavaScript)

#### 认证流程
1. `checkAuthStatus()` - 检查认证状态
2. `showAuthLogin()` - 显示认证页面
3. `handleAuthLogin()` - 处理登录
4. `handleAuthRegister()` - 处理注册
5. `handleGuestLogin()` - 处理游客登录

#### 管理面板
- `toggleAdminPanel(show)` - 切换管理面板
- `switchAdminTab(tab)` - 切换标签
- `loadAdminUsers()` - 加载用户列表
- `updateUserGroup(username, group)` - 更新用户组
- `loadAdminGroups()` - 加载权限组

## 安全考虑

### 密码安全
- 密码使用SHA256哈希存储
- 不存储明文密码
- 传输时使用HTTPS（生产环境建议）

### 会话安全
- 会话ID使用2048位UUID
- 会话有效期7天
- 自动清理过期会话

### 权限控制
- API中间件自动检查权限
- 权限不足返回403错误
- 管理操作需要管理员权限验证

### 数据保护
- 用户文件名使用SHA256哈希（防止路径遍历）
- 线程安全的文件访问
- 错误信息不暴露内部细节

## 使用示例

### 1. 首次设置

#### 1.1 配置超级管理员
编辑`config.ini`：
```ini
[Admin]
super_admin = admin
```

#### 1.2 注册超级管理员账号
1. 访问应用
2. 点击"注册"标签
3. 输入用户名`admin`和密码
4. 注册成功

#### 1.3 管理员登录
1. 使用`admin`账号登录
2. 进入主界面后看到"管理"按钮

### 2. 用户管理

#### 2.1 查看用户
1. 点击"管理"按钮
2. 默认显示"用户管理"标签
3. 查看所有注册用户

#### 2.2 更改用户权限
1. 在用户列表中找到目标用户
2. 在权限组下拉菜单中选择新的权限组
3. 系统自动保存

### 3. 权限组管理

#### 3.1 查看权限组
1. 在管理面板中点击"权限组管理"标签
2. 查看所有权限组及其权限

#### 3.2 创建自定义权限组（API）
```python
auth_system.create_permission_group(
    'vip',
    {
        'view_notifications': True,
        'mark_notifications_read': True,
        'execute_multi_account': True,
        'use_attendance': True,
        'execute_single_task': True,
        'import_offline': True,
        'export_data': True,
        'modify_params': True,
        'manage_users': False,
        'manage_permissions': False
    },
    'VIP用户'
)
```

## 故障排除

### 无法注册
**症状**：注册时提示"用户名已存在"
**解决**：用户名已被占用，换一个用户名

### 无法登录
**症状**：登录时提示"密码错误"
**解决**：检查密码是否正确，区分大小写

### 游客登录不可用
**症状**：看不到游客登录按钮
**解决**：检查`config.ini`中的`allow_guest_login`设置

### 管理按钮不显示
**症状**：管理员登录后看不到管理按钮
**解决**：
1. 检查用户是否在`admin`或`super_admin`组
2. 刷新页面

### 权限检查失败
**症状**：API返回403权限不足
**解决**：
1. 确认当前用户权限组
2. 检查权限组配置是否正确
3. 联系管理员更改权限组

## 未来扩展

### 短期
- [ ] 添加密码重置功能
- [ ] 添加用户头像
- [ ] 添加登录历史记录

### 中期
- [ ] 使用bcrypt替代SHA256（更安全）
- [ ] 添加双因素认证（2FA）
- [ ] 添加OAuth2登录（第三方）

### 长期
- [ ] 用户组织架构
- [ ] 细粒度权限控制
- [ ] 审计日志系统

## 总结

认证和权限管理系统完整实现了以下功能：

✅ **用户认证** - 注册、登录、游客模式
✅ **权限管理** - 4级权限组，可扩展
✅ **管理面板** - 用户和权限组管理
✅ **API保护** - 自动权限检查
✅ **会话集成** - 认证状态持久化
✅ **线程安全** - 并发访问保护
✅ **安全性** - 密码哈希、会话保护

系统已准备好用于生产环境。
