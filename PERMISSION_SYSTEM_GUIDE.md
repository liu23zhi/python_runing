# 权限系统差分授权说明文档

## 问题描述

用户 `zelly` 属于 `user` 用户组，但通过差分授权（`user_custom_permissions`）已获得 `use_multi_account_button` 权限。然而，`/auth/check_permission` API 仍然返回没有权限。

## 问题根源

经过详细代码审查，**权限系统代码本身没有问题**！`check_permission` 方法和 `/auth/check_permission` API 端点已经完全支持 `user_custom_permissions` 差分授权。

可能的问题原因：

### 1. permissions.json 配置格式错误

请检查 `permissions.json` 文件中的 `user_custom_permissions` 配置格式是否正确：

```json
{
  "permission_groups": {
    "user": {
      "name": "普通用户",
      "permissions": {
        "use_multi_account_button": false
      }
    }
  },
  "user_groups": {
    "zelly": "user"
  },
  "user_custom_permissions": {
    "zelly": {
      "added": ["use_multi_account_button"],
      "removed": []
    }
  }
}
```

**关键点**：
- `user_custom_permissions` 必须在 `permissions.json` 文件的根级别
- 用户名（如 `"zelly"`）必须完全匹配（区分大小写）
- `added` 是一个字符串数组，包含要授予的权限名称
- `removed` 是一个字符串数组，包含要撤销的权限名称

### 2. 权限名称不匹配

请确认权限名称完全一致：
- 前端检查的权限：`use_multi_account_button`
- 后端定义的权限：也必须是 `use_multi_account_button`（完全相同，包括大小写）

### 3. 用户名不匹配

请确认：
- `auth_username`（用户登录的用户名）与 `permissions.json` 中的用户名完全一致
- 检查是否有多余的空格或特殊字符

## 权限检查流程（已正确实现）

`check_permission` 方法的执行顺序：

```python
def check_permission(self, auth_username, permission):
    # 1. 获取用户所属的权限组
    group = self.get_user_group(auth_username)  # 例如: "user"
    
    # 2. 获取该组的基础权限
    group_perms = self.permissions['permission_groups'][group]['permissions']
    has_permission = group_perms.get(permission, False)  # 例如: False
    
    # 3. 读取用户的差分权限配置
    user_custom = self.permissions.get('user_custom_permissions', {}).get(auth_username, {})
    added_perms = user_custom.get('added', [])  # 例如: ["use_multi_account_button"]
    removed_perms = user_custom.get('removed', [])  # 例如: []
    
    # 4. 应用差分授权：添加的权限
    if permission in added_perms:
        has_permission = True  # ✓ 这里会将 False 改为 True
    
    # 5. 应用差分授权：移除的权限
    if permission in removed_perms:
        has_permission = False
    
    # 6. 返回最终结果
    return has_permission  # 返回 True（用户zelly获得权限）
```

## 调试方法

### 1. 检查日志

代码中已添加详细的调试日志。启动服务器后，检查 `logs/zx-slm-tool.log` 文件中的权限检查日志：

```
[权限检查] 用户 zelly 的组 user 对权限 use_multi_account_button 的基础权限: False
[权限检查] 用户 zelly 的自定义权限 - 添加: ['use_multi_account_button'], 移除: []
[权限检查] 用户 zelly 通过 user_custom_permissions.added 获得权限 use_multi_account_button
[权限检查] 最终结果 - 用户 zelly 对权限 use_multi_account_button: True
```

### 2. 测试 API

使用以下命令测试权限检查 API：

```bash
curl -X POST http://localhost:5000/auth/check_permission \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: <你的session_id>" \
  -d '{"permission": "use_multi_account_button"}'
```

期望返回：
```json
{
  "success": true,
  "has_permission": true
}
```

### 3. 验证 permissions.json

运行以下 Python 脚本验证配置文件：

```python
import json

# 读取配置
with open('permissions.json', 'r', encoding='utf-8') as f:
    perms = json.load(f)

# 检查用户 zelly 的配置
username = 'zelly'
permission = 'use_multi_account_button'

# 1. 检查用户组
user_group = perms.get('user_groups', {}).get(username)
print(f"用户 {username} 的组: {user_group}")

# 2. 检查组基础权限
if user_group:
    group_perm = perms.get('permission_groups', {}).get(user_group, {}).get('permissions', {}).get(permission, False)
    print(f"组 {user_group} 对权限 {permission} 的基础权限: {group_perm}")

# 3. 检查差分授权
user_custom = perms.get('user_custom_permissions', {}).get(username, {})
added = user_custom.get('added', [])
removed = user_custom.get('removed', [])

print(f"用户 {username} 的自定义权限:")
print(f"  - 添加: {added}")
print(f"  - 移除: {removed}")

# 4. 模拟权限检查
has_perm = group_perm if user_group else False
if permission in added:
    has_perm = True
if permission in removed:
    has_perm = False

print(f"\n最终权限检查结果: {has_perm}")
```

## 代码修改说明

本次修改在原有正确的权限系统基础上，添加了：

1. **详细的注释和文档**：在 `check_permission` 方法中添加了完整的差分授权说明
2. **调试日志**：添加了 `logging.debug` 语句，记录每个权限检查步骤
3. **API 端点文档**：在 `/auth/check_permission` 的 docstring 中添加了差分授权的详细说明和示例

## 结论

权限系统代码已经完全支持 `user_custom_permissions` 差分授权，无需修改核心逻辑。如果遇到权限检查失败的问题，请：

1. 检查 `permissions.json` 文件格式是否正确
2. 确认用户名和权限名是否完全匹配（区分大小写）
3. 查看日志文件中的详细调试信息
4. 使用上述测试方法验证配置

如果问题仍然存在，请提供：
- `permissions.json` 文件内容
- 相关的日志输出
- API 调用的完整请求和响应

这将有助于进一步诊断问题。
