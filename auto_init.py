#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动初始化系统
Auto-initialization system for the application

确保程序在只有main.py和index.html时仍能正常运行
Ensures the program works with only main.py and index.html
"""

import os
import json
import hashlib
from configparser import ConfigParser


def init_system():
    """
    自动初始化系统，创建所有必需的文件和目录
    Auto-initialize system, create all required files and directories
    """
    print("正在初始化系统...")
    
    # 创建必需的目录
    create_directories()
    
    # 创建配置文件
    create_config_ini()
    
    # 创建权限配置文件
    create_permissions_json()
    
    # 创建默认管理员账号
    create_default_admin()
    
    print("系统初始化完成！")


def create_directories():
    """创建必需的目录结构"""
    directories = [
        'logs',
        'logs/audit',
        'school_accounts',
        'school_accounts/system_auth',
        'sessions'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")


def create_config_ini():
    """创建默认的config.ini配置文件"""
    if os.path.exists('config.ini'):
        print("config.ini 已存在，跳过创建")
        return
    
    config = ConfigParser()
    
    # [Admin] 管理员配置
    config['Admin'] = {
        'super_admin': 'admin'
    }
    
    # [Guest] 游客配置
    config['Guest'] = {
        'allow_guest_login': 'true'
    }
    
    # [System] 系统配置
    config['System'] = {
        'session_expiry_days': '7',
        'school_accounts_dir': 'school_accounts',
        'system_accounts_dir': 'school_accounts/system_auth',
        'permissions_file': 'permissions.json'
    }
    
    # [Security] 安全配置
    config['Security'] = {
        'password_storage': 'plaintext',
        'brute_force_protection': 'true',
        'login_log_retention_days': '90'
    }
    
    # [SMS] 短信配置
    config['SMS'] = {
        '# 注意': '短信仅用于注册验证，通知默认使用邮件（短信过于昂贵）',
        'enable_sms': 'false',
        'smsbao_username': '',
        'smsbao_password': '',
        'enable_phone_verification': 'false'
    }
    
    # [Email] 邮件配置
    config['Email'] = {
        'enable_email': 'false',
        'smtp_server': 'smtp.example.com',
        'smtp_port': '587',
        'smtp_username': 'your_email@example.com',
        'smtp_password': 'your_password',
        'from_address': 'noreply@example.com'
    }
    
    # [Notifications] 通知配置
    config['Notifications'] = {
        '# 说明': '用户偏好设置会覆盖这些全局设置',
        'notify_new_device_login': 'true',
        'notify_suspicious_login': 'true',
        'notify_task_complete': 'true',
        'notify_permission_change': 'true',
        'notify_session_expiring_60min': 'true',
        'notify_session_expiring_30min': 'true',
        'notify_session_expiring_20min': 'true',
        'notify_session_expiring_10min': 'true',
        'notify_session_expiring_5min': 'true',
        'notify_session_destroyed': 'true'
    }
    
    # [Monitoring] 监控配置
    config['Monitoring'] = {
        'enable_health_check': 'true',
        'enable_usage_stats': 'true',
        'stats_retention_days': '30'
    }
    
    # [APM] 性能监控配置
    config['APM'] = {
        'enable_sentry': 'false',
        'sentry_dsn': '',
        'enable_prometheus': 'false',
        'prometheus_port': '9090'
    }
    
    # [HotReload] 热更新配置
    config['HotReload'] = {
        'enable_hot_reload': 'true',
        'check_interval': '60'
    }
    
    # [Logging] 日志配置
    config['Logging'] = {
        'enable_log_rotation': 'true',
        'max_log_size_mb': '100',
        'backup_count': '10'
    }
    
    with open('config.ini', 'w', encoding='utf-8') as f:
        config.write(f)
    
    print("创建配置文件: config.ini")


def create_permissions_json():
    """创建默认的permissions.json权限配置文件"""
    if os.path.exists('permissions.json'):
        print("permissions.json 已存在，跳过创建")
        return
    
    permissions = {
        "guest": {
            "view_tasks": True,
            "create_tasks": False,
            "delete_tasks": False,
            "start_tasks": True,
            "stop_tasks": True,
            "view_map": True,
            "record_path": True,
            "auto_generate_path": True,
            "view_notifications": True,
            "mark_notifications_read": False,
            "view_user_details": True,
            "modify_user_settings": False,
            "execute_multi_account": False,
            "use_attendance": False,
            "view_logs": False,
            "clear_logs": False,
            "can_receive_sms_notifications": False
        },
        "user": {
            "view_tasks": True,
            "create_tasks": True,
            "delete_tasks": True,
            "start_tasks": True,
            "stop_tasks": True,
            "view_map": True,
            "record_path": True,
            "auto_generate_path": True,
            "view_notifications": True,
            "mark_notifications_read": True,
            "view_user_details": True,
            "modify_user_settings": True,
            "execute_multi_account": True,
            "use_attendance": True,
            "view_logs": False,
            "clear_logs": False,
            "manage_users": False,
            "manage_permissions": False,
            "reset_user_password": False,
            "view_audit_logs": False,
            "can_receive_sms_notifications": False
        },
        "admin": {
            "view_tasks": True,
            "create_tasks": True,
            "delete_tasks": True,
            "start_tasks": True,
            "stop_tasks": True,
            "view_map": True,
            "record_path": True,
            "auto_generate_path": True,
            "view_notifications": True,
            "mark_notifications_read": True,
            "view_user_details": True,
            "modify_user_settings": True,
            "execute_multi_account": True,
            "use_attendance": True,
            "view_logs": True,
            "clear_logs": True,
            "manage_users": True,
            "manage_permissions": True,
            "reset_user_password": True,
            "view_audit_logs": True,
            "view_all_sessions": True,
            "force_logout_users": True,
            "can_receive_sms_notifications": True
        },
        "super_admin": {
            "view_tasks": True,
            "create_tasks": True,
            "delete_tasks": True,
            "start_tasks": True,
            "stop_tasks": True,
            "view_map": True,
            "record_path": True,
            "auto_generate_path": True,
            "view_notifications": True,
            "mark_notifications_read": True,
            "view_user_details": True,
            "modify_user_settings": True,
            "execute_multi_account": True,
            "use_attendance": True,
            "view_logs": True,
            "clear_logs": True,
            "manage_users": True,
            "manage_permissions": True,
            "reset_user_password": True,
            "view_audit_logs": True,
            "view_all_sessions": True,
            "force_logout_users": True,
            "manage_system": True,
            "create_permission_groups": True,
            "delete_permission_groups": True,
            "can_receive_sms_notifications": True
        },
        "user_groups": {}
    }
    
    with open('permissions.json', 'w', encoding='utf-8') as f:
        json.dump(permissions, f, indent=2, ensure_ascii=False)
    
    print("创建权限配置文件: permissions.json")


def create_default_admin():
    """创建默认的管理员账号"""
    admin_dir = 'school_accounts/system_auth'
    if not os.path.exists(admin_dir):
        os.makedirs(admin_dir)
    
    # 使用用户名的哈希作为文件名
    username = 'admin'
    filename = hashlib.sha256(username.encode()).hexdigest()
    admin_file = os.path.join(admin_dir, f'{filename}.json')
    
    if os.path.exists(admin_file):
        print("默认管理员账号已存在，跳过创建")
        return
    
    admin_data = {
        "username": "admin",
        "password": "admin",
        "phone": "",
        "email": "",
        "permission_group": "super_admin",
        "added_permissions": [],
        "removed_permissions": [],
        "max_sessions": -1,
        "avatar_url": "",
        "theme": "light",
        "created_at": 0,
        "last_login": 0,
        "twofa_enabled": False,
        "twofa_secret": "",
        "notification_preferences": {
            "enabled": False,
            "channels": ["email"],
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
        },
        "user_sessions": []
    }
    
    with open(admin_file, 'w', encoding='utf-8') as f:
        json.dump(admin_data, f, indent=2, ensure_ascii=False)
    
    print("创建默认管理员账号: admin / admin")
    print("警告: 请在首次登录后立即修改默认密码！")


if __name__ == '__main__':
    # 可以独立运行此脚本进行初始化
    init_system()
