#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
差分权限系统测试脚本

此脚本用于验证 AuthSystem.check_permission 方法的差分授权功能是否正常工作。
它模拟了 main.py 中 check_permission 方法的完整逻辑。
"""

import json
import sys
import os

def load_permissions():
    """加载权限配置文件"""
    permissions_file = 'permissions.json'
    if not os.path.exists(permissions_file):
        print(f"✗ 错误：找不到 {permissions_file} 文件")
        return None
    
    with open(permissions_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_user_group(permissions, auth_username):
    """获取用户所属的权限组"""
    # 检查 user_groups 配置
    user_groups = permissions.get('user_groups', {})
    
    if auth_username in user_groups:
        return user_groups[auth_username]
    
    # 默认返回 user 组
    return 'user'

def check_permission(permissions, auth_username, permission):
    """
    检查用户是否有特定权限（完全模拟 main.py 中的 check_permission 方法）
    
    权限计算顺序：
    1. 获取用户所属权限组的基础权限
    2. 应用用户的自定义权限（added/removed）
    """
    print(f"\n{'='*70}")
    print(f"权限检查: 用户={auth_username}, 权限={permission}")
    print(f"{'='*70}")
    
    # 获取用户组
    group = get_user_group(permissions, auth_username)
    print(f"[步骤1] 用户所属组: {group}")
    
    # 获取组权限（基础权限）
    group_perms = permissions.get('permission_groups', {}).get(group, {}).get('permissions', {})
    has_permission = group_perms.get(permission, False)
    print(f"[步骤2] 组 '{group}' 对权限 '{permission}' 的基础权限: {has_permission}")
    
    # 应用用户的差分化权限
    user_custom = permissions.get('user_custom_permissions', {}).get(auth_username, {})
    added_perms = user_custom.get('added', [])
    removed_perms = user_custom.get('removed', [])
    
    if added_perms or removed_perms:
        print(f"[步骤3] 用户的差分权限配置:")
        print(f"        - 添加的权限: {added_perms}")
        print(f"        - 移除的权限: {removed_perms}")
    else:
        print(f"[步骤3] 用户没有差分权限配置")
    
    # 如果权限在added列表中，则有权限
    if permission in added_perms:
        has_permission = True
        print(f"[步骤4] ✓ 权限 '{permission}' 在 added 列表中")
        print(f"        → 权限状态从 {group_perms.get(permission, False)} 改为 True")
    
    # 如果权限在removed列表中，则无权限
    if permission in removed_perms:
        has_permission = False
        print(f"[步骤5] ✗ 权限 '{permission}' 在 removed 列表中")
        print(f"        → 权限状态改为 False")
    
    print(f"\n{'─'*70}")
    print(f"最终结果: has_permission = {has_permission}")
    print(f"{'─'*70}")
    
    return has_permission

def run_test_suite():
    """运行完整的测试套件"""
    print("\n" + "="*70)
    print("差分权限系统测试套件")
    print("="*70)
    
    # 加载权限配置
    permissions = load_permissions()
    if not permissions:
        return False
    
    print("\n✓ 成功加载 permissions.json")
    
    # 测试用例列表
    test_cases = [
        # (用户名, 权限名, 预期结果, 描述)
        ('zelly', 'use_multi_account_button', True, 
         "用户zelly在user组（无基础权限），通过差分授权获得权限"),
        
        ('zelly', 'view_tasks', True,
         "用户zelly在user组，有基础权限view_tasks"),
        
        ('zelly', 'execute_multi_account', False,
         "用户zelly在user组，没有execute_multi_account权限"),
        
        ('testuser', 'use_multi_account_button', False,
         "用户testuser在user组，没有差分授权，应该没有权限"),
        
        ('testuser', 'view_tasks', True,
         "用户testuser在user组，有基础权限view_tasks"),
        
        ('admin', 'use_multi_account_button', True,
         "管理员admin，通过组权限有use_multi_account_button"),
        
        ('admin', 'execute_multi_account', True,
         "管理员admin，通过组权限有execute_multi_account"),
    ]
    
    # 运行测试
    passed = 0
    failed = 0
    
    for username, permission, expected, description in test_cases:
        result = check_permission(permissions, username, permission)
        
        if result == expected:
            print(f"\n✓✓✓ 测试通过")
            print(f"    {description}")
            passed += 1
        else:
            print(f"\n✗✗✗ 测试失败")
            print(f"    {description}")
            print(f"    预期: {expected}, 实际: {result}")
            failed += 1
    
    # 输出测试总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"总测试数: {len(test_cases)}")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！差分权限系统工作正常！")
        return True
    else:
        print(f"\n⚠ 有 {failed} 个测试失败，请检查权限配置！")
        return False

if __name__ == '__main__':
    success = run_test_suite()
    sys.exit(0 if success else 1)
