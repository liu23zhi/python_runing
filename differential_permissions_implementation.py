# Differential Permission System Implementation
# To be integrated into AuthSystem class in main.py

# ========== Differential Permission Storage ==========

def get_effective_permissions(self, username):
    """
    获取用户的有效权限（差分计算）
    Returns: dict of {permission_name: bool}
    """
    user_data = self.get_user(username)
    if not user_data:
        return {}
    
    # 获取基础权限组
    group_name = user_data.get('permission_group', 'guest')
    permissions_data = self.load_permissions()
    
    if group_name not in permissions_data['permission_groups']:
        group_name = 'guest'  # 默认为游客
    
    # 克隆组权限作为基础
    base_permissions = permissions_data['permission_groups'][group_name]['permissions'].copy()
    
    # 应用新增的权限
    added_permissions = user_data.get('added_permissions', [])
    for perm in added_permissions:
        base_permissions[perm] = True
    
    # 移除被删除的权限
    removed_permissions = user_data.get('removed_permissions', [])
    for perm in removed_permissions:
        base_permissions[perm] = False
    
    return base_permissions


def add_user_permission(self, username, permission):
    """
    为用户新增额外权限（差分记录）
    """
    user_data = self.get_user(username)
    if not user_data:
        return False, "用户不存在"
    
    # 初始化差分字段
    if 'added_permissions' not in user_data:
        user_data['added_permissions'] = []
    if 'removed_permissions' not in user_data:
        user_data['removed_permissions'] = []
    
    # 如果该权限在removed列表中，则移除（表示恢复）
    if permission in user_data['removed_permissions']:
        user_data['removed_permissions'].remove(permission)
    # 否则添加到added列表（如果不存在）
    elif permission not in user_data['added_permissions']:
        user_data['added_permissions'].append(permission)
    
    # 保存用户数据
    self.save_user(user_data)
    return True, f"成功为用户 {username} 添加权限: {permission}"


def remove_user_permission(self, username, permission):
    """
    移除用户的某个权限（差分记录）
    """
    user_data = self.get_user(username)
    if not user_data:
        return False, "用户不存在"
    
    # 初始化差分字段
    if 'added_permissions' not in user_data:
        user_data['added_permissions'] = []
    if 'removed_permissions' not in user_data:
        user_data['removed_permissions'] = []
    
    # 如果该权限在added列表中，则移除（表示撤销新增）
    if permission in user_data['added_permissions']:
        user_data['added_permissions'].remove(permission)
    # 否则添加到removed列表（如果不存在）
    elif permission not in user_data['removed_permissions']:
        user_data['removed_permissions'].append(permission)
    
    # 保存用户数据
    self.save_user(user_data)
    return True, f"成功为用户 {username} 移除权限: {permission}"


def migrate_user_to_differential(self, username):
    """
    将旧格式用户数据迁移到差分权限格式
    """
    user_data = self.get_user(username)
    if not user_data:
        return False
    
    # 检查是否已经是差分格式
    if 'permission_group' in user_data and ('added_permissions' in user_data or 'removed_permissions' in user_data):
        return True  # 已经是新格式
    
    # 如果有完整的permissions字段，说明是旧格式
    if 'permissions' in user_data:
        # 确定用户应该属于哪个组（根据权限特征判断）
        user_perms = user_data['permissions']
        
        # 判断逻辑：如果有manage_system权限，则为super_admin
        if user_perms.get('manage_system', False):
            target_group = 'super_admin'
        elif user_perms.get('manage_users', False):
            target_group = 'admin'
        elif user_perms.get('execute_multi_account', False):
            target_group = 'user'
        else:
            target_group = 'guest'
        
        # 获取目标组的基础权限
        permissions_data = self.load_permissions()
        base_permissions = permissions_data['permission_groups'][target_group]['permissions']
        
        # 计算差异
        added_permissions = []
        removed_permissions = []
        
        for perm, value in user_perms.items():
            base_value = base_permissions.get(perm, False)
            if value and not base_value:
                added_permissions.append(perm)
            elif not value and base_value:
                removed_permissions.append(perm)
        
        # 更新用户数据为新格式
        user_data['permission_group'] = target_group
        user_data['added_permissions'] = added_permissions
        user_data['removed_permissions'] = removed_permissions
        del user_data['permissions']  # 删除旧字段
        
        self.save_user(user_data)
        logging.info(f"用户 {username} 已迁移到差分权限格式，所属组: {target_group}")
        return True
    
    return False


# ========== Session Destroyed Notification Enhancement ==========

def notify_session_destroyed(self, username, session_id, reason, device_info=None):
    """
    发送会话销毁通知
    
    Args:
        username: 用户名
        session_id: 会话ID
        reason: 销毁原因 (manual_delete/auto_cleanup/limit_exceeded/expired)
        device_info: 设备信息（可选）
    """
    if not self.config.getboolean('Notifications', 'notify_session_destroyed', fallback=True):
        return
    
    user_data = self.get_user(username)
    if not user_data:
        return
    
    # 获取用户有效权限（差分计算）
    permissions = self.get_effective_permissions(username)
    
    # 构建通知内容
    reason_text = {
        'manual_delete': '手动删除',
        'auto_cleanup': '自动清理（5分钟无活动）',
        'limit_exceeded': '超出会话数量限制',
        'expired': '会话过期'
    }.get(reason, reason)
    
    subject = "会话已销毁通知"
    content = f"""
您好 {username}，

您的一个会话已被销毁：
- 会话ID: {session_id[:8]}...
- 销毁原因: {reason_text}
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    if device_info:
        content += f"- 设备信息: {device_info}\n"
    
    content += "\n如非本人操作，请立即检查账号安全。"
    
    # 发送通知
    notification = {
        'type': 'session_destroyed',
        'username': username,
        'email': user_data.get('email', ''),
        'phone': user_data.get('phone', ''),
        'subject': subject,
        'content': content,
        'use_sms': permissions.get('can_receive_sms_notifications', False)
    }
    
    if hasattr(self, 'notification_service'):
        self.notification_service.send_notification(notification)


# ========== API Routes for Differential Permissions ==========

@app.route('/auth/admin/add_user_permission', methods=['POST'])
def api_add_user_permission():
    """为用户添加额外权限"""
    try:
        data = request.get_json()
        session_id = request.args.get('session_id')
        
        if not session_id or session_id not in web_sessions:
            return jsonify({'error': '无效的会话'}), 401
        
        session_data = web_sessions[session_id]
        auth_username = session_data.get('auth_username')
        
        # 检查权限
        if not auth_system.has_permission(auth_username, 'manage_permissions'):
            return jsonify({'error': '权限不足'}), 403
        
        username = data.get('username')
        permission = data.get('permission')
        
        if not username or not permission:
            return jsonify({'error': '缺少参数'}), 400
        
        success, message = auth_system.add_user_permission(username, permission)
        
        if success:
            # 记录审计日志
            auth_system.audit_log(
                auth_username,
                'add_user_permission',
                f'为用户 {username} 添加权限: {permission}',
                request.remote_addr,
                session_id
            )
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        logging.error(f"添加用户权限失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/auth/admin/remove_user_permission', methods=['POST'])
def api_remove_user_permission():
    """移除用户的某个权限"""
    try:
        data = request.get_json()
        session_id = request.args.get('session_id')
        
        if not session_id or session_id not in web_sessions:
            return jsonify({'error': '无效的会话'}), 401
        
        session_data = web_sessions[session_id]
        auth_username = session_data.get('auth_username')
        
        # 检查权限
        if not auth_system.has_permission(auth_username, 'manage_permissions'):
            return jsonify({'error': '权限不足'}), 403
        
        username = data.get('username')
        permission = data.get('permission')
        
        if not username or not permission:
            return jsonify({'error': '缺少参数'}), 400
        
        success, message = auth_system.remove_user_permission(username, permission)
        
        if success:
            # 记录审计日志
            auth_system.audit_log(
                auth_username,
                'remove_user_permission',
                f'为用户 {username} 移除权限: {permission}',
                request.remote_addr,
                session_id
            )
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        logging.error(f"移除用户权限失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/auth/admin/get_user_effective_permissions', methods=['GET'])
def api_get_user_effective_permissions():
    """获取用户的有效权限（差分计算后）"""
    try:
        session_id = request.args.get('session_id')
        username = request.args.get('username')
        
        if not session_id or session_id not in web_sessions:
            return jsonify({'error': '无效的会话'}), 401
        
        session_data = web_sessions[session_id]
        auth_username = session_data.get('auth_username')
        
        # 检查权限
        if not auth_system.has_permission(auth_username, 'manage_permissions'):
            return jsonify({'error': '权限不足'}), 403
        
        if not username:
            return jsonify({'error': '缺少用户名参数'}), 400
        
        user_data = auth_system.get_user(username)
        if not user_data:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取有效权限
        effective_permissions = auth_system.get_effective_permissions(username)
        
        return jsonify({
            'success': True,
            'username': username,
            'permission_group': user_data.get('permission_group', 'guest'),
            'added_permissions': user_data.get('added_permissions', []),
            'removed_permissions': user_data.get('removed_permissions', []),
            'effective_permissions': effective_permissions
        })
            
    except Exception as e:
        logging.error(f"获取用户有效权限失败: {e}")
        return jsonify({'error': str(e)}), 500
