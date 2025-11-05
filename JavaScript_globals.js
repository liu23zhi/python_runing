// ==============================================================================
// 跑步助手 - JavaScript 全局变量 (优先加载)
// ==============================================================================
// 
// 文件说明：
//   本文件包含所有 JavaScript 全局变量的声明
//   必须在其他 JavaScript 代码之前加载，以避免变量未定义错误
//
// 加载顺序：
//   1. JavaScript_globals.js (本文件 - 全局变量)
//   2. JavaScript.js (主要功能代码)
//
// 为什么需要独立文件：
//   由于使用动态加载，如果全局变量和函数代码一起加载，
//   可能导致某些函数在执行时全局变量尚未初始化
//   将全局变量独立出来并优先加载可以避免此问题
//
// ==============================================================================

// 配置TailwindCSS
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: { 'sans': ['Noto Sans SC', 'system-ui', 'sans-serif'], 'display': ['Zilla Slab', 'serif'] },
          colors: { 'base': '#7dd3fc' }
        }
      }
    }

    // ==============================================================================
    // JavaScript代码部分
    // ==============================================================================

    // 全局变量

    let refreshUserListInterval = null;
    let isInNetworkErrorState = false; // 跟踪网络错误状态
    let cdnErrorCount = 0;
    let cdnErrorTimer = null;
    let appInitialized = false;

    let currentUserIsGuest = false;
    let currentAuthUsername = null; // 存储当前系统认证的用户名
    let healthAutoRefreshInterval = null; // 系统健康状态自动刷新定时器
    let avatarCropper = null; // 头像裁剪器实例
    let currentLogPage = 1; // 用于日志分页的当前页码
    let croppedAvatarFile = null; // 裁剪后的头像文件

    // 会话管理相关变量
    let currentSessionInfo = {
      maxSessions: 1,
      currentCount: 0
    };


    let AMAP_API_KEY = ""; // 全局API Key变量
    let isRefreshingNotifications = false; // 通知刷新的“in-flight”标志

    let isRefreshingTasks = false;


    // 离线模式标志
    let IS_OFFLINE = false;
    let sessionUUID = null;  // 当前会话UUID
    

    // 单账号模式：GPS点进度计数
    let singleProcessedPoints = 0;       // 已处理/已上报的点数
    let singleTotalPoints = 0;           // 当前任务总点数（run_coords长度）


    // 统一的 AMap 单例与加载控制
    let AMapInstance, map;
    let amapLoadingPromise = null;   // 保证只触发一次加载
    let AMapReady = false;           // 高德地图SDK是否已加载就绪

    let currentTasks = [];
    let selectedTaskIndex = -1;
    let currentUserData = {};
    let currentRunData = {};
    let polylines = { recommended: [], draft: null, run: null, history: null };
    let markers = [];
    let runnerMarker = null;
    let drawingInfoMarker = null;
    let tempAttendanceMarker = null;
    let tempAttendanceCircle = null;
    let isDrawing = false;
    let isPathDrawing = false;
    let leftMouseDown = false;
    const $ = (id) => document.getElementById(id);

    let multiAccountMap;
    let multiAccountMarkers = {}; // {username: AMap.Marker}
    const userColors = ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107', '#FF9800', '#FF5722'];
    let colorIndex = 0;
    let path_planning_queue = [];
    let is_planning_path = false;

    let currentSessionUA = ""

    let pendingMultiPositions = []; // [{ username, lon, lat, name }]

    // -- 地图初始化Promise，用于确保地图完全加载后再执行绘图操作 --
    let mapReadyPromise = null;
    let resolveMapReady = null;

    // 参数定义（详细版：标签、单位、帮助）
    const paramDefs = {
      // 采样与速度
      "interval_ms": {
        label: "采样间隔",
        unit: "ms",
        help: "相邻 GPS 点之间的时间间隔，用于模拟上报节奏。"
      },
      "interval_random_ms": {
        label: "间隔随机范围",
        unit: "ms",
        help: "在采样间隔的基础上上下浮动的随机抖动幅度。"
      },
      "speed_mps": {
        label: "平均速度",
        unit: "m/s",
        help: "生成/处理路径时的目标平均速度。"
      },
      "speed_random_mps": {
        label: "速度随机范围",
        unit: "m/s",
        help: "速度的上下浮动范围，用于模拟自然波动。"
      },
      "location_random_m": {
        label: "定位随机偏移半径",

        unit: "m",
        help: "对每个 GPS 点施加的随机偏移的半径，模拟定位噪声。"
      },

      // 任务间隔
      "task_gap_min_s": {
        label: "任务间隙下限",
        unit: "s",
        help: "连续执行任务之间的最短等待时间。"
      },
      "task_gap_max_s": {
        label: "任务间隙上限",
        unit: "s",
        help: "连续执行任务之间的最长等待时间。"
      },

      // 路径规划API失败时的重试策略配置
      "api_fallback_line": {
        label: "规划失败时使用直线连接",
        unit: "",
        help: "启用后，当某段步行路径规划失败时，使用起终点直线代替。"
      },
      "api_retries": {
        label: "API重试次数",
        unit: "次",
        help: "步行路径每一段失败后的重试次数。"
      },

      "api_retry_delay_s": {
        label: "API重试间隔",
        unit: "s",
        help: "步行路径失败后发起下一次重试前的等待时间。"
      },
      "ignore_task_time": {
        label: "忽略任务时间仅对比日期",
        unit: "",
        help: "勾选后，判断任务是否“未开始”或“已过期”时，只对比年月日，忽略具体时分秒。"
      },

      // 自动生成路径目标
      "min_time_m": {
        label: "目标时长下限",
        unit: "分钟",
        help: "自动生成路径的总时长最小值。"
      },
      "max_time_m": {
        label: "目标时长上限",
        unit: "分钟",
        help: "自动生成路径的总时长最大值。"
      },
      "min_dist_m": {
        label: "目标距离下限",
        unit: "m",
        help: "自动生成路径的总距离下限。上限按 1.0–1.15 倍随机浮动。"
      },

      // 主题
      "theme_style": {
        label: "界面主题风格",
        unit: "",
        help: "切换应用界面的外观。主题切换后将自动保存。",
        type: "theme_selector" // 自定义类型，用于生成主题按钮
      },
      "theme_base_color": {
        label: "主题基础颜色",
        unit: "",
        help: "界面主色调（点击颜色块进行选择）。",
        type: "color_picker" // 自定义类型，用于生成颜色选择器
      },
      "auto_attendance_enabled": {
        label: "开启自动签到",
        unit: "",
        help: "开启后，将在后台自动刷新通知并尝试签到",
        type: "checkbox"
      },
      "auto_attendance_refresh_s": {
        label: "刷新间隔",
        unit: "秒",
        help: "自动刷新通知的间隔时间（秒），建议不低于60"
      },
      "attendance_user_radius_m": {
        label: "随机半径",
        unit: "米",
        help: "自动签到时，在服务器允许范围内的最大随机偏移半径。设为0为精确签到。"
      }
    };

    // 参数分组定义
    const paramGroups = [
      {
        title: "采样与速度",
        keys: ["interval_ms", "interval_random_ms", "speed_mps", "speed_random_mps", "location_random_m"]
      },
      {
        title: "任务间隔",
        keys: ["task_gap_min_s", "task_gap_max_s", "ignore_task_time"]
      },
      {
        title: "路径规划重试策略",
        keys: ["api_fallback_line", "api_retries", "api_retry_delay_s"]
      },
      {
        title: "自动生成目标",
        keys: ["min_time_m", "max_time_m", "min_dist_m"]
      },
      {
        title: "主题与外观",
        keys: ["theme_style", "theme_base_color"]
      },
      {
        title: "自动签到",
        keys: ["auto_attendance_enabled", "auto_attendance_refresh_s", "attendance_user_radius_m"]
      }
    ];

    let pythonParams = {};

    let runAccumulatedMs = 0;
    let draftTotalDist = 0;
    
  

    // ====================
    // 管理面板功能
    // ====================

    // 权限中英文翻译映射
    const permissionTranslations = {
      // 基础权限
      'view_dashboard': '查看仪表板',
      'view_tasks': '查看任务',
      'execute_tasks': '执行任务',
      'view_history': '查看历史记录',

      // 用户管理
      'manage_users': '管理用户',
      'create_users': '创建用户',
      'delete_users': '删除用户',
      'ban_users': '封禁用户',
      'view_users': '查看用户',

      // 权限管理
      'manage_permissions': '管理权限',
      'manage_groups': '管理权限组',
      'assign_permissions': '分配权限',

      // 会话管理
      'manage_sessions': '管理会话',
      'view_all_sessions': '查看所有会话',
      'delete_sessions': '删除会话',
      'god_mode': '上帝模式',

      // 系统管理
      'view_logs': '查看日志',
      'system_settings': '系统设置',
      'manage_api': '管理API',

      // 任务相关
      'create_tasks': '创建任务',
      'modify_tasks': '修改任务',
      'delete_tasks': '删除任务',
      'schedule_tasks': '定时任务',

      // 数据权限
      'export_data': '导出数据',
      'import_data': '导入数据',
      'backup_data': '备份数据',

      // 通知权限
      'send_notifications': '发送通知',
      'manage_notifications': '管理通知',

      // 其他
      'admin_panel': '管理面板',
      'debug_mode': '调试模式'
    };

    
    let currentEditGroupKey = null;
    let currentManageUsername = null;

    
    let socket = null; // 全局 socket 变量

    
      // DOM文档已完成加载，直接执行初始化流程
      // [BUG修复] initializeApp() 已移至 index.html 的 mainScript.onload 中，
      // 因为 initializeApp() 定义在 JavaScript.js (mainScript) 中，
      // 必须等待 mainScript 加载完成后才能调用。
    


    