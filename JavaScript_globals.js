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

    
