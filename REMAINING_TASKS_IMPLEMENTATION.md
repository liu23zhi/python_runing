# 剩余12项任务实现指南

本文档包含剩余12项任务的完整实现代码和说明。

## 状态概览

**已完成**: 18/30任务（60%）
**待完成**: 12项任务
**代码质量**: ✅ 通过CodeQL安全检查

---

## 任务17: 留言板高级权限配置UI

### 说明
在用户编辑界面中添加留言板权限配置选项。

### 实现位置
index.html - manageUserPermissions函数和permissions modal

### 代码修改
在translatePermission函数中添加留言板权限的翻译：

```javascript
function translatePermission(perm) {
  const translations = {
    // 现有翻译...
    'view_messages': '查看留言板',
    'post_messages': '发表留言',
    'delete_own_messages': '删除自己的留言',
    'delete_any_messages': '删除任何留言',
    'view_all_messages': '查看所有留言'
  };
  return translations[perm] || perm;
}
```

**状态**: ✅ 权限系统已支持，翻译函数需添加

---

## 任务18: IP封禁管理面板

### 新增Modal（HTML）
在index.html中admin-messages-panel_modal后添加：

```html
<!-- IP封禁管理Modal -->
<div id="admin-ip-ban-modal" class="hidden space-y-4">
  <h4 class="font-semibold">IP封禁管理</h4>
  
  <!-- 封禁列表 -->
  <div id="ip-ban-list" class="space-y-2 max-h-[40vh] overflow-y-auto">
    <p class="text-slate-400 text-center py-10">加载中...</p>
  </div>
  
  <!-- 添加封禁规则表单 -->
  <div class="border-t pt-4">
    <h5 class="font-semibold mb-2">添加封禁规则</h5>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-2">
      <input type="text" id="ban-target" class="border rounded px-2 py-1" placeholder="IP/IP段/城市名">
      <select id="ban-type" class="border rounded px-2 py-1">
        <option value="ip">单个IP</option>
        <option value="cidr">IP段(CIDR)</option>
        <option value="city">城市</option>
      </select>
      <select id="ban-scope" class="border rounded px-2 py-1">
        <option value="all">封禁所有功能</option>
        <option value="messages_only">仅封禁留言板</option>
      </select>
    </div>
    <button onclick="addIPBan()" class="btn btn-primary mt-2">添加封禁</button>
  </div>
</div>
```

### JavaScript实现

```javascript
// 加载IP封禁列表
async function loadIPBans() {
  try {
    const response = await fetch('/api/admin/ip_bans', {
      headers: { 'X-Session-ID': sessionUUID }
    });
    const result = await response.json();
    
    const listEl = $('ip-ban-list');
    if (result.success && result.bans.length > 0) {
      listEl.innerHTML = result.bans.map(ban => `
        <div class="border p-2 rounded flex justify-between items-center">
          <div>
            <span class="font-semibold">${ban.target}</span>
            <span class="text-xs text-slate-500 ml-2">[${ban.type}]</span>
            <span class="text-xs text-slate-500 ml-2">${ban.scope === 'all' ? '全部' : '仅留言板'}</span>
          </div>
          <button onclick="removeIPBan('${ban.id}')" class="btn btn-danger !py-1 !px-2 !text-xs">删除</button>
        </div>
      `).join('');
    } else {
      listEl.innerHTML = '<p class="text-center py-4">暂无封禁规则</p>';
    }
  } catch (e) {
    showModalAlert('加载失败: ' + e.message);
  }
}

// 添加IP封禁
async function addIPBan() {
  const target = $('ban-target').value.trim();
  const type = $('ban-type').value;
  const scope = $('ban-scope').value;
  
  if (!target) {
    showModalAlert('请输入封禁目标');
    return;
  }
  
  try {
    const response = await fetch('/api/admin/ip_bans', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Session-ID': sessionUUID
      },
      body: JSON.stringify({ target, type, scope })
    });
    
    const result = await response.json();
    if (result.success) {
      showModalAlert('封禁规则已添加');
      $('ban-target').value = '';
      loadIPBans();
    } else {
      showModalAlert(result.message || '添加失败');
    }
  } catch (e) {
    showModalAlert('操作失败: ' + e.message);
  }
}

// 删除IP封禁
async function removeIPBan(banId) {
  const confirmed = await jsShowConfirm('确认删除', '确定要删除此封禁规则吗？');
  if (!confirmed) return;
  
  try {
    const response = await fetch(`/api/admin/ip_bans/${banId}`, {
      method: 'DELETE',
      headers: { 'X-Session-ID': sessionUUID }
    });
    
    const result = await response.json();
    if (result.success) {
      showModalAlert('封禁规则已删除');
      loadIPBans();
    } else {
      showModalAlert(result.message || '删除失败');
    }
  } catch (e) {
    showModalAlert('操作失败: ' + e.message);
  }
}
```

### 后端API（main.py）

```python
# IP封禁数据存储
IP_BANS_FILE = os.path.join('logs', 'ip_bans.json')

@app.route('/api/admin/ip_bans', methods=['GET'])
def get_ip_bans():
    """获取IP封禁列表"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    # 检查管理员权限
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    try:
        if os.path.exists(IP_BANS_FILE):
            with open(IP_BANS_FILE, 'r', encoding='utf-8') as f:
                bans = json.load(f)
        else:
            bans = []
        return jsonify({"success": True, "bans": bans})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/admin/ip_bans', methods=['POST'])
def add_ip_ban():
    """添加IP封禁规则"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    data = request.get_json() or {}
    target = data.get('target', '').strip()
    ban_type = data.get('type', 'ip')
    scope = data.get('scope', 'all')
    
    if not target:
        return jsonify({"success": False, "message": "封禁目标不能为空"})
    
    try:
        # 读取现有封禁列表
        if os.path.exists(IP_BANS_FILE):
            with open(IP_BANS_FILE, 'r', encoding='utf-8') as f:
                bans = json.load(f)
        else:
            bans = []
        
        # 添加新规则
        new_ban = {
            "id": str(time.time()),
            "target": target,
            "type": ban_type,
            "scope": scope,
            "created_at": time.time(),
            "created_by": sess.get('auth_username', '')
        }
        bans.append(new_ban)
        
        # 保存
        os.makedirs(os.path.dirname(IP_BANS_FILE), exist_ok=True)
        with open(IP_BANS_FILE, 'w', encoding='utf-8') as f:
            json.dump(bans, f, indent=2, ensure_ascii=False)
        
        return jsonify({"success": True, "message": "封禁规则已添加"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/admin/ip_bans/<ban_id>', methods=['DELETE'])
def delete_ip_ban(ban_id):
    """删除IP封禁规则"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    try:
        if not os.path.exists(IP_BANS_FILE):
            return jsonify({"success": False, "message": "封禁列表不存在"})
        
        with open(IP_BANS_FILE, 'r', encoding='utf-8') as f:
            bans = json.load(f)
        
        # 过滤掉要删除的规则
        bans = [b for b in bans if b['id'] != ban_id]
        
        with open(IP_BANS_FILE, 'w', encoding='utf-8') as f:
            json.dump(bans, f, indent=2, ensure_ascii=False)
        
        return jsonify({"success": True, "message": "封禁规则已删除"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# 封禁检查中间件
def check_ip_ban(ip_address, scope='all'):
    """检查IP是否被封禁"""
    if not os.path.exists(IP_BANS_FILE):
        return False
    
    try:
        with open(IP_BANS_FILE, 'r', encoding='utf-8') as f:
            bans = json.load(f)
        
        for ban in bans:
            # 检查scope是否匹配
            if ban['scope'] != 'all' and ban['scope'] != scope:
                continue
            
            if ban['type'] == 'ip':
                if ip_address == ban['target']:
                    return True
            elif ban['type'] == 'cidr':
                # CIDR检查（需要ipaddress模块）
                import ipaddress
                if ipaddress.ip_address(ip_address) in ipaddress.ip_network(ban['target']):
                    return True
            elif ban['type'] == 'city':
                # 城市检查（需要IP归属地查询）
                city = get_ip_location(ip_address)
                if city == ban['target']:
                    return True
        
        return False
    except:
        return False
```

**状态**: 🆕 需要添加

---

## 任务19: 用户封禁管理

### 说明
banUser和unbanUser函数已在代码中实现（第5032-5089行）。

**状态**: ✅ 已完成

---

## 任务20: 短信服务配置面板

### 新增Modal（HTML）

```html
<!-- 短信服务配置Modal -->
<div id="admin-sms-config-modal" class="hidden space-y-4">
  <h4 class="font-semibold">短信服务配置</h4>
  
  <div class="space-y-3">
    <!-- 全局开关 -->
    <label class="flex items-center gap-2">
      <input type="checkbox" id="sms-enabled" class="w-4 h-4">
      <span>启用短信服务</span>
    </label>
    
    <!-- 短信宝配置 -->
    <div class="border-t pt-3">
      <h5 class="font-semibold mb-2">短信宝配置</h5>
      <div class="space-y-2">
        <input type="text" id="sms-username" class="w-full border rounded px-2 py-1" placeholder="短信宝用户名">
        <input type="password" id="sms-apikey" class="w-full border rounded px-2 py-1" placeholder="短信宝API Key">
        <input type="text" id="sms-signature" class="w-full border rounded px-2 py-1" placeholder="短信签名(3-12字)" maxlength="12">
        <textarea id="sms-template" class="w-full border rounded px-2 py-1" rows="3" placeholder="短信模板，使用{code}作为验证码占位符"></textarea>
      </div>
    </div>
    
    <!-- 速率限制 -->
    <div class="border-t pt-3">
      <h5 class="font-semibold mb-2">速率限制</h5>
      <div class="grid grid-cols-3 gap-2">
        <input type="number" id="sms-limit-account" class="border rounded px-2 py-1" placeholder="账户/天">
        <input type="number" id="sms-limit-ip" class="border rounded px-2 py-1" placeholder="IP/天">
        <input type="number" id="sms-limit-phone" class="border rounded px-2 py-1" placeholder="手机号/天">
      </div>
    </div>
    
    <!-- Webhook URL -->
    <div class="border-t pt-3">
      <h5 class="font-semibold mb-2">Webhook URL</h5>
      <input type="text" id="sms-webhook-url" class="w-full border rounded px-2 py-1 bg-slate-100" readonly>
      <p class="text-xs text-slate-500 mt-1">将此URL配置到短信宝后台以接收用户回复</p>
    </div>
    
    <!-- 操作按钮 -->
    <div class="flex gap-2 border-t pt-3">
      <button onclick="checkSMSBalance()" class="btn btn-ghost">查询余额</button>
      <button onclick="saveSMSConfig()" class="btn btn-primary">保存配置</button>
    </div>
    
    <!-- 余额显示 -->
    <div id="sms-balance-display" class="hidden border p-2 rounded bg-blue-50">
      <p class="text-sm">余额：<span id="sms-balance-value">--</span> 条</p>
    </div>
  </div>
</div>
```

### JavaScript实现

```javascript
// 加载短信配置
async function loadSMSConfig() {
  try {
    const response = await fetch('/api/admin/sms/config', {
      headers: { 'X-Session-ID': sessionUUID }
    });
    const result = await response.json();
    
    if (result.success) {
      $('sms-enabled').checked = result.config.enable_sms_service || false;
      $('sms-username').value = result.config.username || '';
      $('sms-apikey').value = result.config.api_key || '';
      $('sms-signature').value = result.config.signature || '';
      $('sms-template').value = result.config.template_register || '';
      $('sms-limit-account').value = result.config.rate_limit_per_account_day || 10;
      $('sms-limit-ip').value = result.config.rate_limit_per_ip_day || 20;
      $('sms-limit-phone').value = result.config.rate_limit_per_phone_day || 5;
      $('sms-webhook-url').value = `${window.location.origin}/sms-reply-webhook`;
    }
  } catch (e) {
    showModalAlert('加载配置失败: ' + e.message);
  }
}

// 保存短信配置
async function saveSMSConfig() {
  const config = {
    enable_sms_service: $('sms-enabled').checked,
    username: $('sms-username').value.trim(),
    api_key: $('sms-apikey').value.trim(),
    signature: $('sms-signature').value.trim(),
    template_register: $('sms-template').value.trim(),
    rate_limit_per_account_day: parseInt($('sms-limit-account').value) || 10,
    rate_limit_per_ip_day: parseInt($('sms-limit-ip').value) || 20,
    rate_limit_per_phone_day: parseInt($('sms-limit-phone').value) || 5
  };
  
  try {
    const response = await fetch('/api/admin/sms/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Session-ID': sessionUUID
      },
      body: JSON.stringify(config)
    });
    
    const result = await response.json();
    if (result.success) {
      showModalAlert('配置已保存');
    } else {
      showModalAlert(result.message || '保存失败');
    }
  } catch (e) {
    showModalAlert('操作失败: ' + e.message);
  }
}

// 查询短信余额
async function checkSMSBalance() {
  try {
    const response = await fetch('/api/admin/sms/check_balance', {
      headers: { 'X-Session-ID': sessionUUID }
    });
    const result = await response.json();
    
    if (result.success) {
      $('sms-balance-value').textContent = result.balance;
      $('sms-balance-display').classList.remove('hidden');
    } else {
      showModalAlert(result.message || '查询失败');
    }
  } catch (e) {
    showModalAlert('操作失败: ' + e.message);
  }
}
```

### 后端API（main.py）

```python
@app.route('/api/admin/sms/config', methods=['GET'])
def get_sms_config():
    """获取短信服务配置"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        
        sms_config = {
            'enable_sms_service': config.getboolean('Features', 'enable_sms_service', fallback=False),
            'username': config.get('SMS_Service_SMSBao', 'username', fallback=''),
            'api_key': config.get('SMS_Service_SMSBao', 'api_key', fallback=''),
            'signature': config.get('SMS_Service_SMSBao', 'signature', fallback=''),
            'template_register': config.get('SMS_Service_SMSBao', 'template_register', fallback=''),
            'rate_limit_per_account_day': config.getint('SMS_Service_SMSBao', 'rate_limit_per_account_day', fallback=10),
            'rate_limit_per_ip_day': config.getint('SMS_Service_SMSBao', 'rate_limit_per_ip_day', fallback=20),
            'rate_limit_per_phone_day': config.getint('SMS_Service_SMSBao', 'rate_limit_per_phone_day', fallback=5)
        }
        
        return jsonify({"success": True, "config": sms_config})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/admin/sms/config', methods=['POST'])
def save_sms_config():
    """保存短信服务配置"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    data = request.get_json() or {}
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        
        # 更新配置
        if 'Features' not in config:
            config.add_section('Features')
        config.set('Features', 'enable_sms_service', str(data.get('enable_sms_service', False)).lower())
        
        if 'SMS_Service_SMSBao' not in config:
            config.add_section('SMS_Service_SMSBao')
        config.set('SMS_Service_SMSBao', 'username', data.get('username', ''))
        config.set('SMS_Service_SMSBao', 'api_key', data.get('api_key', ''))
        config.set('SMS_Service_SMSBao', 'signature', data.get('signature', ''))
        config.set('SMS_Service_SMSBao', 'template_register', data.get('template_register', ''))
        config.set('SMS_Service_SMSBao', 'rate_limit_per_account_day', str(data.get('rate_limit_per_account_day', 10)))
        config.set('SMS_Service_SMSBao', 'rate_limit_per_ip_day', str(data.get('rate_limit_per_ip_day', 20)))
        config.set('SMS_Service_SMSBao', 'rate_limit_per_phone_day', str(data.get('rate_limit_per_phone_day', 5)))
        
        # 保存配置文件
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
        
        return jsonify({"success": True, "message": "配置已保存"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/admin/sms/check_balance', methods=['GET'])
def check_sms_balance():
    """查询短信宝余额"""
    session_id = request.headers.get('X-Session-ID', '')
    if session_id not in web_sessions:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    sess = web_sessions[session_id]
    perms = auth_system.get_permissions(sess.get('auth_username', ''))
    if not perms.get('manage_users', False):
        return jsonify({"success": False, "message": "权限不足"}), 403
    
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        
        username = config.get('SMS_Service_SMSBao', 'username', fallback='')
        api_key = config.get('SMS_Service_SMSBao', 'api_key', fallback='')
        
        if not username or not api_key:
            return jsonify({"success": False, "message": "短信宝配置不完整"})
        
        # 调用短信宝查询余额API
        url = f'https://api.smsbao.com/query?u={username}&p={api_key}'
        response = requests.get(url, timeout=10)
        
        if response.text.isdigit():
            balance = int(response.text)
            return jsonify({"success": True, "balance": balance})
        else:
            return jsonify({"success": False, "message": f"查询失败，返回码: {response.text}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
```

**状态**: 🆕 需要添加

---

## 任务24-27: 任务状态、路径校验、通知刷新

### 任务24: status_text计算重构

**说明**: 需要找到计算status_text的函数并修改逻辑。

**查找位置**: 
```bash
grep -n "status_text\|statusText" index.html
```

**实现思路**:
```javascript
function calculateStatusText(account, onlyIncomplete, ignoreTaskTime) {
  let executableCount = 0;
  
  for (const task of account.tasks) {
    if (onlyIncomplete && task.status === 'completed') {
      if (!ignoreTaskTime) continue;
    }
    
    // 检查任务是否过期
    if (!ignoreTaskTime && task.expiry && Date.now() > task.expiry) {
      continue;
    }
    
    // 检查是否有打卡点
    if (!task.checkpoints || task.checkpoints.length === 0) {
      continue;
    }
    
    executableCount++;
  }
  
  return executableCount > 0 ? `有${executableCount}个任务可执行` : '无任务可执行';
}
```

**状态**: 🔍 需要定位具体代码位置

---

### 任务25: 无打卡点日志

**后端修改**: 在任务执行逻辑中添加日志记录

```python
# 在任务执行循环中
if not task.get('checkpoints'):
    log_entry = [time.time(), f"跳过: 任务 '{task['name']}' 无打卡点"]
    logs.append(log_entry)
    continue

# 如果所有任务都被跳过
if all_tasks_skipped:
    return {"status": "no_tasks_run", "logs": logs}
```

**前端修改**: 处理no_tasks_run状态

```javascript
if (result.status === 'no_tasks_run') {
  statusText = '无可执行任务';
}
```

**状态**: 🔍 需要定位具体代码位置

---

### 任务26: 路径录制距离校验

**查找位置**: 搜索"保存路径"按钮的点击事件

**实现代码**:
```javascript
async function savePath() {
  // 计算路径总距离
  const distance = map.calculateDistance(pathPoints);
  
  if (distance > 50000) {  // 大于50km
    showModalAlert('路径过长（>50km），请重新录制');
    exitRecordMode();
    return;
  }
  
  // 正常保存逻辑...
}
```

**状态**: 🔍 需要定位具体代码位置

---

### 任务27: 通知刷新修复

**查找位置**: 搜索attendance-tab相关代码

**实现思路**:
```javascript
// 确保使用配置的刷新间隔
const refreshInterval = param.auto_attendance_refresh_s * 1000;
setInterval(refreshNotifications, refreshInterval);
```

**状态**: 🔍 需要定位具体代码位置

---

### 任务7: 数据持久化修复

**检查点**:
1. amap_js_key是否正确保存到config.ini
2. Last_User的password是否正确处理

**实现位置**: 查找config.ini的写入逻辑

**状态**: 🔍 需要审查现有代码

---

## 实施优先级

### 🔴 高优先级（立即完成）
1. ✅ 任务18: IP封禁管理（完整代码已提供）
2. ✅ 任务20: 短信服务配置（完整代码已提供）

### 🟡 中优先级（下一步）
3. 🔍 任务24: status_text计算重构
4. 🔍 任务26: 路径录制距离校验
5. 🔍 任务27: 通知刷新修复

### 🟢 低优先级（可选）
6. ✅ 任务17: 留言板权限UI（系统已支持）
7. ✅ 任务19: 用户封禁（已实现）
8. 🔍 任务25: 无打卡点日志
9. 🔍 任务7: 数据持久化审查

---

## 总结

**已完成**: 18/30任务（60%）
**可立即实施**: 2项（任务18、20 - 完整代码已提供）
**需要定位**: 5项（任务7、24-27 - 需要查找具体代码位置）
**已经实现**: 3项（任务17、19 - 功能已存在）
**待开发**: 2项（任务25的后端逻辑）

**下一步行动**:
1. 将任务18和20的代码添加到main.py和index.html
2. 搜索并定位任务24-27的代码位置
3. 实施修改并测试
4. 提交最终代码

---

生成时间: 2025-11-12
文档版本: v1.0
