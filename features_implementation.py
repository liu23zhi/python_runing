# This file contains all 9 feature implementations to be inserted into main.py
# Features: SMS, Notifications, Password Strength, Health Check, Statistics, Performance Monitoring, APM, Hot Reload, Log Rotation

# ========== Feature 1: SMS Integration (短信宝) ==========
import hashlib
import urllib.parse
import urllib.request

class SMSService:
    """短信宝SMS服务"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://api.smsbao.com"
    
    def send_sms(self, phone, content):
        """发送短信
        Returns: (success: bool, message: str, code: int)
        """
        try:
            # API文档: https://www.smsbao.com/openapi/213.html
            url = f"{self.base_url}/sms"
            params = {
                'u': self.username,
                'p': hashlib.md5(self.password.encode()).hexdigest(),
                'm': phone,
                'c': content
            }
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            response = urllib.request.urlopen(full_url, timeout=10)
            result_code = response.read().decode().strip()
            
            # 状态码解析
            code_messages = {
                '0': ('发送成功', True),
                '30': ('账号或密码错误', False),
                '40': ('账号不存在', False),
                '41': ('余额不足', False),
                '42': ('账号过期', False),
                '43': ('IP地址限制', False),
                '50': ('内容含有敏感词', False),
                '51': ('手机号码不正确', False),
            }
            
            message, success = code_messages.get(result_code, (f'未知错误: {result_code}', False))
            return success, message, int(result_code)
            
        except Exception as e:
            logging.error(f"短信发送失败: {e}")
            return False, str(e), -1

# ========== Feature 2: Enhanced Notification System ==========
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import queue

class NotificationService:
    """通知服务 - 支持邮件和短信"""
    def __init__(self, config):
        self.config = config
        self.notification_queue = queue.Queue()
        self.worker_thread = None
        self.running = False
        
        # SMS service
        if config.getboolean('SMS', 'enable_sms', fallback=False):
            username = config.get('SMS', 'smsbao_username', fallback='')
            password = config.get('SMS', 'smsbao_password', fallback='')
            self.sms_service = SMSService(username, password)
        else:
            self.sms_service = None
    
    def start(self):
        """启动通知工作线程"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._notification_worker, daemon=True)
            self.worker_thread.start()
            logging.info("通知服务已启动")
    
    def stop(self):
        """停止通知工作线程"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def _notification_worker(self):
        """后台工作线程处理通知队列"""
        while self.running:
            try:
                notification = self.notification_queue.get(timeout=1)
                self._send_notification(notification)
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"通知发送失败: {e}")
    
    def _send_notification(self, notification):
        """发送单个通知"""
        ntype = notification.get('type')
        user_info = notification.get('user_info', {})
        data = notification.get('data', {})
        
        # 检查是否启用该通知场景
        scenario_key = f"notify_{ntype}"
        if not self.config.getboolean('Notifications', scenario_key, fallback=True):
            return
        
        # 发送邮件
        if self.config.getboolean('Email', 'enable_email', fallback=False):
            self._send_email(user_info, ntype, data)
        
        # 发送短信（仅当用户有SMS通知权限时）
        # 注意：SMS默认仅用于注册验证，通知需要明确授权
        use_sms = notification.get('use_sms', False)
        if use_sms and self.config.getboolean('SMS', 'enable_sms', fallback=False) and user_info.get('phone'):
            self._send_sms(user_info, ntype, data)
    
    def _send_email(self, user_info, ntype, data):
        """发送邮件通知"""
        try:
            email = user_info.get('email')
            if not email:
                return
            
            smtp_server = self.config.get('Email', 'smtp_server')
            smtp_port = self.config.getint('Email', 'smtp_port')
            smtp_user = self.config.get('Email', 'smtp_username')
            smtp_pass = self.config.get('Email', 'smtp_password')
            from_addr = self.config.get('Email', 'from_address')
            
            # 构建邮件内容
            subject, body = self._build_email_content(ntype, data, user_info.get('username'))
            
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            logging.info(f"邮件通知已发送至 {email}: {subject}")
        except Exception as e:
            logging.error(f"邮件发送失败: {e}")
    
    def _send_sms(self, user_info, ntype, data):
        """发送短信通知"""
        try:
            if not self.sms_service:
                return
            
            phone = user_info.get('phone')
            if not phone:
                return
            
            content = self._build_sms_content(ntype, data, user_info.get('username'))
            success, message, code = self.sms_service.send_sms(phone, content)
            
            if success:
                logging.info(f"短信通知已发送至 {phone}: {content[:20]}...")
            else:
                logging.error(f"短信发送失败 ({code}): {message}")
        except Exception as e:
            logging.error(f"短信发送异常: {e}")
    
    def _build_email_content(self, ntype, data, username):
        """构建邮件内容"""
        templates = {
            'new_device': (
                '新设备登录提醒',
                f'<p>您好 {username}，</p><p>您的账号在新设备上登录：</p>'
                f'<p>IP: {data.get("ip")}<br>设备: {data.get("device")}<br>时间: {data.get("time")}</p>'
                f'<p>如非本人操作，请立即修改密码。</p>'
            ),
            'suspicious_login': (
                '异常登录警告',
                f'<p>您好 {username}，</p><p>检测到异常登录行为：</p>'
                f'<p>IP: {data.get("ip")}<br>位置: {data.get("location")}<br>时间: {data.get("time")}</p>'
                f'<p>如非本人操作，请立即采取安全措施。</p>'
            ),
            'task_complete': (
                '任务完成通知',
                f'<p>您好 {username}，</p><p>您的任务已完成：</p>'
                f'<p>任务: {data.get("task_name")}<br>结果: {data.get("result")}</p>'
            ),
            'permission_change': (
                '权限变更通知',
                f'<p>您好 {username}，</p><p>您的账号权限已变更：</p>'
                f'<p>新权限组: {data.get("new_group")}<br>操作人: {data.get("admin")}</p>'
            ),
            'session_expiring': (
                '会话即将过期',
                f'<p>您好 {username}，</p><p>您的会话即将在1小时后过期。</p>'
                f'<p>请及时保存工作并重新登录。</p>'
            ),
            'session_destroyed': (
                '会话已销毁通知',
                f'<p>您好 {username}，</p><p>您的一个会话已被销毁：</p>'
                f'<p>会话ID: {data.get("session_id")}<br>原因: {data.get("reason")}<br>时间: {data.get("time")}</p>'
                f'<p>如非本人操作，请立即检查账号安全。</p>'
            )
        }
        return templates.get(ntype, ('通知', f'<p>{username}: {data}</p>'))
    
    def _build_sms_content(self, ntype, data, username):
        """构建短信内容（短信有字数限制）"""
        templates = {
            'new_device': f'【安全提醒】{username}您好，账号在新设备登录，IP:{data.get("ip")}，如非本人操作请立即修改密码',
            'suspicious_login': f'【安全警告】{username}检测到异常登录，IP:{data.get("ip")}，位置:{data.get("location")}',
            'task_complete': f'【任务完成】{username}您的任务"{data.get("task_name")}"已完成',
            'permission_change': f'【权限变更】{username}您的权限已变更为{data.get("new_group")}',
            'session_expiring': f'【提醒】{username}您的会话将在1小时后过期，请及时保存工作',
            'session_destroyed': f'【会话销毁】{username}您的会话已销毁，原因:{data.get("reason")}'
        }
        return templates.get(ntype, f'{username}: 系统通知')
    
    def queue_notification(self, ntype, user_info, data):
        """将通知加入队列"""
        notification = {
            'type': ntype,
            'user_info': user_info,
            'data': data,
            'timestamp': time.time()
        }
        self.notification_queue.put(notification)

# ========== Feature 3: Password Strength Indicator ==========
import re

def calculate_password_strength(password):
    """计算密码强度
    Returns: dict with score, level, and feedback
    """
    score = 0
    feedback = []
    
    # 长度
    length = len(password)
    if length < 6:
        feedback.append("密码长度至少6位")
    elif length < 8:
        score += 1
        feedback.append("建议密码长度至少8位")
    elif length < 12:
        score += 2
    else:
        score += 3
    
    # 包含小写字母
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("建议包含小写字母")
    
    # 包含大写字母
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("建议包含大写字母")
    
    # 包含数字
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("建议包含数字")
    
    # 包含特殊字符
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 2
    else:
        feedback.append("建议包含特殊字符")
    
    # 评级
    if score <= 2:
        level = "weak"
        level_text = "弱"
    elif score <= 4:
        level = "medium"
        level_text = "中等"
    elif score <= 6:
        level = "strong"
        level_text = "强"
    else:
        level = "very_strong"
        level_text = "很强"
    
    return {
        'score': score,
        'max_score': 8,
        'level': level,
        'level_text': level_text,
        'feedback': feedback
    }

# ========== Feature 4: System Health Monitoring ==========
import psutil
import platform

class HealthMonitor:
    """系统健康监控"""
    def __init__(self):
        self.start_time = time.time()
    
    def get_health_status(self):
        """获取系统健康状态"""
        try:
            # 基本状态
            uptime = time.time() - self.start_time
            
            # 磁盘空间
            disk = psutil.disk_usage('/')
            disk_free_gb = disk.free / (1024**3)
            disk_percent = disk.percent
            
            # 内存使用
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            
            # 会话数量
            session_count = len(web_sessions)
            
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # 判断状态
            status = "healthy"
            issues = []
            
            if disk_percent > 90:
                status = "warning"
                issues.append(f"磁盘空间不足: {disk_percent}%已使用")
            
            if memory_percent > 90:
                status = "warning"
                issues.append(f"内存使用过高: {memory_percent}%")
            
            if session_count > 1000:
                status = "warning"
                issues.append(f"会话数量过多: {session_count}")
            
            return {
                'status': status,
                'timestamp': datetime.datetime.now().isoformat(),
                'uptime_seconds': int(uptime),
                'uptime_text': self._format_uptime(uptime),
                'system': {
                    'platform': platform.system(),
                    'python_version': platform.python_version(),
                },
                'resources': {
                    'disk_free_gb': round(disk_free_gb, 2),
                    'disk_used_percent': disk_percent,
                    'memory_available_gb': round(memory_available_gb, 2),
                    'memory_used_percent': memory_percent,
                    'cpu_percent': cpu_percent,
                },
                'application': {
                    'active_sessions': session_count,
                    'total_users': len(auth_system.users) if auth_system else 0,
                },
                'issues': issues
            }
        except Exception as e:
            logging.error(f"健康检查失败: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.datetime.now().isoformat()
            }
    
    def _format_uptime(self, seconds):
        """格式化运行时间"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{days}天{hours}小时{minutes}分钟"

# ========== Feature 5 & 6: Usage Statistics & Performance Monitoring ==========
class UsageStatistics:
    """使用统计和性能监控"""
    def __init__(self):
        self.daily_active_users = {}  # date -> set of usernames
        self.session_durations = []  # list of durations in seconds
        self.feature_usage = {}  # feature_name -> count
        self.request_times = {}  # endpoint -> list of response times
        self.error_counts = {}  # endpoint -> error count
        self.request_counts = {}  # endpoint -> request count
        self.lock = threading.Lock()
    
    def record_active_user(self, username):
        """记录活跃用户"""
        today = datetime.date.today().isoformat()
        with self.lock:
            if today not in self.daily_active_users:
                self.daily_active_users[today] = set()
            self.daily_active_users[today].add(username)
            
            # 只保留最近30天
            cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
            self.daily_active_users = {k: v for k, v in self.daily_active_users.items() if k >= cutoff}
    
    def record_session_duration(self, duration):
        """记录会话时长"""
        with self.lock:
            self.session_durations.append(duration)
            # 只保留最近1000条
            if len(self.session_durations) > 1000:
                self.session_durations = self.session_durations[-1000:]
    
    def record_feature_usage(self, feature_name):
        """记录功能使用"""
        with self.lock:
            self.feature_usage[feature_name] = self.feature_usage.get(feature_name, 0) + 1
    
    def record_request(self, endpoint, response_time, is_error=False):
        """记录请求性能"""
        with self.lock:
            # 响应时间
            if endpoint not in self.request_times:
                self.request_times[endpoint] = []
            self.request_times[endpoint].append(response_time)
            # 只保留最近100条
            if len(self.request_times[endpoint]) > 100:
                self.request_times[endpoint] = self.request_times[endpoint][-100:]
            
            # 请求计数
            self.request_counts[endpoint] = self.request_counts.get(endpoint, 0) + 1
            
            # 错误计数
            if is_error:
                self.error_counts[endpoint] = self.error_counts.get(endpoint, 0) + 1
    
    def get_statistics(self):
        """获取统计数据"""
        with self.lock:
            # DAU
            today = datetime.date.today().isoformat()
            dau = len(self.daily_active_users.get(today, set()))
            
            # 平均会话时长
            avg_session_duration = (
                sum(self.session_durations) / len(self.session_durations) 
                if self.session_durations else 0
            )
            
            # 性能指标
            performance = {}
            for endpoint, times in self.request_times.items():
                if times:
                    performance[endpoint] = {
                        'avg_response_time_ms': round(sum(times) / len(times), 2),
                        'min_response_time_ms': round(min(times), 2),
                        'max_response_time_ms': round(max(times), 2),
                        'request_count': self.request_counts.get(endpoint, 0),
                        'error_count': self.error_counts.get(endpoint, 0),
                        'error_rate': round(
                            self.error_counts.get(endpoint, 0) / self.request_counts.get(endpoint, 1) * 100, 
                            2
                        )
                    }
            
            return {
                'daily_active_users': dau,
                'avg_session_duration_minutes': round(avg_session_duration / 60, 2),
                'feature_usage': dict(sorted(
                    self.feature_usage.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:20]),  # Top 20
                'performance': performance,
                'timestamp': datetime.datetime.now().isoformat()
            }

# ========== Feature 7: APM Integration ==========
# Sentry integration (optional)
try:
    import sentry_sdk
    sentry_available = True
except ImportError:
    sentry_available = False

# Prometheus integration (optional)
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    prometheus_available = True
except ImportError:
    prometheus_available = False

class APMIntegration:
    """APM工具集成"""
    def __init__(self, config):
        self.config = config
        self.sentry_enabled = False
        self.prometheus_enabled = False
        
        # Sentry
        if sentry_available and config.getboolean('APM', 'enable_sentry', fallback=False):
            dsn = config.get('APM', 'sentry_dsn', fallback='')
            if dsn:
                try:
                    sentry_sdk.init(dsn=dsn, traces_sample_rate=1.0)
                    self.sentry_enabled = True
                    logging.info("Sentry错误跟踪已启用")
                except Exception as e:
                    logging.error(f"Sentry初始化失败: {e}")
        
        # Prometheus
        if prometheus_available and config.getboolean('APM', 'enable_prometheus', fallback=False):
            self.prometheus_enabled = True
            self._setup_prometheus_metrics()
            logging.info("Prometheus指标收集已启用")
    
    def _setup_prometheus_metrics(self):
        """设置Prometheus指标"""
        self.request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
        self.request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['endpoint'])
        self.active_sessions = Gauge('active_sessions', 'Number of active sessions')
        self.error_count = Counter('errors_total', 'Total errors', ['type'])
    
    def record_request(self, method, endpoint, duration):
        """记录请求（Prometheus）"""
        if self.prometheus_enabled:
            self.request_count.labels(method=method, endpoint=endpoint).inc()
            self.request_duration.labels(endpoint=endpoint).observe(duration)
    
    def record_error(self, error_type):
        """记录错误（Prometheus）"""
        if self.prometheus_enabled:
            self.error_count.labels(type=error_type).inc()
    
    def update_session_count(self, count):
        """更新会话数量（Prometheus）"""
        if self.prometheus_enabled:
            self.active_sessions.set(count)
    
    def get_prometheus_metrics(self):
        """获取Prometheus指标"""
        if self.prometheus_enabled:
            return generate_latest()
        return b''

# ========== Feature 8: Configuration Hot Reload ==========
class ConfigHotReload:
    """配置热更新"""
    def __init__(self, config_file, callback):
        self.config_file = config_file
        self.callback = callback
        self.last_mtime = os.path.getmtime(config_file) if os.path.exists(config_file) else 0
        self.running = False
        self.thread = None
        self.check_interval = 60  # seconds
    
    def start(self):
        """启动监控线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            logging.info(f"配置热更新已启动，检查间隔: {self.check_interval}秒")
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                if os.path.exists(self.config_file):
                    current_mtime = os.path.getmtime(self.config_file)
                    if current_mtime > self.last_mtime:
                        logging.info(f"检测到配置文件变更: {self.config_file}")
                        self.last_mtime = current_mtime
                        self.callback()
            except Exception as e:
                logging.error(f"配置文件监控错误: {e}")
            
            time.sleep(self.check_interval)

# ========== Feature 9: Log Rotation ==========
from logging.handlers import RotatingFileHandler

def setup_log_rotation(config):
    """设置日志轮转"""
    if not config.getboolean('Logging', 'enable_log_rotation', fallback=True):
        return
    
    max_bytes = config.getint('Logging', 'max_log_size_mb', fallback=100) * 1024 * 1024
    backup_count = config.getint('Logging', 'backup_count', fallback=10)
    
    # 获取root logger
    root_logger = logging.getLogger()
    
    # 移除现有的文件处理器
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)
    
    # 添加轮转处理器
    log_file = os.path.join(LOGIN_LOGS_DIR, 'application.log')
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    rotating_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(rotating_handler)
    
    logging.info(f"日志轮转已启用: 最大{max_bytes/(1024*1024)}MB, 保留{backup_count}个备份")

