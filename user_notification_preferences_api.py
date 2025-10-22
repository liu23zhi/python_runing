#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户通知偏好设置API
User Notification Preferences API

允许用户自主设置是否接收通知，以及通知方式
Allows users to control whether they receive notifications and notification methods
"""

import json
import os
import hashlib
from threading import Lock


# 线程锁
user_files_lock = Lock()


def get_user_notification_preferences(username, system_accounts_dir='school_accounts/system_auth'):
    """
    获取用户的通知偏好设置
    Get user's notification preferences
    
    Args:
        username: 用户名
        system_accounts_dir: 系统账号目录
        
    Returns:
        dict: 通知偏好设置
    """
    # 默认偏好设置
    default_preferences = {
        "enabled": False,  # 默认不通知
        "channels": ["email"],  # 可用渠道: email, sms
        "scenarios": {
            "new_device_login": True,
            "suspicious_login": True,
            "task_complete": False,
            "permission_change": True,
            "session_expiring_60min": False,
            "session_expiring_30min": False,
            "session_expiring_20min": False,
            "session_expiring_10min": False,
            "session_expiring_5min": False,
            "session_destroyed": False
        }
    }
    
    with user_files_lock:
        # 读取用户文件
        filename = hashlib.sha256(username.encode()).hexdigest()
        user_file = os.path.join(system_accounts_dir, f'{filename}.json')
        
        if not os.path.exists(user_file):
            return default_preferences
        
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
        
        # 返回用户的偏好设置，如果不存在则返回默认值
        return user_data.get('notification_preferences', default_preferences)


def update_user_notification_preferences(username, preferences, system_accounts_dir='school_accounts/system_auth'):
    """
    更新用户的通知偏好设置
    Update user's notification preferences
    
    Args:
        username: 用户名
        preferences: 新的偏好设置
        system_accounts_dir: 系统账号目录
        
    Returns:
        bool: 是否成功
    """
    with user_files_lock:
        # 读取用户文件
        filename = hashlib.sha256(username.encode()).hexdigest()
        user_file = os.path.join(system_accounts_dir, f'{filename}.json')
        
        if not os.path.exists(user_file):
            return False
        
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
        
        # 更新偏好设置
        if 'notification_preferences' not in user_data:
            user_data['notification_preferences'] = {}
        
        # 部分更新 - 只更新提供的字段
        if 'enabled' in preferences:
            user_data['notification_preferences']['enabled'] = preferences['enabled']
        
        if 'channels' in preferences:
            user_data['notification_preferences']['channels'] = preferences['channels']
        
        if 'scenarios' in preferences:
            if 'scenarios' not in user_data['notification_preferences']:
                user_data['notification_preferences']['scenarios'] = {}
            # 更新指定的场景设置
            for scenario, enabled in preferences['scenarios'].items():
                user_data['notification_preferences']['scenarios'][scenario] = enabled
        
        # 保存更新后的用户数据
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        
        return True


def check_user_wants_notification(username, scenario, system_accounts_dir='school_accounts/system_auth'):
    """
    检查用户是否希望接收特定场景的通知
    Check if user wants to receive notification for a specific scenario
    
    Args:
        username: 用户名
        scenario: 通知场景 (如: 'new_device_login', 'session_expiring_5min')
        system_accounts_dir: 系统账号目录
        
    Returns:
        tuple: (是否发送通知, 使用的渠道列表)
    """
    preferences = get_user_notification_preferences(username, system_accounts_dir)
    
    # 如果通知总开关是关闭的，不发送任何通知
    if not preferences.get('enabled', False):
        return False, []
    
    # 检查特定场景是否启用
    scenarios = preferences.get('scenarios', {})
    if not scenarios.get(scenario, False):
        return False, []
    
    # 返回启用的渠道
    channels = preferences.get('channels', ['email'])
    return True, channels


# Flask API 路由实现

def api_get_notification_preferences(auth_system, session_id):
    """
    API: 获取当前用户的通知偏好设置
    GET /auth/user/notification_preferences?session_id=xxx
    """
    # 从会话获取用户名
    username = auth_system.get_username_from_session(session_id)
    if not username:
        return {
            'success': False,
            'error': '无效的会话'
        }, 401
    
    preferences = get_user_notification_preferences(
        username, 
        auth_system.system_accounts_dir
    )
    
    return {
        'success': True,
        'preferences': preferences
    }, 200


def api_update_notification_preferences(auth_system, session_id, preferences):
    """
    API: 更新当前用户的通知偏好设置
    POST /auth/user/update_notification_preferences?session_id=xxx
    Body: {
        'enabled': true,
        'channels': ['email', 'sms'],
        'scenarios': {
            'session_expiring_5min': true
        }
    }
    """
    # 从会话获取用户名
    username = auth_system.get_username_from_session(session_id)
    if not username:
        return {
            'success': False,
            'error': '无效的会话'
        }, 401
    
    # 验证输入
    if not isinstance(preferences, dict):
        return {
            'success': False,
            'error': '无效的请求数据'
        }, 400
    
    # 更新偏好设置
    success = update_user_notification_preferences(
        username,
        preferences,
        auth_system.system_accounts_dir
    )
    
    if success:
        return {
            'success': True,
            'message': '通知偏好设置已更新'
        }, 200
    else:
        return {
            'success': False,
            'error': '更新失败'
        }, 500


# 集成到 Flask 应用的示例代码：
"""
from user_notification_preferences_api import (
    api_get_notification_preferences,
    api_update_notification_preferences
)

@app.route('/auth/user/notification_preferences', methods=['GET'])
def get_notification_preferences():
    session_id = request.args.get('session_id')
    return api_get_notification_preferences(auth_system, session_id)

@app.route('/auth/user/update_notification_preferences', methods=['POST'])
def update_notification_preferences():
    session_id = request.args.get('session_id')
    preferences = request.get_json()
    return api_update_notification_preferences(auth_system, session_id, preferences)
"""
