# 跑步助手
# 这是一个基于Flask的Web应用，用于模拟跑步任务的执行


from __future__ import annotations

_import_failures = []  # 导入失败列表，用于收集所有导入失败的信息
_log_buffer = []  # 日志缓冲区，用于存储初始化前的日志


def _buffer_log(level, message):
    """
    暂存日志到缓冲区，同时打印到控制台。
    level: 'INFO', 'WARNING', 'ERROR' 等
    """
    print(message)  # 保证控制台依然能看到
    _log_buffer.append((level, message))  # 存入缓冲区


def _try_import_builtin(module_name, display_name=None, use_print=False):
    """
    尝试导入内置模块，失败时记录但不立即退出。
    """
    if display_name is None:
        display_name = module_name

    try:
        module = __import__(module_name)
        # [修改] 使用缓冲日志函数
        _buffer_log("INFO", f"[导入检查] ✓ {display_name} 导入成功")
        return module
    except ImportError as e:
        # error_msg = f"内置模块 '{display_name}' 导入失败: {e}"
        _import_failures.append(
            {"module": display_name, "type": "builtin", "error": str(e)}
        )
        # [修改] 使用缓冲日志函数
        _buffer_log("ERROR", f"[导入检查] ✗ {display_name} 导入失败: {e}")
        return None


_buffer_log("INFO", "[导入检查] 开始导入Python内置模块...")
logging = _try_import_builtin("logging", None, True)
sys = _try_import_builtin("sys")
os = _try_import_builtin("os")
re = _try_import_builtin("re")
time = _try_import_builtin("time")
threading = _try_import_builtin("threading")
hashlib = _try_import_builtin("hashlib")
json = _try_import_builtin("json")
configparser = _try_import_builtin("configparser")
datetime = _try_import_builtin("datetime")
traceback = _try_import_builtin("traceback")
zipfile = _try_import_builtin("zipfile")
random = _try_import_builtin("random")
argparse = _try_import_builtin("argparse")
gc = _try_import_builtin("gc")  # 垃圾回收模块，用于内存优化
heapq = _try_import_builtin("heapq")  # 堆队列模块，用于高效排序

if _import_failures:
    _buffer_log("ERROR", f"\n{'='*70}")
    _buffer_log("ERROR", f"[致命错误] 内置模块导入失败")
    _buffer_log("ERROR", f"{'='*70}")
    _buffer_log("ERROR", f"\n检测到 {len(_import_failures)} 个内置模块导入失败：\n")
    for i, failure in enumerate(_import_failures, 1):
        _buffer_log("ERROR", f"  {i}. {failure['module']}")
        _buffer_log("ERROR", f"     错误: {failure['error']}\n")
    _buffer_log("ERROR", "这通常表示您的 Python 环境已损坏。")
    _buffer_log("ERROR", "建议重新安装 Python 或修复当前安装。")
    _buffer_log(f"{'='*70}\n")
    # 清理内存
    _import_failures.clear()
    if sys:
        sys.exit(1)
    else:
        exit(1)

_buffer_log("INFO", "[导入检查] ✓ 所有内置模块导入成功\n")
# 清理导入失败列表，释放内存
_import_failures.clear()

# 配置UTF-8编码（用于日志和控制台输出）
if sys and sys.platform.startswith("win"):
    # Windows系统特殊处理
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        # Python 3.6及更早版本不支持reconfigure
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


def import_standard_libraries():
    """
    逐步导入所有必需的标准库。
    """
    logging.info("=" * 80)
    logging.info("开始检查并导入 Python 标准库...")
    logging.info("[依赖检查] 正在导入 Python 标准库...")

    # (模块名, 导入命令)
    std_libs = [
        ("ssl", "import ssl"),
        ("eventlet", "import eventlet"),
        ("eventlet.wsgi", "import eventlet.wsgi"),
        ("argparse", "import argparse"),
        ("base64", "import base64"),
        ("bisect", "import bisect"),
        ("collections", "import collections"),
        ("configparser", "import configparser"),
        ("copy", "import copy"),
        ("csv", "import csv"),
        ("datetime", "import datetime"),
        ("hashlib", "import hashlib"),
        ("json", "import json"),
        ("math", "import math"),
        ("pickle", "import pickle"),
        ("queue", "import queue"),
        ("random", "import random"),
        ("re", "import re"),
        ("secrets", "import secrets"),
        ("socket", "import socket"),
        ("threading", "import threading"),
        ("time", "import time"),
        ("traceback", "import traceback"),
        ("urllib", "import urllib.parse"),  # urllib 是一个包, 导入其子模块
        ("uuid", "import uuid"),
        ("warnings", "import warnings"),
        ("atexit", "import atexit"),
        ("io", "import io"),
        ("zipfile", "import zipfile"),
        ("functools", "import functools"),
        ("ipaddress", "import ipaddress"),
        ("string", "import string"),
    ]

    failed_imports = []

    # 逐个尝试导入，收集所有失败的模块
    for name, import_cmd in std_libs:
        try:
            logging.info(f"  -> 正在导入 {name}...")
            logging.info(f"[依赖检查]   -> {name}...")
            exec(import_cmd, globals())
            logging.info(f"  ✓ {name} 导入成功")
            logging.info("✓")
        except ImportError as e:
            logging.error(f"  ✗ {name} 导入失败: {e}")
            logging.error(f"✗ ({e})")
            failed_imports.append({"name": name, "error": str(e)})

    # 特殊处理 fcntl (仅限非 Windows 平台)
    if sys.platform != "win32":
        try:
            logging.info("  -> 正在导入 fcntl (非Windows)...")
            logging.info("[依赖检查]   -> fcntl (非Windows)...")
            import fcntl

            globals()["fcntl"] = fcntl
            logging.info("  ✓ fcntl 导入成功")
            logging.info("✓")
        except ImportError as e:
            logging.error(f"  ✗ fcntl 导入失败: {e}")
            logging.error(f"✗ ({e})")
            failed_imports.append({"name": "fcntl", "error": str(e)})
    else:
        logging.warning("  -> fcntl 模块在 Windows 平台不可用，已跳过。")
        logging.info("[依赖检查]   -> fcntl (Windows平台跳过)")
    if "eventlet" in globals():
        try:
            logging.info("  -> 正在应用 eventlet.monkey_patch()...")
            logging.info("[依赖检查]   -> eventlet.monkey_patch()...")
            eventlet.monkey_patch()
            logging.info("  ✓ eventlet.monkey_patch() 应用成功")
            logging.info("✓")
        except Exception as e:
            logging.error(f"  ✗ eventlet.monkey_patch() 应用失败: {e}")
            logging.error(f"✗ ({e})")
            failed_imports.append(
                {
                    "name": "eventlet.monkey_patch()",
                    "pip_name": "eventlet",
                    "error": str(e),
                }
            )

    # 如果有导入失败，统一报告
    if failed_imports:
        logging.critical(f"标准库导入失败，共 {len(failed_imports)} 个模块")
        print(f"\n{'='*70}")
        print(f"[致命错误] Python 标准库导入失败")
        print(f"{'='*70}")
        print(f"\n检测到 {len(failed_imports)} 个标准库导入失败：\n")
        for i, failure in enumerate(failed_imports, 1):
            print(f"  {i}. {failure['name']}")
            print(f"     错误: {failure['error']}\n")
        print("这可能表示您的 Python 环境已损坏。")
        print("请检查您的 Python 安装或尝试重新安装 Python。")
        print(f"{'='*70}\n")
        sys.exit(1)

    print("[依赖检查] ✓ 所有标准库导入成功！")
    logging.info("所有标准库导入成功！")


def import_core_third_party():
    """
    导入 'check_and_import_dependencies' 未涵盖的核心第三方库。
    """
    logging.info("=" * 80)
    logging.info("开始检查并导入核心第三方库 (Pillow, bcrypt, Flask-SocketIO)...")
    print("[依赖检查] 正在导入核心第三方库...")

    # (显示名称, 导入命令, pip包名)
    core_libs = [
        ("PIL (Pillow)", "from PIL import Image", "Pillow"),
        ("bcrypt", "import bcrypt", "bcrypt"),
        (
            "Flask-SocketIO",
            "from flask_socketio import SocketIO, emit, join_room, leave_room",
            "Flask-SocketIO",
        ),
        ("eventlet", "import eventlet", "eventlet"),  # <-- 修正：添加 eventlet 导入
    ]

    failed_imports = []

    # 逐个尝试导入
    for display_name, import_cmd, pip_name in core_libs:
        try:
            logging.info(f"  -> 正在导入 {display_name}...")
            print(f"[依赖检查]   -> {display_name}...", end=" ")
            exec(import_cmd, globals())
            logging.info(f"  ✓ {display_name} 导入成功")
            print("✓")
        except ImportError as e:
            logging.error(f"  ✗ {display_name} 导入失败: {e}")
            print(f"✗ ({e})")
            failed_imports.append(
                {"name": display_name, "pip_name": pip_name, "error": str(e)}
            )

    # 如果有导入失败，统一报告
    if failed_imports:
        logging.critical(f"核心第三方库导入失败，共 {len(failed_imports)} 个模块")
        pip_install_list = " ".join([f["pip_name"] for f in failed_imports])

        print(f"\n{'='*70}")
        print(f"[依赖缺失错误] 核心第三方库导入失败")
        print(f"{'='*70}")
        print(f"\n检测到 {len(failed_imports)} 个核心库导入失败：\n")
        for i, failure in enumerate(failed_imports, 1):
            print(f"  {i}. {failure['name']} (pip包名: {failure['pip_name']})")
            print(f"     错误: {failure['error']}\n")
        print("请在您的终端（命令行）中运行以下命令来安装缺失的库:")
        print(f"\n  pip install {pip_install_list}\n")
        print("如果您使用的是 pip3，请运行:")
        print(f"\n  pip3 install {pip_install_list}\n")
        print(f"{'='*70}\n")
        sys.exit(1)

    print("[依赖检查] ✓ 核心第三方库导入成功！")
    logging.info("核心第三方库导入成功！")


def check_and_import_dependencies():
    """
    检查并导入所有主要的第三方库 (Flask, requests, playwright 等)。
    收集所有导入失败的模块，最后统一报告并提供安装命令。
    """
    logging.info("=" * 80)
    logging.info("开始检查并导入主要应用依赖库...")
    print("[依赖检查] 开始检查并导入主要应用依赖库...")

    # 声明我们将要修改全局变量
    global Flask, render_template_string, session, redirect, url_for, request, jsonify, make_response, g, send_file
    global CORS, pyotp, requests, openpyxl, xlrd, xlwt, chardet, sync_playwright, np
    global cssutils, playwright_available

    # 声明 socketio 为全局变量
    global cryptography, socketio

    # 将所有变量预设为 None，以防导入成功但未完全解包
    (
        Flask,
        render_template_string,
        session,
        redirect,
        url_for,
        request,
        jsonify,
        make_response,
        g,
    ) = (None,) * 9
    (
        CORS,
        pyotp,
        requests,
        openpyxl,
        xlrd,
        xlwt,
        chardet,
        sync_playwright,
        np,
        cssutils,
    ) = (None,) * 10
    playwright_available = False

    cryptography = None

    # 声明 socketio 为全局变量
    socketio = None

    # (显示名称, 导入代码, pip包名)
    dependencies = [
        (
            "Flask Web框架",
            "from flask import Flask, render_template_string, session, redirect, url_for, request, jsonify, make_response, g, send_file",
            "Flask",
        ),
        ("Flask CORS", "from flask_cors import CORS", "flask-cors"),
        ("pyotp (一次性密码)", "import pyotp", "pyotp"),
        ("requests (HTTP库)", "import requests", "requests"),
        ("openpyxl (Excel .xlsx)", "import openpyxl", "openpyxl"),
        ("xlrd (Excel .xls读取)", "import xlrd", "xlrd"),
        ("xlwt (Excel .xls写入)", "import xlwt", "xlwt"),
        ("chardet (编码检测)", "import chardet", "chardet"),
        (
            "Playwright (浏览器自动化)",
            "from playwright.sync_api import sync_playwright",
            "playwright",
        ),
        ("NumPy (科学计算)", "import numpy as np", "numpy"),
        ("cssutils (CSS解析)", "import cssutils", "cssutils"),
        ("cryptography (SSL/加密)", "import cryptography", "cryptography"),
        ("BeautifulSoup (HTML解析)", "from bs4 import BeautifulSoup", "beautifulsoup4"),
    ]

    failed_imports = []

    # 逐个尝试导入
    for display_name, import_cmd, pip_name in dependencies:
        try:
            logging.info(f"  -> 正在导入 {display_name}...")
            print(f"[依赖检查]   -> {display_name}...", end=" ")
            exec(import_cmd, globals())
            logging.info(f"  ✓ {display_name} 导入成功")
            print("✓")

            # 特殊处理：标记 playwright 可用
            if pip_name == "playwright":
                playwright_available = True

        except ImportError as e:
            logging.error(f"  ✗ {display_name} 导入失败: {e}")
            print(f"✗ ({e})")
            failed_imports.append(
                {"name": display_name, "pip_name": pip_name, "error": str(e)}
            )

    # 如果有导入失败，统一报告
    if failed_imports:
        logging.critical(f"主要应用依赖导入失败，共 {len(failed_imports)} 个模块")
        pip_install_list = " ".join([f["pip_name"] for f in failed_imports])

        print(f"\n{'='*70}")
        print(f"[依赖缺失错误] 主要应用依赖导入失败")
        print(f"{'='*70}")
        print(f"\n检测到 {len(failed_imports)} 个依赖库导入失败：\n")
        for i, failure in enumerate(failed_imports, 1):
            print(f"  {i}. {failure['name']} (pip包名: {failure['pip_name']})")
            print(f"     错误: {failure['error']}\n")
        print("请在您的终端（命令行）中运行以下命令来安装 *所有* 缺失的依赖:")
        print(f"\n  pip install {pip_install_list}\n")
        print("如果您使用的是 pip3，请运行:")
        print(f"\n  pip3 install {pip_install_list}\n")

        # 特别提示 playwright
        if any(f["pip_name"] == "playwright" for f in failed_imports):
            print("--- 特别提示：关于 'playwright' ---")
            print("playwright 库在首次安装后，还需要安装浏览器驱动。")
            print("请在安装完 pip 包后，额外运行一次:")
            print("  playwright install chromium")
            print("--------------------------------------\n")

        print(f"{'='*70}\n")
        sys.exit(1)

    logging.info("所有主要应用依赖库导入完成！")
    print("[依赖检查] ✓ 所有主要应用依赖库导入完成！")
    logging.info("=" * 80)


def initialize_global_variables():
    """
    初始化所有全局变量和应用状态。
    """
    logging.info("开始初始化全局变量...")

    # 声明我们将要创建的全局变量
    global auth_system, token_manager, html_content
    global web_sessions, web_sessions_lock, session_file_locks, session_file_locks_lock
    global session_activity, session_activity_lock
    global chrome_pool, background_task_manager

    auth_system = AuthSystem()
    token_manager = TokenManager(TOKENS_STORAGE_DIR)
    logging.info("认证系统和Token管理器已创建。")

    # 读取 HTML
    html_content = ""
    try:
        html_path = "index.html"  # 临时占位符

        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        logging.info("成功读取 index.html 文件！")

    except FileNotFoundError:
        logging.error(f"错误: 未在路径 '{html_path}' 中找到 'index.html' 文件。")
        sys.exit(1)
    except Exception as e:
        logging.error(f"读取文件时发生错误: {e}", exc_info=True)
        sys.exit(1)

    # 全局会话存储
    web_sessions = {}
    web_sessions_lock = threading.Lock()

    # 内存优化：会话数量限制（防止内存溢出）
    # 当内存中的会话数超过此值时，cleanup_sessions会更频繁地清理过期会话
    MAX_MEMORY_SESSIONS = 1000  # 最多保持1000个会话在内存中

    # 会话文件锁
    session_file_locks = {}
    session_file_locks_lock = threading.Lock()

    # 会话活动追踪
    session_activity = {}
    session_activity_lock = threading.Lock()
    logging.info("会话存储和锁已初始化。")

    # 全局浏览器池和任务管理器
    chrome_pool = None
    background_task_manager = None
    logging.info("浏览器池和任务管理器已初始化为 None。")

    logging.info("全局变量初始化完成。")


# ==============================================================================
#  1. 日志系统配置
# ==============================================================================


class NoColorFileFormatter(logging.Formatter):
    """
    自定义日志格式化程序，用于在写入文件前去除ANSI颜色代码。

    某些日志处理器可能会添加颜色代码（如colorlog），这些代码在文件中显示为乱码。
    此格式化程序确保写入日志文件的内容是纯文本，便于文本编辑器查看。

    属性:
        ansi_escape_regex: 编译好的正则表达式，用于匹配和删除ANSI转义序列
    """

    # ANSI转义码正则表达式详解：
    # \x1B 是ESC字符（ASCII 27）
    # [@-Z\\-_] 匹配单字符转义序列
    # \[[0-?]*[ -/]*[@-~] 匹配CSI序列（控制序列引导符）
    # 这个模式可以匹配大多数终端颜色代码和格式化指令
    ansi_escape_regex = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def format(self, record):
        """
        格式化日志记录并移除颜色代码。

        处理流程：
        1. 调用父类的format方法，生成可能包含ANSI颜色代码的日志消息
        2. 使用正则表达式替换所有ANSI转义序列为空字符串
        3. 返回清理后的纯文本消息

        参数:
            record: LogRecord对象，包含日志信息（级别、消息、时间等）

        返回:
            str: 不含ANSI颜色代码的格式化日志消息
        """
        original_message = super().format(record)
        # 使用sub方法替换所有匹配的ANSI代码为空字符串
        cleaned_message = self.ansi_escape_regex.sub("", original_message)
        return cleaned_message


class CustomLogHandler(logging.FileHandler):
    """
    自定义日志处理器，实现文件大小检查和轮转。

    当日志文件大小超过阈值时，进行轮转：
    - 重命名 zx-slm-tool.log 为 zx-slm-tool-01.log
    - 如果 zx-slm-tool-01.log 已存在，重命名为 zx-slm-tool-02.log
    - 以此类推
    - 创建新的 zx-slm-tool.log
    """

    def __init__(
        self, filename, mode="a", encoding="utf-8", max_bytes=10 * 1024 * 1024
    ):
        """
        初始化自定义日志处理器。

        参数:
            filename: 日志文件路径
            mode: 文件打开模式
            encoding: 编码
            max_bytes: 最大文件大小（字节）
        """
        self.max_bytes = max_bytes
        self.base_filename = filename
        super().__init__(filename, mode, encoding)

    def emit(self, record):
        """
        写入日志记录前检查文件大小。
        """
        try:
            # 检查文件大小
            if self.stream and os.path.exists(self.baseFilename):
                self.stream.flush()
                if os.path.getsize(self.baseFilename) >= self.max_bytes:
                    self.do_rollover()

            # 写入日志
            super().emit(record)

        except Exception:
            self.handleError(record)

    def do_rollover(self):
        """
        执行标准的日志轮转。
        实现逻辑：
        1. 检查 zx-slm-tool-09.log 是否存在，如果存在则删除
        2. 将 zx-slm-tool-08.log 重命名为 zx-slm-tool-09.log
        3. 将 zx-slm-tool-07.log 重命名为 zx-slm-tool-08.log
        4. ...
        5. 将 zx-slm-tool-01.log 重命名为 zx-slm-tool-02.log
        6. 最后将 zx-slm-tool.log 重命名为 zx-slm-tool-01.log
        7. 创建一个新的 zx-slm-tool.log 文件用于后续写入
        """
        # 关闭当前文件流
        if self.stream:
            self.stream.close()
            self.stream = None

        # 获取日志目录和基础文件名
        log_dir = os.path.dirname(self.baseFilename)
        base_name = "zx-slm-tool"

        # 定义最大轮转文件数量（保留10个历史文件：zx-slm-tool-01.log 到 zx-slm-tool-10.log）
        max_backup_count = 10

        # 从最大编号开始，依次向后移动文件
        # 如果 zx-slm-tool-10.log 存在，则删除它（最旧的文件）
        for i in range(max_backup_count, 0, -1):
            old_log = os.path.join(log_dir, f"{base_name}-{i:02d}.log")

            if i == max_backup_count:
                # 删除最旧的文件（编号为 max_backup_count）
                if os.path.exists(old_log):
                    try:
                        os.remove(old_log)
                        print(
                            f"[日志轮转] 已删除最旧的日志文件: {os.path.basename(old_log)}"
                        )
                    except Exception as e:
                        print(f"[日志轮转] 删除 {os.path.basename(old_log)} 失败: {e}")
            else:
                # 将 zx-slm-tool-0X.log 重命名为 zx-slm-tool-0(X+1).log
                if os.path.exists(old_log):
                    new_log = os.path.join(log_dir, f"{base_name}-{i+1:02d}.log")
                    try:
                        os.rename(old_log, new_log)
                        print(
                            f"[日志轮转] {os.path.basename(old_log)} -> {os.path.basename(new_log)}"
                        )
                    except Exception as e:
                        print(
                            f"[日志轮转] 重命名 {os.path.basename(old_log)} 失败: {e}"
                        )

        # 最后，将当前的 zx-slm-tool.log 重命名为 zx-slm-tool-01.log
        first_backup = os.path.join(log_dir, f"{base_name}-01.log")
        try:
            # 如果 zx-slm-tool-01.log 已经存在（不应该发生，但作为安全检查）
            if os.path.exists(first_backup):
                os.remove(first_backup)

            os.rename(self.baseFilename, first_backup)
            print(
                f"[日志轮转] {os.path.basename(self.baseFilename)} -> {os.path.basename(first_backup)}"
            )
        except Exception as e:
            print(f"[日志轮转] 轮转主日志文件失败: {e}")

        # 重新打开一个新的 zx-slm-tool.log 文件用于后续写入
        self.stream = self._open()


def archive_old_logs():
    """
    归档旧的日志文件。

    在程序启动时调用，将上一次运行的日志文件压缩并移动到归档目录。
    支持归档 zx-slm-tool.log 和 zx-slm-tool-*.log 格式的文件。
    """

    # 确保归档目录存在
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir, exist_ok=True)
        print(f"[日志归档] 创建归档目录: {archive_dir}")

    # 查找所有需要归档的日志文件
    log_files_to_archive = []
    for filename in os.listdir(log_dir):
        if filename == "zx-slm-tool.log" or (
            filename.startswith("zx-slm-tool-") and filename.endswith(".log")
        ):
            log_path = os.path.join(log_dir, filename)
            # 只归档非空文件
            if os.path.isfile(log_path) and os.path.getsize(log_path) > 0:
                log_files_to_archive.append((log_path, filename))

    if not log_files_to_archive:
        print(f"[日志归档] 没有需要归档的日志文件")
        return

    # 生成归档文件名（毫秒级时间戳）
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]  # 毫秒级
    archive_filename = f"{timestamp}.zip"
    archive_path = os.path.join(archive_dir, archive_filename)

    try:
        # 创建ZIP归档
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for log_path, filename in log_files_to_archive:
                zipf.write(log_path, filename)
                print(f"[日志归档] 已压缩: {filename}")

        # 删除已归档的日志文件
        for log_path, filename in log_files_to_archive:
            os.remove(log_path)
            print(f"[日志归档] 已删除原文件: {filename}")

        print(f"[日志归档] 归档完成: {archive_path}")

        # 清理内存 - 使用全局导入的gc模块
        gc.collect()

    except Exception as e:
        print(f"[日志归档] 归档失败: {e}")

        traceback.print_exc()


def cleanup_archive_directory(archive_dir, max_size_mb):
    """
    清理归档目录，确保不超过指定大小。

    当归档目录大小超过限制时，删除最早的归档文件。

    参数:
        archive_dir: 归档目录路径
        max_size_mb: 最大大小（MB），0表示不限制
    """
    if max_size_mb <= 0:
        return  # 不限制大小

    if not os.path.exists(archive_dir):
        return

    try:
        # 获取所有归档文件及其大小
        archive_files = []
        total_size = 0

        for filename in os.listdir(archive_dir):
            if filename.endswith(".zip"):
                file_path = os.path.join(archive_dir, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    # 获取文件修改时间
                    mtime = os.path.getmtime(file_path)
                    archive_files.append((file_path, filename, file_size, mtime))
                    total_size += file_size

        max_size_bytes = max_size_mb * 1024 * 1024
        current_size_mb = total_size / (1024 * 1024)

        if total_size <= max_size_bytes:
            print(
                f"[归档清理] 归档目录大小: {current_size_mb:.2f}MB / {max_size_mb}MB (无需清理)"
            )
            return

        print(
            f"[归档清理] 归档目录大小: {current_size_mb:.2f}MB 超过限制 {max_size_mb}MB，开始清理..."
        )

        # 按时间排序（最早的在前）
        archive_files.sort(key=lambda x: x[3])

        # 删除最早的文件直到大小满足要求
        deleted_count = 0
        for file_path, filename, file_size, _ in archive_files:
            if total_size <= max_size_bytes:
                break

            os.remove(file_path)
            total_size -= file_size
            deleted_count += 1
            print(f"[归档清理] 已删除: {filename} ({file_size / (1024 * 1024):.2f}MB)")

        final_size_mb = total_size / (1024 * 1024)
        print(
            f"[归档清理] 清理完成，删除了 {deleted_count} 个文件，当前大小: {final_size_mb:.2f}MB"
        )

        # 如果删除了文件，进行垃圾回收以释放内存 - 使用全局导入的gc模块
        if deleted_count > 0:
            gc.collect()

    except Exception as e:
        print(f"[归档清理] 清理失败: {e}")

        traceback.print_exc()


def setup_logging():
    """
    配置详细的日志系统（带自定义轮转逻辑）。

    功能：
    1. 启动时归档旧日志文件到 logs/archive（压缩为 zip）
    2. 当 zx-slm-tool.log 大小超过配置限制时自动轮转
    3. 清理归档目录，防止占用过多磁盘空间

    配置项（config.ini [Logging]）：
    - log_rotation_size_mb: 单个日志文件最大大小（MB）
    - archive_max_size_mb: 归档目录最大大小（MB），0表示不限制
    """
    # 读取配置（如果配置文件存在）
    log_rotation_size_mb = 10  # 默认10MB
    archive_max_size_mb = 500  # 默认500MB
    global log_dir, archive_dir
    log_dir = "logs"
    archive_dir = os.path.join(log_dir, "archive")

    try:
        if os.path.exists("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            if "Logging" in config:
                log_rotation_size_mb = config.getint(
                    "Logging", "log_rotation_size_mb", fallback=10
                )
                archive_max_size_mb = config.getint(
                    "Logging", "archive_max_size_mb", fallback=500
                )
                log_dir = config.get("Logging", "log_dir", fallback="logs")
                archive_dir = config.get(
                    "Logging", "archive_dir", fallback="logs/archive"
                )
    except Exception as e:
        print(f"[日志系统] 读取配置失败，使用默认值: {e}")

    # 确保logs目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        print(f"[日志系统] 创建日志目录: {log_dir}")

    # 步骤1: 归档旧日志文件
    archive_old_logs()

    # 步骤2: 清理归档目录
    cleanup_archive_directory(archive_dir, archive_max_size_mb)

    log_file = os.path.join(log_dir, "zx-slm-tool.log")

    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 清除已有的处理器
    logger.handlers.clear()

    # 日志格式 - 包含详细信息
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器 - 输出到标准输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 文件处理器 - 使用自定义轮转处理器
    max_bytes = log_rotation_size_mb * 1024 * 1024
    file_handler = CustomLogHandler(
        log_file, mode="a", encoding="utf-8", max_bytes=max_bytes
    )
    file_handler.setLevel(logging.DEBUG)

    # 修复：为 file_handler 应用“无颜色”格式化程序
    # 我们从原始 log_format 中提取格式字符串和日期格式
    no_color_formatter = NoColorFileFormatter(
        log_format._fmt, datefmt=log_format.datefmt
    )
    file_handler.setFormatter(no_color_formatter)

    logger.addHandler(file_handler)

    # ========== 新增：警告和错误日志文件处理器 ==========
    # 创建专门用于记录WARNING、ERROR和CRITICAL级别日志的处理器
    # 这样可以将警告和严重错误单独记录到一个文件中，方便快速定位问题
    # 使用WARNING.log作为文件名，表示记录WARNING及以上级别的日志
    warning_log_file = os.path.join(log_dir, "zx-slm-tool-WARNING.log")

    # 使用与主日志相同的轮转配置（max_bytes）和归档逻辑
    # 这确保了警告日志也会被自动轮转和归档，防止文件过大
    warning_file_handler = CustomLogHandler(
        warning_log_file,  # 警告日志文件路径
        mode="a",  # 追加模式（append），保留历史警告日志
        encoding="utf-8",  # UTF-8编码，支持中文日志
        max_bytes=max_bytes,  # 使用与主日志相同的大小限制
    )

    # 设置日志级别为WARNING：记录WARNING、ERROR和CRITICAL级别的日志
    # 这样可以过滤掉DEBUG和INFO级别的日志，只保留需要关注的警告和错误
    warning_file_handler.setLevel(logging.WARNING)

    # 为警告日志处理器应用"无颜色"格式化程序
    # 使用与主日志相同的格式，确保日志格式的一致性
    warning_no_color_formatter = NoColorFileFormatter(
        log_format._fmt,  # 使用相同的日志格式字符串
        datefmt=log_format.datefmt,  # 使用相同的日期格式
    )
    warning_file_handler.setFormatter(warning_no_color_formatter)

    # 将警告日志处理器添加到logger中
    # 现在所有WARNING、ERROR和CRITICAL日志会同时写入主日志和警告日志文件
    logger.addHandler(warning_file_handler)
    # ========== 结束：警告和错误日志文件处理器 ==========

    # ========== 新增：错误日志文件处理器 ==========
    # 创建专门用于记录ERROR和CRITICAL级别日志的处理器
    # 这样可以将严重错误单独记录到一个文件中，方便快速定位关键问题
    # 使用ERROR.log作为文件名，只记录ERROR及以上级别的日志
    error_log_file = os.path.join(log_dir, "zx-slm-tool-ERROR.log")

    # 使用与主日志相同的轮转配置（max_bytes）和归档逻辑
    # 这确保了错误日志也会被自动轮转和归档，防止文件过大
    error_file_handler = CustomLogHandler(
        error_log_file,  # 错误日志文件路径
        mode="a",  # 追加模式（append），保留历史错误日志
        encoding="utf-8",  # UTF-8编码，支持中文日志
        max_bytes=max_bytes,  # 使用与主日志相同的大小限制
    )

    # 设置日志级别为ERROR：只记录ERROR和CRITICAL级别的日志
    # 这样可以过滤掉DEBUG、INFO和WARNING级别的日志，只保留最严重的错误
    error_file_handler.setLevel(logging.ERROR)

    # 为错误日志处理器应用"无颜色"格式化程序
    # 使用与主日志相同的格式，确保日志格式的一致性
    error_no_color_formatter = NoColorFileFormatter(
        log_format._fmt,  # 使用相同的日志格式字符串
        datefmt=log_format.datefmt,  # 使用相同的日期格式
    )
    error_file_handler.setFormatter(error_no_color_formatter)

    # 将错误日志处理器添加到logger中
    # 现在所有ERROR和CRITICAL日志会同时写入主日志、警告日志和错误日志文件
    logger.addHandler(error_file_handler)
    # ========== 结束：错误日志文件处理器 ==========

    # 回放缓冲区的早期日志
    global _log_buffer
    if _log_buffer:
        # 先记录一条分割线，表示上方是补录的日志
        # 但为了保持时间顺序，我们直接按顺序写入
        for level_str, msg in _log_buffer:
            level_num = getattr(logging, level_str.upper(), logging.INFO)
            logger.log(level_num, msg.rstrip())

        # 清空缓冲区，释放内存
        _log_buffer.clear()
        # 强制垃圾回收以释放内存 - 使用全局导入的gc模块
        gc.collect()

    # 记录日志系统启动
    logging.info("=" * 80)
    logging.info("日志系统初始化完成！")
    logging.info(f"日志文件: {log_file}")
    logging.info(f"警告日志文件: {warning_log_file}")  # 添加警告日志文件信息
    logging.info(f"错误日志文件: {error_log_file}")  # 添加错误日志文件信息
    logging.info(f"日志级别: DEBUG (所有级别)")
    logging.info(f"日志轮转: 单文件最大{log_rotation_size_mb}MB")
    logging.info(
        f"归档目录: {archive_dir}, 最大{archive_max_size_mb}MB{'（不限制）' if archive_max_size_mb == 0 else ''}"
    )
    logging.info("=" * 80)

    return logger


# 自动初始化系统


def auto_init_system():
    """
    自动初始化系统，创建所有必需的文件和目录。
    """
    logging.info("=" * 80)
    logging.info("开始自动初始化系统...")
    print("[系统初始化] 开始自动初始化系统...")

    try:
        # ===== 步骤1：创建目录结构 =====
        # 必须最先执行，因为后续步骤需要写入文件到这些目录
        logging.info("步骤1: 创建必需的目录...")
        print("[系统初始化] 创建必需的目录...")
        _create_directories()

        # ===== 步骤2：配置文件管理 =====
        # 如果config.ini不存在则创建，如果存在则检查并补全缺失的配置项
        # 这保证了配置文件的向后兼容性
        logging.info("步骤2: 创建/更新配置文件...")
        print("[系统初始化] 创建/更新配置文件...")
        _create_config_ini()

        # ===== 步骤3：权限系统初始化 =====
        # 创建permissions.json，定义权限组（guest、user、admin、super_admin）
        # 只在文件不存在时创建，避免覆盖用户的权限配置
        logging.info("步骤3: 创建权限配置文件...")
        print("[系统初始化] 创建权限配置文件...")
        _create_permissions_json()

        # ===== 步骤4：默认管理员账号 =====
        # 创建admin账号，确保至少有一个账号可以登录
        # 密码存储在system_accounts目录下的哈希文件名中
        logging.info("步骤4: 创建默认管理员账号...")
        print("[系统初始化] 创建默认管理员账号...")
        _create_default_admin()

        logging.info("系统初始化完成！")
        logging.info("=" * 80)
        print("[系统初始化] 系统初始化完成！")

    except Exception as e:
        # 捕获所有异常，确保初始化失败不会导致程序崩溃
        # 但会详细记录错误信息，便于用户排查问题
        logging.error(f"系统初始化失败: {e}", exc_info=True)
        print(f"[系统初始化] 错误: 系统初始化失败 - {e}")
        # 注意：这里不抛出异常，允许程序继续运行
        # 因为有些功能可能在部分初始化失败的情况下仍能工作


# 初始化全局目录变量
# 这些变量会在 _create_directories() 中根据 config.ini 配置更新
SCHOOL_ACCOUNTS_DIR = "school_accounts"
SYSTEM_ACCOUNTS_DIR = "system_accounts"
LOGIN_LOGS_DIR = "logs"
SESSION_STORAGE_DIR = "sessions"
TOKENS_STORAGE_DIR = "tokens"
CONFIG_FILE = "config.ini"
PERMISSIONS_FILE = "permissions.json"
SESSION_INDEX_FILE = None  # 将在 _create_directories() 后初始化
LOGIN_LOG_FILE = None  # 将在 _create_directories() 后初始化
AUDIT_LOG_FILE = None  # 将在 _create_directories() 后初始化


def _create_directories():
    """
    创建程序运行所需的目录结构，目录路径从 config.ini 配置文件读取。

    目录说明：
    - logs: 日志文件存储目录（可在 config.ini [Logging] log_dir 配置）
    - school_accounts: 学校账号信息存储（可在 config.ini [System] school_accounts_dir 配置）
    - system_accounts: 系统认证账号存储（可在 config.ini [System] system_accounts_dir 配置）
    - sessions: 用户会话持久化存储（可在 config.ini [System] sessions_dir 配置）
    - tokens: API令牌存储目录（可在 config.ini [System] tokens_dir 配置）

    注意：此函数会更新全局变量，使其他模块可以使用配置的路径。
    """
    global SCHOOL_ACCOUNTS_DIR, SYSTEM_ACCOUNTS_DIR, LOGIN_LOGS_DIR
    global SESSION_STORAGE_DIR, TOKENS_STORAGE_DIR
    global SESSION_INDEX_FILE, LOGIN_LOG_FILE, AUDIT_LOG_FILE

    # 默认目录配置
    default_dirs = {
        "school_accounts_dir": "school_accounts",
        "system_accounts_dir": "system_accounts",
        "log_dir": "logs",
        "sessions_dir": "sessions",
        "tokens_dir": "tokens",
    }

    # 尝试从 config.ini 读取目录配置
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")
    if os.path.exists(config_file):
        try:
            config = configparser.ConfigParser()
            config.read(config_file, encoding="utf-8")

            # 从 [System] 节读取配置
            if config.has_section("System"):
                default_dirs["school_accounts_dir"] = config.get(
                    "System",
                    "school_accounts_dir",
                    fallback=default_dirs["school_accounts_dir"],
                )
                default_dirs["system_accounts_dir"] = config.get(
                    "System",
                    "system_accounts_dir",
                    fallback=default_dirs["system_accounts_dir"],
                )
                default_dirs["sessions_dir"] = config.get(
                    "System", "sessions_dir", fallback=default_dirs["sessions_dir"]
                )
                default_dirs["tokens_dir"] = config.get(
                    "System", "tokens_dir", fallback=default_dirs["tokens_dir"]
                )

            # 从 [Logging] 节读取日志目录配置
            if config.has_section("Logging"):
                default_dirs["log_dir"] = config.get(
                    "Logging", "log_dir", fallback=default_dirs["log_dir"]
                )

            print(f"[配置读取] 成功从 config.ini 读取目录配置")
        except Exception as e:
            print(f"[配置读取] 警告: 读取 config.ini 失败，使用默认配置: {e}")
    else:
        print(f"[配置读取] config.ini 不存在，使用默认目录配置")

    # 更新全局变量（使用绝对路径）
    base_dir = os.path.dirname(__file__)
    SCHOOL_ACCOUNTS_DIR = os.path.join(base_dir, default_dirs["school_accounts_dir"])
    SYSTEM_ACCOUNTS_DIR = os.path.join(base_dir, default_dirs["system_accounts_dir"])
    LOGIN_LOGS_DIR = os.path.join(base_dir, default_dirs["log_dir"])
    SESSION_STORAGE_DIR = os.path.join(base_dir, default_dirs["sessions_dir"])
    TOKENS_STORAGE_DIR = os.path.join(base_dir, default_dirs["tokens_dir"])

    # 创建所有目录
    directories = {
        "school_accounts": SCHOOL_ACCOUNTS_DIR,
        "system_accounts": SYSTEM_ACCOUNTS_DIR,
        "logs": LOGIN_LOGS_DIR,
        "sessions": SESSION_STORAGE_DIR,
        "tokens": TOKENS_STORAGE_DIR,
    }

    for name, directory in directories.items():
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[目录创建] 创建目录: {name} -> {directory}")
            logging.info(f"[系统初始化] 创建目录: {name} -> {directory}")
        else:
            print(f"[目录创建] 目录已存在: {name} -> {directory}")

    # 创建 user_accounts 子目录用于存储按用户分类的 school_account 密码
    user_accounts_dir = os.path.join(SCHOOL_ACCOUNTS_DIR, "user_accounts")
    if not os.path.exists(user_accounts_dir):
        os.makedirs(user_accounts_dir, exist_ok=True)
        print(f"[目录创建] 创建目录: user_accounts -> {user_accounts_dir}")
        logging.info(f"[系统初始化] 创建目录: user_accounts -> {user_accounts_dir}")
    else:
        print(f"[目录创建] 目录已存在: user_accounts -> {user_accounts_dir}")

    # 初始化依赖于目录路径的全局变量
    SESSION_INDEX_FILE = os.path.join(SESSION_STORAGE_DIR, "_index.json")
    LOGIN_LOG_FILE = os.path.join(LOGIN_LOGS_DIR, "login_history.jsonl")
    AUDIT_LOG_FILE = os.path.join(LOGIN_LOGS_DIR, "audit.jsonl")

    print(f"[目录创建] 所有目录创建完成")


def _get_default_config():
    """
    获取默认配置项字典。
    """
    config = configparser.ConfigParser()

    # [Admin] 管理员配置
    config["Admin"] = {"super_admin": "admin"}

    # [Guest] 游客配置
    config["Guest"] = {"allow_guest_login": "true"}

    # [System] 系统配置
    config["System"] = {
        "session_expiry_days": "7",
        "school_accounts_dir": "school_accounts",
        "system_accounts_dir": "system_accounts",
        "sessions_dir": "sessions",  # 新增：会话存储目录
        "tokens_dir": "tokens",  # 新增：Token存储目录
        "permissions_file": "permissions.json",
        "session_monitor_check_interval": "60",  # 会话监控检查间隔（秒），默认60秒
        "session_inactivity_timeout": "300",  # 会话不活跃超时时间（秒），默认300秒（5分钟）
    }

    # [Logging] 日志配置
    config["Logging"] = {
        "log_rotation_size_mb": "10",  # 单个日志文件最大大小（MB）
        "archive_max_size_mb": "500",  # 归档目录最大大小（MB），0表示不限制
        "log_dir": "logs",
        "archive_dir": "logs/archive",
    }

    # [Security] 安全配置
    config["Security"] = {
        "password_storage": "plaintext",
        "brute_force_protection": "true",
        "login_log_retention_days": "90",
    }

    # [Map] 地图配置
    config["Map"] = {
        "amap_js_key": "",  # 高德地图JS API密钥
    }

    # ========================================
    # [API] 第三方API配置
    # ========================================
    # 存储第三方服务的API密钥和凭证
    config["API"] = {
        "ip_api_key": "",  # IP地理位置查询API密钥（可选，留空则使用免费接口）
        # 注意：验证码已改用本地生成器，不再需要第三方API密钥
    }

    # ========================================
    # [Captcha] 本地验证码生成器配置
    # ========================================
    # 使用MicroPixelCaptcha生成黑白像素风格验证码
    # 无需第三方API，更稳定、更安全、响应更快
    config["Captcha"] = {
        "length": "4",  # 【验证码字符数】范围3-6，默认4（推荐）
        "scale_factor": "2",  # 【像素细分倍数】范围2-4，默认2（推荐2或3）
        "noise_level": "0.08",  # 【噪点比例】范围0.0-0.3，默认0.08（8%噪点）
    }

    # [Features] 功能开关配置
    # 控制系统各项功能的启用/禁用状态，便于灵活管理
    config["Features"] = {
        "enable_phone_modification": "false",  # 是否允许用户修改手机号
        "enable_phone_login": "false",  # 是否支持手机号登录
        "enable_phone_registration_verify": "false",  # 注册时是否需要短信验证
        "enable_sms_service": "false",  # 短信服务总开关（关闭则所有短信功能不可用）
    }

    # [SMS_Service_SMSBao] 短信宝服务配置
    # 用于发送验证码、通知等短信，需要在短信宝官网注册账号获取凭证
    config["SMS_Service_SMSBao"] = {
        "username": "",  # 短信宝账户用户名
        "api_key": "",  # 短信宝API密钥（在短信宝后台获取）
        "signature": "【电科大跑步助手】",  # 短信签名（需提前在短信宝审核通过）
        "template_register": "您的验证码是：{code}，{minutes}分钟内有效。",  # 注册验证码短信模板，支持{code}和{minutes}占位符
        "code_expire_minutes": "5",  # 验证码有效期（分钟），默认5分钟，管理员可修改
        "send_interval_seconds": "180",  # 发送间隔（秒），默认180秒（3分钟），防止频繁发送
        "rate_limit_per_account_day": "10",  # 单个账号每天最多发送次数
        "rate_limit_per_ip_day": "20",  # 单个IP每天最多发送次数
        "rate_limit_per_phone_day": "5",  # 单个手机号每天最多发送次数
    }

    return config


def _write_config_with_comments(config_obj, filepath):
    """
    将配置写入文件，包含详细的中文注释。

    由于ConfigParser不保留注释，这个函数手动写入带注释的配置文件。
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# ========================================\n")
        f.write("# 跑步工具配置文件\n")
        f.write("# ========================================\n")
        f.write("# 说明：修改配置后需要重启程序生效\n")
        f.write("# ========================================\n\n")

        # [Admin] 配置
        f.write("[Admin]\n")
        f.write("# 超级管理员账号名称（有且只有一个）\n")
        f.write("# 注意：super_admin 只能在此配置文件中设置，不能在界面创建\n")
        f.write("# 默认账号: admin，默认密码: admin（首次登录后请立即修改）\n")
        f.write(
            f"super_admin = {config_obj.get('Admin', 'super_admin', fallback='admin')}\n\n"
        )

        # [Guest] 配置
        f.write("[Guest]\n")
        f.write("# 是否允许游客登录（true/false）\n")
        f.write("# true：允许未注册用户以游客身份使用系统（权限受限）\n")
        f.write("# false：禁止游客登录，所有用户必须注册\n")
        f.write(
            f"allow_guest_login = {config_obj.get('Guest', 'allow_guest_login', fallback='true')}\n\n"
        )

        # [System] 配置
        f.write("[System]\n")
        f.write("# 会话过期时间（天）\n")
        f.write("# 超过此时间未访问的会话将自动清理\n")
        f.write(
            f"session_expiry_days = {config_obj.get('System', 'session_expiry_days', fallback='7')}\n"
        )
        f.write("# 学校账号数据存储目录\n")
        f.write(
            f"school_accounts_dir = {config_obj.get('System', 'school_accounts_dir', fallback='school_accounts')}\n"
        )
        f.write("# 系统账号数据存储目录\n")
        f.write(
            f"system_accounts_dir = {config_obj.get('System', 'system_accounts_dir', fallback='system_accounts')}\n"
        )
        f.write("# 权限配置文件路径\n")
        f.write(
            f"permissions_file = {config_obj.get('System', 'permissions_file', fallback='permissions.json')}\n"
        )

        f.write("# 会话持久化数据存储目录\n")
        f.write(
            f"sessions_dir = {config_obj.get('System', 'sessions_dir', fallback='sessions')}\n"
        )
        f.write("# API令牌数据存储目录\n")
        f.write(
            f"tokens_dir = {config_obj.get('System', 'tokens_dir', fallback='tokens')}\n"
        )

        f.write("# 会话监控检查间隔时间（秒）\n")
        f.write("# 系统每隔此时间检查一次会话活跃状态，默认60秒\n")
        f.write(
            f"session_monitor_check_interval = {config_obj.get('System', 'session_monitor_check_interval', fallback='60')}\n"
        )
        f.write("# 会话不活跃超时时间（秒）\n")
        f.write(
            "# 会话超过此时间无活动（且无正在执行的任务）将被自动清理，默认300秒（5分钟）\n"
        )
        f.write(
            f"session_inactivity_timeout = {config_obj.get('System', 'session_inactivity_timeout', fallback='300')}\n\n"
        )

        # [Logging] 配置
        f.write("[Logging]\n")
        f.write("# 单个日志文件最大大小（MB）\n")
        f.write("# 超过此大小时会自动轮转到新文件（如 zx-slm-tool-01.log）\n")
        f.write(
            f"log_rotation_size_mb = {config_obj.get('Logging', 'log_rotation_size_mb', fallback='10')}\n"
        )
        f.write("# 归档目录最大大小（MB）\n")
        f.write("# 超过此大小时会删除最早的归档文件，设置为0表示不限制\n")
        f.write(
            f"archive_max_size_mb = {config_obj.get('Logging', 'archive_max_size_mb', fallback='500')}\n"
        )
        f.write("# 日志文件存储目录\n")
        f.write(f"log_dir = {config_obj.get('Logging', 'log_dir', fallback='logs')}\n")
        f.write("# 日志归档目录（启动时会自动压缩旧日志到此目录）\n")
        f.write(
            f"archive_dir = {config_obj.get('Logging', 'archive_dir', fallback='logs/archive')}\n\n"
        )

        # [Security] 配置
        f.write("[Security]\n")
        f.write("# 密码存储方式（plaintext/sha256/bcrypt）\n")
        f.write("# plaintext：明文存储（不推荐，仅用于测试）\n")
        f.write("# sha256：SHA256哈希（已弃用，不够安全）\n")
        f.write("# bcrypt：bcrypt加密（推荐，自动加盐，抗暴力破解）\n")
        f.write(
            f"password_storage = {config_obj.get('Security', 'password_storage', fallback='plaintext')}\n"
        )
        f.write("# 是否启用暴力破解防护（true/false）\n")
        f.write("# true：启用登录尝试限制和账号临时锁定\n")
        f.write(
            f"brute_force_protection = {config_obj.get('Security', 'brute_force_protection', fallback='true')}\n"
        )
        f.write("# 登录日志保留天数\n")
        f.write("# 超过此时间的登录审计日志将被清理\n")
        f.write(
            f"login_log_retention_days = {config_obj.get('Security', 'login_log_retention_days', fallback='90')}\n\n"
        )

        # [Map] 配置
        f.write("[Map]\n")
        f.write("# 高德地图 JS API 密钥\n")
        f.write("# 用于前端地图显示，请在高德开放平台申请：https://console.amap.com/\n")
        f.write("# 申请类型：Web端(JS API)，服务平台：Web端\n")
        f.write(
            f"amap_js_key = {config_obj.get('Map', 'amap_js_key', fallback='')}\n\n"
        )

        # ========================================
        # [API] 第三方API配置
        # ========================================
        f.write("# ========================================\n")
        f.write("# [API] 第三方API配置\n")
        f.write("# ========================================\n")
        f.write("[API]\n")
        f.write("# IP地理位置查询API密钥（可选）\n")
        f.write("# 用于获取用户登录IP的地理位置信息\n")
        f.write("# 留空则使用免费接口（有频率限制）\n")
        f.write(f"ip_api_key = {config_obj.get('API', 'ip_api_key', fallback='')}\n")
        f.write(
            "# 注意：验证码已改用本地生成器（见[Captcha]节），不再需要第三方API密钥\n\n"
        )

        # ========================================
        # [Captcha] 本地验证码生成器配置
        # ========================================
        f.write("# ========================================\n")
        f.write("# [Captcha] 本地验证码生成器配置\n")
        f.write("# ========================================\n")
        f.write("# 使用MicroPixelCaptcha生成黑白像素风格验证码\n")
        f.write("# 无需第三方API，更稳定、更安全、响应更快\n")
        f.write("# ========================================\n\n")
        f.write("[Captcha]\n")
        f.write("# 验证码字符数（3-6）\n")
        f.write(f"length = {config_obj.get('Captcha', 'length', fallback='4')}\n")
        f.write("# 像素细分倍数（2-4）\n")
        f.write(
            f"scale_factor = {config_obj.get('Captcha', 'scale_factor', fallback='2')}\n"
        )
        f.write("# 噪点比例（0.0-0.3）\n")
        f.write(
            f"noise_level = {config_obj.get('Captcha', 'noise_level', fallback='0.08')}\n\n"
        )

        # [Features] 功能开关配置
        f.write("[Features]\n")
        f.write("# 是否允许用户修改手机号（true/false）\n")
        f.write("# true：用户可在个人资料中修改手机号\n")
        f.write(
            f"enable_phone_modification = {config_obj.get('Features', 'enable_phone_modification', fallback='false')}\n"
        )
        f.write("# 是否支持手机号登录（true/false）\n")
        f.write("# true：用户可使用手机号+密码登录（手机号作为login_id）\n")
        f.write(
            f"enable_phone_login = {config_obj.get('Features', 'enable_phone_login', fallback='false')}\n"
        )
        f.write("# 注册时是否需要短信验证（true/false）\n")
        f.write("# true：用户注册时必须填写手机号并通过短信验证码验证\n")
        f.write(
            f"enable_phone_registration_verify = {config_obj.get('Features', 'enable_phone_registration_verify', fallback='false')}\n"
        )
        f.write("# 短信服务总开关（true/false）\n")
        f.write("# false：关闭所有短信功能，即使其他选项为true也不会发送短信\n")
        f.write(
            f"enable_sms_service = {config_obj.get('Features', 'enable_sms_service', fallback='false')}\n\n"
        )

        # [SMS_Service_SMSBao] 短信宝服务配置
        f.write("[SMS_Service_SMSBao]\n")
        f.write("# 短信宝服务配置（官网：https://www.smsbao.com/）\n")
        f.write("# 用于发送验证码、通知等短信\n")
        f.write("# 注意：使用前需要在短信宝注册账号并充值\n")
        f.write("# 短信宝账户用户名\n")
        f.write(
            f"username = {config_obj.get('SMS_Service_SMSBao', 'username', fallback='')}\n"
        )
        f.write("# 短信宝API密钥（在短信宝后台获取）\n")
        f.write(
            f"api_key = {config_obj.get('SMS_Service_SMSBao', 'api_key', fallback='')}\n"
        )
        f.write("# 短信签名（需提前在短信宝审核通过，格式：【签名内容】）\n")
        f.write(
            f"signature = {config_obj.get('SMS_Service_SMSBao', 'signature', fallback='【电科大跑步助手】')}\n"
        )
        f.write(
            "# 注册验证码短信模板（{code}会被替换为验证码，{minutes}会被替换为有效期分钟数）\n"
        )
        f.write(
            f"template_register = {config_obj.get('SMS_Service_SMSBao', 'template_register', fallback='您的验证码是：{{code}}，{{minutes}}分钟内有效。')}\n"
        )
        f.write("# 验证码有效期（分钟），默认5分钟，管理员可根据需要修改\n")
        f.write(
            f"code_expire_minutes = {config_obj.get('SMS_Service_SMSBao', 'code_expire_minutes', fallback='5')}\n"
        )
        f.write("# 发送间隔（秒），默认180秒（3分钟），防止频繁发送，增强安全性\n")
        f.write(
            f"send_interval_seconds = {config_obj.get('SMS_Service_SMSBao', 'send_interval_seconds', fallback='180')}\n"
        )
        f.write("# 单个账号每天最多发送次数（防止滥用）\n")
        f.write(
            f"rate_limit_per_account_day = {config_obj.get('SMS_Service_SMSBao', 'rate_limit_per_account_day', fallback='10')}\n"
        )
        f.write("# 单个IP每天最多发送次数（防止攻击）\n")
        f.write(
            f"rate_limit_per_ip_day = {config_obj.get('SMS_Service_SMSBao', 'rate_limit_per_ip_day', fallback='20')}\n"
        )
        f.write("# 单个手机号每天最多发送次数（防止骚扰）\n")
        f.write(
            f"rate_limit_per_phone_day = {config_obj.get('SMS_Service_SMSBao', 'rate_limit_per_phone_day', fallback='5')}\n\n"
        )

        # [SSL] 配置 - 新增SSL配置节的写入逻辑
        f.write("[SSL]\n")
        f.write("# SSL/HTTPS 配置\n")
        f.write("# 是否启用SSL（true/false）\n")
        f.write("# true：启用HTTPS协议访问\n")
        f.write("# false：使用HTTP协议访问\n")
        f.write(
            f"ssl_enabled = {config_obj.get('SSL', 'ssl_enabled', fallback='false')}\n"
        )
        f.write("# SSL证书文件路径\n")
        f.write("# 用于HTTPS服务的证书文件（PEM格式）\n")
        f.write(
            f"ssl_cert_path = {config_obj.get('SSL', 'ssl_cert_path', fallback='ssl/fullchain.pem')}\n"
        )
        f.write("# SSL私钥文件路径\n")
        f.write("# 用于HTTPS服务的私钥文件（KEY格式）\n")
        f.write(
            f"ssl_key_path = {config_obj.get('SSL', 'ssl_key_path', fallback='ssl/privkey.key')}\n"
        )
        f.write("# 是否仅允许HTTPS访问（true/false）\n")
        f.write("# true：禁止HTTP访问，所有HTTP请求将被重定向到HTTPS\n")
        f.write("# false：同时允许HTTP和HTTPS访问\n")
        f.write(
            "# 由于端口具有绑定优先级，只要开启HTTPS，但未开启此选项，HTTP可能仍然无法访问\n"
        )
        f.write(
            f"https_only = {config_obj.get('SSL', 'https_only', fallback='false')}\n\n"
        )


def _create_config_ini():
    """创建或更新config.ini配置文件（兼容旧版本，自动补全缺失参数）"""
    default_config = _get_default_config()

    if os.path.exists("config.ini"):
        print("[配置文件] config.ini 已存在，检查是否需要更新...")
        # 读取现有配置
        existing_config = configparser.ConfigParser()
        try:
            # 读取配置时保持大小写（如果后续需要区分的话，但主要问题在检查）
            existing_config.optionxform = str
            existing_config.read("config.ini", encoding="utf-8")
        except configparser.DuplicateOptionError as e:
            # 如果读取时就发现重复，直接提示用户手动修复
            print(f"\n[错误] 配置文件 'config.ini' 格式错误，请手动修复:")
            print(f"  - 文件中存在重复的配置项: {e}")
            print(
                f"  - 请打开 config.ini 文件，找到 [{e.section}] 部分，确保 '{e.option}' 只出现一次（不区分大小写）。"
            )
            print(f"  - 修复后重新运行程序。")
            # 可以选择在这里退出程序 sys.exit(1) 或者继续尝试（可能不准确）
            logging.error(f"配置文件读取失败，存在重复项: {e}")
            # 如果选择继续，后面的逻辑可能基于不完整的配置
            # return # 或者直接返回，让程序启动失败

        # 检查并补全缺失的节和参数
        updated = False
        for section in default_config.sections():
            if not existing_config.has_section(section):
                existing_config.add_section(section)
                updated = True
                print(f"[配置文件] 添加新的配置节: {section}")
                # 如果节是新增的，可以直接添加所有默认键值对
                for key, value in default_config.items(section):
                    existing_config.set(section, key, value)
                    print(f"[配置文件] 为新节添加配置项: [{section}] {key} = {value}")
            else:
                # 节已存在，检查缺失的键
                # 获取该节下所有现有 key 的小写形式
                existing_keys_lower = {
                    k.lower() for k in existing_config.options(section)
                }
                for key, value in default_config.items(section):
                    # 检查默认 key 的小写形式是否已存在
                    if key.lower() not in existing_keys_lower:
                        existing_config.set(section, key, value)  # 使用默认的大小写添加
                        updated = True
                        print(
                            f"[配置文件] 添加缺失的配置项: [{section}] {key} = {value}"
                        )

        # 如果有更新，保存配置文件（使用带注释的版本）
        if updated:
            try:
                _write_config_with_comments(existing_config, "config.ini")
                logging.info("配置文件已更新：自动补全缺失参数")
                print("[配置文件] 配置文件已更新并保存（包含详细注释）")
            except Exception as e:
                print(f"[错误] 保存更新后的 config.ini 失败: {e}")
                logging.error(f"保存更新后的 config.ini 失败: {e}")
        else:
            print("[配置文件] 配置文件无需更新")
    else:
        print("[配置文件] config.ini 不存在，创建新配置文件...")
        # 创建新配置文件（带详细注释）
        _write_config_with_comments(default_config, "config.ini")
        print("[配置文件] 配置文件创建完成（包含详细注释）")


def _create_permissions_json():
    """创建默认的permissions.json权限配置文件"""
    if os.path.exists("permissions.json"):
        print("[权限配置] permissions.json 已存在，跳过创建")
        return

    print("[权限配置] 创建新的 permissions.json 文件...")
    permissions = {
        "permission_groups": {
            "guest": {
                "name": "游客",
                "is_system": True,  # 系统预设权限组，不可删除
                "permissions": {
                    # 基础权限
                    "view_tasks": True,
                    "create_tasks": False,
                    "delete_tasks": False,
                    "start_tasks": True,
                    "stop_tasks": True,
                    # 地图权限
                    "view_map": True,
                    "record_path": True,
                    "auto_generate_path": True,
                    # 通知权限
                    "view_notifications": True,
                    "mark_notifications_read": False,
                    # 用户权限
                    "view_user_details": True,
                    "modify_user_settings": False,
                    # 多账号和签到
                    "execute_multi_account": False,
                    "use_attendance": False,
                    # 日志权限
                    "view_logs": False,
                    "clear_logs": False,
                    # 新增细分权限
                    "auto_fill_password": False,  # 查看全部 school_account
                    "import_offline": True,
                    "export_data": True,
                    "modify_params": True,
                    "manage_own_sessions": False,  # 管理自己的会话（游客默认不能）
                    # UI按钮权限（细粒度控制）
                    "use_login_button": True,  # 登录按钮（游客默认有）
                    "use_multi_account_button": False,  # 多账号控制台按钮（游客默认无）
                    "use_import_button": False,  # 导入离线文件按钮（游客默认无）
                    # 留言板权限
                    "view_messages": True,  # 查看留言
                    "post_messages": True,  # 发表留言（游客需填写邮箱和昵称）
                    "delete_own_messages": False,  # 删除自己的留言（游客不能删除）
                    "delete_any_messages": False,  # 删除任何人的留言（游客不能）
                    "modify_config": False,  # 修改配置文件
                },
            },
            "user": {
                "name": "普通用户",
                "is_system": True,  # 系统预设权限组，不可删除
                "permissions": {
                    # 基础权限
                    "view_tasks": True,
                    "create_tasks": True,
                    "delete_tasks": True,
                    "start_tasks": True,
                    "stop_tasks": True,
                    # 地图权限
                    "view_map": True,
                    "record_path": True,
                    "auto_generate_path": True,
                    # 通知权限
                    "view_notifications": True,
                    "mark_notifications_read": True,
                    # 用户权限
                    "view_user_details": True,
                    "modify_user_settings": True,
                    # 多账号和签到
                    "execute_multi_account": True,
                    "use_attendance": True,
                    # 日志权限
                    "view_logs": False,
                    "clear_logs": False,
                    # 新增细分权限
                    "auto_fill_password": False,  # 查看全部 school_account（普通用户默认无此权限）
                    "import_offline": True,
                    "export_data": True,
                    "modify_params": True,
                    "manage_own_sessions": True,  # 管理自己的会话
                    # UI按钮权限（细粒度控制）
                    "use_login_button": True,  # 登录按钮
                    "use_multi_account_button": False,  # 多账号控制台按钮（新用户默认关闭）
                    "use_import_button": False,  # 导入离线文件按钮（新用户默认关闭）
                    # 留言板权限
                    "view_messages": True,  # 查看留言
                    "post_messages": True,  # 发表留言
                    "delete_own_messages": True,  # 删除自己的留言
                    "delete_any_messages": False,  # 删除任何人的留言（仅管理员）
                    # "execute_single_account": True,  # 退出单账号模式
                    "modify_config": True,  # 修改配置文件
                    "view_session_details": True,
                },
            },
            "admin": {
                "name": "管理员",
                "is_system": True,  # 系统预设权限组，不可删除
                "permissions": {
                    # 基础权限
                    "view_tasks": True,
                    "create_tasks": True,
                    "delete_tasks": True,
                    "start_tasks": True,
                    "stop_tasks": True,
                    # 地图权限
                    "view_map": True,
                    "record_path": True,
                    "auto_generate_path": True,
                    # 通知权限
                    "view_notifications": True,
                    "mark_notifications_read": True,
                    # 用户权限
                    "view_user_details": True,
                    "modify_user_settings": True,
                    # 多账号和签到
                    "execute_multi_account": True,
                    "use_attendance": True,
                    # 日志权限
                    "view_logs": True,
                    "clear_logs": True,
                    # 管理权限
                    "manage_users": True,
                    "manage_permissions": True,
                    "reset_user_password": True,
                    "view_audit_logs": True,
                    "view_all_sessions": True,
                    "force_logout_users": True,
                    # 新增细分权限
                    "auto_fill_password": True,
                    "import_offline": True,
                    "export_data": True,
                    "modify_params": True,
                    "manage_own_sessions": True,
                    "manage_user_sessions": True,  # 管理其他用户的会话
                    "view_session_details": True,
                    # UI按钮权限（细粒度控制）
                    "use_login_button": True,  # 登录按钮
                    "use_multi_account_button": True,  # 多账号控制台按钮
                    "use_import_button": True,  # 导入离线文件按钮
                    # 留言板权限
                    "view_messages": True,  # 查看留言
                    "post_messages": True,  # 发表留言
                    "delete_own_messages": True,  # 删除自己的留言
                    "delete_any_messages": True,  # 删除任何人的留言（管理员）
                    "view_captcha_history": True,
                    # "execute_single_account": True,  # 退出单账号模式
                    "modify_config": True,  # 修改配置文件
                },
            },
            "super_admin": {
                "name": "超级管理员",
                "is_system": True,  # 系统预设权限组，不可删除
                "permissions": {
                    # 基础权限
                    "view_tasks": True,
                    "create_tasks": True,
                    "delete_tasks": True,
                    "start_tasks": True,
                    "stop_tasks": True,
                    # 地图权限
                    "view_map": True,
                    "record_path": True,
                    "auto_generate_path": True,
                    # 通知权限
                    "view_notifications": True,
                    "mark_notifications_read": True,
                    # 用户权限
                    "view_user_details": True,
                    "modify_user_settings": True,
                    # 多账号和签到
                    "execute_multi_account": True,
                    "use_attendance": True,
                    # 日志权限
                    "view_logs": True,
                    "clear_logs": True,
                    # 管理权限
                    "manage_users": True,
                    "manage_permissions": True,
                    "reset_user_password": True,
                    "view_audit_logs": True,
                    "view_all_sessions": True,
                    "force_logout_users": True,
                    "manage_system": True,
                    "create_permission_groups": True,
                    "delete_permission_groups": True,
                    "modify_permission_groups": True,
                    # 新增细分权限
                    "auto_fill_password": True,
                    "import_offline": True,
                    "export_data": True,
                    "modify_params": True,
                    "manage_own_sessions": True,
                    "manage_user_sessions": True,
                    "view_captcha_history": True,
                    "view_session_details": True,
                    "god_mode": True,  # 查看所有会话：可以查看和销毁所有会话
                    # UI按钮权限（细粒度控制）
                    "use_login_button": True,  # 登录按钮
                    "use_multi_account_button": True,  # 多账号控制台按钮
                    "use_import_button": True,  # 导入离线文件按钮
                    # 留言板权限
                    "view_messages": True,  # 查看留言
                    "post_messages": True,  # 发表留言
                    "delete_own_messages": True,  # 删除自己的留言
                    "delete_any_messages": True,  # 删除任何人的留言（管理员）
                    # "execute_single_account": True,  # 退出单账号模式
                    "modify_config": True,  # 修改配置文件
                },
            },
        },
        "user_groups": {},
        "user_custom_permissions": {},  # 用户差分权限存储：{username: {added: [], removed: []}}
    }

    with open("permissions.json", "w", encoding="utf-8") as f:
        json.dump(permissions, f, indent=2, ensure_ascii=False)
    print("[权限配置] permissions.json 文件创建完成")


def _create_default_admin():
    """创建默认的管理员账号"""
    admin_dir = "system_accounts"  # 修正：系统账号独立存储
    if not os.path.exists(admin_dir):
        os.makedirs(admin_dir, exist_ok=True)
        print(f"[管理员账号] 创建目录: {admin_dir}")

    # 使用用户名的哈希作为文件名
    username = "admin"
    filename = hashlib.sha256(username.encode()).hexdigest()
    admin_file = os.path.join(admin_dir, f"{filename}.json")

    if os.path.exists(admin_file):
        print("[管理员账号] 默认管理员账号已存在，跳过创建")
        logging.info(
            f"[系统初始化] 管理员账号已存在 --> 文件路径: {admin_file}, 跳过创建流程"
        )
        return

    print("[管理员账号] 创建默认管理员账号 (用户名: admin, 密码: admin)...")
    logging.info(
        f"[系统初始化] 开始创建默认管理员账号 --> 用户名: admin, 密码: admin (⚠️ 建议首次登录后立即修改), 权限组: super_admin, 文件路径: {admin_file}"
    )
    # 创建默认管理员账户数据，包含所有必要字段
    # 新增字段：phone（手机号）、nickname（昵称）、avatar_url（头像URL）
    admin_data = {
        "auth_username": "admin",  # 管理员登录用户名
        "password": "admin",  # 默认密码
        "group": "super_admin",  # 权限组：超级管理员
        "created_at": time.time(),  # 创建时间戳
        "last_login": None,  # 最后登录时间
        "session_ids": [],  # 活跃会话ID列表
        "2fa_enabled": False,  # 双因素认证开关
        "2fa_secret": None,  # 双因素认证密钥
        "avatar_url": "default_avatar.png",  # 默认头像文件名
        "max_sessions": -1,  # 最大并发会话数
        "theme": "light",  # 界面主题
        "phone": "",  # 手机号
        "nickname": "超级管理员",  # 显示昵称
    }

    with open(admin_file, "w", encoding="utf-8") as f:
        json.dump(admin_data, f, indent=2, ensure_ascii=False)
    print("[管理员账号] 默认管理员账号创建完成")
    logging.info(
        f"[系统初始化] 管理员账号创建成功 --> 文件路径: {admin_file}, 账号信息: 用户名=admin, 权限组=super_admin, 双因素认证=未启用, 最大会话数=无限制, 主题=light"
    )


def get_session_file_path(session_id: str) -> str:
    """根据 session_id (UUID) 计算会话文件的完整路径"""
    session_hash = hashlib.sha256(session_id.encode()).hexdigest()
    return os.path.join(SESSION_STORAGE_DIR, f"{session_hash}.json")


# ==============================================================================
# 认证和权限管理系统
# ==============================================================================


class AuthSystem:
    """用户认证和权限管理系统"""

    def __init__(self):
        logging.info("=" * 80)
        logging.info("初始化AuthSystem认证系统...")
        self.config = self._load_config()
        logging.info("配置文件已加载")
        self.permissions = self._load_permissions()
        logging.info("权限配置已加载")
        self.lock = threading.Lock()  # 使用Lock代替Semaphore(1)以提升性能
        logging.info("线程锁已创建（使用threading.Lock）")
        # 在系统初始化时，立即同步超级管理员权限
        self._synchronize_super_admin_permissions()
        logging.info("AuthSystem初始化完成")
        logging.info("=" * 80)

    def _load_config(self):
        """加载配置文件（增强：处理重复项错误并提示用户修复）"""
        logging.debug("_load_config: 开始加载配置文件...")
        # 首先确保配置文件结构是最新的（尝试补全缺失项）
        # 注意：如果 _create_config_ini 内部读取失败，它应该已打印错误
        try:
            _create_config_ini()
        except configparser.DuplicateOptionError as e:
            # 如果 _create_config_ini 内部读取时就出错，这里无需再做处理，它已经提示
            # 可以选择在这里直接退出或抛出异常
            logging.error(
                f"[系统初始化] 配置文件检查失败 --> 错误类型: {type(e).__name__}, 错误详情: {e}, 可能原因: 配置文件损坏或存在重复选项",
                exc_info=True,
            )
            print(
                f"\n[严重错误] 配置文件 ('config.ini') 已损坏。请修复上述提到的重复选项，然后重新启动程序。"
            )
            sys.exit(1)  # 强制退出，避免使用损坏的配置
        except Exception as e:
            logging.error(
                f"[系统初始化] 配置文件检查时发生未知错误 --> 错误类型: {type(e).__name__}, 错误详情: {e}",
                exc_info=True,
            )
            print(
                f"\n[严重错误] 检查配置文件 'config.ini' 时发生意外错误: {e}\n请检查文件格式是否正确，然后重新启动程序。"
            )
            sys.exit(1)  # 强制退出

        # 现在尝试正式加载配置供 AuthSystem 使用
        config = configparser.ConfigParser()
        # 尝试保留大小写读取，有助于调试，但 configparser 默认行为仍可能合并
        config.optionxform = str
        try:
            config.read(CONFIG_FILE, encoding="utf-8")
            logging.debug(
                f"_load_config: 配置文件加载完成，配置节: {list(config.sections())}"
            )
            return config
        except configparser.DuplicateOptionError as e:
            # !!! 捕获重复项错误 !!!
            logging.error(
                f"加载配置文件 '{CONFIG_FILE}' 失败，存在重复的配置项: {e}",
                exc_info=True,
            )
            print(f"\n{'='*60}")
            print(f"[配置文件错误] 无法加载 config.ini 文件！")
            print(
                f"  错误原因: 在区域 [{e.section}] 中发现重复的选项 '{e.option}' (不区分大小写)."
            )
            print(f"  错误位置: 大约在文件的第 {e.lineno} 行附近.")
            print(f"\n  请手动打开文件 '{CONFIG_FILE}' 并进行以下操作:")
            print(f"    1. 找到 [{e.section}] 区域.")
            print(
                f"    2. 确保选项 '{e.option}' (例如 LastUser 或 lastuser) 只出现一次."
            )
            print(f"    3. 删除重复的那一行.")
            print(f"    4. 保存文件后重新运行程序.")
            print(f"{'='*60}\n")
            # 强制退出程序，因为配置无法加载
            sys.exit(1)
        except Exception as e:
            # 捕获其他可能的读取错误
            logging.error(
                f"加载配置文件 '{CONFIG_FILE}' 时发生未知错误: {e}", exc_info=True
            )
            print(f"\n[配置文件错误] 读取 config.ini 文件时发生意外错误: {e}")
            print(f"  请检查文件是否存在、是否有读取权限以及格式是否基本正确。")
            sys.exit(1)

    def find_user_by_phone(self, phone):
        """
        遍历所有系统账号，查找绑定了特定手机号的用户。

        参数:
            phone (str): 要查找的手机号。

        返回:
            str: 绑定的用户名，如果未找到则返回 None。
        """
        # 仅在 system_accounts_dir 中查找，因为学校账号是导入的，不参与系统认证
        accounts_dir = SYSTEM_ACCOUNTS_DIR
        if not os.path.exists(accounts_dir):
            return None

        for filename in os.listdir(accounts_dir):
            if filename.endswith(".json"):
                user_file = os.path.join(accounts_dir, filename)
                try:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)
                        if user_data.get("phone") == phone:
                            return user_data.get("auth_username")
                except Exception:
                    continue  # 跳过损坏的文件
        return None

    def unbind_phone_from_user(self, phone, except_username=None):
        """
        查找绑定了指定手机号的用户，并将其手机号字段清空。

        参数:
            phone (str): 要解绑的手机号。
            except_username (str, 可选): 如果找到的用户是此用户，则不解绑。
        """
        if not phone:
            return

        bound_username = self.find_user_by_phone(phone)

        if bound_username and bound_username != except_username:
            logging.info(
                f"[手机号解绑] 手机号 {phone} 原本绑定在 {bound_username}。正在解绑..."
            )
            user_file = self.get_user_file_path(bound_username)
            if os.path.exists(user_file):
                try:
                    # 使用 AuthSystem 的锁确保文件操作安全
                    with self.lock:
                        with open(user_file, "r", encoding="utf-8") as f:
                            user_data = json.load(f)

                        if user_data.get("phone") == phone:
                            user_data["phone"] = ""  # 清空手机号
                            with open(user_file, "w", encoding="utf-8") as f:
                                json.dump(user_data, f, indent=2, ensure_ascii=False)
                            logging.info(
                                f"[手机号解绑] 已成功解绑用户 {bound_username} 的手机号。"
                            )

                            # 记录审计日志
                            self.log_audit(
                                "System",
                                "auto_unbind_phone",
                                f"因手机号 {phone} 被新用户注册或绑定，系统自动解绑了用户 {bound_username} 的手机号",
                            )
                except Exception as e:
                    logging.error(
                        f"[手机号解绑] 解绑用户 {bound_username} 手机号失败: {e}",
                        exc_info=True,
                    )

    def _load_permissions(self):
        """加载权限配置"""
        logging.debug(f"_load_permissions: 检查权限文件: {PERMISSIONS_FILE}")
        if os.path.exists(PERMISSIONS_FILE):
            with open(PERMISSIONS_FILE, "r", encoding="utf-8") as f:
                perms = json.load(f)
            logging.debug(
                f"_load_permissions: 权限配置已加载，权限组数: {len(perms.get('permission_groups', {}))}, 用户组数: {len(perms.get('user_groups', {}))}"
            )
            return perms
        logging.debug("_load_permissions: 权限文件不存在，使用默认配置")
        return {"permission_groups": {}, "user_groups": {}}

    def _save_permissions(self):
        """保存权限配置"""
        logging.debug("_save_permissions: 保存权限配置到文件...")
        # 不使用 self.lock，因为调用者可能已经持有锁
        # 调用者负责确保线程安全
        with open(PERMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.permissions, f, indent=2, ensure_ascii=False)
        logging.debug(f"_save_permissions: 权限配置已保存到 {PERMISSIONS_FILE}")

    def get_user_file_path(self, auth_username):
        """获取用户文件路径"""
        user_hash = hashlib.sha256(auth_username.encode()).hexdigest()
        file_path = os.path.join(SYSTEM_ACCOUNTS_DIR, f"{user_hash}.json")
        logging.debug(
            f"get_user_file_path: 用户 {auth_username} 的文件路径: {file_path}"
        )
        return file_path

    def _update_user_file_group(self, username, new_group):
        """
        (辅助函数) 更新 system_accounts 中用户JSON文件内的 group 字段。
        这确保了 permissions.json 和用户文件之间的数据一致性。
        """
        user_file = self.get_user_file_path(username)
        if os.path.exists(user_file):
            try:
                # 注意：这里在 AuthSystem 的 self.lock 锁内部调用，
                # 但文件IO本身是原子的，为避免死锁风险，不重复获取锁。
                # 或者，更安全的做法是要求调用者必须持有 self.lock。
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                if user_data.get("group") != new_group:
                    user_data["group"] = new_group
                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2, ensure_ascii=False)
                    logging.debug(
                        f"[权限同步] 已更新用户文件 {os.path.basename(user_file)} 的权限组为 {new_group}"
                    )
                    return True
            except Exception as e:
                logging.error(
                    f"[权限同步] 更新用户文件 {os.path.basename(user_file)} 失败: {e}",
                    exc_info=True,
                )
        else:
            logging.warning(
                f"[权限同步] 找不到用户 {username} 的文件，无法更新其文件内的权限组。"
            )
        return False

    def _get_password_storage_method(self):
        """
        获取密码存储方式配置。

        从config.ini的[Security]节读取password_storage配置项：
        - 'plaintext': 明文存储（默认，不安全）
        - 'encrypted': SHA256哈希存储

        ⚠️ 安全警告：
        - 默认为plaintext，密码完全可见
        - encrypted模式使用SHA256但不加盐，仍不够安全

        💡 建议改进：
        - 添加bcrypt或argon2选项
        - 强制encrypted模式，禁止plaintext
        - 密码哈希应使用慢速算法+随机盐

        返回:
            str: 'plaintext' 或 'encrypted'
        """
        method = self.config.get("Security", "password_storage", fallback="plaintext")
        logging.debug(f"_get_password_storage_method: 密码存储方式: {method}")
        return method

    def _encrypt_password(self, password):
        """
        加密密码（根据配置决定是否加密）。

        加密方式：
        - plaintext: 不加密，直接返回原密码（已废弃，不推荐）
        - encrypted: 使用SHA256哈希（已废弃，仅用于向后兼容）
        - bcrypt: 使用bcrypt算法（推荐，自动加盐，抗暴力破解）

        ⚠️ 安全说明：
        1. bcrypt自动生成随机盐并嵌入到哈希中
        2. bcrypt计算慢，抗GPU/ASIC暴力破解
        3. 每次加密相同密码产生不同哈希（因为盐不同）
        4. SHA256模式仅用于向后兼容旧密码

        参数:
            password (str): 明文密码

        返回:
            str: 加密后的密码（或明文）

        示例:
            >>> _encrypt_password("admin")
            # bcrypt模式: "$2b$12$abcd..."（60字符）
            # SHA256模式（旧）: "8c6976e5b5..."（64字符）
            # plaintext模式（极不安全）: "admin"
        """
        method = self._get_password_storage_method()
        logging.debug(
            f"[密码加密] 开始处理密码加密 --> 加密方法: {method}, 密码长度: {len(password)}字符"
        )

        if method == "bcrypt":
            # 使用bcrypt加密（推荐方式）
            try:

                # bcrypt.gensalt() 自动生成随机盐
                # 默认cost=12，可以通过rounds参数调整
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
                # bcrypt返回bytes，需要解码为字符串存储
                encrypted = hashed.decode("utf-8")
                logging.debug(
                    f"[密码加密] 密码已使用bcrypt加密 --> 哈希长度: {len(encrypted)}字符, 哈希前缀: {encrypted[:7]}... (✓ 安全: 自动加盐，抗暴力破解)"
                )
                return encrypted
            except ImportError:
                logging.error(
                    "[密码加密] bcrypt库未安装，无法使用bcrypt加密。请运行: pip install bcrypt"
                )
                logging.warning("[密码加密] 降级使用SHA256加密（不安全）")
                # 降级到SHA256
                method = "encrypted"

        if method == "encrypted":
            # SHA256哈希（仅用于向后兼容）
            # 为了向后兼容，对旧的SHA256哈希添加简单的盐值支持
            # 使用用户名的哈希作为盐（不完美但比无盐好）
            # 注：这只是临时方案，新密码应使用bcrypt
            encrypted = hashlib.sha256(password.encode()).hexdigest()
            logging.debug(
                f"[密码加密] 密码已使用SHA256加密 --> 哈希长度: {len(encrypted)}字符, 哈希值前8位: {encrypted[:8]}... (⚠️ 警告: SHA256不加盐存在安全风险，建议迁移到bcrypt)"
            )
            return encrypted

        # plaintext模式（不推荐）
        logging.warning(
            f"[密码加密] 使用明文存储密码 --> ⚠️ 严重安全警告: 明文密码存储极度不安全，强烈建议使用bcrypt模式"
        )
        return password  # 明文返回

    def _verify_password(self, input_password, stored_password):
        """
        验证用户输入的密码是否正确。

        验证流程：
        1. 自动检测存储密码的格式（bcrypt/SHA256/plaintext）
        2. bcrypt模式：使用bcrypt.checkpw()验证（推荐）
        3. encrypted模式：使用secrets.compare_digest()常量时间比较
        4. plaintext模式：使用secrets.compare_digest()比较（不推荐）

        ✓ 安全改进：
        1. 使用secrets.compare_digest()防止时序攻击
        2. 支持bcrypt自动验证（包含盐值检查）
        3. 常量时间比较，响应时间不泄露密码信息
        4. 自动检测密码格式，兼容旧密码

        参数:
            input_password (str): 用户输入的密码（明文）
            stored_password (str): 存储的密码（明文/SHA256哈希/bcrypt哈希）

        返回:
            bool: True表示密码正确，False表示密码错误

        安全特性：
        - 无论密码对错，响应时间基本相同（常量时间）
        - 防止通过响应时间分析推测密码
        """
        logging.debug(
            f"[密码验证] 开始验证密码 --> 输入密码长度: {len(input_password)}字符, 存储密码长度: {len(stored_password)}字符"
        )

        # 自动检测存储密码的格式
        # bcrypt哈希格式: $2b$12$... (60字符，以$2b$或$2a$开头)
        # SHA256哈希格式: 64个十六进制字符
        # plaintext: 其他

        if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
            # bcrypt格式密码
            try:

                # bcrypt.checkpw自动处理盐值验证，内部使用常量时间比较
                result = bcrypt.checkpw(
                    input_password.encode("utf-8"), stored_password.encode("utf-8")
                )
                logging.debug(
                    f"[密码验证] bcrypt验证完成 --> 验证结果: {'✓ 成功' if result else '✗ 失败'} (✓ 安全: 使用bcrypt.checkpw，防时序攻击)"
                )
                return result
            except ImportError:
                logging.error("[密码验证] bcrypt库未安装，无法验证bcrypt密码")
                return False
            except Exception as e:
                logging.error(f"[密码验证] bcrypt验证失败 --> 错误: {e}")
                return False

        elif len(stored_password) == 64 and all(
            c in "0123456789abcdef" for c in stored_password.lower()
        ):
            # SHA256格式密码（64个十六进制字符）
            input_hash = hashlib.sha256(input_password.encode()).hexdigest()
            # ✓ 使用secrets.compare_digest()进行常量时间比较，防止时序攻击
            result = secrets.compare_digest(input_hash, stored_password)
            logging.debug(
                f"[密码验证] SHA256哈希验证完成 --> 输入密码哈希前8位: {input_hash[:8]}..., 存储密码哈希前8位: {stored_password[:8]}..., 验证结果: {'✓ 成功' if result else '✗ 失败'} (✓ 安全: 使用secrets.compare_digest防时序攻击)"
            )
            return result

        else:
            # plaintext格式（不推荐）
            # ✓ 即使是明文，也使用secrets.compare_digest()防止时序攻击
            result = secrets.compare_digest(input_password, stored_password)
            logging.warning(
                f"[密码验证] 明文密码验证完成 --> 验证结果: {'✓ 成功' if result else '✗ 失败'}"
            )
            return result

    def _log_login_attempt(
        self, auth_username, success, ip_address="", user_agent="", reason=""
    ):
        """
        记录用户登录尝试到日志文件。

        记录的信息：
        - timestamp: Unix时间戳（秒）
        - datetime: ISO格式的时间字符串
        - username: 登录的用户名
        - success: 是否成功（True/False）
        - ip_address: 客户端IP地址
        - user_agent: 浏览器User-Agent字符串
        - reason: 失败原因（如"密码错误"、"账号锁定"）

        存储格式：
        - JSONL（JSON Lines）：每行一个完整的JSON对象
        - 优点：便于流式处理、追加写入、逐行解析
        - 文件：logs/login_history.jsonl

        用途：
        1. 安全审计：追踪异常登录行为
        2. 入侵检测：识别暴力破解尝试
        3. 合规要求：满足审计日志要求
        4. 问题排查：帮助用户找回登录失败原因

        ⚠️ 潜在问题：
        1. 日志文件无限增长，没有轮转机制
        2. 敏感信息（用户名、IP）明文存储
        3. 文件I/O可能成为性能瓶颈
        4. 并发写入可能导致行混乱（虽然概率低）

        💡 改进建议：
        - 实现日志轮转（按大小或时间）
        - 使用日志库的RotatingFileHandler
        - 考虑异步写入（避免阻塞主线程）
        - 添加日志归档和压缩功能

        参数:
            auth_username (str): 尝试登录的用户名
            success (bool): 登录是否成功
            ip_address (str): 客户端IP地址
            user_agent (str): HTTP User-Agent头
            reason (str): 失败原因描述
        """
        logging.info(
            f"[登录审计] 登录尝试记录 --> 用户名: {auth_username}, 登录结果: {'✓ 成功' if success else '✗ 失败'}, 客户端IP: {ip_address}, User-Agent: {user_agent[:50]}{'...' if len(user_agent) > 50 else ''}, {'失败原因: ' + reason if not success else '登录成功'}"
        )

        # 构建日志条目（字典）
        log_entry = {
            "timestamp": time.time(),  # 精确到毫秒的时间戳
            "datetime": datetime.datetime.now().isoformat(),  # 可读的时间字符串
            "username": auth_username,
            "success": success,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "reason": reason,
        }

        try:
            # 追加模式打开文件，每次写入一行JSON
            # ensure_ascii=False: 允许中文字符
            # 每条记录以换行符结束
            with open(LOGIN_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            logging.debug(
                f"[登录审计] 登录日志已写入文件 --> 文件路径: {LOGIN_LOG_FILE}, 用户: {auth_username}, 时间戳: {log_entry['timestamp']}, 格式: JSONL (每行一个JSON对象)"
            )
        except Exception as e:
            # 日志写入失败不应该影响登录流程
            # 只记录错误但不抛出异常
            logging.error(
                f"[登录审计] 写入登录日志失败 --> 目标文件: {LOGIN_LOG_FILE}, 用户: {auth_username}, 错误类型: {type(e).__name__}, 错误详情: {e}, 注意: 日志写入失败不影响登录流程继续执行",
                exc_info=True,
            )

    def get_login_history(self, username=None, limit=100):
        """获取登录历史 - 优化：避免加载所有记录到内存"""
        if not os.path.exists(LOGIN_LOG_FILE):
            return []

        # 优化：使用双端队列存储最近的记录，避免列表频繁扩展
        # collections已在标准库导入中全局导入
        history = collections.deque(maxlen=limit * 2)  # 预留2倍空间用于过滤

        try:
            with open(LOGIN_LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if username is None or entry.get("username") == username:
                            history.append(entry)
                    except json.JSONDecodeError as e:
                        # 跳过损坏的日志行，继续读取下一行
                        logging.warning(
                            f"[登录审计] 跳过损坏的日志行 --> 行内容: {line.strip()[:100]}{'...' if len(line.strip()) > 100 else ''}, JSON解析错误: {e}"
                        )
                        continue
                    except Exception as e:
                        # 捕获其他意外错误
                        logging.warning(
                            f"[登录审计] 处理日志行时发生错误 --> 行内容: {line.strip()[:100]}{'...' if len(line.strip()) > 100 else ''}, 错误类型: {type(e).__name__}, 错误详情: {e}"
                        )
                        continue
        except Exception as e:
            logging.error(
                f"[登录审计] 读取登录历史失败 --> 文件路径: {LOGIN_LOG_FILE}, 查询用户: {username if username else '全部'}, 限制条数: {limit}, 错误类型: {type(e).__name__}, 错误详情: {e}",
                exc_info=True,
            )

        # 返回最近的记录 - 转换为列表并限制数量
        result = list(history)[-limit:]
        return result

    def check_brute_force(self, auth_username, ip_address):
        """检查暴力破解（5分钟内最多5次失败）- 优化：找到足够记录后提前退出"""
        recent_attempts = []
        current_time = time.time()
        cutoff_time = current_time - 300  # 5分钟前
        MAX_ATTEMPTS = 5  # 定义为常量

        if os.path.exists(LOGIN_LOG_FILE):
            try:
                with open(LOGIN_LOG_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("timestamp", 0) > cutoff_time:
                                if (
                                    entry.get("username") == auth_username
                                    or entry.get("ip_address") == ip_address
                                ):
                                    if not entry.get("success", False):
                                        recent_attempts.append(entry)
                                        # 优化：找到超过阈值的失败尝试后立即返回
                                        if len(recent_attempts) >= MAX_ATTEMPTS:
                                            return (
                                                True,
                                                "登录失败次数过多，请5分钟后再试",
                                            )
                        except json.JSONDecodeError as e:
                            # 跳过损坏的日志行
                            logging.debug(
                                f"[安全检查] 暴力破解检查时跳过损坏的日志行 --> JSON解析错误: {e}"
                            )
                            continue
                        except Exception as e:
                            logging.debug(
                                f"[安全检查] 暴力破解检查时处理日志行错误 --> 错误类型: {type(e).__name__}, 错误详情: {e}"
                            )
                            continue
            except Exception as e:
                logging.error(
                    f"[安全检查] 检查暴力破解失败 --> 目标用户: {auth_username}, IP地址: {ip_address}, 时间窗口: 5分钟, 错误类型: {type(e).__name__}, 错误详情: {e}",
                    exc_info=True,
                )

        # 如果5分钟内失败次数未超过阈值，返回正常
        return False, ""

    def generate_2fa_secret(self, auth_username):
        """生成2FA密钥"""
        try:

            secret = pyotp.random_base32()

            user_file = self.get_user_file_path(auth_username)
            if os.path.exists(user_file):
                with self.lock:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)

                    user_data["2fa_secret"] = secret
                    user_data["2fa_enabled"] = False  # 初始未启用，需要验证后启用

                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2, ensure_ascii=False)

                # 生成二维码URI
                totp = pyotp.TOTP(secret)
                uri = totp.provisioning_uri(
                    name=auth_username, issuer_name="Zelly's Personal Assistant Tools"
                )
                return {"success": True, "secret": secret, "qr_uri": uri}
            return {"success": False, "message": "用户不存在"}
        except ImportError:
            return {
                "success": False,
                "message": "2FA功能需要安装pyotp库：pip install pyotp",
            }

    def enable_2fa(self, auth_username, verification_code):
        """启用2FA（需要验证一次）"""
        try:

            user_file = self.get_user_file_path(auth_username)
            if os.path.exists(user_file):
                with self.lock:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)

                    secret = user_data.get("2fa_secret")
                    if not secret:
                        return {"success": False, "message": "请先生成2FA密钥"}

                    totp = pyotp.TOTP(secret)
                    if totp.verify(verification_code):
                        user_data["2fa_enabled"] = True
                        with open(user_file, "w", encoding="utf-8") as f:
                            json.dump(user_data, f, indent=2, ensure_ascii=False)
                        return {"success": True, "message": "2FA已启用"}
                    return {"success": False, "message": "验证码错误"}
            return {"success": False, "message": "用户不存在"}
        except ImportError:
            return {"success": False, "message": "2FA功能需要安装pyotp库"}

    def verify_2fa(self, auth_username, verification_code):
        """验证2FA代码"""
        try:

            user_file = self.get_user_file_path(auth_username)
            if os.path.exists(user_file):
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                if not user_data.get("2fa_enabled", False):
                    return True  # 2FA未启用，直接通过

                secret = user_data.get("2fa_secret")
                if not secret:
                    return False

                totp = pyotp.TOTP(secret)
                return totp.verify(verification_code)
            return False
        except ImportError:
            logging.warning("2FA验证失败：pyotp库未安装")
            return True  # 如果库未安装，允许通过

    def register_user(
        self,
        auth_username,
        auth_password,
        group="user",
        phone="",
        nickname="",
        avatar_url="",
    ):
        """
        注册新用户（已升级支持扩展字段）

        参数：
        - auth_username: 用户名（必填，唯一标识）
        - auth_password: 密码（必填，将根据配置加密存储）
        - group: 权限组（默认'user'）
        - phone: 手机号（可选）
        - nickname: 昵称（可选，默认为用户名）
        - avatar_url: 头像URL（可选，默认为空）

        返回：
        - success: 是否成功
        - message: 提示信息
        """
        logging.info(f"register_user: 开始注册新用户: {auth_username}, 权限组: {group}")
        print(f"[用户注册] 开始注册新用户: {auth_username}, 权限组: {group}")
        with self.lock:
            if phone:
                self.unbind_phone_from_user(phone, except_username=auth_username)
            user_file = self.get_user_file_path(auth_username)
            logging.debug(f"register_user: 检查用户文件是否存在: {user_file}")
            if os.path.exists(user_file):
                logging.warning(f"register_user: 用户名已存在: {auth_username}")
                print(f"[用户注册] 用户名已存在: {auth_username}")
                return {"success": False, "message": "用户名已存在"}

            # 根据配置选择密码存储方式
            logging.debug(f"register_user: 加密密码...")
            print(f"[用户注册] 加密密码...")
            stored_password = self._encrypt_password(auth_password)

            # 创建用户数据，包含扩展字段
            user_data = {
                "auth_username": auth_username,  # 用户名（登录凭证）
                "password": stored_password,  # 加密后的密码
                "group": group,  # 权限组
                "created_at": time.time(),  # 创建时间戳
                "last_login": None,  # 最后登录时间（初始为空）
                "session_ids": [],  # 用于关联用户的会话ID列表
                "2fa_enabled": False,  # 双因素认证开关
                "2fa_secret": None,  # 双因素认证密钥
                "avatar_url": avatar_url or "default_avatar.png",  # 用户头像URL（新增）
                "max_sessions": 1,  # 允许的最大会话数量 (1=单会话, >1=多会话, -1=无限制)
                "theme": "light",  # 主题偏好：light/dark
                "phone": phone,  # 手机号（新增，用于登录和通知）
                "nickname": nickname or auth_username,  # 显示昵称（新增，用于前端展示）
            }

            logging.debug(f"register_user: 保存用户数据到文件: {user_file}")
            print(f"[用户注册] 保存用户数据到文件...")
            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 添加到权限组
            logging.debug(f"register_user: 添加用户到权限组: {group}")
            self.permissions["user_groups"][auth_username] = group
            self._save_permissions()

            logging.info(
                f"新用户注册: {auth_username} (组: {group}, 手机: {phone}, 昵称: {nickname})"
            )
            print(f"[用户注册] ✓ 用户注册成功: {auth_username} (组: {group})")
            return {"success": True, "message": "注册成功"}

    def authenticate(
        self, auth_username, auth_password, ip_address="", user_agent="", two_fa_code=""
    ):
        """验证用户登录（支持2FA和暴力破解防护）"""
        logging.info(f"authenticate: 开始认证用户: {auth_username}, IP: {ip_address}")
        print(f"[用户认证] 开始认证用户: {auth_username}, IP: {ip_address}")
        with self.lock:
            # 检查是否为游客登录
            if auth_username == "guest" and self.config.getboolean(
                "Guest", "allow_guest_login", fallback=True
            ):
                logging.info(f"authenticate: 游客登录成功: {auth_username}")
                print(f"[用户认证] 游客登录成功: {auth_username}")
                self._log_login_attempt(
                    auth_username, True, ip_address, user_agent, "guest_login"
                )
                return {
                    "success": True,
                    "auth_username": "guest",
                    "group": "guest",
                    "is_guest": True,
                }

            # 检查暴力破解
            logging.debug(f"authenticate: 检查暴力破解防护: {auth_username}")
            print(f"[用户认证] 检查暴力破解: {auth_username}")
            is_locked, lock_message = self.check_brute_force(auth_username, ip_address)
            if is_locked:
                logging.warning(
                    f"authenticate: 用户被锁定（暴力破解防护）: {auth_username}"
                )
                print(f"[用户认证] 用户被锁定（暴力破解防护）: {auth_username}")
                self._log_login_attempt(
                    auth_username, False, ip_address, user_agent, "brute_force_locked"
                )
                return {"success": False, "message": lock_message}

            user_file = self.get_user_file_path(auth_username)
            logging.debug(f"authenticate: 检查用户文件: {user_file}")
            if not os.path.exists(user_file):
                logging.warning(f"authenticate: 用户不存在: {auth_username}")
                print(f"[用户认证] 用户不存在: {auth_username}")
                self._log_login_attempt(
                    auth_username, False, ip_address, user_agent, "user_not_found"
                )
                return {"success": False, "message": "用户不存在"}

            logging.debug(f"authenticate: 读取用户数据: {auth_username}")
            print(f"[用户认证] 读取用户数据: {auth_username}")
            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            # 检查用户是否被封禁
            if user_data.get("banned", False):
                logging.warning(f"authenticate: 用户已被封禁: {auth_username}")
                print(f"[用户认证] 用户已被封禁: {auth_username}")
                self._log_login_attempt(
                    auth_username, False, ip_address, user_agent, "user_banned"
                )
                return {"success": False, "message": "账号已被封禁，请联系管理员"}

            # 验证密码
            logging.debug(f"authenticate: 验证密码: {auth_username}")
            print(f"[用户认证] 验证密码: {auth_username}")
            if not self._verify_password(auth_password, user_data.get("password")):
                logging.warning(f"authenticate: 密码错误: {auth_username}")
                print(f"[用户认证] 密码错误: {auth_username}")
                self._log_login_attempt(
                    auth_username, False, ip_address, user_agent, "wrong_password"
                )
                return {"success": False, "message": "密码错误"}

            # 验证2FA（如果启用）
            if user_data.get("2fa_enabled", False):
                logging.debug(f"authenticate: 检查2FA验证: {auth_username}")
                print(f"[用户认证] 检查2FA验证: {auth_username}")
                if not two_fa_code:
                    logging.info(f"authenticate: 需要2FA验证码: {auth_username}")
                    print(f"[用户认证] 需要2FA验证码: {auth_username}")
                    # 返回 success: True，并附带 auth_username，以便前端JS正确处理
                    return {
                        "success": True,
                        "message": "需要2FA验证码",
                        "requires_2fa": True,
                        "auth_username": auth_username,
                    }

                if not self.verify_2fa(auth_username, two_fa_code):
                    logging.warning(f"authenticate: 2FA验证失败: {auth_username}")
                    print(f"[用户认证] 2FA验证失败: {auth_username}")
                    self._log_login_attempt(
                        auth_username, False, ip_address, user_agent, "2fa_failed"
                    )
                    return {"success": False, "message": "2FA验证码错误"}

            # 更新最后登录时间
            logging.debug(f"authenticate: 更新最后登录时间: {auth_username}")
            print(f"[用户认证] 更新最后登录时间: {auth_username}")
            user_data["last_login"] = time.time()
            user_data["last_login_ip"] = ip_address
            if "session_ids" not in user_data:
                user_data["session_ids"] = []

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 检查是否为超级管理员
            super_admin = self.config.get("Admin", "super_admin", fallback="admin")
            if auth_username == super_admin:
                group = "super_admin"
            else:
                group = user_data.get("group", "user")

            self._log_login_attempt(
                auth_username, True, ip_address, user_agent, "success"
            )
            logging.info(f"用户登录: {auth_username} (组: {group}) from {ip_address}")
            print(f"[用户认证] ✓ 用户登录成功: {auth_username} (组: {group})")
            logging.info(f"authenticate: ✓ 认证成功，返回用户信息")
            return {
                "success": True,
                "auth_username": auth_username,
                "group": group,
                "is_guest": False,
                "max_sessions": user_data.get("max_sessions", 1),
                "avatar_url": user_data.get("avatar_url") or "default_avatar.png",
                "theme": user_data.get("theme", "light"),
                "session_ids": user_data.get("session_ids", []),
            }

    def check_permission(self, auth_username, permission):
        """检查用户是否有特定权限（支持差分化权限）

        权限计算顺序：
        1. 获取用户所属权限组的基础权限
        2. 应用用户的自定义权限（added/removed）

        重要说明：
        此方法已完全支持 user_custom_permissions 差分授权！
        - 即使用户所在组没有某权限，也可以通过 user_custom_permissions.added 单独授予
        - 即使用户所在组有某权限，也可以通过 user_custom_permissions.removed 单独撤销

        示例：用户 zelly 在 user 组（默认无 use_multi_account_button 权限）
        通过在 permissions.json 中添加：
        {
          "user_custom_permissions": {
            "zelly": {
              "added": ["use_multi_account_button"],
              "removed": []
            }
          }
        }
        该用户即可获得该权限，check_permission 会正确返回 True。
        """
        # 获取用户组（此函数已包含 super_admin 检查）
        group = self.get_user_group(auth_username)

        # 获取组权限（基础权限）
        group_perms = (
            self.permissions["permission_groups"].get(group, {}).get("permissions", {})
        )
        has_permission = group_perms.get(permission, False)

        # 记录组权限检查结果（用于调试）
        logging.debug(
            f"[权限检查] 用户 {auth_username} 的组 {group} 对权限 {permission} 的基础权限: {has_permission}"
        )

        # 应用用户的差分化权限（user_custom_permissions）
        # 这是差分授权的核心：允许在不改变用户组的情况下，为特定用户添加或移除权限
        user_custom = self.permissions.get("user_custom_permissions", {}).get(
            auth_username, {}
        )
        added_perms = user_custom.get("added", [])
        removed_perms = user_custom.get("removed", [])

        # 记录用户自定义权限（用于调试）
        if added_perms or removed_perms:
            logging.debug(
                f"[权限检查] 用户 {auth_username} 的自定义权限 - 添加: {added_perms}, 移除: {removed_perms}"
            )

        # 如果权限在added列表中，则有权限（覆盖组权限）
        if permission in added_perms:
            has_permission = True
            logging.debug(
                f"[权限检查] 用户 {auth_username} 通过 user_custom_permissions.added 获得权限 {permission}"
            )

        # 如果权限在removed列表中，则无权限（覆盖组权限和added）
        if permission in removed_perms:
            has_permission = False
            logging.debug(
                f"[权限检查] 用户 {auth_username} 通过 user_custom_permissions.removed 被撤销权限 {permission}"
            )

        # 记录最终权限结果
        logging.debug(
            f"[权限检查] 最终结果 - 用户 {auth_username} 对权限 {permission}: {has_permission}"
        )

        return has_permission

    def get_user_permissions(self, auth_username):
        """获取用户的完整权限列表（包含差分权限）"""
        # 获取用户组
        group = self.get_user_group(auth_username)

        # 获取组权限
        group_perms = (
            self.permissions["permission_groups"].get(group, {}).get("permissions", {})
        )

        # 复制基础权限
        user_perms = dict(group_perms)

        # 应用差分化权限
        user_custom = self.permissions.get("user_custom_permissions", {}).get(
            auth_username, {}
        )
        added_perms = user_custom.get("added", [])
        removed_perms = user_custom.get("removed", [])

        # 添加额外权限
        for perm in added_perms:
            user_perms[perm] = True

        # 移除权限
        for perm in removed_perms:
            user_perms[perm] = False

        return user_perms

    def set_user_custom_permission(self, auth_username, permission, grant):
        """为用户设置自定义权限（差分化存储）

        Args:
            auth_username: 用户名
            permission: 权限名
            grant: True=授予权限, False=移除权限
        """
        with self.lock:
            # 初始化user_custom_permissions结构
            if "user_custom_permissions" not in self.permissions:
                self.permissions["user_custom_permissions"] = {}

            if auth_username not in self.permissions["user_custom_permissions"]:
                self.permissions["user_custom_permissions"][auth_username] = {
                    "added": [],
                    "removed": [],
                }

            user_custom = self.permissions["user_custom_permissions"][auth_username]

            # 获取用户组的基础权限
            group = self.get_user_group(auth_username)
            group_perms = (
                self.permissions["permission_groups"]
                .get(group, {})
                .get("permissions", {})
            )
            base_has_permission = group_perms.get(permission, False)

            # 根据授予/移除状态更新差分列表
            if grant:
                # 授予权限
                if not base_has_permission:
                    # 基础权限没有，添加到added列表
                    if permission not in user_custom["added"]:
                        user_custom["added"].append(permission)
                    # 从removed列表移除（如果存在）
                    if permission in user_custom["removed"]:
                        user_custom["removed"].remove(permission)
                else:
                    # 基础权限已有，从removed列表移除（如果存在）
                    if permission in user_custom["removed"]:
                        user_custom["removed"].remove(permission)
            else:
                # 移除权限
                if base_has_permission:
                    # 基础权限有，添加到removed列表
                    if permission not in user_custom["removed"]:
                        user_custom["removed"].append(permission)
                    # 从added列表移除（如果存在）
                    if permission in user_custom["added"]:
                        user_custom["added"].remove(permission)
                else:
                    # 基础权限没有，从added列表移除（如果存在）
                    if permission in user_custom["added"]:
                        user_custom["added"].remove(permission)

            self._save_permissions()

            logging.info(f"设置用户 {auth_username} 权限 {permission} = {grant}")
            return {"success": True, "message": "权限已更新"}

    def get_user_group(self, auth_username):
        """获取用户所属组"""
        super_admin = self.config.get("Admin", "super_admin", fallback="admin")
        if auth_username == super_admin:
            return "super_admin"
        return self.permissions["user_groups"].get(auth_username, "guest")

    def update_user_group(self, auth_username, new_group):
        """更新用户组（需要管理员权限）"""
        if new_group == "super_admin":
            return {"success": False, "message": "不允许将用户设置为超级管理员"}
        with self.lock:
            if new_group not in self.permissions["permission_groups"]:
                return {"success": False, "message": "权限组不存在"}

            # 更新用户组映射
            self.permissions["user_groups"][auth_username] = new_group

            # 【修正】清空该用户的差分权限（user_custom_permissions）
            # 切换组后，基础权限变更，之前的差分配置应重置以防冲突
            if (
                "user_custom_permissions" in self.permissions
                and auth_username in self.permissions["user_custom_permissions"]
            ):
                del self.permissions["user_custom_permissions"][auth_username]
                logging.info(
                    f"[权限管理] 用户 {auth_username} 切换到组 {new_group}，已自动清空其自定义差分权限"
                )

            self._save_permissions()

            # 同时更新用户文件
            user_file = self.get_user_file_path(auth_username)
            if os.path.exists(user_file):
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                user_data["group"] = new_group
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

            return {"success": True, "message": "权限组已更新"}

    def create_permission_group(self, group_name, permissions, display_name):
        """创建新的权限组（需要超级管理员权限）"""
        with self.lock:
            if group_name in self.permissions["permission_groups"]:
                return {"success": False, "message": "权限组已存在"}

            self.permissions["permission_groups"][group_name] = {
                "name": display_name,
                "is_system": False,  # 用户创建的权限组可以删除
                "permissions": permissions,
            }
            self._save_permissions()
            return {"success": True, "message": "权限组已创建"}

    def update_permission_group(self, group_name, permissions):
        """更新权限组（需要超级管理员权限）

        注意：系统预设权限组可以修改，但不能删除
        """
        with self.lock:
            if group_name not in self.permissions["permission_groups"]:
                return {"success": False, "message": "权限组不存在"}

            self.permissions["permission_groups"][group_name][
                "permissions"
            ] = permissions
            self._save_permissions()
            return {"success": True, "message": "权限组已更新"}

    def delete_permission_group(self, group_name):
        """删除权限组（需要超级管理员权限）

        注意：不允许删除系统预设权限组（guest、user、admin、super_admin）
        """
        with self.lock:
            if group_name not in self.permissions["permission_groups"]:
                return {"success": False, "message": "权限组不存在"}

            # 检查是否为系统预设权限组
            group_info = self.permissions["permission_groups"][group_name]
            if group_info.get("is_system", False):
                return {"success": False, "message": "不允许删除系统预设权限组"}

            # 检查是否有用户正在使用此权限组
            users_count = sum(
                1 for u, g in self.permissions["user_groups"].items() if g == group_name
            )
            if users_count > 0:
                return {
                    "success": False,
                    "message": f"无法删除：有 {users_count} 个用户正在使用此权限组",
                }

            # 删除权限组
            del self.permissions["permission_groups"][group_name]
            self._save_permissions()

            logging.info(f"权限组已删除: {group_name}")
            return {"success": True, "message": "权限组已删除"}

    def list_users(self):
        """列出所有用户"""
        users = []
        for filename in os.listdir(SYSTEM_ACCOUNTS_DIR):
            if filename.endswith(".json"):
                user_file = os.path.join(SYSTEM_ACCOUNTS_DIR, filename)
                try:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)

                    # 修正：获取IP并查询城市
                    last_ip = user_data.get("last_login_ip", None)
                    last_city = None
                    if last_ip:
                        try:
                            # 调用已移至全局的 get_ip_location
                            last_city = get_ip_location(last_ip)
                        except Exception as ip_e:
                            logging.warning(f"查询IP归属地失败 {last_ip}: {ip_e}")
                            last_city = "查询失败"

                    users.append(
                        {
                            "auth_username": user_data["auth_username"],
                            "nickname": user_data.get("nickname", ""),  # 修正：添加昵称
                            "phone": user_data.get("phone", ""),  # 修正：添加手机号
                            "group": user_data.get("group", "user"),
                            "created_at": user_data.get("created_at"),
                            "last_login": user_data.get("last_login"),
                            "last_login_ip": last_ip,  # 修正：添加IP
                            "last_login_city": last_city,  # 修正：添加城市
                            "2fa_enabled": user_data.get("2fa_enabled", False),
                            "banned": user_data.get("banned", False),
                            "max_sessions": user_data.get("max_sessions", 1),
                        }
                    )
                except Exception as e:
                    logging.error(
                        f"[用户管理] 读取用户文件失败 --> 文件名: {filename}, 文件路径: {user_file}, 错误类型: {type(e).__name__}, 错误详情: {e}, 可能原因: 文件损坏、JSON格式错误或权限不足",
                        exc_info=True,
                    )
        return users

    def get_all_groups(self):
        """获取所有权限组"""
        return self.permissions["permission_groups"]

    def link_session_to_user(self, auth_username, session_id):
        """关联会话ID到用户账号（用于状态恢复）"""
        if auth_username == "guest":
            return  # 游客不关联会话

        # 跳过无效的session_id
        if not session_id or session_id == "null" or session_id.strip() == "":
            logging.debug(
                f"[会话管理] 跳过关联无效会话 --> 会话ID: '{session_id}', 目标用户: {auth_username}, 原因: 会话ID为空、null或仅包含空白字符"
            )
            return

        user_file = self.get_user_file_path(auth_username)
        if os.path.exists(user_file):
            with self.lock:
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                if "session_ids" not in user_data:
                    user_data["session_ids"] = []

                # 添加新会话（如果不存在）
                if session_id not in user_data["session_ids"]:
                    user_data["session_ids"].append(session_id)

                    # 根据max_sessions配置限制会话数量
                    max_sessions = user_data.get("max_sessions", 1)
                    if max_sessions > 0:  # 有限制
                        user_data["session_ids"] = user_data["session_ids"][
                            -max_sessions:
                        ]
                    # max_sessions == -1 时不限制，保留所有会话

                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

    def get_user_sessions(self, auth_username):
        """获取用户关联的会话ID列表"""
        if auth_username == "guest":
            return []

        user_file = self.get_user_file_path(auth_username)
        if os.path.exists(user_file):
            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            return user_data.get("session_ids", [])
        return []

    def unlink_session_from_user(self, auth_username, session_id):
        """取消会话与用户的关联"""
        if auth_username == "guest":
            return

        user_file = self.get_user_file_path(auth_username)
        if os.path.exists(user_file):
            with self.lock:
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                if (
                    "session_ids" in user_data
                    and session_id in user_data["session_ids"]
                ):
                    user_data["session_ids"].remove(session_id)

                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2, ensure_ascii=False)

    def reset_user_password(self, auth_username, new_password):
        """重置用户密码（管理员功能）"""
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            # 加密新密码
            user_data["password"] = self._encrypt_password(new_password)

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            logging.info(f"管理员重置密码: {auth_username}")
            return {"success": True, "message": "密码已重置"}

    def update_user_avatar(self, auth_username, avatar_url):
        """更新用户头像"""
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            user_data["avatar_url"] = avatar_url

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            return {"success": True, "message": "头像已更新"}

    def update_user_theme(self, auth_username, theme):
        """更新用户主题偏好"""
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            user_data["theme"] = theme

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            return {"success": True, "message": "主题已更新"}

    def update_max_sessions(self, auth_username, max_sessions):
        """更新用户最大会话数量

        Args:
            auth_username: 用户名
            max_sessions: 最大会话数 (1=单会话, >1=指定数量, -1=无限制)
        """
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            user_data["max_sessions"] = max_sessions

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 生成提示信息
            if max_sessions == 1:
                msg = f"已设置为单会话模式：用户每次只能保持1个活跃会话"
            elif max_sessions == -1:
                msg = f"已设置为无限会话模式：用户可以创建任意数量的会话"
            else:
                msg = f"已设置最大会话数量为：{max_sessions}个，超出时将自动清理最旧的会话"

            return {"success": True, "message": msg}

    def ban_user(self, auth_username):
        """封禁用户"""
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            user_data["banned"] = True
            user_data["banned_at"] = time.time()

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            logging.info(f"用户已封禁: {auth_username}")
            return {"success": True, "message": "用户已封禁"}

    def unban_user(self, auth_username):
        """解封用户"""
        with self.lock:
            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            user_data["banned"] = False
            user_data["unbanned_at"] = time.time()

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            logging.info(f"用户已解封: {auth_username}")
            return {"success": True, "message": "用户已解封"}

    def delete_user(self, auth_username):
        """删除用户（需要管理员权限）"""
        with self.lock:
            # 不允许删除超级管理员
            super_admin = self.config.get("Admin", "super_admin", fallback="admin")
            if auth_username == super_admin:
                return {"success": False, "message": "不允许删除超级管理员"}

            user_file = self.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return {"success": False, "message": "用户不存在"}

            # 删除用户文件
            try:
                os.remove(user_file)
            except Exception as e:
                logging.error(f"删除用户文件失败: {e}")
                return {"success": False, "message": f"删除失败: {e}"}

            # 删除用户对应的 school accounts 文件
            # 这样可以确保用户的所有关联数据都被清理
            try:
                school_accounts_file = self._get_user_accounts_file(auth_username)
                if os.path.exists(school_accounts_file):
                    os.remove(school_accounts_file)
                    logging.info(f"已删除用户 {auth_username} 的 school accounts 文件")
            except Exception as e:
                logging.error(
                    f"删除用户 {auth_username} 的 school accounts 文件失败: {e}"
                )
                # 不中断流程，继续删除权限信息

            # 从权限组映射中移除
            if auth_username in self.permissions.get("user_groups", {}):
                del self.permissions["user_groups"][auth_username]

            # 从差分权限中移除
            if (
                "user_custom_permissions" in self.permissions
                and auth_username in self.permissions["user_custom_permissions"]
            ):
                del self.permissions["user_custom_permissions"][auth_username]

            self._save_permissions()

            logging.info(f"用户已删除: {auth_username}")
            return {"success": True, "message": "用户已删除"}

    def get_user_details(self, auth_username):
        """获取用户详细信息"""
        user_file = self.get_user_file_path(auth_username)
        if not os.path.exists(user_file):
            return None

        with open(user_file, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        # 返回用户信息（不包含密码）
        return {
            "auth_username": user_data["auth_username"],
            "group": user_data.get("group", "user"),
            "created_at": user_data.get("created_at"),
            "last_login": user_data.get("last_login"),
            "2fa_enabled": user_data.get("2fa_enabled", False),
            "avatar_url": user_data.get("avatar_url") or "default_avatar.png",
            "max_sessions": user_data.get("max_sessions", 1),
            "theme": user_data.get("theme", "light"),
            "session_ids": user_data.get("session_ids", []),
            "nickname": user_data.get("nickname", user_data["auth_username"]),
            "phone": user_data.get("phone", ""),
        }

    def check_single_session_enforcement(self, auth_username, new_session_id):
        """检查并强制执行会话数量限制

        根据用户的max_sessions设置：
        - max_sessions = 1: 单会话模式，移除所有旧会话
        - max_sessions > 1: 多会话模式，超出时移除最旧的会话
        - max_sessions = -1: 无限制模式，不移除任何会话

        Returns:
            tuple: (需要清理的旧会话列表, 提示信息)
        """
        if auth_username == "guest":
            return [], ""  # 游客不受限制

        user_file = self.get_user_file_path(auth_username)
        if not os.path.exists(user_file):
            return [], ""

        with self.lock:
            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            max_sessions = user_data.get("max_sessions", 1)
            old_sessions = user_data.get("session_ids", [])

            # 无限制模式，不清理
            if max_sessions == -1:
                return [], ""

            # # 单会话模式：移除所有旧会话
            # if max_sessions == 1:
            #     user_data['session_ids'] = [new_session_id]

            #     with open(user_file, 'w', encoding='utf-8') as f:
            #         json.dump(user_data, f, indent=2, ensure_ascii=False)

            #     # 过滤掉无效的session_id
            #     valid_old_sessions = [s for s in old_sessions if s and s != 'null' and s.strip() != '']
            #     message = "单会话模式：已自动清理所有旧会话"
            #     return valid_old_sessions, message

            # 多会话模式：检查是否超出限制
            current_count = len(old_sessions)
            if current_count > max_sessions:
                # 超出限制，移除最旧的会话
                sessions_to_remove = old_sessions[: current_count - max_sessions + 1]
                remaining_sessions = old_sessions[current_count - max_sessions + 1 :]
                user_data["session_ids"] = remaining_sessions + [new_session_id]

                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

                # 过滤掉无效的session_id
                valid_sessions_to_remove = [
                    s
                    for s in sessions_to_remove
                    if s and s != "null" and s.strip() != ""
                ]
                message = ""
                if len(valid_sessions_to_remove) > 0:
                    message = f"已达到最大会话数量限制({max_sessions}个)，已自动清理{len(valid_sessions_to_remove)}个最旧的会话"
                return valid_sessions_to_remove, message
            else:
                # 未超出限制，正常添加
                return [], ""

    def log_audit(
        self, auth_username, action, details="", ip_address="", session_id=""
    ):
        """记录审计日志"""
        audit_entry = {
            "timestamp": time.time(),
            "datetime": datetime.datetime.now().isoformat(),
            "username": auth_username,
            "action": action,
            "details": details,
            "ip_address": ip_address,
            "session_id": session_id,
        }

        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"记录审计日志失败: {e}")

    def get_audit_logs(self, username=None, action=None, limit=100):
        """获取审计日志"""
        if not os.path.exists(AUDIT_LOG_FILE):
            return []

        logs = []
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        # 修复：使用 (not username ...) 来同时处理 None 和 "" (空字符串)
                        if (not username or entry.get("username") == username) and (
                            not action or entry.get("action") == action
                        ):
                            logs.append(entry)
                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        logging.debug(f"[审计日志] 跳过无效日志行: {e}")
                        continue
        except Exception as e:
            logging.error(f"读取审计日志失败: {e}")

        # 返回最近的记录
        return logs[-limit:]

    def _synchronize_super_admin_permissions(self):
        """
        [启动检查] 同步 config.ini 中的 super_admin 与 permissions.json 中的权限组。

        逻辑:
        1. (降级) 如果用户在 permissions.json 中是 super_admin，但与 config.ini 不符，则降级为 admin。
        2. (升级) 如果 config.ini 中指定的用户在 permissions.json 中不是 super_admin，则升级为 super_admin。
        3. (添加) 如果 config.ini 中指定的用户不在 permissions.json 中，则添加。
        """
        logging.info(
            "[权限同步] 开始检查 config.ini 与 permissions.json 的 super_admin 一致性..."
        )

        try:
            # 1. 从 config.ini 获取配置的超级管理员用户名
            super_admin_username = self.config.get(
                "Admin", "super_admin", fallback="admin"
            )
            if not super_admin_username:
                logging.error(
                    "[权限同步] config.ini 中 [Admin]super_admin 未配置，同步中止。"
                )
                return

            # 2. 获取锁，准备修改权限数据
            with self.lock:  #
                changes_made = False

                if "user_groups" not in self.permissions:
                    self.permissions["user_groups"] = {}

                user_groups = self.permissions["user_groups"]

                # 3. 遍历所有已知的用户权限组
                #    使用 .copy().items() 允许在迭代时修改字典
                for username, group in user_groups.copy().items():

                    # 规则1 (降级): 该用户是超管，但他不是配置中的超管
                    if group == "super_admin" and username != super_admin_username:
                        user_groups[username] = "admin"  # 降级为 admin
                        self._update_user_file_group(username, "admin")  #
                        logging.warning(
                            f"[权限同步] 用户 '{username}' 在 permissions.json 中是 super_admin，"
                            f"但他不是 config.ini 中指定的超管 ('{super_admin_username}')。"
                            f"已自动降级为 'admin'。"
                        )
                        changes_made = True

                    # 规则2 (升级): 该用户是配置中的超管，但他当前的组不是 super_admin
                    elif username == super_admin_username and group != "super_admin":
                        user_groups[username] = "super_admin"  # 升级
                        self._update_user_file_group(username, "super_admin")  #
                        logging.info(
                            f"[权限同步] 用户 '{username}' 是 config.ini 指定的超管，"
                            f"但在 permissions.json 中是 '{group}'。已自动升级为 'super_admin'。"
                        )
                        changes_made = True

                # 规则3 (添加): 配置中的超管在 permissions.json 中完全不存在
                if super_admin_username not in user_groups:
                    user_groups[super_admin_username] = "super_admin"
                    # 尝试更新用户文件（如果文件已存在）
                    self._update_user_file_group(super_admin_username, "super_admin")  #
                    logging.info(
                        f"[权限同步] config.ini 指定的超管 '{super_admin_username}' "
                        f"不在 permissions.json 中。已自动添加为 'super_admin'。"
                    )
                    changes_made = True

                # 4. 如果有变动，保存回 permissions.json
                if changes_made:
                    self._save_permissions()  #
                    logging.info("[权限同步] 权限数据已更新并保存。")
                else:
                    logging.info("[权限同步] 权限一致，无需更新。")

        except Exception as e:
            logging.error(
                f"[权限同步] 同步 super_admin 权限时发生严重错误: {e}", exc_info=True
            )


# ==============================================================================
# Token管理系统
# ==============================================================================


class TokenManager:
    """管理用户登录令牌的系统

    功能:
    - 生成2048位(256字节)安全令牌
    - 持久化存储令牌到独立文件
    - 验证令牌有效性(1小时过期)
    - 检测多设备登录
    - 自动刷新活跃用户的令牌
    """

    def __init__(self, tokens_dir):
        logging.info("=" * 80)
        logging.info(f"TokenManager: 初始化令牌管理器，目录: {tokens_dir}")
        self.tokens_dir = tokens_dir
        self.lock = threading.Lock()
        if not os.path.exists(tokens_dir):
            os.makedirs(tokens_dir)
            logging.info(f"TokenManager: 创建令牌目录: {tokens_dir}")
        else:
            logging.debug(f"TokenManager: 令牌目录已存在: {tokens_dir}")
        logging.info("TokenManager: 初始化完成")
        logging.info("=" * 80)

    def _get_token_file_path(self, username):
        """获取用户的token文件路径"""
        # 直接使用用户名作为文件名（简化格式）
        file_path = os.path.join(self.tokens_dir, f"{username}.json")
        logging.debug(f"_get_token_file_path: 用户 {username} 的令牌文件: {file_path}")
        return file_path

    def generate_token(self):
        """生成2048位(256字节)的安全令牌"""
        # secrets.token_hex(256) 生成 256字节 = 2048位 的随机令牌
        token = secrets.token_hex(256)
        logging.debug(f"generate_token: 生成新令牌，长度: {len(token)} 字符")
        return token

    def create_token(self, username, session_id=None):
        """为用户创建新令牌并存储

        新的简化设计：一个用户只有一个token，不再关联session_id
        session信息由./sessions目录管理，token只负责认证

        Args:
            username: 用户名
            session_id: 会话UUID（保留参数以兼容现有调用，但不再存储）

        Returns:
            token: 生成的令牌字符串
        """
        logging.info(f"create_token: 为用户 {username} 创建令牌...")
        token = self.generate_token()
        created_at = time.time()
        expires_at = created_at + 3600  # 1小时后过期

        # 简化的token数据：只存储token本身和时间信息，不存储session_id
        token_data = {
            "token": token,
            "created_at": created_at,
            "expires_at": expires_at,
            "last_activity": created_at,
        }

        with self.lock:
            token_file = self._get_token_file_path(username)

            # 直接覆盖写入，一个用户只有一个token
            with open(token_file, "w", encoding="utf-8") as f:
                json.dump(token_data, f, indent=2, ensure_ascii=False)

        logging.info(f"为用户 {username} 创建新令牌完成")
        return token

    def verify_token(self, username, session_id, token):
        """验证令牌是否有效

        新的简化设计：只验证用户名和token，不再关联session_id
        session_id参数保留以兼容现有调用

        Args:
            username: 用户名
            session_id: 会话UUID（保留参数以兼容，不再使用）
            token: 要验证的令牌

        Returns:
            tuple: (is_valid, reason)
        """
        token_file = self._get_token_file_path(username)

        if not os.path.exists(token_file):
            return False, "no_token_file"

        try:
            with open(token_file, "r", encoding="utf-8") as f:
                token_data = json.load(f)

            # 检查令牌是否匹配
            if token_data.get("token") != token:
                return False, "token_mismatch"

            # 检查是否过期
            if time.time() > token_data.get("expires_at", 0):
                return False, "token_expired"

            return True, "valid"

        except Exception as e:
            logging.error(f"验证令牌时出错: {e}")
            return False, "error"

    def get_valid_token_for_session(self, username, session_id=None):
        """
        获取指定用户的有效Token（如果存在且未过期）。
        如果找到有效Token，会刷新其活动时间。

        新的简化设计：不再关联session_id，每个用户只有一个token

        Args:
            username: 用户名
            session_id: 会话UUID（保留参数以兼容，不再使用）

        Returns:
            str | None: 如果找到有效Token则返回Token字符串，否则返回None。
        """
        token_file = self._get_token_file_path(username)

        if not os.path.exists(token_file):
            return None

        try:
            # 使用锁确保读取和可能的刷新操作是原子的
            with self.lock:
                with open(token_file, "r", encoding="utf-8") as f:
                    token_data = json.load(f)

                current_time = time.time()

                # 检查是否过期
                if current_time > token_data.get("expires_at", 0):
                    logging.debug(
                        f"get_valid_token_for_session: 用户 {username} 的Token已过期"
                    )
                    return None

                # Token有效，刷新活动时间并延长有效期
                token_data["last_activity"] = current_time
                token_data["expires_at"] = current_time + 3600  # 延长1小时

                # 写回更新后的Token数据
                with open(token_file, "w", encoding="utf-8") as f:
                    json.dump(token_data, f, indent=2, ensure_ascii=False)

                logging.info(
                    f"get_valid_token_for_session: 找到并刷新了用户 {username} 的有效Token"
                )
                return token_data.get("token")  # 返回有效的Token字符串

        except Exception as e:
            logging.error(f"获取Token时出错 (用户: {username}): {e}")
            return None

    def refresh_token(self, username, session_id=None):
        """刷新令牌的过期时间和最后活动时间

        新的简化设计：不再关联session_id

        Args:
            username: 用户名
            session_id: 会话UUID（保留参数以兼容，不再使用）

        Returns:
            bool: 是否刷新成功
        """
        with self.lock:
            token_file = self._get_token_file_path(username)

            if not os.path.exists(token_file):
                return False

            try:
                with open(token_file, "r", encoding="utf-8") as f:
                    token_data = json.load(f)

                # 更新过期时间和最后活动时间
                current_time = time.time()
                token_data["expires_at"] = current_time + 3600  # 延长1小时
                token_data["last_activity"] = current_time

                # 保存
                with open(token_file, "w", encoding="utf-8") as f:
                    json.dump(token_data, f, indent=2, ensure_ascii=False)

                return True

            except Exception as e:
                logging.error(f"刷新令牌时出错: {e}")
                return False

    def invalidate_token(self, username, session_id=None):
        """使令牌失效（用于登出）

        新的简化设计：直接删除用户的token文件

        Args:
            username: 用户名
            session_id: 会话UUID（保留参数以兼容，不再使用）
        """
        with self.lock:
            token_file = self._get_token_file_path(username)

            if os.path.exists(token_file):
                try:
                    os.remove(token_file)
                    logging.info(f"令牌已失效: {username}")
                except Exception as e:
                    logging.error(f"删除令牌文件时出错: {e}")

    def get_active_sessions(self, username):
        """获取用户所有有效的会话

        新的简化设计：不再由token文件管理session列表
        session信息应从./sessions目录获取

        Args:
            username: 用户名

        Returns:
            list: 空列表（session管理已移至./sessions目录）
        """
        # Token文件不再存储session信息，返回空列表
        # 如需获取活跃会话，应查询./sessions目录
        logging.debug(
            f"get_active_sessions: token文件不再管理session列表，请使用session管理功能"
        )
        return []

    def cleanup_expired_tokens(self, username):
        """清理过期的令牌

        新的简化设计：如果token过期，直接删除整个token文件

        Args:
            username: 用户名
        """
        with self.lock:
            token_file = self._get_token_file_path(username)

            if not os.path.exists(token_file):
                return

            try:
                with open(token_file, "r", encoding="utf-8") as f:
                    token_data = json.load(f)

                current_time = time.time()

                # 如果token已过期，删除文件
                if current_time > token_data.get("expires_at", 0):
                    os.remove(token_file)
                    logging.info(f"清理了过期令牌: {username}")

            except Exception as e:
                logging.error(f"清理过期令牌时出错: {e}")

    def detect_multi_device_login(self, username, new_session_id):
        """检测多设备登录

        Args:
            username: 用户名
            new_session_id: 新的会话ID

        Returns:
            list: 需要踢出的旧会话ID列表
        """
        active_sessions = self.get_active_sessions(username)

        # 排除新会话本身
        old_sessions = [s for s in active_sessions if s != new_session_id]

        if old_sessions:
            logging.info(f"检测到多设备登录: {username}, 旧会话数: {len(old_sessions)}")

        return old_sessions


# ==============================================================================
# 数据结构定义
# ==============================================================================


class UserData:
    """存储用户相关信息的类"""

    def __init__(self):
        self.name: str = ""
        self.phone: str = ""
        self.student_id: str = ""
        self.id: str = ""
        self.registration_time: str = ""
        self.first_login_time: str = ""
        self.id_card: str = ""
        self.last_login_time: str = ""
        self.current_login_time: str = ""
        self.username: str = ""
        self.gender: str = ""
        self.school_name: str = ""
        self.attribute_type: str = ""
        self.avatar_url: str = ""


class RunData:
    """存储单个跑步任务相关数据的类"""

    def __init__(self):
        # 路径数据
        # (经度, 纬度, 是否关键点) - 用户绘制的草稿路径
        self.draft_coords: list[tuple[float, float, int]] = []
        # (经度, 纬度, 与上一点的时间间隔ms) - 处理后用于模拟的最终路径
        self.run_coords: list[tuple[float, float, int]] = []
        # (经度, 纬度) - 服务器返回的推荐路线, (0,0)用于分段
        self.recommended_coords: list[tuple[float, float]] = []
        self.target_points: list[tuple[float, float]] = (
            []
        )  # (经度, 纬度) - 任务必须经过的打卡点

        # 任务基本信息
        self.target_point_names: str = ""  # 打卡点名称，用'|'分隔
        self.upload_time: str = ""  # 完成时间
        self.start_time: str = ""  # 任务开始时间
        self.end_time: str = ""  # 任务结束时间
        self.run_name: str = ""  # 任务名称
        self.errand_id: str = ""  # 任务ID
        self.errand_schedule: str = ""  # 任务计划ID
        self.status: int = 0  # 任务状态 (0: 未完成, 1: 已完成)

        # 运行时状态
        self.target_sequence: int = (
            0  # 当前目标打卡点序号（0-based，0表示第一个打卡点）
        )
        self.is_in_target_zone: bool = False  # 是否在当前打卡点范围内
        self.trid: str = ""  # 本次跑步的唯一轨迹ID
        self.details_fetched: bool = False  # 任务详情是否已加载
        self.total_run_time_s: float = 0.0  # 模拟总时长(秒)
        self.total_run_distance_m: float = 0.0  # 模拟总距离(米)
        self.distance_covered_m: float = 0.0  # 实时已跑距离(米)


class AccountSession:
    """封装单个账号的所有运行时数据、状态和操作"""

    def __init__(self, username, password, api_bridge, tag=None):
        self.username: str = username
        self.password: str = password
        self.api_bridge = api_bridge  # Api 类的实例引用
        self.window = api_bridge.window

        # 每个账号拥有独立的ApiClient和requests.Session，确保Cookie隔离
        self.api_client = ApiClient(self)
        self.user_data = UserData()
        self.all_run_data: list[RunData] = []

        # 从全局参数深拷贝一份独立的参数配置
        self.params = copy.deepcopy(api_bridge.global_params)
        self.device_ua: str = ""  # 将在登录时生成或加载

        # --- 账号独立的签到半径缓存 ---
        self.server_attendance_radius_m = 0.0
        self.last_radius_fetch_time = 0

        # 标记信息
        self.tag: str = tag if tag else ""  # 账号标记（备注/标签）

        # 首次登录验证状态
        self.is_first_login_verified: bool = False  # 是否已完成首次登录验证
        self.is_verifying: bool = False  # 是否正在进行首次验证

        # 最后刷新时间戳（用于避免重复刷新）
        self.last_refresh_time: float = 0  # 上次刷新的时间戳

        self.status_text: str = "待命"  # UI上显示的状态
        self.summary = {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "executable": 0,
            "expired": 0,
            "not_started": 0,
        }

        self.worker_thread: threading.Thread | None = None
        self.stop_event = threading.Event()

    def log(self, message: str):
        """为日志自动添加账号前缀"""
        # 使用主 Api 实例的 log 方法来确保日志发送到UI
        self.api_bridge.log(f"[{self.username}] {message}")


class ApiClient:
    """处理与后端服务器网络请求的类"""

    BASE_URL = "https://zslf.zsc.edu.cn"
    API_VERSION = 66

    def __init__(self, owner_instance):
        self.session = requests.Session()
        self.app = owner_instance
        logging.debug("ApiClient已初始化，创建了新的requests.Session会话实例")

    def _get_headers(self) -> dict:
        """构建请求头，包含认证信息和设备信息"""
        headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            # 'Content-Type': 'application/x-www-form-urlencoded',
            "X-Requested-With": "com.zx.slm",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": self.app.device_ua,
        }
        # 仅当存在登录后返回的 shiroCookie 时才携带 Authorization

        # 修复：使用 get_dict() 解决 CookieConflictError
        # 当服务器为不同路径（如 / 和 /app）设置多个同名 cookie 时
        # .get() 会失败，而 .get_dict() 会智能选择一个
        try:
            auth_token = self.session.cookies.get_dict().get("shiroCookie")
        except requests.cookies.CookieConflictError:
            # 极端情况下的回退：如果 get_dict() 仍然失败，尝试手动查找
            logging.warning(
                "CookieConflictError 即使在使用 get_dict() 时也发生，尝试手动查找..."
            )
            auth_token = None
            for cookie in self.session.cookies:
                if cookie.name == "shiroCookie":
                    auth_token = cookie.value
                    logging.warning(f"手动查找到 'shiroCookie': {auth_token[:10]}...")
                    break

        if auth_token:
            logging.debug(
                f"使用shiroCookie作为认证令牌进行Authorization请求头设置: {auth_token}"
            )
            headers["Authorization"] = auth_token
        else:
            logging.debug("未找到shiroCookie认证令牌，将不会设置Authorization请求头")
        return headers

    def _request(
        self,
        method: str,
        url: str,
        data: dict = None,
        params: dict = None,
        is_post_str=False,
        force_content_type: str = None,
    ) -> requests.Response | None:
        """统一的网络请求方法（增强：支持取消）"""

        # 在多账号模式下，app 可能是 AccountSession 实例，需要获取正确的日志函数和离线模式状态
        log_func = self.app.log if hasattr(self.app, "log") else self.app.api_bridge.log
        is_offline = (
            self.app.is_offline_mode
            if hasattr(self.app, "is_offline_mode")
            else self.app.api_bridge.is_offline_mode
        )

        # 全局/局部取消检查
        cancel_requested = False
        # try:
        #     # 单账号线程停止
        #     if hasattr(self.app, 'stop_event') and isinstance(self.app.stop_event, threading.Event):
        #         cancel_requested = cancel_requested or self.app.stop_event.is_set()
        #     # 多账号全局停止
        #     if hasattr(self.app, 'api_bridge') and hasattr(self.app.api_bridge, 'multi_run_stop_flag'):
        #         cancel_requested = cancel_requested or self.app.api_bridge.multi_run_stop_flag.is_set()
        #     # 单账号模式下的 stop_run_flag
        #     if hasattr(self.app, 'api_bridge') and hasattr(self.app.api_bridge, 'stop_run_flag'):
        #         cancel_requested = cancel_requested or self.app.api_bridge.stop_run_flag.is_set()
        # except Exception:
        #     pass

        if cancel_requested:
            log_func("操作已取消，跳过网络请求。")
            logging.debug(
                f"[网络请求] 请求已取消 --> 请求方法: {method.upper()}, 目标URL: {url}, 取消原因: 用户停止操作或系统取消标志已设置"
            )
            return None

        if is_offline:
            log_func("离线模式：网络请求已被禁用。")
            logging.debug(
                f"[网络请求] 离线模式已启用，已阻止网络请求 --> 请求方法: {method.upper()}, 目标URL: {url}, 说明: 离线模式下所有网络通信将被禁用"
            )
            return None

        retries = 3
        connect_timeout = 5  # 连接超时设置为 5 秒
        read_timeout = 10  # 读取超时设置为 10 秒

        log_data = data
        if is_post_str and isinstance(data, str) and len(data) > 500:
            log_data = (
                data[:500] + "... (已截断，完整数据长度: " + str(len(data)) + " 字节)"
            )

        logging.debug(
            f"[网络请求] 准备发起HTTP请求 --> 请求方法: {method.upper()}, 目标URL: {url}, 重试次数配置: {retries}次, 连接超时: {connect_timeout}秒, 读取超时: {read_timeout}秒\n[请求数据]: {log_data}"
        )

        for attempt in range(retries):
            try:
                # 再次检查取消（避免刚发起时被取消）
                # try:
                #     if hasattr(self.app, 'stop_event') and self.app.stop_event.is_set():
                #         log_func("操作已取消。")
                #         return None
                #     if hasattr(self.app, 'api_bridge') and self.app.api_bridge.multi_run_stop_flag.is_set():
                #         log_func("操作已取消。")
                #         return None
                #     if hasattr(self.app, 'api_bridge') and self.app.api_bridge.stop_run_flag.is_set():
                #         log_func("操作已取消。")
                #         return None
                # except Exception:
                #     pass

                # 获取基础 headers
                headers = self._get_headers()

                if method.upper() == "POST":
                    post_data_bytes = b""

                    # 1. 确定 Content-Type
                    if force_content_type:
                        headers["Content-Type"] = force_content_type
                    elif is_post_str:
                        # 默认为 form-urlencoded (用于 submit_run_track)
                        # 如果data是JSON字符串，调用者应使用 force_content_type
                        headers["Content-Type"] = "application/x-www-form-urlencoded"
                    else:
                        # 默认: form-urlencoded (用于 login)
                        headers["Content-Type"] = "application/x-www-form-urlencoded"

                    # 2. 准备 Body
                    if is_post_str:
                        post_data_bytes = (data or "").encode("utf-8")
                    else:
                        # 默认: form-urlencoded
                        post_data_bytes = urllib.parse.urlencode(data or {}).encode(
                            "utf-8"
                        )

                    # 修复 Bug A: 移除了在 post 之前的错误日志记录
                    resp = self.session.post(
                        url,
                        data=post_data_bytes,
                        params=params,
                        headers=headers,
                        # 使用元组分别设置连接和读取超时
                        timeout=(connect_timeout, read_timeout),
                    )
                else:
                    # GET 请求 (data 被用作 params)
                    resp = self.session.get(
                        url,
                        params=data,
                        headers=headers,
                        # 使用元组分别设置连接和读取超时
                        timeout=(connect_timeout, read_timeout),
                    )

                # --- 成功响应处理 (Bug A 和 B 均在此修复) ---
                # 修复 Bug B: 这段代码现在位于 try 块内部，但在所有 except 块之前
                logging.debug(
                    f"[网络请求] 收到服务器响应 <-- 状态码: {resp.status_code} ({resp.reason}), 来源URL: {url}, 响应头: {dict(resp.headers)}, 响应内容长度: {len(resp.content)} 字节"
                )
                resp.raise_for_status()  # 如果状态码不是 2xx，会抛出 HTTPError
                return resp

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as net_err:
                # --- 新增：专门捕获连接错误和超时 ---
                log_func(f"网络连接失败 (第{attempt+1}/{retries}次): {net_err}")
                logging.error(
                    f"[网络请求] 网络连接失败 --> 重试次数: 第{attempt+1}次/共{retries}次, 请求方法: {method.upper()}, 目标URL: {url}, 错误类型: {type(net_err).__name__}, 错误详情: {net_err}, 连接超时配置: {connect_timeout}秒, 读取超时配置: {read_timeout}秒",
                    exc_info=False,
                )
                if attempt + 1 == retries:
                    log_func(f"网络连接最终失败: 无法连接到服务器 {self.BASE_URL}")
                    logging.error(
                        f"[网络请求] 网络连接最终失败 --> 已达到最大重试次数({retries}次), 目标服务器: {self.BASE_URL}, 无法建立连接"
                    )
                    return None  # 连接失败，直接返回 None
                logging.info(
                    f"[网络请求] 准备重试 --> 等待1.5秒后进行第{attempt+2}次请求尝试"
                )
                time.sleep(1.5)  # 重试前等待
                continue  # 继续下一次重试

                # 修复 Bug B: 原本错误放置在这里的代码已被移到 try 块末尾

            except requests.exceptions.HTTPError as http_err:
                # --- 处理非 2xx 状态码的错误 (例如 404, 500) ---
                log_func(
                    f"服务器返回错误 (第{attempt+1}次): {http_err.response.status_code}"
                )
                logging.error(
                    f"[网络请求] HTTP错误 --> 重试次数: 第{attempt+1}次/共{retries}次, 请求方法: {method.upper()}, 目标URL: {url}, HTTP状态码: {http_err.response.status_code}, 状态描述: {http_err.response.reason}, 服务器响应内容: {http_err.response.text[:200]}{'...(已截断)' if len(http_err.response.text) > 200 else ''}",
                    exc_info=False,
                )
                if attempt + 1 == retries:
                    log_func(f"服务器错误: {http_err.response.status_code}")
                    logging.error(
                        f"[网络请求] HTTP请求最终失败 --> 已达到最大重试次数({retries}次), HTTP状态码: {http_err.response.status_code}, 请求无法成功完成"
                    )
                    # 可以考虑返回包含错误信息的 response 对象，或者依然返回 None
                    # return http_err.response # 如果上层需要处理具体错误
                    return None  # 保持返回 None
                logging.info(
                    f"[网络请求] 准备重试 --> 等待1.5秒后进行第{attempt+2}次请求尝试"
                )
                time.sleep(1.5)  # 重试前等待
                continue  # 继续下一次重试

            except requests.exceptions.RequestException as req_err:
                # --- 捕获其他所有 requests 相关的异常 (作为兜底) ---
                log_func(f"请求发生意外错误 (第{attempt+1}次): {req_err}")
                logging.error(
                    f"[网络请求] 意外的请求异常 --> 重试次数: 第{attempt+1}次/共{retries}次, 请求方法: {method.upper()}, 目标URL: {url}, 异常类型: {type(req_err).__name__}, 异常详情: {req_err}, 完整堆栈信息如下:",
                    exc_info=True,
                )
                if attempt + 1 == retries:
                    log_func(f"请求最终失败: {req_err}")
                    logging.error(
                        f"[网络请求] 请求最终失败 --> 已达到最大重试次数({retries}次), 所有重试均失败, 异常信息: {req_err}"
                    )
                    return None  # 最终失败返回 None
                logging.info(
                    f"[网络请求] 准备重试 --> 等待1.5秒后进行第{attempt+2}次请求尝试"
                )
                time.sleep(1.5)  # 重试前等待
                continue  # 继续下一次重试

        return None  # 如果循环结束仍未成功

    def _json(self, resp: requests.Response | None) -> dict | None:
        """安全地将Response对象解析为JSON字典"""
        log_func = self.app.log if hasattr(self.app, "log") else self.app.api_bridge.log
        if resp:
            try:
                json_data = resp.json()
                logging.debug(
                    f"[JSON解析] 成功解析JSON响应 --> 响应状态码: {resp.status_code}, JSON数据字段: {list(json_data.keys()) if isinstance(json_data, dict) else type(json_data).__name__}"
                )
                return json_data
            except json.JSONDecodeError as e:
                log_func("服务器响应解析失败。")
                logging.error(
                    f"[JSON解析] JSON解码失败 --> 响应状态码: {resp.status_code}, 响应内容类型: {resp.headers.get('Content-Type', '未知')}, 解码错误位置: 第{e.lineno}行第{e.colno}列, 响应文本内容(前500字符): {resp.text[:500]}{'...(已截断)' if len(resp.text) > 500 else ''}, 错误详情: {e}"
                )
                return None
        logging.debug(f"[JSON解析] 响应对象为空，无法解析JSON")
        return None

    def login(self, username, password):
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}/app/login",
                {
                    "username": username,
                    "password": password,
                    "appVersion": self.API_VERSION,
                },
            )
        )

    def get_run_list(self, user_id, offset=0):
        return self._json(
            self._request(
                "GET",
                f"{self.BASE_URL}:9097/run/errand/getErrandList",
                {
                    "userId": user_id,
                    "offset": offset,
                    "limit": 10,
                    "appVersion": self.API_VERSION,
                },
            )
        )

    def get_run_details(self, errand_id, user_id, errand_schedule_id):
        return self._json(
            self._request(
                "GET",
                f"{self.BASE_URL}:9097/run/errand/getErrandDetail",
                {
                    "errandId": errand_id,
                    "userId": user_id,
                    "errandScheduleId": errand_schedule_id,
                    "appVersion": self.API_VERSION,
                },
            )
        )

    def get_run_history_list(self, user_id, errand_schedule_id):
        return self._json(
            self._request(
                "GET",
                f"{self.BASE_URL}:9097/run/errand/getUserErrandTrackRecord",
                {
                    "errandScheduleId": errand_schedule_id,
                    "userId": user_id,
                    "offset": 0,
                    "limit": 20,
                    "appVersion": self.API_VERSION,
                },
            )
        )

    def get_history_track_by_trid(self, trid):
        return self._json(
            self._request(
                "GET",
                f"{self.BASE_URL}:9097/run/errand/getTrackByTrid",
                {"trid": trid, "appVersion": self.API_VERSION},
            )
        )

    def submit_run_track(self, payload_str):
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}:9097/run/errand/addErrandTrack",
                payload_str,
                is_post_str=True,
            )
        )

    def get_run_info_by_trid(self, trid):
        return self._json(
            self._request(
                "GET",
                f"{self.BASE_URL}:9097/run/errand/getTrackRecordByTrid",
                {"trid": trid, "appVersion": self.API_VERSION},
            )
        )

    def get_unread_notice_count(self):
        """获取未读通知数量 (POST, 空body, application/json)"""
        # 该API需要POST一个空 body 并且 Content-Type 为 application/json
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}/app/appNotice/unreadNumber",
                data="",  # 发送空字符串
                is_post_str=True,
                force_content_type="application/json;charset=UTF-8",  # 强制指定类型
            )
        )

    def get_notice_list(self, offset=0, limit=10, type_id=0):
        """获取通知列表 (POST, 空body, 带URL参数)"""
        params = {"offset": offset, "limit": limit, "typeId": type_id}
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}/app/appNotice/noticeListByType",
                data="",  # 发送空字符串
                params=params,
                is_post_str=True,
                force_content_type="application/json;charset=UTF-8",  # 强制指定类型
            )
        )

    def mark_notice_as_read(self, notice_id):
        """将单个通知设为已读 (POST, 空body, 带URL参数)"""
        params = {"noticeId": notice_id}
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}/app/appNotice/updateNoticeIsRead",
                data="",  # 发送空字符串
                params=params,
                is_post_str=True,
                force_content_type="application/json;charset=UTF-8",  # 强制指定类型
            )
        )

    @staticmethod
    def generate_random_ua():
        """生成一个随机的、模拟安卓设备的User-Agent字符串"""
        build_texts = [
            "TD1A.221105.001.A1",
            "TP1A.221005.003",
            "SQ3A.220705.004",
            "SP2A.220505.008",
            "SQ1D.220205.004",
            "RP1A.201005.004",
        ]
        phone_models = [
            "Xiaomi 12",
            "Xiaomi 13 Pro",
            "Redmi K60",
            "vivo X90",
            "iQOO 11",
            "OPPO Find X6 Pro",
            "Realme GT Neo5",
            "HONOR Magic5 Pro",
            "OnePlus 11",
        ]
        android_version_map = {"T": 13, "S": 12, "R": 11, "Q": 10, "P": 9}
        random_build = random.choice(build_texts)
        build_letter = random_build.split(".")[0][0]
        android_version = android_version_map.get(build_letter, 13)
        chrome_version = f"Chrome/{random.randint(100, 120)}.0.{random.randint(4000, 6000)}.{random.randint(100, 200)}"
        return f"Mozilla/5.0 (Linux; Android {android_version}; {random.choice(phone_models)} Build/{random_build}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 {chrome_version} Mobile Safari/537.36"

    def get_roll_call_info(self, roll_call_id, user_id):
        """获取指定签到活动的信息"""
        params = {"id": roll_call_id, "userId": user_id, "appVersion": self.API_VERSION}
        # 注意：原始请求是 POST 但参数在 URL 中，且 Body 为空
        # 这里模拟这种行为，将参数放在 params 里，data 设为空字符串
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}:9097/run/attendanceRecord/getAttendanceByRollCallId",
                data="",  # 发送空字符串
                params=params,
                is_post_str=True,  # 告诉 _request data 是字符串
                force_content_type="application/json;charset=UTF-8",  # 强制类型以发送空 body
            )
        )

    def submit_attendance(self, payload: dict):
        """提交签到记录"""
        # 假设签到提交使用 form-urlencoded 格式
        # payload 应包含: rollCallId, userId, coordinate, distance, status, signCode 等
        payload["appVersion"] = self.API_VERSION
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}:9097/run/attendanceRecord/addAttendance",
                data=payload,
                is_post_str=False,  # 使用默认的 form-urlencoded
            )
        )

    def get_attendance_radius(self):
        """获取服务器设定的签到半径"""
        # POST, 空body, application/json, 带URL参数
        params = {"code": "attendanceRadius", "num": 1}
        logging.debug("正在从服务器请求签到有效半径配置参数...")
        return self._json(
            self._request(
                "POST",
                f"{self.BASE_URL}/app/appFind/getDictTips",
                data="",  # 发送空字符串
                params=params,
                is_post_str=True,
                force_content_type="application/json;charset=UTF-8",
            )
        )


# ==============================================================================
# 3. 后端主逻辑 (Backend API Bridge)
#    作为Python后端和WebView前端之间的桥梁，处理所有业务逻辑。
# ==============================================================================


class Api:
    """此类的方法会暴露给WebView前端的JavaScript调用"""

    def __init__(self, args):
        self.args = args
        self.window = None
        self.path_gen_callbacks = {}

        # --- 路径和配置部分保持不变 ---
        self.run_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.user_dir = SCHOOL_ACCOUNTS_DIR  # 使用新的学校账号目录
        os.makedirs(self.user_dir, exist_ok=True)
        self.config_path = os.path.join(self.run_dir, "config.ini")
        self.user_config_path = self.config_path

        # --- 为单用户模式保留一个api_client实例 ---
        self.api_client = ApiClient(self)

        # --- 初始化状态变量 ---
        self._init_state_variables()

        # --- 全局“数据提交”串行队列：同一时间只允许提交一个数据包 ---
        # 说明：
        # - 任何 addErrandTrack 的提交都会被封装为任务入队；
        # - 后台仅有一个工作线程串行处理，保证“同时只提交一个数据包”；
        # - 调用方在入队后阻塞等待本次提交的结果（带超时）。
        # - 调用方在入队后阻塞等待本次提交的结果（带超时）。
        # 提交串行队列相关的共享状态
        self._submission_queue: queue.Queue | None = getattr(
            self, "_submission_queue", None
        )
        self._submission_worker_thread: threading.Thread | None = getattr(
            self, "_submission_worker_thread", None
        )
        self._submission_worker_stop: threading.Event | None = getattr(
            self, "_submission_worker_stop", None
        )
        if self._submission_queue is None:
            self._submission_queue = queue.Queue()
        if self._submission_worker_stop is None:
            self._submission_worker_stop = threading.Event()
        if (self._submission_worker_thread is None) or (
            not self._submission_worker_thread.is_alive()
        ):
            self._submission_worker_thread = threading.Thread(
                target=self._submission_worker_loop,
                name="SubmissionWorker",
                daemon=True,
            )
            self._submission_worker_thread.start()

    def _init_state_variables(self):
        """初始化或重置应用的所有状态变量"""
        # --- 单用户模式变量 (大部分保留) ---
        self.device_ua = ""
        self.is_offline_mode = False
        self.user_data = UserData()
        self.all_run_data: list[RunData] = []
        self.current_run_idx = -1
        self.stop_run_flag = threading.Event()
        self.stop_run_flag.set()
        # 修复打卡点检测：设置合理的打卡半径（米）
        # 如果未来服务器返回此值，应从任务详情中更新
        self.target_range_m = 30.0  # 默认30米打卡范围

        # 修复会话持久化：初始化登录状态标志（不清除已存在的）
        if not hasattr(self, "login_success"):
            self.login_success = False
        if not hasattr(self, "user_info"):
            self.user_info = None
        # 全局登录并发控制（多账号模式下串行登录）
        # 固定并发为 1；若已有实例，则保持现状（防止模式切换时重复创建）
        if not hasattr(self, "multi_login_lock") or self.multi_login_lock is None:
            self.multi_login_lock = threading.Semaphore(1)

        # --- 将原params作为全局参数的模板 ---
        self.global_params = {
            "interval_ms": 3000,
            "interval_random_ms": 500,
            "speed_mps": 1.5,
            "speed_random_mps": 0.5,
            "location_random_m": 1.5,
            "task_gap_min_s": 600,
            "task_gap_max_s": 3600,
            "api_fallback_line": False,
            "api_retries": 2,
            "api_retry_delay_s": 0.5,
            "ignore_task_time": True,  # 新增：忽略任务起止时间，仅对比日期
            "theme_base_color": "#7dd3fc",
            "theme_style": "default",  # 新增：主题风格参数，默认为 'default'
            # 多账号模式下的路径规划参数
            "min_time_m": 20,
            "max_time_m": 30,
            "min_dist_m": 2000,
            # --- 自动签到参数 ---
            "auto_attendance_enabled": False,  # 是否开启自动签到
            "auto_attendance_refresh_s": 30,  # 自动刷新间隔（秒）
            "attendance_user_radius_m": 40,  # 用户期望的随机半径（默认40m）
            # 高德地图JS API Key
            "amap_js_key": "",
        }

        # --- 签到半径的全局缓存 ---
        self.server_attendance_radius_m = 0.0  # 服务器返回的最大半径，0表示精确签到
        self.last_radius_fetch_time = 0  # 上次获取半径的时间

        # --- 单账号自动刷新线程 ---
        self.auto_refresh_thread: threading.Thread | None = None
        self.stop_auto_refresh = threading.Event()
        self.stop_auto_refresh.set()  # 默认停止

        # --- 多账号自动签到线程 ---
        self.multi_auto_refresh_thread: threading.Thread | None = None
        self.stop_multi_auto_refresh = threading.Event()
        self.stop_multi_auto_refresh.set()  # 默认停止

        # self.params 将在单用户模式下使用，是 global_params 的一个副本
        self.params = self.global_params.copy()

        self._first_center_done = False

        # --- 新增多账号模式变量 ---
        self.is_multi_account_mode = False
        # 停止并清理所有账号会话
        if hasattr(self, "accounts"):
            for acc in self.accounts.values():
                if acc.worker_thread and acc.worker_thread.is_alive():
                    acc.stop_event.set()
        # {username: AccountSession}
        self.accounts: dict[str, AccountSession] = {}
        # 使用 threading（已被 eventlet monkey_patch 绿化）
        self.multi_run_stop_flag = threading.Event()
        self.multi_run_stop_flag.set()

        self._load_tasks_lock = threading.RLock()
        self._load_tasks_inflight = False
        self.multi_run_only_incomplete = True

    def set_multi_run_only_incomplete(self, flag: bool):
        """
        设置多账号模式下“仅执行未完成”的全局开关，并立即刷新全局按钮。
        """
        try:
            self.multi_run_only_incomplete = bool(flag)
            # 轻量刷新一次全局按钮状态（不阻塞）
            self._update_multi_global_buttons()
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def log(self, message):
        """将日志消息通过 WebSocket 发送到前端界面显示"""
        # 尝试获取当前 Api 实例关联的 session_id
        session_id = getattr(self, "_web_session_id", None)
        logging.info(message)
        if session_id and socketio:
            try:
                # 使用 session_id 作为房间名，确保消息只发给对应的浏览器标签页
                socketio.emit("log_message", {"msg": str(message)}, room=session_id)
            except Exception as e:
                # 在后台记录发送失败的日志，避免程序崩溃
                logging.error(
                    f"WebSocket emit log failed for session {session_id[:8]}: {e}"
                )
        else:
            # 如果没有 session_id 或 socketio 未初始化，则仅记录到后端日志
            logging.debug(
                f"[Log Emission Skipped] Session ID or SocketIO missing. Message: {message}"
            )

    def js_log(self, level, message):
        """接收并记录来自JavaScript的日志"""
        level = level.upper()
        if level == "INFO":
            logging.info(f"{message}")
        elif level == "DEBUG":
            logging.debug(f"{message}")
        elif level == "WARNING":
            logging.warning(f"{message}")
        elif level == "ERROR":
            logging.error(f"{message}")
        else:
            logging.info(f"[JS-{level}] {message}")

    @staticmethod
    def _robust_decode(raw: bytes) -> str:
        """尽可能兼容所有编码的解码函数"""
        # 1. 自动检测
        if chardet:
            det = chardet.detect(raw) or {}
            enc = det.get("encoding")
            if enc:
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    pass

        # 2. 常见编码回退
        for enc in ("utf-8", "gbk", "big5", "shift_jis", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue

        # 3. 最终兜底：强制替换非法字符
        return raw.decode("utf-8", errors="replace")

    def normalize_chinese_config_to_english(self, path: str) -> None:
        """
        将可能包含中文分区/键名的 INI 配置文件，转换为标准英文分区与键名，并统一写回 UTF-8。
        - [增强] 只保留当前程序定义的有效参数，抛弃所有未知或已弃用的参数。
        - 若文件已是英文分区（Config/System），不做任何改写（避免清空原配置）。
        - 若不存在中文分区时，保留原文（以 UTF-8 重写），避免写入空配置。
        - 写回前创建 .bak 备份。
        """
        if not os.path.exists(path):
            return

        # 原始字节与文本
        with open(path, "rb") as f:
            raw = f.read()
        text = self._robust_decode(raw)

        # 先用标准解析器尝试读取（判断是否已是英文分区）
        cfg_existing = configparser.ConfigParser(
            delimiters=("=", ":"),
            comment_prefixes=("#"),
            strict=False,
            interpolation=None,
        )
        try:
            cfg_existing.read_string(text)
        except Exception:
            # 原文有异常时，直接以 UTF-8 重写原文并返回
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return

        # 如果已存在英文分区（Config 或 System），直接保留，不转换不写回
        if cfg_existing.has_section("Config") or cfg_existing.has_section("System"):
            # 已是英文结构，尊重现有内容
            return

        # 继续尝试中文分区读取
        cfg_cn = configparser.ConfigParser(
            delimiters=("=", ":"),
            comment_prefixes=("#"),
            strict=False,
            interpolation=None,
        )
        try:
            cfg_cn.read_string(text)
        except Exception:
            # 解析失败则以 UTF-8 重写原文并返回（不清空）
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return

        # 若没有中文分区（“配置”/“系统”均不存在），保留原文，不写空文件
        if not (cfg_cn.has_section("配置") or cfg_cn.has_section("系统")):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return

        # 分区与键映射
        config_key_map = {
            "间隔时间": "interval_ms",
            "间隔时间随机": "interval_random_ms",
            "速度": "speed_mps",
            "速度随机": "speed_random_mps",
            "定位随机": "location_random_m",
            "任务间速度": "task_interval_speed",
            "用户名": "Username",
            "密码": "Password",
            "有效": "Enabled",
            "未完成次数": "PendingCount",
            "未完成次数上次检查时间": "LastPendingCheckTs",
            "下次最早开始时间": "NextEarliestStartTs",
        }
        system_key_map = {
            "cookie": "AuthorizationCookie",
            "UA": "UA",
        }

        # 构建英文配置
        cfg_en = configparser.ConfigParser(
            delimiters=("=", ":"),
            comment_prefixes=("#"),
            strict=False,
            interpolation=None,
        )
        cfg_en.add_section("Config")
        cfg_en.add_section("System")

        # 1. 定义所有当前有效的Config参数键（白名单）
        valid_config_keys = set(self.global_params.keys())
        valid_config_keys.add("Username")
        valid_config_keys.add("Password")

        # 2. 遍历旧配置，只写入白名单中的键
        if cfg_cn.has_section("配置"):
            for k, v in cfg_cn.items("配置"):
                # 转换中文键为英文键
                k_en = config_key_map.get(k, k)
                # 只有当转换后的键是有效参数时，才将其保留
                if k_en in valid_config_keys:
                    cfg_en.set("Config", k_en, v)

        if cfg_cn.has_section("系统"):
            for k, v in cfg_cn.items("系统"):
                k_en = system_key_map.get(k, k)
                if (
                    k_en == "UA"
                    and isinstance(v, str)
                    and v.lower().startswith("user-agent:")
                ):
                    v = v.split(":", 1)[1].strip()
                # 系统区的参数也做白名单校验
                if k_en in ["AuthorizationCookie", "UA"]:
                    cfg_en.set("System", k_en, v)

        # 写回前做备份
        try:
            backup_path = f"{path}.bak"
            with open(backup_path, "wb") as bf:
                bf.write(raw)
        except Exception:
            # 备份失败不阻止写回
            pass

        # 写回 UTF-8（仅当确有中文分区内容需要转换）
        with open(path, "w", encoding="utf-8") as f:
            cfg_en.write(f)

    def _get_user_accounts_file(self, auth_username):
        """
        获取指定认证用户的 school_accounts 存储文件路径。

        参数:
            auth_username: 认证用户名（system_accounts中的用户名）

        返回:
            文件路径字符串
        """
        user_accounts_dir = os.path.join(SCHOOL_ACCOUNTS_DIR, "user_accounts")
        return os.path.join(user_accounts_dir, f"{auth_username}.json")

    def _load_user_school_accounts(self, auth_username):
        """
        加载指定认证用户的所有 school_account 账户密码和UA。

        参数:
            auth_username: 认证用户名

        返回:
            字典，格式为 {school_username: {"password": "xxx", "ua": "xxx"}, ...}
            或旧格式 {school_username: password, ...}（向后兼容）
        """
        if not auth_username or auth_username == "guest":
            # 游客没有 school_accounts
            return {}

        file_path = self._get_user_accounts_file(auth_username)
        if not os.path.exists(file_path):
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logging.debug(
                f"成功加载用户 {auth_username} 的 school_accounts，共 {len(data)} 个账户"
            )
            return data
        except Exception as e:
            logging.error(
                f"加载用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return {}

    def _save_user_school_accounts(self, auth_username, accounts_dict):
        """
        保存指定认证用户的所有 school_account 账户密码和UA。

        参数:
            auth_username: 认证用户名
            accounts_dict: 字典，格式为 {school_username: {"password": "xxx", "ua": "xxx"}, ...}
        """
        if not auth_username or auth_username == "guest":
            # 游客不保存 school_accounts
            logging.debug("游客用户不保存 school_accounts")
            return

        file_path = self._get_user_accounts_file(auth_username)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(accounts_dict, f, ensure_ascii=False, indent=2)
            logging.debug(
                f"成功保存用户 {auth_username} 的 school_accounts，共 {len(accounts_dict)} 个账户"
            )
        except Exception as e:
            logging.error(
                f"保存用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )

    def _update_school_account_password(
        self, auth_username, school_username, password, ua=None, login_verified=False
    ):
        """
        更新指定认证用户的某个 school_account 的密码和UA。

        参数:
            auth_username: 认证用户名
            school_username: 学校账户用户名
            password: 密码
            ua: User-Agent（可选）
            login_verified: 是否已验证登录成功（True 时才会覆盖现有密码）
        """
        if not auth_username or auth_username == "guest":
            return

        accounts = self._load_user_school_accounts(auth_username)

        # 处理旧格式（字符串）和新格式（字典）
        existing_data = accounts.get(school_username)
        if existing_data:
            # 检查是否是旧格式（字符串）
            if isinstance(existing_data, str):
                # 旧格式，转换为新格式
                existing_data = {"password": existing_data, "ua": ""}

            # 如果存在冲突，只在登录验证成功后才覆盖
            if not login_verified:
                logging.debug(
                    f"school_account {school_username} 已存在，且未验证登录成功，跳过更新"
                )
                return

        # 更新或添加账户信息
        accounts[school_username] = {"password": password, "ua": ua if ua else ""}
        self._save_user_school_accounts(auth_username, accounts)
        logging.info(
            f"已更新用户 {auth_username} 的 school_account {school_username} 的密码和UA"
        )

    def _get_school_account_password(self, auth_username, school_username):
        """
        获取指定认证用户的某个 school_account 的密码。

        参数:
            auth_username: 认证用户名
            school_username: 学校账户用户名

        返回:
            密码字符串，如果不存在则返回 None
        """
        if not auth_username or auth_username == "guest":
            return None

        accounts = self._load_user_school_accounts(auth_username)
        account_data = accounts.get(school_username)

        # 处理旧格式（字符串）和新格式（字典）
        if isinstance(account_data, str):
            return account_data
        elif isinstance(account_data, dict):
            return account_data.get("password")
        return None

    def _get_school_account_ua(self, auth_username, school_username):
        """
        获取指定认证用户的某个 school_account 的UA。

        参数:
            auth_username: 认证用户名
            school_username: 学校账户用户名

        返回:
            UA字符串，如果不存在则返回 None
        """
        if not auth_username or auth_username == "guest":
            return None

        accounts = self._load_user_school_accounts(auth_username)
        account_data = accounts.get(school_username)

        # 只有新格式（字典）才有UA
        if isinstance(account_data, dict):
            return account_data.get("ua", "")
        return None

    def _save_config(self, username, password=None, ua=None):
        """保存指定用户的配置到 user/<username>.ini；当 password 为 None 时保留现有密码；当 ua 为 None 时保留现有 UA。同时更新主 config.ini 的 LastUser 和 amap_js_key。"""
        logging.debug(
            f"Saving config: username={username!r}, password provided: {password is not None}, ua provided: {ua is not None}"
        )

        # --- 1. 处理用户独立的 .ini 文件 ---
        user_ini_path = os.path.join(self.user_dir, f"{username}.ini")

        # 将旧配置文件（可能是中文各种编码）规范化为英文UTF-8 (这一步保持不变)
        self.normalize_chinese_config_to_english(user_ini_path)

        # 读取旧密码（仅当需要保留时）
        # --- 1. 创建或读取现有配置 ---
        cfg_to_save = configparser.RawConfigParser()
        cfg_to_save.optionxform = str  # 保持键的大小写
        if os.path.exists(user_ini_path):
            try:
                cfg_to_save.read(user_ini_path, encoding="utf-8")
            except Exception as e:
                logging.warning(
                    f"读取旧配置文件 {user_ini_path} 失败: {e}, 将创建新的。"
                )

        # --- 2. 确保分区存在 ---
        if not cfg_to_save.has_section("Config"):
            cfg_to_save.add_section("Config")
        if not cfg_to_save.has_section("System"):
            cfg_to_save.add_section("System")

        # --- 3. 设置 Username ---
        cfg_to_save.set("Config", "Username", username)

        # --- 4. 智能处理密码 ---
        # 仅当 *提供了新的* password (非 None) 时，才覆盖密码
        if password is not None:
            # 场景: 提供了新密码 (来自 login, multi_add_account)
            cfg_to_save.set("Config", "Password", password)
        else:
            # 场景: 未提供新密码 (来自 update_param)

            # 修复：检查密码行是否*完全不存在*于 .ini 文件中
            if not cfg_to_save.has_option("Config", "Password"):
                # 选项不存在，尝试从备份文件中恢复
                backup_path = f"{user_ini_path}.bak"
                if os.path.exists(backup_path):
                    try:
                        # 尝试从备份文件中读取密码，使用robust_decode确保兼容各种编码
                        with open(backup_path, "rb") as bf:
                            raw_backup = bf.read()
                        backup_text = self._robust_decode(raw_backup)
                        for line in backup_text.splitlines():
                            clean_line = line.strip()
                            # 规范化用于匹配
                            normalized_line = clean_line.lower().replace(" ", "")
                            if normalized_line.startswith(
                                "password="
                            ) or normalized_line.startswith("密码="):
                                # 从原始clean_line中分割（保留原始大小写和值）
                                parts = clean_line.split("=", 1)
                                if len(parts) == 2:
                                    recovered_password = parts[1].strip()
                                    if recovered_password:
                                        cfg_to_save.set(
                                            "Config", "Password", recovered_password
                                        )
                                        logging.info(
                                            f"已从备份文件恢复用户 {username} 的密码"
                                        )
                                        break
                    except Exception as e:
                        logging.warning(f"从备份文件恢复密码失败: {e}")
            else:
                # 选项存在 (has_option 为 True)，无论其值是 "mypass" 还是 "" (空字符串)，
                # 我们都“什么也不做”，以保留 cfg_to_save 对象中已读取的状态。
                # 这可以防止 configparser 在写回时丢弃该行。
                pass

        # --- 5. 智能处理 UA ---
        # 仅当 *提供了新的* ua (非 None) 时，才覆盖 UA
        # 修复：避免在切换账号时误将当前实例的 UA 覆盖到其他用户的配置文件
        if ua is not None:
            # 场景: 明确提供了新 UA (来自 login, generate_new_ua)
            cfg_to_save.set("System", "UA", ua)
        # 场景: 未提供新 UA (来自 update_param 等)
        # 则 *不* 触碰 UA 键，从而保留 cfg_to_save 中已加载的旧 UA(或它的缺失状态)。

        # --- 6. 参数：从当前实例状态获取 ---
        params_to_save = self.params
        if self.is_multi_account_mode and username in self.accounts:
            params_to_save = self.accounts[username].params
        for k, v in params_to_save.items():
            # 仅保存当前全局参数模板中存在的键
            # 排除 amap_js_key，因为它应该只保存在主 config.ini 中，不应在用户 .ini 中
            if k in self.global_params and k != "amap_js_key":
                cfg_to_save.set("Config", k, str(v))

        # --- 7. 安全写入用户 .ini 文件 ---
        try:
            with open(user_ini_path, "w", encoding="utf-8") as f:
                cfg_to_save.write(f)
            logging.debug(f"Saved user config for {username} -> {user_ini_path}")
        except Exception as e:
            logging.error(f"写入用户配置文件 {user_ini_path} 失败: {e}", exc_info=True)
            # 可以选择在这里向上抛出异常或返回错误状态

        # --- 7.5. 保存到 auth_username 的 school_accounts 文件 ---
        # 如果有密码且当前有认证用户，保存到 user_accounts/<auth_username>.json
        if (
            password is not None
            and hasattr(self, "auth_username")
            and self.auth_username
        ):
            self._update_school_account_password(
                self.auth_username, username, password, ua, login_verified=False
            )

        # --- 2. 处理主 config.ini 文件 ---
        main_cfg = configparser.RawConfigParser()
        main_cfg.optionxform = str  # 保持键的大小写

        # 先尝试读取现有文件，以获取其中的 amap_js_key
        if os.path.exists(self.config_path):
            try:
                main_cfg.read(self.config_path, encoding="utf-8")
            except Exception as e:
                logging.warning(
                    f"读取主配置文件 {self.config_path} 失败: {e}, 将创建新的。"
                )

        # 确保 [Config] 分区存在并更新 LastUser
        if not main_cfg.has_section("Config"):
            main_cfg.add_section("Config")
        main_cfg.set("Config", "LastUser", username)

        # 确保 [Map] 分区存在
        if not main_cfg.has_section("Map"):
            main_cfg.add_section("Map")

        # 【修复】智能更新 amap_js_key，防止空值覆盖
        # 1. 获取内存中的值
        amap_key_in_memory = self.global_params.get("amap_js_key", "").strip()
        # 2. 获取文件中的现有值
        amap_key_in_file = main_cfg.get("Map", "amap_js_key", fallback="").strip()

        if amap_key_in_memory:
            # 如果内存中有值（例如用户刚在前端设置了），则更新到文件
            main_cfg.set("Map", "amap_js_key", amap_key_in_memory)
        elif amap_key_in_file:
            # 如果内存为空但文件里有值，则保留文件里的值（不要覆盖为空）
            # 同时反向同步到内存，防止后续逻辑读取到空值
            self.global_params["amap_js_key"] = amap_key_in_file
            # main_cfg.set 保持不变即可
        else:
            # 两个都为空，确保键存在
            main_cfg.set("Map", "amap_js_key", "")

        # 安全写入主 config.ini 文件
        try:
            # with open(self.config_path, 'w', encoding='utf-8') as f:
            #     main_cfg.write(f)
            _write_config_with_comments(main_cfg, self.config_path)
            # logging.debug(
            # f"Updated main config {self.config_path} with LastUser and amap_js_key")
            logging.debug(f"更新主配置文件 {self.config_path} 成功")
        except Exception as e:
            logging.error(f"写入主配置文件 {self.config_path} 失败: {e}", exc_info=True)

    def _load_global_config(self):
        """从主 config.ini 加载全局配置（优先读取新版 Map.amap_js_key，兼容旧版 System.AmapJsKey）"""
        if not os.path.exists(self.config_path):
            return
        cfg = configparser.RawConfigParser()
        cfg.optionxform = str  # 保持键的大小写
        try:
            cfg.read(self.config_path, encoding="utf-8")

            # 优先读取新版配置 [Map] amap_js_key
            amap_key = cfg.get("Map", "amap_js_key", fallback="")

            # 如果新版配置为空，尝试读取旧版配置 [System] AmapJsKey（兼容性）
            if not amap_key:
                amap_key = cfg.get("System", "AmapJsKey", fallback="")
                # 如果旧版有值，迁移到新版
                if amap_key:
                    if not cfg.has_section("Map"):
                        cfg.add_section("Map")
                    cfg.set("Map", "amap_js_key", amap_key)
                    with open(self.config_path, "w", encoding="utf-8") as f:
                        cfg.write(f)
                    logging.info("已将AmapJsKey从旧版[System]迁移到新版[Map]")

            self.global_params["amap_js_key"] = amap_key
            logging.info(
                f"Loaded global Amap JS Key: {amap_key if amap_key else '(empty)'}"
            )
        except Exception as e:
            logging.error(
                f"加载全局配置文件 {self.config_path} 失败: {e}", exc_info=True
            )

    def _load_config(self, username):
        """从.ini文件加载指定用户的配置"""
        self.user_config_path = os.path.join(self.user_dir, f"{username}.ini")
        if not os.path.exists(self.user_config_path):
            return None

        # 先将旧配置文件（可能是中文+各种编码）规范化为英文+UTF-8
        self.normalize_chinese_config_to_english(self.user_config_path)

        # 修正：设置 strict=False 以允许配置文件中存在重复选项（容错）
        # 并添加 try-except 块处理其他可能的读取错误
        cfg = configparser.ConfigParser(strict=False)
        try:
            cfg.read(self.user_config_path, encoding="utf-8")
        except Exception as e:
            logging.warning(f"解析用户配置文件 {username} 时出错 (已忽略): {e}")

        password = cfg.get("Config", "Password", fallback="")
        if not password:
            # 如果密码为空，尝试从原始文件中扫描 "Password=" 或 "密码="，以兼容规范化失败的情况
            try:
                with open(
                    self.user_config_path, "r", encoding="utf-8", errors="ignore"
                ) as rf:
                    for line in rf:
                        clean_line = line.strip()
                        # 兼容英文键（不区分大小写）和中文键
                        temp_line_for_check = clean_line.lower().replace(" ", "")
                        if temp_line_for_check.startswith(
                            "password="
                        ) or temp_line_for_check.startswith("密码="):
                            # 从第一个 "=" 处分割，避免密码中包含 "=" 导致的问题
                            parts = clean_line.split("=", 1)
                            if len(parts) == 2:
                                password = parts[1].strip()
                                # 只要成功获取到密码，就立即跳出循环
                                if password:
                                    break
            except Exception:
                pass

        # 初始化 ua 变量，防止 UnboundLocalError
        ua = None

        # 尝试从 auth_username 的 school_accounts 加载密码和UA（优先级更高）
        if hasattr(self, "auth_username") and self.auth_username:
            school_password = self._get_school_account_password(
                self.auth_username, username
            )
            school_ua = self._get_school_account_ua(self.auth_username, username)
            if school_password:
                password = school_password
                logging.debug(
                    f"从用户 {self.auth_username} 的 school_accounts 加载了 {username} 的密码"
                )
            if school_ua:
                ua = school_ua
                logging.debug(
                    f"从用户 {self.auth_username} 的 school_accounts 加载了 {username} 的UA"
                )

        # 加载的配置应该应用到正确的对象上
        target_params = self.params
        if self.is_multi_account_mode and username in self.accounts:
            target_params = self.accounts[username].params

        if not ua:
            ua = cfg.get("System", "UA", fallback="")
        if self.is_multi_account_mode and username in self.accounts:
            self.accounts[username].device_ua = ua
        else:
            self.device_ua = ua

        for k in self.global_params:  # 迭代全局模板以确保所有键都存在
            if k in target_params:
                try:
                    if cfg.has_option("Config", k):
                        val_str = cfg.get("Config", k)
                        original_type = type(target_params[k])
                        if original_type is bool:
                            target_params[k] = val_str.lower() in (
                                "true",
                                "1",
                                "t",
                                "yes",
                            )
                        else:
                            target_params[k] = original_type(val_str)
                except ValueError:
                    logging.warning(
                        f"Could not parse config value for '{k}' for user {username}. Using default."
                    )
                    pass
        logging.debug(f"已成功加载用户配置: {username}")
        return password

    def _save_account_tag(self, username, tag):
        """保存账号标记到用户配置文件"""
        user_ini_path = os.path.join(self.user_dir, f"{username}.ini")

        cfg = configparser.RawConfigParser()
        cfg.optionxform = str  # 保持键的大小写
        if os.path.exists(user_ini_path):
            try:
                cfg.read(user_ini_path, encoding="utf-8")
            except Exception as e:
                logging.warning(f"读取配置文件 {user_ini_path} 失败: {e}")

        # 确保分区存在
        if not cfg.has_section("Account"):
            cfg.add_section("Account")

        # 设置标记
        cfg.set("Account", "Tag", str(tag))

        # 写入文件
        try:
            with open(user_ini_path, "w", encoding="utf-8") as f:
                cfg.write(f)
            logging.debug(f"已保存账号 {username} 的标记: {tag}")
        except Exception as e:
            logging.error(f"保存账号标记失败 {user_ini_path}: {e}", exc_info=True)

    def _load_account_tag(self, username):
        """从用户配置文件加载账号标记"""
        user_ini_path = os.path.join(self.user_dir, f"{username}.ini")
        if not os.path.exists(user_ini_path):
            return None

        cfg = configparser.ConfigParser()
        try:
            cfg.read(user_ini_path, encoding="utf-8")
            if cfg.has_option("Account", "Tag"):
                tag_str = cfg.get("Account", "Tag")
                return tag_str
        except Exception as e:
            logging.warning(f"加载账号标记失败 {username}: {e}")

        return None

    def _get_full_user_info_dict(self):
        """获取当前用户所有信息的字典"""
        return {
            k: v for k, v in self.user_data.__dict__.items() if not k.startswith("_")
        }

    def get_initial_data(self):
        """应用启动时由前端调用，获取初始用户列表和最后登录用户"""

        try:
            logging.info(
                "API调用: get_initial_data - 获取应用初始数据（用户列表和最后登录用户）"
            )

            # 获取当前已有的用户配置文件列表
            all_users = sorted(
                [
                    os.path.splitext(f)[0]
                    for f in os.listdir(self.user_dir)
                    if f.endswith(".ini")
                ]
            )

            # 检查认证状态
            is_authenticated = (
                hasattr(self, "is_authenticated") and self.is_authenticated
            )
            auth_username = getattr(self, "auth_username", None)
            auth_group = getattr(self, "auth_group", "guest")
            is_guest = getattr(self, "is_guest", False)

            # ========== 权限检查：根据用户权限过滤可见的用户列表 ==========
            # 这是一个关键的安全功能，防止普通用户看到或访问其他用户的账户
            if is_guest:
                # 游客不返回任何用户列表
                # 游客没有任何权限，不应该看到任何学校账户
                users = []
                logging.debug(f"游客用户请求 get_initial_data，返回空用户列表")
            elif auth_username and not is_guest:
                # 已认证的非游客用户：需要检查 auto_fill_password 权限
                # 此权限决定用户是否可以查看和自动填充所有学校账户的密码

                # 第一步：检查是否有 auto_fill_password 权限
                has_view_all_permission = False

                # 方法1：检查用户组（管理员自动拥有此权限）
                if auth_group in ["admin", "super_admin"]:
                    has_view_all_permission = True
                    logging.debug(
                        f"用户 {auth_username} 是管理员，拥有查看所有账户的权限"
                    )
                elif hasattr(self, "auth_system"):
                    # 方法2：使用 auth_system 检查权限（支持差分化授权）
                    # 即使用户不是管理员，也可能通过 user_custom_permissions 获得此权限
                    try:
                        has_view_all_permission = auth_system.check_permission(
                            auth_username, "auto_fill_password"
                        )
                        if has_view_all_permission:
                            logging.debug(
                                f"用户 {auth_username} 通过自定义权限获得了查看所有账户的权限"
                            )
                    except Exception as e:
                        # 权限检查失败（例如 auth_system 不可用），保持 False
                        logging.warning(
                            f"检查用户 {auth_username} 的 auto_fill_password 权限时出错: {e}"
                        )
                        pass

                # 第二步：根据权限决定返回的用户列表
                if has_view_all_permission:
                    # 有权限的用户可以查看所有 .ini 文件（所有学校账户）
                    # 这允许管理员管理和查看所有学校账户的信息
                    users = all_users
                    logging.debug(
                        f"用户 {auth_username} 有权限，返回所有 {len(users)} 个学校账户"
                    )
                else:
                    # 普通用户只能看到自己的账户（从 school_accounts/<auth_username>.json 加载）
                    # 这是关键的安全措施：防止普通用户访问其他用户的账户密码
                    users = []

                    # 加载该认证用户自己的学校账户列表
                    # _load_user_school_accounts 返回格式：{school_username: {"password": "xxx", "ua": "xxx"}, ...}
                    school_accounts = self._load_user_school_accounts(auth_username)

                    if school_accounts:
                        # 提取所有学校账户的用户名（键）
                        users = list(school_accounts.keys())
                        logging.debug(
                            f"普通用户 {auth_username} 无全局权限，返回其自己的 {len(users)} 个学校账户"
                        )
                    else:
                        # 如果该用户还没有任何学校账户，返回空列表
                        logging.debug(f"普通用户 {auth_username} 还没有任何学校账户")
            else:
                # 未认证用户：返回所有用户列表（向后兼容旧版本逻辑）
                # 注意：这可能是一个安全风险，但为了向后兼容保留
                # 建议在未来版本中要求用户必须先认证才能访问
                users = all_users
                logging.debug(
                    f"未认证用户请求 get_initial_data，返回所有 {len(users)} 个账户（向后兼容）"
                )

            # 读取全局配置
            cfg = configparser.RawConfigParser()
            cfg.optionxform = str  # 保持键的大小写
            cfg.read(self.config_path, encoding="utf-8")

            # 确保有 Config 分段
            if not cfg.has_section("Config"):
                cfg.add_section("Config")

            last_user = cfg.get("Config", "LastUser", fallback="").strip()

            # 如果 last_user 不为空但对应的 .ini 不存在，则清空并写回
            if last_user and last_user not in all_users:
                logging.warning(f"LastUser '{last_user}' 不存在对应的 .ini，自动清空。")
                cfg.set("Config", "LastUser", "")
                try:
                    with open(self.config_path, "w", encoding="utf-8") as f:
                        cfg.write(f)
                except Exception as e:
                    logging.error(f"写回 config.ini 失败：{e}", exc_info=True)
                last_user = ""

            # 在返回数据前，先加载一次全局配置
            self._load_global_config()

            # 修复Issue 5: 检查是否已登录（会话持久化）
            is_logged_in = hasattr(self, "login_success") and self.login_success
            user_info = None
            if is_logged_in and hasattr(self, "user_info"):
                user_info = self.user_info

            logging.debug(
                f"Initial users={users}, last user={last_user}, logged_in={is_logged_in}"
            )

            # ========================================
            # 【本地验证码】读取验证码生成器配置
            # ========================================
            # 从config.ini的[Captcha]节读取本地验证码生成器的参数
            # 这些参数将传递给前端，用于"验证码设置"面板的初始化

            # 修复：定义本地读取函数或直接使用 cfg.get，避免 NameError
            def _safe_get_int(section, key, default):
                try:
                    return int(cfg.get(section, key, fallback=str(default)))
                except (ValueError, TypeError):
                    return int(default)

            def _safe_get_float(section, key, default):
                try:
                    return float(cfg.get(section, key, fallback=str(default)))
                except (ValueError, TypeError):
                    return float(default)

            captcha_settings = {
                "length": _safe_get_int("Captcha", "length", 4),
                "scale_factor": _safe_get_int("Captcha", "scale_factor", 2),
                "noise_level": _safe_get_float("Captcha", "noise_level", 0.08),
            }
            logging.debug(f"【本地验证码】加载验证码设置: {captcha_settings}")

            # [代码片段 2.1：替换掉旧的 return 语句]
            # 构造返回字典
            response_data = {
                "success": True,
                "users": users,
                "lastUser": last_user,
                # 确保使用 amap_js_key
                "amap_key": self.global_params.get("amap_js_key", ""),
                "isLoggedIn": is_logged_in,
                "userInfo": user_info,
                "is_authenticated": is_authenticated,
                "auth_username": auth_username,
                "auth_group": auth_group,
                "is_guest": is_guest,
                # [修复] 添加多账号模式状态，用于会话恢复和PC/移动端切换
                "is_multi_account_mode": getattr(self, "is_multi_account_mode", False),
                # 【本地验证码】添加验证码设置到响应数据
                "captcha_settings": captcha_settings,
            }

            # [BUG 2 修复] 如果是已登录状态（会话恢复），则从实例中提取 device_ua
            # (注意：self.device_ua 是在 restore_session_to_api_instance 中被恢复的)
            if is_logged_in and hasattr(self, "device_ua"):
                response_data["device_ua"] = self.device_ua

            logging.debug(
                f"Initial data response prepared: users={len(users)}, last user={last_user}, logged_in={is_logged_in}, ua_sent={response_data.get('device_ua') is not None}"
            )

            return response_data
        except Exception as e:
            logging.error(f"获取初始数据时发生错误: {e}", exc_info=True)
            self.is_offline_mode = True
            return {
                "success": False,
                "offline": True,
                "message": "后端无法连接服务器，已切换到离线模式",
            }

    def get_user_sessions(self):
        """获取当前认证用户的会话列表（供前端调用）"""
        logging.info("API调用: get_user_sessions - 获取当前用户的所有活动会话列表")

        # 检查当前会话是否已认证且非游客
        auth_username = getattr(self, "auth_username", None)
        is_guest = getattr(self, "is_guest", True)

        if not auth_username or is_guest:
            logging.warning("get_user_sessions: 用户未登录或为游客，返回空列表。")
            # 游客或未登录用户没有关联会话，返回成功但列表为空
            # 对于游客，特殊处理：只返回当前会话信息
            if is_guest and hasattr(self, "_web_session_id"):
                current_session_id = self._web_session_id
                session_file = get_session_file_path(current_session_id)
                created_at = 0
                last_activity = 0
                if os.path.exists(session_file):
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            s_data = json.load(f)
                        created_at = s_data.get("created_at", 0)
                        last_activity = s_data.get("last_accessed", 0)
                    except Exception:
                        pass  # 忽略读取错误

                guest_session_info = [
                    {
                        "session_id": current_session_id,
                        "session_hash": hashlib.sha256(
                            current_session_id.encode()
                        ).hexdigest()[:16],
                        "created_at": created_at,
                        "last_activity": last_activity,
                        "is_current": True,
                        "login_success": False,  # 游客没有学校账号登录状态
                        "is_multi_account_mode": False,  # <-- 修复：添加此行
                        "user_data": {"username": "guest"},
                    }
                ]
                return jsonify(
                    {
                        "success": True,
                        "sessions": guest_session_info,
                        "max_sessions": -1,
                    }
                )
            else:
                # 非游客但未认证，或游客但无法获取当前session_id
                return {"success": True, "sessions": []}

        try:
            # 调用 AuthSystem 获取该用户关联的所有会话 ID
            session_ids = auth_system.get_user_sessions(auth_username)
            logging.debug(
                f"Found {len(session_ids)} linked session IDs for user {auth_username}"
            )

            sessions_info = []
            current_session_id = getattr(
                self, "_web_session_id", None
            )  # 获取当前请求的会话ID

            for sid in session_ids:
                # 检查会话是否还存在（文件是否存在）
                session_file = get_session_file_path(sid)
                if os.path.exists(session_file):
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            session_data = json.load(f)

                        # 确保加载的数据属于当前用户 (虽然理论上 link_session_to_user 保证了这一点)
                        if session_data.get("auth_username") == auth_username:
                            sessions_info.append(
                                {
                                    "session_id": sid,
                                    # 添加哈希
                                    "session_hash": hashlib.sha256(
                                        sid.encode()
                                    ).hexdigest()[:16],
                                    "created_at": session_data.get("created_at", 0),
                                    # 使用 last_accessed
                                    "last_activity": session_data.get(
                                        "last_accessed", 0
                                    ),
                                    "is_current": sid == session_id,
                                    "login_success": session_data.get(
                                        "login_success", False
                                    ),
                                    "is_multi_account_mode": session_data.get(
                                        "is_multi_account_mode", False
                                    ),  # <-- 修复：添加此行
                                    "user_data": session_data.get("user_data", {}),
                                }
                            )
                    except Exception as e:
                        logging.warning(
                            f"读取会话文件 {session_file} 失败: {e}, 跳过该会话。"
                        )
                        continue  # 跳过损坏或无法读取的文件

            logging.info(
                f"成功获取用户 {auth_username} 的 {len(sessions_info)} 个会话信息。"
            )
            return {"success": True, "sessions": sessions_info}
        except Exception as e:
            logging.error(f"获取用户会话列表时发生错误: {e}", exc_info=True)
            return {"success": False, "message": f"服务器内部错误: {e}"}

    def save_amap_key(self, api_key: str):
        """由JS调用，保存高德地图API Key到主配置文件"""
        try:
            self.global_params["amap_js_key"] = api_key
            cfg = configparser.RawConfigParser()
            cfg.optionxform = str  # 保持键的大小写
            if os.path.exists(self.config_path):
                cfg.read(self.config_path, encoding="utf-8")

            # 确保 [Map] 分区存在并更新 amap_js_key（新版）
            if not cfg.has_section("Map"):
                cfg.add_section("Map")
            cfg.set("Map", "amap_js_key", api_key)

            _write_config_with_comments(cfg, self.config_path)

            self.log("高德地图API Key已保存。")
            logging.info("已成功保存新的高德地图JavaScript API密钥")
            return {"success": True}
        except Exception as e:
            self.log(f"保存高德地图API Key失败: {e}")
            logging.error(f"保存高德地图JavaScript API密钥失败: {e}")
            return {"success": False, "message": str(e)}
        except Exception as e:
            self.log(f"API Key保存失败: {e}")
            logging.error(
                f"保存高德地图JavaScript API密钥时发生异常: {e}", exc_info=True
            )
            return {"success": False, "message": str(e)}

    def on_user_selected(self, username):
        # return
        """
        当用户在登录界面选择一个已有用户时调用。

        功能说明：
        - 返回选中用户的密码、UA和其他配置信息
        - 用于自动填充登录表单

        权限检查（安全增强）：
        - 管理员或有 auto_fill_password 权限的用户：可以查看所有学校账户的密码
        - 普通用户：只能查看自己的学校账户列表中的密码
        - 未认证用户：向后兼容，可以查看所有账户（但建议在未来版本中移除）

        参数:
            username: 选中的学校账户用户名

        返回:
            字典，包含 password, ua, params, userInfo
        """
        logging.info(
            f"API调用: on_user_selected - 用户选择事件触发，选中的用户名: '{username}'"
        )

        # ========== 输入验证 ==========
        # 如果没有提供用户名，返回空数据
        if not username:
            return {"password": "", "ua": "", "params": self.params, "userInfo": {}}

        # ========== 关键安全增强：权限检查 ==========
        # 获取当前认证用户的信息
        auth_username = getattr(self, "auth_username", None)  # 当前认证用户名
        auth_group = getattr(self, "auth_group", "guest")  # 用户组
        is_guest = getattr(self, "is_guest", False)  # 是否是游客
        is_authenticated = (
            hasattr(self, "is_authenticated") and self.is_authenticated
        )  # 是否已认证

        # 只对已认证的非游客用户进行权限检查
        if is_authenticated and auth_username and not is_guest:
            # 第一步：检查是否有 auto_fill_password 权限
            has_view_all_permission = False

            # 方法1：检查用户组（管理员自动拥有此权限）
            if auth_group in ["admin", "super_admin"]:
                has_view_all_permission = True
                logging.debug(f"用户 {auth_username} 是管理员，可以查看所有账户密码")
            elif hasattr(self, "auth_system"):
                # 方法2：使用 auth_system 检查权限（支持差分化授权）
                try:
                    has_view_all_permission = auth_system.check_permission(
                        auth_username, "auto_fill_password"
                    )
                    if has_view_all_permission:
                        logging.debug(
                            f"用户 {auth_username} 通过自定义权限获得了查看所有账户密码的权限"
                        )
                except Exception as e:
                    # 权限检查失败，保持 False
                    logging.warning(
                        f"检查用户 {auth_username} 的 auto_fill_password 权限时出错: {e}"
                    )
                    pass

            # 第二步：如果用户没有全局权限，检查是否在其授权列表中
            if not has_view_all_permission:
                # 普通用户只能查看自己的学校账户列表中的账户
                # 加载该认证用户自己的学校账户列表
                school_accounts = self._load_user_school_accounts(auth_username)

                # 检查请求的 username 是否在该用户的授权列表中
                if not school_accounts or username not in school_accounts:
                    # 权限不足：用户试图访问不属于他的账户
                    logging.warning(
                        f"权限拒绝: 普通用户 {auth_username} 试图访问未授权的学校账户 {username}"
                    )
                    # 返回空数据，不泄露任何信息
                    # 前端会显示为"未保存密码"或"新用户"
                    return {
                        "password": "",
                        "ua": "",
                        "params": self.params,
                        "userInfo": {},
                    }
                else:
                    # 权限验证通过：该账户在用户的授权列表中
                    logging.debug(
                        f"权限验证通过: 用户 {auth_username} 可以访问其学校账户 {username}"
                    )

        # ========== 权限检查通过或未启用认证，继续加载数据 ==========
        # 从配置文件加载密码
        # _load_config 会读取 school_accounts/<username>.ini 文件
        password = self._load_config(username)

        # 修复：如果配置文件不存在（password返回None），UA应该返回空字符串
        # 这样前端会显示"(新用户将在登录时自动生成)"
        if password is None:
            ua = ""
        else:
            ua = self.device_ua or ""

        # 记录调试日志（不记录真实密码，只记录是否存在）
        logging.debug(
            f"on_user_selected: username={username}, ua={ua}, password={'***' if password else 'empty'}"
        )

        # 构建用户信息字典
        info = {"name": self.user_data.name, "student_id": self.user_data.student_id}

        # 返回完整数据
        return {
            "password": password or "",
            "ua": ua,
            "params": self.params,
            "userInfo": info,
        }

    def generate_new_ua(self):
        """生成一个新的UA并保存"""
        logging.info("API调用: generate_new_ua - 生成新的随机User-Agent字符串")
        self.device_ua = ApiClient.generate_random_ua()
        cfg = configparser.ConfigParser()
        if os.path.exists(self.user_config_path):
            cfg.read(self.user_config_path, encoding="utf-8")
            if not cfg.has_section("System"):
                cfg.add_section("System")
            cfg.set("System", "UA", self.device_ua)
            with open(self.user_config_path, "w", encoding="utf-8") as f:
                cfg.write(f)
        logging.info(f"已成功生成新的User-Agent字符串: {self.device_ua}")
        return self.device_ua

    def login(self, username, password):
        logging.info(f"API调用: login - 用户登录请求，用户名: '{username}'")
        if not username or not password:
            return {"success": False, "message": "用户名和密码不能为空！"}

        self.log("正在登录...")
        logging.debug(f"正在尝试为用户进行登录认证: 用户名={username}")
        self.user_data = UserData()
        # 记录“登录时输入的账号”，作为兜底
        input_username = username
        # UA 如未生成则生成
        if not self.device_ua:
            self.device_ua = ApiClient.generate_random_ua()

        resp = self.api_client.login(input_username, password)
        if not resp or not resp.get("success"):
            msg = resp.get("message", "未知错误") if resp else "网络连接失败"
            self.log(f"服务器反馈登录失败：{msg}")
            logging.warning(f"用户登录失败: {msg}")
            return {"success": False, "message": msg}

        # 先解析用户信息，再决定用哪个“主键”保存
        self.log("登录成功，正在解析用户信息...")
        data = resp.get("data", {})
        user_info = data.get("userInfo", {})
        dept_info = data.get("deptInfo", {})
        ud = self.user_data

        ud.name = user_info.get("name", "")
        ud.phone = user_info.get("phone", "")
        ud.student_id = user_info.get("account", "")  # 学号/账号（后端唯一标识）
        ud.id = user_info.get("id", "")
        # 这里把 username 统一设成“学号”，而不是 nickname
        # 若后端未返回学号，则回退到输入的 username
        ud.username = ud.student_id or input_username

        ud.registration_time = user_info.get("createtime", "")
        ud.first_login_time = user_info.get("firstlogin", "")
        ud.id_card = user_info.get("iDcard", "")
        ud.current_login_time = user_info.get("logintime", "")
        ud.last_login_time = dept_info.get("logintime", "")
        ud.gender = dept_info.get("sexValue", "")
        ud.school_name = dept_info.get("schoolName", "")
        ud.attribute_type = dept_info.get("typeValue", "")

        # ---备份 user_info 到 school_accounts/<username>_backup.json ---
        try:
            # 确保 self.user_dir (即 school_accounts) 存在
            if ud.username and os.path.exists(self.user_dir):
                backup_filename = f"{ud.username}_backup.json"
                backup_filepath = os.path.join(self.user_dir, backup_filename)

                # 将 user_info 和 dept_info 合并备份
                backup_data = {
                    "userInfo": user_info,
                    "deptInfo": dept_info,
                    "backup_timestamp": time.time(),
                }

                with open(backup_filepath, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)

                logging.info(f"已成功备份 user_info 到: {backup_filepath}")
            elif not ud.username:
                logging.warning("备份 user_info 失败：无法确定用户名(学号)")

        except Exception as e:
            logging.error(f"备份 user_info 失败: {e}", exc_info=True)
            # 备份失败不应阻止登录流程，仅记录日志

        # 至此，ud.username 已经是“用于保存配置的主键”（学号优先）
        # 现在再保存配置（文件名与 LastUser 都用 ud.username）
        self._save_config(ud.username, password, self.device_ua)

        # 登录成功后，更新 school_account 密码和UA（使用 login_verified=True）
        if hasattr(self, "auth_username") and self.auth_username:
            self._update_school_account_password(
                self.auth_username,
                ud.username,
                password,
                self.device_ua,
                login_verified=True,
            )
            logging.info(
                f"已更新认证用户 {self.auth_username} 的 school_account {ud.username} 密码和UA（登录验证成功）"
            )

        # --- 登录成功后，立即获取并缓存签到半径 ---
        try:
            # None 表示这是在单账号模式下调用
            self._fetch_server_attendance_radius_if_needed(self.api_client, None)
        except Exception as e:
            self.log(f"获取签到半径失败: {e}")
            logging.warning(f"Failed to fetch attendance radius post-login: {e}")

        self._first_center_done = False
        logging.info(
            f"Login successful: uid={ud.id}, name={ud.name}, sid={ud.student_id}"
        )
        # 双保险：后端主动提示前端刷新任务列表
        if self.window:
            try:
                self.window.evaluate_js("refreshTasks()")
            except Exception:
                logging.debug(
                    "Attempt to trigger front-end refreshTasks failed (non-fatal)."
                )
        # --- 启动自动刷新线程 ---
        try:
            self.stop_auto_refresh.clear()
            if (
                self.auto_refresh_thread is None
                or not self.auto_refresh_thread.is_alive()
            ):
                self.auto_refresh_thread = threading.Thread(
                    target=self._auto_refresh_worker, daemon=True
                )
                self.auto_refresh_thread.start()
        except Exception as e:
            self.log(f"启动自动刷新线程失败: {e}")

        # 构造要返回给前端的 userInfo 字典
        user_info_dict = self._get_full_user_info_dict()
        # --- 将获取到的半径附加到返回信息中 ---
        user_info_dict["server_attendance_radius_m"] = self.server_attendance_radius_m

        # 修复Issue 5: 设置登录状态标志用于会话持久化
        self.login_success = True
        self.user_info = user_info_dict
        logging.info(
            f"会话状态已保存: login_success={self.login_success}, user_id={ud.id}"
        )

        # --- 预加载前5条通知并缓存到会话 ---
        cached_notifications = None
        try:
            logging.info("登录成功后预加载前5条通知...")
            notif_result = self.get_notifications(
                is_auto_refresh=False, request_limit=5, request_offset=0
            )
            if notif_result and notif_result.get("success"):
                cached_notifications = {
                    "notices": notif_result.get("notices", []),
                    "unreadCount": notif_result.get("unreadCount", 0),
                    "cached_at": time.time(),
                }
                # 保存到实例属性中，后续会被 save_session_state 保存
                self.cached_notifications = cached_notifications
                logging.info(
                    f"成功预加载并缓存 {len(cached_notifications['notices'])} 条通知"
                )
        except Exception as e:
            logging.warning(f"预加载通知失败（非致命错误）: {e}")

        # --- 在成功登录的返回结果中包含 auth_group ---
        auth_group = getattr(
            self, "auth_group", "guest"
        )  # 从 Api 实例获取认证时确定的组

        return {
            "success": True,
            "userInfo": user_info_dict,
            "ua": self.device_ua,
            "amap_key": self.global_params.get("amap_js_key", ""),
            "auth_group": auth_group,
            "cached_notifications": cached_notifications,  # 返回缓存的通知给前端
        }

    def logout(self):
        """处理注销逻辑"""
        logging.info("API调用: logout - 用户注销登出操作")
        self.log("已注销。")
        logging.info("用户已成功登出，正在清除会话和状态数据")
        # --- 停止自动刷新线程 ---
        try:
            self.stop_auto_refresh.set()
            if self.auto_refresh_thread and self.auto_refresh_thread.is_alive():
                self.auto_refresh_thread.join(timeout=1.0)
            self.auto_refresh_thread = None
        except Exception as e:
            logging.warning(f"停止自动刷新线程失败: {e}")

        # 修复Issue 5: 清除登录状态标志
        self.login_success = False
        self.user_info = None

        self._init_state_variables()
        self._load_global_config()
        self.api_client.session.cookies.clear()
        return {"success": True}

    def load_tasks(self):
        """加载任务列表（增强：稳健去重 + 并发保护 + 离线模式支持）"""
        logging.info("API调用: load_tasks - 加载用户任务列表")

        # 离线模式或无用户ID但有任务数据时，直接返回已加载的任务
        if not self.user_data.id:
            # 检查是否有已加载的任务（例如从会话恢复或导入的离线文件）
            if hasattr(self, "all_run_data") and self.all_run_data:
                logging.info(
                    f"load_tasks: 离线模式，返回已加载的 {len(self.all_run_data)} 个任务"
                )
                tasks_for_js = []
                for run in self.all_run_data:
                    task_dict = run.__dict__.copy()
                    task_dict["info_text"] = self._get_task_info_text(run)
                    tasks_for_js.append(task_dict)
                return {"success": True, "tasks": tasks_for_js}
            else:
                return {"success": False, "message": "用户未登录且无离线任务"}

        # 并发保护：避免多次快速点击导致并发刷新交错
        if not hasattr(self, "_load_tasks_lock"):
            self._load_tasks_lock = threading.RLock()
        if not hasattr(self, "_load_tasks_inflight"):
            self._load_tasks_inflight = False

        with self._load_tasks_lock:
            if self._load_tasks_inflight:
                logging.debug("load_tasks skipped: another refresh is in-flight.")
                # 返回当前缓存（避免空白）——即使并发点击，也不会重复追加
                tasks_for_js = []
                for run in self.all_run_data:
                    task_dict = run.__dict__.copy()
                    task_dict["info_text"] = self._get_task_info_text(run)
                    tasks_for_js.append(task_dict)
                return {"success": True, "tasks": tasks_for_js}

            self._load_tasks_inflight = True
            try:
                self.log("正在获取任务列表...")
                logging.debug("正在从服务器获取任务运行列表数据")

                # 重置缓存
                self.all_run_data = []
                # 复合去重：优先 errandId；若为空或重复，则落到 schedule+时间 的复合 key
                seen_keys: set[str] = set()
                offset = 0
                dup_count = 0

                while True:
                    resp = self.api_client.get_run_list(self.user_data.id, offset)
                    if not resp or not resp.get("success"):
                        self.log("获取任务列表失败。")
                        logging.warning("从服务器获取任务列表失败")
                        break

                    tasks = resp.get("data", {}).get("errandList", [])
                    if not tasks:
                        break

                    for td in tasks:
                        eid = td.get("errandId") or ""
                        es = td.get("errandSchedule") or ""
                        st = td.get("startTime") or ""
                        et = td.get("endTime") or ""

                        # 构造稳健唯一键（兼容 errandId 缺失 / 重复）
                        # 优先 errandId；若为空，则用 "SCHEDULE|START|END" 兜底；若 errandId 存在也加入 schedule 时间以提高稳健性
                        unique_key = f"{eid}|{es}|{st}|{et}"

                        if unique_key in seen_keys:
                            dup_count += 1
                            continue
                        seen_keys.add(unique_key)

                        run = RunData()
                        run.run_name = td.get("eName")

                        # 统一将 isExecute 规范为整型 0/1，防止字符串导致后续比较失败
                        try:
                            run.status = int(td.get("isExecute") or 0)
                        except (TypeError, ValueError):
                            run.status = (
                                1 if str(td.get("isExecute")).strip() == "1" else 0
                            )

                        run.errand_id = td.get("errandId")
                        run.errand_schedule = td.get("errandSchedule")
                        run.start_time = td.get("startTime")
                        run.end_time = td.get("endTime")
                        run.upload_time = td.get("updateTime")
                        self.all_run_data.append(run)

                    offset += len(tasks)
                    if len(tasks) < 10:
                        break

                # 日志与前端数据整理
                self.log(f"任务列表加载完毕，共 {len(self.all_run_data)} 项。")
                if dup_count > 0:
                    logging.info(
                        f"Task de-dup completed: {dup_count} duplicates skipped (robust key)."
                    )

                tasks_for_js = []
                for run in self.all_run_data:
                    task_dict = run.__dict__.copy()
                    task_dict["info_text"] = self._get_task_info_text(run)
                    tasks_for_js.append(task_dict)
                return {"success": True, "tasks": tasks_for_js}
            finally:
                self._load_tasks_inflight = False

    def _try_parse_dt(self, s):
        """
        (已重构为类方法)
        尝试将不同格式的时间字符串解析为 datetime，支持多种常见格式和值类型。失败返回 None。
        """
        if not s:
            return None
        # 若为数字字符串或数字（可能是时间戳毫秒/秒）
        try:
            if isinstance(s, (int, float)):
                # 判断是秒还是毫秒（如果大于 10^12 认为是毫秒）
                ts = int(s)
                if ts > 1e12:
                    return datetime.datetime.fromtimestamp(ts / 1000.0)
                if ts > 1e9:
                    return datetime.datetime.fromtimestamp(ts / 1000.0)
                return datetime.datetime.fromtimestamp(ts)
            if s.isdigit():
                ts = int(s)
                if ts > 1e12:
                    return datetime.datetime.fromtimestamp(ts / 1000.0)
                if ts > 1e9:
                    return datetime.datetime.fromtimestamp(ts / 1000.0)
                return datetime.datetime.fromtimestamp(ts)
        except Exception:
            pass

        # 尝试多种常见格式
        fmts = [
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M",
        ]
        for f in fmts:
            try:
                return datetime.datetime.strptime(s, f)
            except Exception:
                continue
        # 尝试 ISO 解析的简易回退（去掉时区 Z）
        try:
            txt = s.rstrip("Z").split("+")[0]
            return datetime.datetime.fromisoformat(txt)
        except Exception:
            pass
        return None

    def _get_task_info_text(self, run: RunData) -> str:
        """根据任务状态生成一个简短的信息文本（增强：多格式时间解析、稳健回退）"""
        if run.status == 1:
            return "已完成"

        now = datetime.datetime.now()
        ignore_time = self.params.get("ignore_task_time", True)

        def try_parse_dt(s):
            """尝试将不同格式的时间字符串解析为 datetime，支持多种常见格式和值类型。失败返回 None。"""
            if not s:
                return None
            # 若为数字字符串或数字（可能是时间戳毫秒/秒）
            try:
                if isinstance(s, (int, float)):
                    # 判断是秒还是毫秒（如果大于 10^12 认为是毫秒）
                    ts = int(s)
                    if ts > 1e12:
                        return datetime.datetime.fromtimestamp(ts / 1000.0)
                    if ts > 1e9:
                        return datetime.datetime.fromtimestamp(ts / 1000.0)
                    return datetime.datetime.fromtimestamp(ts)
                if s.isdigit():
                    ts = int(s)
                    if ts > 1e12:
                        return datetime.datetime.fromtimestamp(ts / 1000.0)
                    if ts > 1e9:
                        return datetime.datetime.fromtimestamp(ts / 1000.0)
                    return datetime.datetime.fromtimestamp(ts)
            except Exception:
                pass

            # 尝试多种常见格式
            fmts = [
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%d %H:%M",
            ]
            for f in fmts:
                try:
                    return datetime.datetime.strptime(s, f)
                except Exception:
                    continue
            # 尝试 ISO 解析的简易回退（去掉时区 Z）
            try:
                txt = s.rstrip("Z").split("+")[0]
                return datetime.datetime.fromisoformat(txt)
            except Exception:
                pass
            return None

        # 检查是否已过期
        if run.end_time:
            end_dt = self._try_parse_dt(run.end_time)
            if end_dt:
                if (ignore_time and end_dt.date() < now.date()) or (
                    not ignore_time and end_dt < now
                ):
                    return "已过期"

        # 检查是否未开始
        if run.start_time:
            start_dt = self._try_parse_dt(run.start_time)
            if start_dt:
                if (ignore_time and now.date() < start_dt.date()) or (
                    not ignore_time and now < start_dt
                ):
                    # 返回更简洁的未开始标记，便于前端直接判断显示“未开始”
                    return f"开始于: {start_dt.strftime('%Y-%m-%d')}"
            else:
                # 若解析失败但字符串明显为仅有日期（例如 '2025-09-30'）且长度合适，尝试按日期对比
                try:
                    s = str(run.start_time).strip()
                    if len(s) == 10 and s[4] == "-" and s[7] == "-":
                        sd = datetime.datetime.strptime(s, "%Y-%m-%d")
                        if (ignore_time and now.date() < sd.date()) or (
                            not ignore_time and now < sd
                        ):
                            return f"开始于: {sd.strftime('%Y-%m-%d')}"
                except Exception:
                    pass

        # 进行中或带截止日期的显示
        if run.end_time:
            try:
                # 优先以可解析的 end_time 的日期部分显示
                end_dt = self._try_parse_dt(run.end_time)
                if end_dt:
                    return f"截止: {end_dt.strftime('%Y-%m-%d')}"
            except Exception:
                pass

        return "进行中"

    def get_task_details(self, index):
        """获取指定任务的详细信息"""
        logging.info(f"API调用: get_task_details - 获取任务详细信息，任务索引: {index}")
        if not (0 <= index < len(self.all_run_data)):
            return {"success": False, "message": "无效的任务索引"}

        self.current_run_idx = index
        run_data = self.all_run_data[index]

        if run_data.details_fetched:
            task_dict = run_data.__dict__.copy()
            task_dict["target_range_m"] = self.target_range_m
            return {"success": True, "details": task_dict}

        self.log(f"正在加载任务详情...")
        logging.debug(
            f"正在获取任务详细信息: 任务索引={index}, 任务名称={run_data.run_name}"
        )
        resp = self.api_client.get_run_details(
            run_data.errand_id, self.user_data.id, run_data.errand_schedule
        )

        if resp and resp.get("success"):
            details = resp.get("data", {}).get("errandDetail", {})
            run_data.target_points = [
                (float(p["lon"]), float(p["lat"]))
                for p in details.get("geoCoorList", [])
                if p.get("lon") is not None and p.get("lat") is not None
            ]
            run_data.target_point_names = "|".join(
                [p.get("name", "") for p in details.get("geoCoorList", [])]
            )

            if not run_data.target_points:
                logging.warning(
                    f"[警告] 任务 '{run_data.run_name}' (ScheduleID: {run_data.errand_schedule}) 未包含任何打卡点 (geoCoorList为空)。"
                )

            temp_coords = []
            walk_paths = details.get("walkPaths", [])
            if walk_paths:
                for i, seg in enumerate(walk_paths):
                    for pt in seg:
                        if (
                            isinstance(pt, list)
                            and len(pt) == 2
                            and pt[0] is not None
                            and pt[1] is not None
                        ):
                            try:
                                temp_coords.append((float(pt[0]), float(pt[1])))
                            except (TypeError, ValueError):
                                logging.warning(
                                    f"Invalid coordinate in recommended path: {pt}"
                                )
                    if i < len(walk_paths) - 1:
                        temp_coords.append((0.0, 0.0))
            run_data.recommended_coords = temp_coords
            run_data.details_fetched = True
            self.log("任务详情加载成功。")
            logging.debug(
                f"任务详情获取成功: 目标点数量={len(run_data.target_points)}, 推荐路径点数量={len(run_data.recommended_coords)}"
            )
            task_dict = run_data.__dict__.copy()
            task_dict["target_range_m"] = self.target_range_m
            return {"success": True, "details": task_dict}
        else:
            self.log("获取任务详情失败。")
            logging.warning("从服务器获取任务详情失败")
            return {"success": False, "message": "获取任务详情失败"}

    def set_draft_path(self, coords):
        """接收前端手动绘制的草稿路径"""

        # 添加对 coords 为 None 的检查，防止 TypeError
        if coords is None:
            # coords 可能是 None，例如在清除路径时调用
            # 这种情况应该被视为空路径，而不是错误
            coords_len = 0
            logging.info(f"API调用: set_draft_path - 接收到空的(None)草稿路径")
        else:
            try:
                coords_len = len(coords)
            except TypeError:
                # coords 不是一个列表或None，这是一个错误
                logging.error(
                    f"set_draft_path 失败：coords 参数不是一个列表: {type(coords)}",
                    exc_info=True,
                )
                return {"success": False, "message": "无效的路径数据格式"}

        logging.info(f"API调用: set_draft_path - 设置草稿路径，点数: {coords_len}")

        # 修复索引检查：必须检查索引是否在 all_run_data 的当前范围内
        # 之前的检查 (== -1) 不足以防止索引越界 (IndexError)
        if not (0 <= self.current_run_idx < len(self.all_run_data)):
            logging.warning(
                f"set_draft_path 失败：任务索引无效 (Index: {self.current_run_idx}, List length: {len(self.all_run_data)})"
            )
            return {"success": False, "message": "未选择任务或任务列表已失效"}

        try:
            run = self.all_run_data[self.current_run_idx]

            # 修复数据格式错误：
            # 1. 确保 coords 是一个可迭代对象 (在开头已检查)
            # 2. 确保 c 是一个字典 (使用 .get 避免 TypeError/KeyError)

            draft_coords_list = []
            if coords:  # 仅在 coords 不为 None 或空列表时迭代
                for c in coords:
                    # 确保 c 是一个字典
                    if not isinstance(c, dict):
                        logging.warning(
                            f"set_draft_path: 跳过无效的坐标点（非字典）: {c}"
                        )
                        continue

                    # 使用 .get() 避免 KeyError，如果缺少键则返回 None
                    lng = c.get("lng")
                    lat = c.get("lat")

                    # 确保经纬度都存在
                    if lng is None or lat is None:
                        logging.warning(
                            f"set_draft_path: 跳过无效的坐标点（缺少lng或lat）: {c}"
                        )
                        continue

                    draft_coords_list.append((lng, lat, c.get("isKey", 0)))

            run.draft_coords = draft_coords_list

            logging.debug(f"已成功设置草稿路径，包含 {len(run.draft_coords)} 个坐标点")
            return {"success": True}

        except IndexError:
            # 捕获万一发生的竞态条件（例如列表在检查后但在访问前被清空）
            logging.error(
                f"set_draft_path 发生索引错误: Index {self.current_run_idx}, List length {len(self.all_run_data)}",
                exc_info=True,
            )
            return {"success": False, "message": "服务器内部错误：任务列表索引失效"}
        except (TypeError, KeyError) as e:
            # 捕获无效的 coords 数据结构
            logging.error(f"set_draft_path 发生数据结构错误: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"服务器内部错误：路径数据格式无效 ({e})",
            }
        except Exception as e:
            # 捕获所有其他意外错误
            logging.error(f"set_draft_path 发生未知错误: {e}", exc_info=True)
            return {"success": False, "message": f"服务器内部错误: {e}"}

    def _calculate_distance_m(self, lon1, lat1, lon2, lat2):
        """
        使用Haversine公式精确计算两个GPS坐标点之间的距离（米）。

        算法说明：
        - 使用Haversine公式考虑地球曲率
        - 适用于任意距离和任意纬度
        - 精度高，适合GPS应用

        Haversine公式：
        a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
        c = 2 * atan2(√a, √(1-a))
        distance = R * c

        其中 R = 6371000 米（地球平均半径）

        ✓ 改进：
        1. 考虑地球曲率，精度更高
        2. 适用于任意纬度（赤道、极地均可）
        3. 适用于任意距离（短距离和长距离）
        4. 标准的GPS距离计算方法

        参数:
            lon1 (float): 起点经度（度）
            lat1 (float): 起点纬度（度）
            lon2 (float): 终点经度（度）
            lat2 (float): 终点纬度（度）

        返回:
            float: 距离（米）

        示例:
            >>> _calculate_distance_m(120.0, 30.0, 120.01, 30.01)
            1536.8  # 约1.5公里（更精确）
        """
        # 地球平均半径（米）
        R = 6371000

        # 转换为弧度
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        # Haversine公式
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

    def _calculate_distances_vectorized(self, coords):
        """
        ✓ 使用NumPy向量化计算多个坐标点之间的距离（性能优化，问题#11）

        参数:
            coords: [(lon, lat, interval_ms), ...] 坐标列表

        返回:
            float: 总距离（米）

        说明:
            当NumPy可用时，使用向量化操作一次性计算所有相邻点的距离，
            比逐对计算快10-100倍（取决于点数）。如果NumPy不可用，回退到循环计算。
        """
        if len(coords) < 2:
            return 0.0

        # 尝试使用numpy向量化计算（如果可用）
        if np is not None:
            try:
                # 提取经纬度到numpy数组
                lons = np.array([c[0] for c in coords])
                lats = np.array([c[1] for c in coords])

                # 计算相邻点的差值
                delta_lons = np.diff(lons)
                delta_lats = np.diff(lats)

                # 转换为弧度（向量化）
                lat1_rad = np.radians(lats[:-1])
                lat2_rad = np.radians(lats[1:])
                delta_lat_rad = np.radians(delta_lats)
                delta_lon_rad = np.radians(delta_lons)

                # Haversine公式（向量化）
                R = 6371000
                a = (
                    np.sin(delta_lat_rad / 2) ** 2
                    + np.cos(lat1_rad)
                    * np.cos(lat2_rad)
                    * np.sin(delta_lon_rad / 2) ** 2
                )
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
                distances = R * c

                return np.sum(distances)
            except Exception as e:
                logging.debug(f"[性能优化] NumPy向量化计算失败，回退到循环: {e}")

        # 回退到循环计算（当NumPy不可用或失败时）
        total_dist = 0.0
        for i in range(len(coords) - 1):
            total_dist += self._calculate_distance_m(
                coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1]
            )
        return total_dist

    def _gps_random_offset(self, lon, lat, params):
        """
        对GPS坐标添加随机偏移，模拟真实GPS的漂移误差。

        功能说明：
        真实GPS定位存在误差（通常5-10米），为了让模拟轨迹更真实，
        需要在关键点之间的插值点上添加随机偏移，避免完美的直线。

        偏移计算：
        1. 从params中读取偏移范围（location_random_m，单位：米）
        2. 在[-m, m]范围内随机选择偏移量
        3. 将米转换为经纬度偏移：
           - 经度偏移 = 米 / 102834.74
           - 纬度偏移 = 米 / 111712.69

        使用场景：
        - 关键点（打卡点）：不添加偏移，保持精确坐标
        - 插值点：添加偏移，模拟GPS漂移

        转换系数说明：
        - 同_calculate_distance_m，基于纬度30度的近似值
        - 经度转换随纬度变化，但对小偏移影响不大

        ⚠️ 注意：
        1. 偏移是独立的，经度和纬度分别随机
        2. 实际GPS误差可能有方向性（如受建筑遮挡）
        3. 偏移量过大会导致轨迹看起来不自然

        参数:
            lon (float): 原始经度
            lat (float): 原始纬度
            params (dict): 参数字典，必须包含'location_random_m'键

        返回:
            tuple: (偏移后的经度, 偏移后的纬度)

        示例:
            >>> params = {'location_random_m': 5}  # 5米偏移
            >>> _gps_random_offset(120.0, 30.0, params)
            (120.00003, 30.00004)  # 偏移约5米
        """
        m = params["location_random_m"]  # 偏移范围（米）
        # 在[-m, m]范围内随机偏移，然后转换为经纬度
        return (
            lon + random.uniform(-m, m) / 102834.74,
            lat + random.uniform(-m, m) / 111712.69,
        )

    def process_path(self):
        """
        处理草稿路径，生成带有时间戳的模拟运动轨迹。

        功能概述：
        将用户在地图上绘制的草稿路径（draft_coords）转换为详细的
        模拟跑步轨迹（run_coords），包含坐标、时间间隔、速度变化。

        算法流程：
        1. 读取草稿路径（关键点序列）
        2. 计算每个时间间隔的移动距离（速度×时间）
        3. 沿着草稿路径插值生成密集的坐标点
        4. 为非关键点添加GPS随机偏移，模拟真实GPS漂移
        5. 记录每个点的时间戳（累积时间）

        数据结构：
        - draft_coords: [(lon, lat, is_key_point), ...]
          - is_key_point=1表示打卡点，必须精确经过
          - is_key_point=0表示普通路径点，可以添加偏移

        - run_coords: [(lon, lat, interval_ms), ...]
          - interval_ms: 距离上一个点的时间间隔（毫秒）
          - 第一个点的interval_ms为0

        模拟参数（从self.params读取）：
        - interval_ms: 上报间隔（毫秒），如5000 = 5秒上报一次
        - interval_random_ms: 间隔随机变化范围
        - speed_mps: 平均速度（米/秒），如3 m/s = 10.8 km/h
        - speed_random_mps: 速度随机变化范围
        - location_random_m: GPS随机偏移范围（米）

        算法特点：
        1. 真实性：速度、间隔、位置都添加随机性
        2. 精确性：保证经过所有打卡点
        3. 连续性：轨迹在草稿路径上连续移动
        4. 可控性：通过参数控制运动特征

        ⚠️ 潜在问题：
        1. 循环嵌套较深，大量坐标点时性能较差
        2. 浮点数累积误差可能导致总距离略有偏差
        3. 速度随机性可能导致局部速度异常（过快或过慢）

        💡 优化建议：
        1. 对超长路径进行分段处理
        2. 缓存距离计算结果
        3. 添加速度平滑算法（避免突变）

        返回:
            dict: {
                "success": True,
                "run_coords": [(lon, lat, interval_ms), ...],
                "total_dist": 总距离（米）,
                "total_time": 总时长（秒）
            }
        """
        logging.info("API调用: process_path - 处理路径，生成模拟运动轨迹")

        # 检查是否选择了任务
        if self.current_run_idx == -1:
            return {"success": False, "message": "未选择任务"}

        run = self.all_run_data[self.current_run_idx]

        # 检查草稿路径是否有效（至少需要起点和终点）
        if not run.draft_coords or len(run.draft_coords) < 2:
            return {"success": False, "message": "没有可处理的路径"}

        self.log("正在处理路径...")
        logging.debug(
            f"正在处理路径: 将 {len(run.draft_coords)} 个草稿点转换为运动坐标序列"
        )

        draft = run.draft_coords  # 草稿路径：用户绘制的关键点
        run.run_coords = []  # 清空之前的模拟路径

        # ===== 步骤1：处理起点 =====
        start_lon, start_lat = draft[0][0], draft[0][1]
        # 如果起点是关键点（打卡点），保持精确坐标；否则添加随机偏移
        lon, lat = (
            (start_lon, start_lat)
            if draft[0][2] == 1
            else self._gps_random_offset(start_lon, start_lat, self.params)
        )
        # 起点的时间间隔为0（初始位置）
        run.run_coords.append((lon, lat, 0))

        # 初始化统计变量
        total_dist, total_time = 0.0, 0.0
        current_gps_pos, draft_idx = (draft[0][0], draft[0][1]), 0  # 当前位置和草稿索引
        p = self.params  # 简化参数引用

        # ===== 步骤2：主循环 - 沿草稿路径插值生成坐标点 =====
        # 算法思想：
        # - 每次迭代代表一个时间间隔（如5秒）
        # - 根据速度和时间计算这个间隔内应该移动的距离
        # - 沿着草稿路径向前移动这段距离，找到新位置
        # - 如果这段距离跨越多个草稿段，需要累积移动

        # ✓ 速度平滑：使用移动平均避免速度突变（问题#12修复）
        speed_history = []  # 记录最近的速度值
        speed_window = 3  # 移动平均窗口大小

        while draft_idx < len(draft) - 1:
            interval_t = max(
                0.2,
                random.uniform(
                    p["interval_ms"] - p["interval_random_ms"],
                    p["interval_ms"] + p["interval_random_ms"],
                )
                / 1000.0,
            )

            # 生成随机速度
            raw_speed = max(
                0.2,
                random.uniform(
                    p["speed_mps"] - p["speed_random_mps"],
                    p["speed_mps"] + p["speed_random_mps"],
                ),
            )

            # ✓ 应用速度平滑算法
            speed_history.append(raw_speed)
            if len(speed_history) > speed_window:
                speed_history.pop(0)  # 保持窗口大小
            # 使用移动平均作为实际速度
            speed = sum(speed_history) / len(speed_history)

            dist_to_go = speed * interval_t

            final_pos, temp_draft_idx = current_gps_pos, draft_idx
            # 内层循环：沿着草稿路径移动dist_to_go距离
            # 如果一条段不够长，就继续下一段，直到移动完成或到达路径终点
            while dist_to_go > 0 and temp_draft_idx < len(draft) - 1:
                # 当前段：从final_pos到下一个草稿点
                seg_start_gps, seg_end_gps = final_pos, (
                    draft[temp_draft_idx + 1][0],
                    draft[temp_draft_idx + 1][1],
                )
                # 计算这一段的长度
                seg_dist = self._calculate_distance_m(
                    seg_start_gps[0], seg_start_gps[1], seg_end_gps[0], seg_end_gps[1]
                )

                # 情况1：这一段足够长，可以在段内插值
                if seg_dist >= dist_to_go:
                    # 线性插值：在段的起点和终点之间按比例找到位置
                    # ratio = 0 在起点，ratio = 1 在终点
                    # 🐛 潜在bug：seg_dist为0时会导致除零，已用三元运算符防护
                    ratio = dist_to_go / seg_dist if seg_dist > 0 else 0
                    # 计算插值位置：起点 + ratio × (终点 - 起点)
                    final_pos = (
                        seg_start_gps[0] + ratio * (seg_end_gps[0] - seg_start_gps[0]),
                        seg_start_gps[1] + ratio * (seg_end_gps[1] - seg_start_gps[1]),
                    )
                    # 已移动完成，更新索引
                    dist_to_go, draft_idx = 0, temp_draft_idx
                # 情况2：这一段不够长，移动到段终点后继续下一段
                else:
                    # 减去这一段的距离，还需要继续移动
                    dist_to_go -= seg_dist
                    # 移动到段终点
                    final_pos = seg_end_gps
                    # 前进到下一个草稿段
                    temp_draft_idx += 1
                    # 如果下一个点是关键点（打卡点），必须在此停止
                    # 因为关键点不能跳过，必须精确到达
                    if draft[temp_draft_idx][2] == 1:
                        dist_to_go = 0

            # 边界情况：如果所有草稿段都用完了还没移动够dist_to_go
            # 说明草稿路径太短，强制移动到终点
            # 🐛 这种情况理论上不应该发生，可能说明参数配置有问题
            if dist_to_go > 0:
                final_pos = (draft[-1][0], draft[-1][1])
            # 更新当前位置和草稿索引，为下一次迭代做准备
            draft_idx, current_gps_pos = temp_draft_idx, final_pos

            # 检查final_pos是否是关键点（打卡点）
            # 如果是关键点，保持精确坐标；如果不是，添加GPS随机偏移
            # ✓ 使用epsilon容差比较，避免浮点数精度问题
            epsilon = 1e-9  # 容差值，约0.0001米
            is_key_point = any(
                abs(d[0] - final_pos[0]) < epsilon
                and abs(d[1] - final_pos[1]) < epsilon
                and d[2] == 1
                for d in draft
            )
            # 根据是否关键点决定是否添加偏移
            lon, lat = (
                (final_pos[0], final_pos[1])
                if is_key_point
                else self._gps_random_offset(final_pos[0], final_pos[1], self.params)
            )

            # ✓ 优化：在生成点的同时计算距离，避免二次遍历
            if len(run.run_coords) > 0:
                prev_coord = run.run_coords[-1]
                segment_dist = self._calculate_distance_m(
                    prev_coord[0], prev_coord[1], lon, lat
                )
                total_dist += segment_dist

            # 添加到run_coords：(经度, 纬度, 距上一点的时间间隔毫秒)
            run.run_coords.append((lon, lat, int(interval_t * 1000)))
            # 累计总时间
            total_time += interval_t

        # ===== 步骤3：计算总距离 ===== (已优化，在生成点时同时计算)

        # 保存结果到run_data对象
        run.total_run_time_s, run.total_run_distance_m = total_time, total_dist
        self.log(f"处理完成。")
        logging.info(
            f"路径处理完成: 生成坐标点数={len(run.run_coords)}, 总距离={total_dist:.1f}米, 总时长={total_time:.1f}秒"
        )
        # 返回成功结果，包含生成的坐标序列和统计信息
        return {
            "success": True,
            "run_coords": run.run_coords,
            "total_dist": total_dist,
            "total_time": total_time,
        }

    def check_target_reached_during_run(
        self, run_data: RunData, current_lon: float, current_lat: float
    ):
        """
        在模拟运行时，检查当前位置是否到达了打卡点。

        功能说明：
        跑步任务通常有多个打卡点（如起点、中间点、终点），必须依次经过。
        此函数在每次位置更新时调用，检测是否进入打卡点范围内。

        打卡点状态机：
        1. 未进入区域 (is_in_target_zone=False) → 进入区域后触发打卡
        2. 已在区域内 (is_in_target_zone=True) → 避免重复打卡
        3. 离开区域 → 重置状态，准备检测下一个打卡点

        关键逻辑：
        - 打卡点必须按顺序(target_sequence)依次到达
        - 每个打卡点只能打卡一次（通过is_in_target_zone标志防重）
        - 打卡成功后自动移动到下一个打卡点
        - 如果当前位置同时在下一个打卡点范围内，自动处理

        ⚠️ 潜在问题：
        1. 如果两个打卡点非常近（距离 < 2×range），可能跳过中间点

        参数:
            run_data (RunData): 任务数据对象，包含打卡点列表和状态
            current_lon (float): 当前经度
            current_lat (float): 当前纬度

        修改状态:
            run_data.target_sequence: 当前应到达的打卡点序号（✓ 0-based，0表示第一个打卡点）
            run_data.is_in_target_zone: 是否在打卡点范围内
        """
        # 边界检查：确保target_sequence有效
        # ✓ target_sequence从0开始（0-based索引），最大值为打卡点数量-1
        if not (0 <= run_data.target_sequence < len(run_data.target_points)):
            logging.debug(
                f"打卡点检查跳过: target_sequence={run_data.target_sequence}, total_points={len(run_data.target_points)}"
            )
            return

        # 获取当前应到达的打卡点坐标
        # ✓ target_sequence直接作为数组索引使用（0-based）
        tar_lon, tar_lat = run_data.target_points[run_data.target_sequence]

        # 计算当前位置与打卡点的距离
        dist = self._calculate_distance_m(current_lon, current_lat, tar_lon, tar_lat)

        # 判断是否在打卡范围内
        # target_range_m通常为50-100米，可配置
        is_in_zone = dist < self.target_range_m

        # 详细的调试日志，记录检查过程（显示为1-based给用户看）
        logging.debug(
            f"打卡点检查: 当前位置=({current_lon:.6f}, {current_lat:.6f}), "
            f"目标点{run_data.target_sequence+1}(索引{run_data.target_sequence})=({tar_lon:.6f}, {tar_lat:.6f}), "
            f"距离={dist:.2f}米, 范围={self.target_range_m:.2f}米, "
            f"在范围内={is_in_zone}, 已在区域内={run_data.is_in_target_zone}"
        )

        # === 状态转换逻辑 (BUG修复) ===

        # 情况1：刚进入一个打卡区域 (之前在外面，现在在里面)
        if is_in_zone and not run_data.is_in_target_zone:
            run_data.is_in_target_zone = True  # 标记为“在区域内”

            # 循环检查所有（可能重叠的）打卡点
            # 只要我们还在下一个打卡点范围内，就继续打卡
            while 0 <= run_data.target_sequence < len(run_data.target_points):
                # 获取当前要检查的打卡点
                current_target_lon, current_target_lat = run_data.target_points[
                    run_data.target_sequence
                ]
                # 重新计算到这个打卡点的距离
                current_dist = self._calculate_distance_m(
                    current_lon, current_lat, current_target_lon, current_target_lat
                )

                # 检查是否在当前目标点范围内
                if current_dist < self.target_range_m:
                    # 命中！记录打卡（1-based）
                    logging.info(
                        f"✓ 到达打卡点 {run_data.target_sequence+1}/{len(run_data.target_points)}"
                    )
                    # 移动到下一个目标点
                    run_data.target_sequence += 1
                    # 继续循环，检查是否也命中了下一个点（处理重叠区域）
                else:
                    # 未命中下一个点，说明已离开重叠区域
                    # 退出循环，等待下一次“离开区域”事件
                    break

        # 情况2：刚离开一个打卡区域 (之前在里面，现在在外面)
        elif not is_in_zone and run_data.is_in_target_zone:
            run_data.is_in_target_zone = False  # 标记为“在区域外”
            # target_sequence 此时指向 *下一个* 目标点
            logging.debug(
                f"离开打卡点 {run_data.target_sequence}（索引{run_data.target_sequence-1}）区域"
            )

    def start_single_run(self):
        """开始执行单个任务"""
        logging.info("API调用: start_single_run - 开始执行单个任务")
        if not self.stop_run_flag.is_set():
            return {"success": False, "message": "已有任务在运行"}
        if (
            self.current_run_idx == -1
            or not self.all_run_data[self.current_run_idx].run_coords
        ):
            return {"success": False, "message": "请选择任务并生成路线"}

        self.stop_run_flag.clear()
        run_data = self.all_run_data[self.current_run_idx]
        run_data.target_sequence = 0  # ✓ 从0开始（0-based索引）
        run_data.is_in_target_zone = False
        self._first_center_done = False

        logging.info(f"正在启动单任务执行: 任务名称={run_data.run_name}")
        # 修正: 为单用户模式传递 self.api_client
        threading.Thread(
            target=self._run_submission_thread,
            args=(run_data, self.current_run_idx, self.api_client, False),
            daemon=True,
        ).start()
        return {"success": True}

    def stop_run(self):
        """停止当前所有正在执行的任务"""
        logging.info("API调用: stop_run - 停止当前所有正在执行的任务")
        self.log("正在停止任务...")
        logging.info("已收到停止运行任务的信号")
        self.stop_run_flag.set()
        return {"success": True}

    def get_run_status(self):
        """获取当前运行状态（用于前端轮询）"""
        # 检查是否有任务在运行
        is_running = not self.stop_run_flag.is_set()

        if not is_running or self.current_run_idx == -1:
            return {"running": False}

        run_data = self.all_run_data[self.current_run_idx]
        total_points = len(run_data.run_coords) if run_data.run_coords else 0

        # 修复Issue 1: 使用current_point_index追踪实际进度
        processed_points = getattr(run_data, "current_point_index", 0)
        processed_points = min(processed_points, total_points)

        # 获取当前位置（如果有的话）
        current_position = None
        if processed_points > 0 and processed_points <= total_points:
            coord = run_data.run_coords[processed_points - 1]
            current_position = {"lon": coord[0], "lat": coord[1]}

        return {
            "running": True,
            "processed_points": processed_points,
            "total_points": total_points,
            "distance_covered": run_data.distance_covered_m,
            "target_sequence": run_data.target_sequence,
            "duration": (
                sum(p[2] for p in run_data.run_coords[:processed_points])
                if processed_points > 0
                else 0
            ),
            "current_position": current_position,
        }

    # 修正: 添加 acc_session 或 api_client 参数
    def _submit_chunk(
        self,
        run_data: RunData,
        chunk,
        start_time,
        is_finish,
        chunk_start_index,
        client: ApiClient,
        user: UserData,
    ):
        """将一小块轨迹数据提交到服务器"""
        log_func = (
            client.app.log if hasattr(client.app, "log") else client.app.api_bridge.log
        )

        # 修复离线测试模式：检查是否为离线模式
        if self.is_offline_mode:
            log_func(f"[离线测试模式] 模拟提交 {len(chunk)} 个GPS点...")
            logging.info(
                f"[离线测试模式] 模拟提交 chunk: start_index={chunk_start_index}, size={len(chunk)}, is_finish={is_finish}"
            )
            time.sleep(0.1)  # 模拟网络延迟
            return True  # 离线模式总是返回成功

        log_func(f"正在提交数据...")
        logging.debug(
            f"Submitting chunk: start_index={chunk_start_index}, size={len(chunk)}, is_finish={is_finish}"
        )

        last_point_gps = (
            chunk[0]
            if chunk_start_index == 0
            else run_data.run_coords[chunk_start_index - 1]
        )
        time_elapsed_before_chunk_ms = sum(
            p[2] for p in run_data.run_coords[:chunk_start_index]
        )
        coords_list, chunk_total_dist, chunk_total_dur = [], 0.0, 0

        for lon, lat, dur_ms in chunk:
            distance = self._calculate_distance_m(
                last_point_gps[0], last_point_gps[1], lon, lat
            )
            time_elapsed_before_chunk_ms += dur_ms
            coords_list.append(
                {
                    "location": f"{lon},{lat}",
                    "locatetime": str(int(time.time() * 1000)),
                    "dis": f"{distance:.1f}",
                    "count": str(int(time_elapsed_before_chunk_ms / 1000)),
                }
            )
            last_point_gps = (lon, lat, dur_ms)
            chunk_total_dist += distance
            chunk_total_dur += dur_ms

        payload = {
            "scheduleId": run_data.errand_schedule,
            "userId": user.id,
            "userName": user.name or "",
            "runLength": str(int(chunk_total_dist)),
            "runTime": str(chunk_total_dur),
            "startPoint": "",
            "endPoint": "",
            "startTime": start_time,
            # endTime 将在下面根据条件添加
            "trid": run_data.trid,
            "sid": "",
            "tid": "",
            "speed": (
                f"{(run_data.total_run_distance_m / run_data.total_run_time_s):.2f}"
                if run_data.total_run_time_s > 0
                else ""
            ),
            "finishType": "1" if is_finish else "0",
            "coordinate": json.dumps(coords_list, separators=(",", ":")),
            "appVersion": ApiClient.API_VERSION,
        }

        # 仅当这是最后一块(is_finish=True)时才添加 endTime
        if is_finish:
            payload["endTime"] = str(int(time.time() * 1000))

        payload_str = urllib.parse.urlencode(payload)

        # 通过全局串行队列进行提交，保证同一时间只提交一个数据包
        # [Debug] 增加提交前的日志
        logging.debug(
            f"[{user.name}] 正在入队提交数据包, 大小: {len(payload_str)} 字节"
        )

        resp = self._enqueue_submission(client, payload_str, wait_timeout=60.0)
        success = bool(resp and resp.get("success"))

        # [Debug] 增强结果日志
        msg = resp.get("message") if resp else "请求无响应或超时"
        if not success:
            log_func(f"数据提交失败: {msg}")
            logging.error(f"[{user.name}] 数据提交失败详情: {resp}")
        else:
            log_func(f"数据提交成功。")
            logging.debug(f"[{user.name}] 数据提交成功: {msg}")

        return success

    # ===================== 提交队列：串行化所有数据包提交 =====================
    def _submission_worker_loop(self):
        """后台工作线程：从队列取出提交任务并串行执行。"""
        logging.info("[SubmissionWorker] 提交队列工作线程已启动")
        while not getattr(self, "_submission_worker_stop", threading.Event()).is_set():
            try:
                task = self._submission_queue.get(timeout=0.5)
            except Exception:
                continue
            try:
                # [Debug] 记录开始处理
                logging.debug("[SubmissionWorker] 正在处理一个提交任务...")

                client: ApiClient = task.get("client")
                payload_str: str = task.get("payload")
                # 实际网络提交（内部已带重试）
                resp = client.submit_run_track(payload_str)
                task["response"] = resp

                # [Debug] 记录处理完成
                logging.debug(
                    f"[SubmissionWorker] 提交任务完成，结果: {bool(resp and resp.get('success'))}"
                )
            except Exception as e:
                logging.error(
                    f"[SubmissionWorker] 提交任务执行异常: {e}", exc_info=True
                )
                task["response"] = None
            finally:
                try:
                    task["event"].set()
                except Exception:
                    pass
                try:
                    self._submission_queue.task_done()
                except Exception:
                    pass

            # 【优化】防止循环过快占用CPU，给其他协程（如SocketIO）留出时间
            # [修复] 使用 time.sleep 替代 socketio.sleep，避免跨线程上下文切换错误
            time.sleep(0.01)

    def _enqueue_submission(
        self, client: ApiClient, payload_str: str, wait_timeout: float = 30.0
    ):
        """将一次提交加入全局队列，并等待结果返回。
        返回值：与 ApiClient.submit_run_track 一致的响应字典，或 None（失败/超时）。
        """
        # 入队任务包
        task = {
            "client": client,
            "payload": payload_str,
            "event": threading.Event(),  # 使用绿化后的 Event
            "response": None,
        }
        # 简要日志：提示入队长度，帮助定位排队情况
        try:
            qsize = self._submission_queue.qsize()
            logging.debug(f"Enqueue submit task. Queue size before push: {qsize}")
        except Exception:
            pass
        self._submission_queue.put(task)
        # 同步等待结果
        signaled = task["event"].wait(timeout=wait_timeout)
        if not signaled:
            logging.warning("提交队列等待超时。")
            return None
        return task.get("response")

    # 修正: 添加 client 参数
    def _finalize_run(self, run_data: RunData, task_index: int, client: ApiClient):
        """在所有数据提交后，查询服务器确认任务是否已标记为完成"""
        log_func = (
            client.app.log if hasattr(client.app, "log") else client.app.api_bridge.log
        )
        log_func("正在确认任务状态...")
        logging.debug(f"正在确认任务完成状态，任务追踪ID: trid={run_data.trid}")
        for _ in range(3):
            resp = client.get_run_info_by_trid(run_data.trid)
            if resp and resp.get("success"):
                record_map = resp.get("data", {}).get("recordMap", {})
                if record_map and record_map.get("status") == 1:
                    run_data.status = 1
                    log_func("任务已确认完成。")
                    logging.info(f"任务已成功完成: 任务名称={run_data.run_name}")
                    # 修正：使用 SocketIO 发送 task_completed 事件
                    session_id = getattr(self, "_web_session_id", None)
                    if socketio and session_id and task_index != -1:
                        try:
                            socketio.emit(
                                "task_completed",
                                {"task_index": task_index},
                                room=session_id,
                            )
                        except Exception as e:
                            logging.error(f"SocketIO发送'task_completed'事件失败: {e}")
                    return
            time.sleep(1)
        log_func("暂未确认完成，请稍后刷新。")
        logging.warning(f"任务完成状态确认失败: 任务名称={run_data.run_name}")

    # 修正: 添加 client 参数
    def _run_submission_thread(
        self,
        run_data: RunData,
        task_index: int,
        client: ApiClient,
        is_all: bool,
        finished_event: threading.Event | None = None,
    ):
        """模拟跑步和提交数据的主线程函数"""
        log_func = (
            client.app.log if hasattr(client.app, "log") else client.app.api_bridge.log
        )
        user_data = (
            client.app.user_data if hasattr(client.app, "user_data") else self.user_data
        )
        stop_flag = (
            client.app.stop_event
            if hasattr(client.app, "stop_event")
            else self.stop_run_flag
        )

        # 获取全局 socketio 对象 (假设它是全局导入的，如果没有则尝试从 globals 获取)
        sio = globals().get("socketio") if "socketio" not in globals() else socketio

        # 1. 获取初始 Session ID
        session_id = getattr(self, "_web_session_id", None)
        last_auto_save_time = time.time()

        try:
            log_func("开始执行任务。")
            logging.info(f"任务提交线程已启动: 任务名称={run_data.run_name}")

            run_data.trid = f"{user_data.student_id}{int(time.time() * 1000)}"
            start_time_ms = str(int(time.time() * 1000))
            run_data.distance_covered_m = 0.0
            last_point_gps = run_data.run_coords[0]
            submission_successful = True

            point_index = 0  # 修复Issue 1: 追踪当前处理的点索引

            # --- 循环开始 ---
            for i in range(0, len(run_data.run_coords), 40):
                if stop_flag.is_set():
                    log_func("任务已中止。")
                    logging.info("检测到停止标志，正在中止任务运行")
                    break

                chunk = run_data.run_coords[i : i + 40]

                for lon, lat, dur_ms in chunk:
                    if stop_flag.wait(timeout=dur_ms / 1000.0):
                        logging.debug("等待下一个坐标点时被停止信号中断")
                        break

                    run_data.distance_covered_m += self._calculate_distance_m(
                        last_point_gps[0], last_point_gps[1], lon, lat
                    )
                    last_point_gps = (lon, lat, dur_ms)
                    point_index += 1  # 修复Issue 1: 更新点索引
                    run_data.current_point_index = (
                        point_index  # 修复Issue 1: 保存到run_data
                    )
                    self.check_target_reached_during_run(run_data, lon, lat)

                    # --- 自动保存逻辑 ---
                    # 重新检查 session_id，以防上下文丢失（优先使用 client.app 中的）
                    current_session_id = session_id
                    if not current_session_id and hasattr(client, "app"):
                        current_session_id = getattr(
                            client.app, "_web_session_id", None
                        )

                    if current_session_id and (time.time() - last_auto_save_time >= 30):
                        try:
                            # 确保 web_sessions_lock 和 web_sessions 在作用域内可用
                            # 如果是全局变量，这里没问题
                            if (
                                "web_sessions_lock" in globals()
                                and "web_sessions" in globals()
                            ):
                                with web_sessions_lock:
                                    if current_session_id in web_sessions:
                                        save_session_state(
                                            current_session_id,
                                            web_sessions[current_session_id],
                                        )
                                        logging.debug(
                                            f"任务执行中自动保存会话状态 (进度: {point_index}/{len(run_data.run_coords)})"
                                        )
                                last_auto_save_time = time.time()
                        except Exception as e:
                            logging.error(f"任务执行中自动保存会话失败: {e}")

                    # --- SocketIO 发送位置更新逻辑 ---
                    debug_sio_status = "存在" if sio else "缺失(None)"
                    debug_emit_cond = self.current_run_idx == task_index

                    logging.debug(
                        f"SocketIO状态检查 -> "
                        f"SIO对象: {debug_sio_status}, "
                        f"SessionID: {current_session_id}, "
                        f"任务匹配: {self.current_run_idx}=={task_index} ({debug_emit_cond})"
                    )
                    # 只有当 SocketIO 实例存在、会话ID存在且符合发送条件时才执行
                    if sio and current_session_id:
                        # 检查是否需要发送更新
                        #  should_emit = (self.current_run_idx == task_index)
                        should_emit = True

                        # if should_emit:
                        #     center_now = False
                        #     # 如果是第一次更新位置，强制前端地图居中
                        #     if not self._first_center_done:
                        #         center_now = True
                        #         self._first_center_done = True

                        # [重要修正] try...except 必须包含在 if should_emit 内部
                        # 否则 center_now 可能会在未定义的情况下被引用，且逻辑上不应发送数据
                        # try:
                        # # 构造数据
                        # message_data_dict = {
                        #     'lon': float(lon),
                        #     'lat': float(lat),
                        #     'distance': float(run_data.distance_covered_m),
                        #     'target_sequence': run_data.target_sequence,
                        #     'duration': int(dur_ms),
                        #     'center_now': center_now,
                        #     'task_index': task_index
                        # }

                        # # 1. 准备两种数据格式
                        # # 格式A: JSON 字符串 (兼容 legacy 前端代码，如使用 JSON.parse)
                        # json_payload_str = json.dumps(message_data_dict, ensure_ascii=False)
                        # # 格式B: 原始字典 (标准用法)
                        # payload_dict = message_data_dict

                        # # 2. 检查房间成员 (保留日志用于确认连接)
                        # try:
                        #     room_participants = sio.server.manager.rooms.get('/', {}).get(current_session_id, set())
                        #     client_count = len(room_participants)
                        #     if client_count > 0:
                        #         logging.info(f"[SocketIO] ✅ 发送数据 -> 房间: {current_session_id} (在线: {client_count})")
                        #     else:
                        #         logging.warning(f"[SocketIO] ⚠️ 房间 {current_session_id} 为空，消息无人接收！")
                        # except Exception:
                        #     pass

                        # 3. 【核心修复】尝试多种发送方式以匹配前端
                        # 尝试 1: 发送 JSON 字符串 (极有可能是前端需要的格式)
                        # sio.emit('runner_position_update', json_payload_str, room=current_session_id, namespace='/')

                        # 尝试 2: 发送 字典对象 (作为备用，防止前端不解析JSON)
                        # 注意：这可能会导致前端收到两次事件，但在调试阶段这能确保至少一次成功
                        # sio.emit('runner_position_update', payload_dict, room=current_session_id, namespace='/')

                        # 尝试 3: 同时发送到 'multi_position_update' (防止前端复用了多账号的监听器)
                        # 多账号监听器通常接收对象，所以这里发字典
                        # sio.emit('multi_position_update', payload_dict, room=current_session_id, namespace='/')

                        # 4. 强制刷新
                        # sio.sleep(0)

                        # logging.debug(f"已通过多种格式发送位置更新: 任务{task_index}, 距离{run_data.distance_covered_m:.2f}")

                        # --- 发送逻辑修正 ---
                        # 1. 只发送一次
                        # 2. 传递字典对象，让 sio 自动处理 JSON 序列化
                        # 3. 增加 sio.sleep(0) 确保 eventlet 协程有机会将数据刷新到网络

                        # sio.emit('runner_position_update', message_data_dict, room=current_session_id)
                        # sio.sleep(0)  # 【关键】强制交出控制权，触发消息立即发送

                        # logging.debug(f"已发送位置更新: 任务{task_index}, 距离{run_data.distance_covered_m:.2f}")

                        # except Exception as e:
                        #     logging.error(f"SocketIO发送'runner_position_update'位置更新事件失败: {e}")

                # 内层 for 循环结束

                if stop_flag.is_set():
                    break

                is_final_chunk = i + 40 >= len(run_data.run_coords)

                # --- 提交数据逻辑 ---
                max_attempts = 3
                attempt = 1
                chunk_submitted = False
                while attempt <= max_attempts:
                    if self._submit_chunk(
                        run_data,
                        chunk,
                        start_time_ms,
                        is_final_chunk,
                        i,
                        client,
                        user_data,
                    ):
                        chunk_submitted = True
                        break

                    # 提交失败处理
                    submission_successful = False
                    if self.is_offline_mode:
                        logging.error(
                            f"[离线测试模式] 模拟提交失败，尝试 {attempt}/{max_attempts}"
                        )
                    else:
                        logging.warning(f"数据提交失败，重试 {attempt}/{max_attempts}")
                        # 使用 stop_flag.wait 替代 sleep 以便快速响应停止
                        if stop_flag.wait(timeout=1.0):
                            submission_successful = False
                            log_func("检测到停止信号，已取消重试")
                            break
                    attempt += 1

                if not chunk_submitted:
                    logging.error(
                        f"数据提交在 {max_attempts} 次尝试后仍然失败，任务中止"
                    )
                    break

            # --- 外层循环结束，处理完成逻辑 ---

            if not stop_flag.is_set() and submission_successful:
                log_func("任务执行完毕，等待确认...")
                logging.info("任务运行执行完毕，等待最终确认")
                time.sleep(3)
                self._finalize_run(run_data, task_index, client)

                # 任务完成后立即保存会话状态
                if session_id:
                    try:
                        if (
                            "web_sessions_lock" in globals()
                            and "web_sessions" in globals()
                        ):
                            with web_sessions_lock:
                                if session_id in web_sessions:
                                    save_session_state(
                                        session_id,
                                        web_sessions[session_id],
                                        force_save=True,
                                    )
                                    logging.info(f"任务完成，已保存会话状态")
                    except Exception as e:
                        logging.error(f"任务完成后保存会话失败: {e}")

        finally:
            # --- 清理和停止逻辑 ---
            # 如果不是批量运行模式（is_all=False），或者出现异常，确保设置停止标志
            if not is_all:
                if not submission_successful or stop_flag.is_set():
                    self.stop_run_flag.set()
                    logging.info(f"任务停止或失败，设置停止标志")
                else:
                    self.stop_run_flag.set()
                    logging.info(f"任务正常完成，重置停止标志")

                # 发送停止事件
                session_id = getattr(self, "_web_session_id", None)
                if sio and session_id:
                    try:
                        sio.emit("run_stopped", {}, room=session_id)
                    except Exception as e:
                        logging.error(f"SocketIO发送'run_stopped'运行停止事件失败: {e}")

            if finished_event:
                finished_event.set()
            logging.info(f"Submission thread finished for task: {run_data.run_name}")

    def _get_path_for_distance(self, path, cumulative_distances, target_dist):
        """如果路径总长不足，则通过来回走的方式凑足目标距离"""
        total_len = cumulative_distances[-1]
        final_path = list(path)
        if 0 < total_len < target_dist:
            rem = target_dist - total_len
            rev = path[::-1]
            acc = 0.0
            for i in range(len(rev) - 1):
                seg = self._calculate_distance_m(
                    rev[i][0], rev[i][1], rev[i + 1][0], rev[i + 1][1]
                )
                if acc + seg < rem:
                    final_path.append(rev[i + 1])
                    acc += seg
                else:
                    ratio = (rem - acc) / seg if seg > 0 else 0
                    s, e = rev[i], rev[i + 1]
                    final_path.append(
                        (s[0] + (e[0] - s[0]) * ratio, s[1] + (e[1] - s[1]) * ratio)
                    )
                    break
        return final_path

    def _get_point_at_distance(self, path, cumulative_distances, dist):
        """在一条路径上，根据距离找到精确的坐标点"""
        idx = bisect.bisect_left(cumulative_distances, dist)
        if idx == 0:
            return path[0]
        if idx >= len(cumulative_distances):
            return path[-1]

        d0, d1 = cumulative_distances[idx - 1], cumulative_distances[idx]
        seg_len = d1 - d0
        ratio = (dist - d0) / seg_len if seg_len > 0 else 0
        s, e = path[idx - 1], path[idx]
        return (s[0] + (e[0] - s[0]) * ratio, s[1] + (e[1] - s[1]) * ratio)

    def auto_generate_path_with_api(self, api_path_coords, min_t_m, max_t_m, min_d_m):
        """接收由前端JS API规划好的路径点，并生成模拟数据"""
        logging.info(
            f"API CALL: auto_generate_path_with_api with {len(api_path_coords)} points"
        )
        if self.current_run_idx == -1:
            return {"success": False, "message": "请先选择任务"}
        run = self.all_run_data[self.current_run_idx]

        self.log("收到JS API路径，正在生成模拟数据...")
        logging.info(
            f"Auto-generating path from {len(api_path_coords)} Amap API points."
        )
        if not api_path_coords or len(api_path_coords) < 2:
            return {"success": False, "message": "高德API未能返回有效路径"}

        final_path_dedup = []
        last_coord = None
        for p in api_path_coords:
            # 修正BUG：同时兼容 'lng' 和 'lon' 两种经度键名
            longitude = p.get("lng", p.get("lon"))
            if longitude is None:
                continue  # 如果经度不存在，则跳过这个点
            coord = (longitude, p["lat"])
            if coord != last_coord:
                final_path_dedup.append(coord)
                last_coord = coord

        target_time_s = random.uniform(min_t_m * 60, max_t_m * 60)
        target_dist_m = random.uniform(min_d_m, min_d_m * 1.15)

        cumulative = [0.0]
        for i in range(len(final_path_dedup) - 1):
            cumulative.append(
                cumulative[-1]
                + self._calculate_distance_m(
                    final_path_dedup[i][0],
                    final_path_dedup[i][1],
                    final_path_dedup[i + 1][0],
                    final_path_dedup[i + 1][1],
                )
            )

        final_geo_path = self._get_path_for_distance(
            final_path_dedup, cumulative, target_dist_m
        )

        final_cumulative = [0.0]
        for i in range(len(final_geo_path) - 1):
            final_cumulative.append(
                final_cumulative[-1]
                + self._calculate_distance_m(
                    final_geo_path[i][0],
                    final_geo_path[i][1],
                    final_geo_path[i + 1][0],
                    final_geo_path[i + 1][1],
                )
            )

        actual_total_dist = final_cumulative[-1] if final_cumulative else 0.0
        if actual_total_dist == 0:
            return {"success": False, "message": "路径计算距离为0"}

        avg_speed = actual_total_dist / target_time_s
        run_coords = []
        if not final_geo_path:
            return {"success": False, "message": "无法生成地理路径"}

        start = final_geo_path[0]
        run_coords.append(
            (self._gps_random_offset(start[0], start[1], self.params) + (0,))
        )
        t_elapsed, d_covered = 0.0, 0.0

        while t_elapsed < target_time_s:
            interval = min(
                random.uniform(
                    self.params["interval_ms"] * 0.9, self.params["interval_ms"] * 1.1
                )
                / 1000.0,
                target_time_s - t_elapsed,
            )
            if interval <= 0.1:
                break

            d_covered = min(
                d_covered + random.uniform(avg_speed * 0.9, avg_speed * 1.1) * interval,
                actual_total_dist,
            )
            lon, lat = self._get_point_at_distance(
                final_geo_path, final_cumulative, d_covered
            )
            lon_o, lat_o = self._gps_random_offset(lon, lat, self.params)
            run_coords.append((lon_o, lat_o, int(interval * 1000)))
            t_elapsed += interval
            if d_covered >= actual_total_dist:
                break

        run.run_coords = run_coords
        run.total_run_time_s = t_elapsed
        run.total_run_distance_m = d_covered

        self.log("自动生成完成。")
        logging.info(
            f"Auto-generated path: points={len(run.run_coords)}, dist={d_covered:.1f}, time={t_elapsed:.1f}"
        )
        return {
            "success": True,
            "run_coords": run.run_coords,
            "total_dist": d_covered,
            "total_time": t_elapsed,
        }

    def start_all_runs(self, ignore_completed, auto_generate):
        """开始执行所有符合条件的任务"""
        logging.info(
            f"API CALL: start_all_runs (ignore_completed={ignore_completed}, auto_generate={auto_generate})"
        )
        if not self.stop_run_flag.is_set():
            return {"success": False, "message": "已有任务在运行"}

        tasks_to_run = []
        for i, d in enumerate(self.all_run_data):
            # 修正BUG：如果任务已完成，并且没有勾选“忽略已完成”，则跳过
            if d.status == 1 and not ignore_completed:
                continue

            is_expired = False
            is_not_started = False
            now = datetime.datetime.now()
            ignore_time = self.params.get("ignore_task_time", True)

            try:
                if d.end_time:
                    end_dt = self._try_parse_dt(d.end_time)
                    if ignore_time:
                        is_expired = end_dt.date() < now.date()
                    else:
                        is_expired = end_dt < now
            except (ValueError, TypeError):
                is_expired = False

            try:
                if d.start_time:
                    start_dt = self._try_parse_dt(d.start_time)
                    if ignore_time:
                        is_not_started = now.date() < start_dt.date()
                    else:
                        is_not_started = now < start_dt
            except (ValueError, TypeError):
                is_not_started = False

            if is_expired or is_not_started:
                continue

            # 只有当需要自动生成，或者任务本身已有路径时，才加入队列
            if auto_generate or d.run_coords:
                tasks_to_run.append(i)

        if not tasks_to_run:
            msg = "没有符合条件的可执行任务。"
            if not auto_generate:
                msg += " (提示: 勾选'全部自动生成'可以为没有路线的任务自动规划)"
            return {"success": False, "message": msg}

        queue = collections.deque(tasks_to_run)
        self.stop_run_flag.clear()
        logging.info(
            f"Starting 'run all' process. Queue={list(queue)}, auto-generate={auto_generate}"
        )
        threading.Thread(
            target=self._run_all_tasks_manager, args=(queue, auto_generate), daemon=True
        ).start()
        return {"success": True}

    def _run_all_tasks_manager(self, queue: collections.deque, auto_gen_enabled: bool):
        """管理“执行所有”任务队列的线程函数"""
        self.log("开始执行所有任务。")
        if self.window:
            self.window.evaluate_js("onAllRunsToggled(true)")
        is_first_task = True

        tasks_executed_count = 0  # 跟踪实际执行的任务数

        while queue:
            if self.stop_run_flag.is_set():
                break

            idx = queue.popleft()
            run_data = self.all_run_data[idx]
            self.current_run_idx = idx

            if self.window:
                self.window.evaluate_js(f"selectTaskFromBackend({idx})")
            time.sleep(1.2)

            if not run_data.run_coords and auto_gen_enabled:
                self.log(f"正在为任务 '{run_data.run_name}' 自动生成路线...")
                logging.info(
                    f"Auto-generating path for task in 'run all' mode: {run_data.run_name}"
                )

                # 1) 确保已加载任务详情，拿到打卡点
                if not run_data.details_fetched:
                    details_resp = self.get_task_details(idx)
                    if not details_resp.get("success"):
                        self.log("获取详情失败，跳过。")
                        logging.warning(
                            f"Skipping task {run_data.run_name}: failed to get details."
                        )
                        continue
                    run_data = self.all_run_data[idx]

                if not run_data.target_points:
                    # 任务25: 记录无打卡点日志，使用明确的提示格式
                    self.log(f"跳过: 任务 '{run_data.run_name}' 无打卡点")
                    logging.warning(
                        f"[Task Skipped] No checkpoints for task {run_data.run_name}, cannot auto-generate path."
                    )
                    continue

                # 2) 触发前端JS路径规划，使用与多账号相同的回调机制
                try:
                    self.log("调用高德API进行路径规划...")
                    # 准备回调通道
                    callback_key = f"single_{idx}_{int(time.time() * 1000)}"
                    path_result: dict = {}
                    completion_event = threading.Event()  # 使用绿化后的 Event
                    self.path_gen_callbacks[callback_key] = (
                        path_result,
                        completion_event,
                    )

                    # 将打卡点传给前端；JS会调用 getWalkingPath 并通过 multi_path_generation_callback 回传
                    # 形如 [(lon, lat), ...]，AMap.Walking.search 支持 [lng, lat] 数组
                    waypoints = run_data.target_points
                    if self.window:
                        self.window.evaluate_js(
                            f'triggerPathGenerationForPy("{callback_key}", {json.dumps(waypoints)})'
                        )

                    # 等待JS完成路径规划
                    path_received = completion_event.wait(timeout=120)
                    if "path" not in path_result:
                        error_msg = path_result.get("error", "超时或未知错误")
                        self.log(f"路径规划失败或超时：{error_msg}，跳过此任务。")
                        logging.warning(
                            f"Path planning failed for task {run_data.run_name}: {error_msg}"
                        )
                        if callback_key in self.path_gen_callbacks:
                            self.path_gen_callbacks.pop(callback_key, None)
                        continue

                    # 形如 [{lng,lat}, ...]
                    api_path_coords = path_result["path"]
                    self.log(
                        f"路径规划成功，共 {len(api_path_coords)} 个点，正在生成模拟数据..."
                    )

                    # 3) 使用后端生成 run_coords（复用已有逻辑与参数）
                    p = self.params
                    gen_resp = self.auto_generate_path_with_api(
                        api_path_coords,
                        p.get("min_time_m", 20),
                        p.get("max_time_m", 30),
                        p.get("min_dist_m", 2000),
                    )
                    if not gen_resp.get("success"):
                        self.log(
                            f"自动生成失败：{gen_resp.get('message', '未知错误')}，跳过。"
                        )
                        logging.warning(
                            f"Auto-generation failed for task {run_data.run_name}: {gen_resp}"
                        )
                        continue

                    # 将生成结果回填到当前任务
                    run_data.run_coords = gen_resp["run_coords"]
                    run_data.total_run_distance_m = gen_resp["total_dist"]
                    run_data.total_run_time_s = gen_resp["total_time"]

                except Exception as e:
                    self.log(f"自动生成失败，跳过：{e}")
                    logging.error(
                        f"Auto-generation failed for {run_data.run_name}: {e}",
                        exc_info=True,
                    )
                    continue

                # 路径生成成功后，通知前端刷新UI以显示新路径和数据
                self.log("路径已生成，正在更新界面...")
                if self.window:
                    self.window.evaluate_js(f"forceRefreshTaskUI({idx})")
                time.sleep(1.0)  # 短暂延时，让用户能看到UI更新

            if not run_data.run_coords:
                self.log(f"任务 '{run_data.run_name}' 无可用路线，跳过。")
                logging.warning(
                    f"Skipping task {run_data.run_name}: no route available."
                )
                continue

            if not is_first_task:
                wait_time = random.uniform(
                    self.params["task_gap_min_s"], self.params["task_gap_max_s"]
                )
                self.log(f"任务间等待中...")
                logging.info(f"等待 {wait_time:.1f}秒 后开始执行下一个任务")
                if self.stop_run_flag.wait(timeout=wait_time):
                    break
            is_first_task = False
            tasks_executed_count += 1  # 任务已通过所有检查，准备执行

            run_data.target_sequence, run_data.is_in_target_zone = 0, False  # ✓ 从0开始
            self._first_center_done = False
            task_finished_event = threading.Event()  # 使用绿化后的 Event
            self._run_submission_thread(
                run_data, idx, self.api_client, True, task_finished_event
            )
            task_finished_event.wait()

        if tasks_executed_count == 0:
            self.log("所有任务均被跳过，未执行任何操作。")
        else:
            self.log("所有任务执行结束。")

        self.stop_run_flag.set()
        if self.window:
            self.window.evaluate_js("onAllRunsToggled(false)")

    def get_task_history(self, index):
        """获取任务的历史跑步记录"""
        logging.info(
            f"API调用: get_task_history - 获取任务历史跑步记录，任务索引: {index}"
        )
        if not (0 <= index < len(self.all_run_data)):
            return {"success": False, "message": "任务索引无效"}
        run_data = self.all_run_data[index]
        self.log("正在获取历史记录...")
        logging.debug(f"正在获取任务的历史记录: 任务名称={run_data.run_name}")
        resp = self.api_client.get_run_history_list(
            self.user_data.id, run_data.errand_schedule
        )

        if resp and resp.get("success"):
            records = resp.get("data", {}).get("userErrandTrackRecord", [])
            history_list = []
            for rec in records:
                run_time_s = rec.get("runTime", 0) / 1000
                length_m = rec.get("runLength", 0)
                km = length_m / 1000 if length_m else 0
                speed_s_per_km = (run_time_s / km) if km > 0 else 0
                s_min, s_sec = divmod(speed_s_per_km, 60)
                total_seconds_int = int(run_time_s)
                run_minutes, run_seconds = divmod(total_seconds_int, 60)
                formatted_used_time = f"{run_minutes:02d}:{run_seconds:02d}"
                history_list.append(
                    {
                        "time": rec.get("createTime", "NULL"),
                        "used_time": formatted_used_time,
                        "len": f"{length_m}m",
                        "speed": (
                            f"{int(s_min)}'{int(s_sec):02d}\"" if km > 0 else "NULL"
                        ),
                        "trid": rec.get("trid"),
                    }
                )
            self.log(f"历史记录已加载。")
            logging.debug(f"已成功加载 {len(records)} 条历史记录")
            return {"success": True, "history": history_list}
        return {"success": False, "message": "获取历史记录失败"}

    def get_historical_track(self, trid):
        """根据轨迹ID获取历史轨迹坐标点"""
        logging.info(
            f"API调用: get_historical_track - 根据轨迹ID获取历史轨迹，trid: {trid}"
        )
        self.log("正在加载历史轨迹...")
        logging.debug(f"正在加载历史运动轨迹数据，轨迹ID: trid={trid}")
        resp = self.api_client.get_history_track_by_trid(trid)
        if resp and resp.get("success"):
            coords = []
            for track_point_list in resp.get("data", {}).get("trackPointList", []):
                try:
                    coords_list = json.loads(track_point_list.get("coordinate", "[]"))
                    for item in coords_list:
                        lon, lat = map(float, item.get("location", "0,0").split(","))
                        coords.append((lon, lat))
                except (json.JSONDecodeError, ValueError):
                    continue
            self.log("历史轨迹加载成功。")
            logging.debug(f"历史轨迹数据加载成功，包含 {len(coords)} 个坐标点")
            return {"success": True, "coords": coords}
        self.log("加载历史轨迹失败。")
        logging.warning("加载历史运动轨迹数据失败")
        return {"success": False, "message": "加载历史轨迹失败"}

    def update_param(self, key, value):
        """更新并保存单个参数"""
        logging.info(f"API调用: update_param - 更新参数，键: {key}, 值: {value}")

        # 决定要更新哪个参数字典
        username_to_update = None
        if self.is_multi_account_mode:
            # 在多账号模式下，这被视为更新全局参数
            target_params = self.global_params
        else:
            target_params = self.params
            username_to_update = self.user_data.username

        if key in target_params:
            try:
                original_type = type(target_params[key])
                if original_type is bool:
                    target_params[key] = (
                        bool(value)
                        if isinstance(value, bool)
                        else str(value).lower() in ("true", "1", "t", "yes")
                    )
                else:
                    target_params[key] = original_type(value)

                # 如果是多账号模式, 更新所有已加载账号的对应参数
                if self.is_multi_account_mode:
                    for acc in self.accounts.values():
                        if key in acc.params:
                            acc.params[key] = target_params[key]
                            # 仅当该账号已有 .ini 时才写回，避免无用文件生成
                            ini_path = os.path.join(
                                self.user_dir, f"{acc.username}.ini"
                            )
                            if os.path.exists(ini_path):
                                self._save_config(acc.username)

                # 获取最后登录的用户名以保存配置
                if not username_to_update:
                    cfg = configparser.ConfigParser()
                    cfg.read(self.config_path, encoding="utf-8")
                    username_to_update = cfg.get("Config", "LastUser", fallback=None)

                if username_to_update and not self.is_multi_account_mode:
                    self._save_config(username_to_update)

                logging.debug(f"参数已更新: 参数名={key}, 新值={target_params[key]}")

                # --- 响应自动签到参数变化 ---
                if (
                    key in ("auto_attendance_enabled", "auto_attendance_refresh_s")
                    and not self.is_multi_account_mode
                ):
                    self.stop_auto_refresh.set()  # 停止旧的
                    if self.auto_refresh_thread and self.auto_refresh_thread.is_alive():
                        self.auto_refresh_thread.join(timeout=1.0)

                    if self.params.get("auto_attendance_enabled", False):
                        # 如果是启用，则重启
                        self.stop_auto_refresh.clear()
                        self.auto_refresh_thread = threading.Thread(
                            target=self._auto_refresh_worker, daemon=True
                        )
                        self.auto_refresh_thread.start()
                        self.log("自动刷新设置已更新并重启。")

                return {"success": True}
            except (ValueError, TypeError) as e:
                return {"success": False, "message": str(e)}
        return {"success": False, "message": "Unknown parameter"}

    def get_params(self):
        """
        获取当前参数配置

        功能说明：
        - 用于前端获取所有参数配置，包括主题颜色、主题风格等
        - 在多账号模式下返回全局参数
        - 在单账号模式下返回当前账号的参数

        返回:
            dict: 包含所有参数的字典
        """
        try:
            # 根据模式返回对应的参数
            if self.is_multi_account_mode:
                return self.global_params.copy()
            else:
                return self.params.copy()
        except Exception as e:
            logging.error(f"获取参数失败: {e}", exc_info=True)
            # 返回默认参数
            return {
                "theme_base_color": "#7dd3fc",
                "theme_style": "default",
                "auto_attendance_enabled": False,
                "auto_attendance_refresh_s": 30,
                "attendance_user_radius_m": 40,
            }

    def export_task_data(self):
        """导出当前任务数据为JSON文件（Web模式：返回JSON数据让前端下载）"""
        logging.info("API调用: export_task_data - 导出当前任务数据为JSON格式")
        logging.info("导出任务数据...")
        if self.current_run_idx == -1:
            logging.warning("未选择任务，无法导出")
            return {"success": False, "message": "请先选择一个任务。"}
        run_data = self.all_run_data[self.current_run_idx]
        if (
            not run_data.draft_coords
            and not run_data.run_coords
            and not run_data.recommended_coords
        ):
            logging.warning("任务无路径数据，无法导出")
            return {"success": False, "message": "当前任务没有可导出的路径数据。"}

        export_data = {
            "task_name": run_data.run_name,
            "errand_id": run_data.errand_id,
            "errand_schedule": run_data.errand_schedule,
            "target_points": run_data.target_points,
            "target_point_names": run_data.target_point_names,
            "recommended_coords": run_data.recommended_coords,
            "draft_coords (gps)": run_data.draft_coords,
            "run_coords (gps)": run_data.run_coords,
        }

        # Web模式：返回数据让前端处理下载
        try:
            logging.info(f"导出任务数据成功: {run_data.run_name}")
            return {
                "success": True,
                "data": export_data,
                "filename": f"task_{run_data.errand_schedule or 'debug'}_{int(time.time())}.json",
                "message": "任务数据已准备完成",
            }
        except Exception as e:
            logging.error(f"导出失败: {e}", exc_info=True)
            return {"success": False, "message": f"导出失败: {e}"}

    def import_task_data(self, json_data=None):
        """导入JSON任务数据，进入离线调试模式（UA=Null，保留用户信息）"""
        logging.info("API调用: import_task_data - 导入JSON任务数据（离线调试模式）")
        logging.info("开始导入任务数据...")

        if not json_data:
            logging.error("导入失败：未提供有效的JSON数据")
            return {"success": False, "message": "未提供导入数据"}

        try:
            # 如果json_data是字符串，解析它
            if isinstance(json_data, str):
                logging.info("解析JSON字符串...")
                data = json.loads(json_data)
            else:
                data = json_data

            logging.info(f"JSON数据解析成功，任务名称: {data.get('task_name', '未知')}")

            # --- 软重置：保留用户信息，但 UA 强制置空 ---
            prev_user = copy.deepcopy(getattr(self, "user_data", UserData()))

            self.is_offline_mode = True
            logging.info("切换到离线模式")
            # 停止任何运行中的单账号任务
            try:
                if hasattr(self, "stop_run_flag") and isinstance(
                    self.stop_run_flag, threading.Event
                ):
                    self.stop_run_flag.set()
                    logging.info("停止运行中的任务")
            except Exception:
                pass
            # 清空运行态
            self.all_run_data = []
            self.current_run_idx = -1
            self._first_center_done = False

            # 恢复用户信息
            self.user_data = prev_user if prev_user else UserData()
            if not (self.user_data.name or "").strip():
                self.user_data.name = "离线调试"
            if not (self.user_data.student_id or "").strip():
                self.user_data.student_id = "NULL"

            logging.info(
                f"用户信息: {self.user_data.name} ({self.user_data.student_id})"
            )

            # 离线模式下 UA 必须为 NULL
            self.device_ua = None

            # 组装离线任务
            debug_run = RunData()
            debug_run.run_name = data.get("task_name", "调试任务 (离线)")
            debug_run.errand_id = data.get("errand_id", "debug_id")
            debug_run.errand_schedule = data.get("errand_schedule", "debug_schedule")
            debug_run.target_points = data.get("target_points", [])
            if "target_point_names" in data and data["target_point_names"]:
                debug_run.target_point_names = data["target_point_names"]
            else:
                num_points = len(debug_run.target_points)
                if num_points > 0:
                    debug_run.target_point_names = "|".join(
                        [f"打卡点 {i + 1}" for i in range(num_points)]
                    )

            debug_run.recommended_coords = data.get("recommended_coords", [])
            debug_run.draft_coords = data.get("draft_coords (gps)", [])
            debug_run.run_coords = data.get("run_coords (gps)", [])

            if debug_run.run_coords and len(debug_run.run_coords) > 1:
                total_dist_m = 0.0
                for i in range(len(debug_run.run_coords) - 1):
                    p1 = debug_run.run_coords[i]
                    p2 = debug_run.run_coords[i + 1]
                    total_dist_m += self._calculate_distance_m(
                        p1[0], p1[1], p2[0], p2[1]
                    )
                total_time_s = sum(p[2] for p in debug_run.run_coords) / 1000.0
                debug_run.total_run_distance_m = total_dist_m
                debug_run.total_run_time_s = total_time_s
                logging.info(
                    f"导入路径统计完成: 距离={total_dist_m:.1f}米, 时间={total_time_s:.1f}秒"
                )

            debug_run.details_fetched = True
            self.all_run_data = [debug_run]
            self.current_run_idx = 0

            self.log("离线数据已导入。")
            logging.info(f"离线数据导入成功: {debug_run.run_name}")

            tasks_for_js = [r.__dict__.copy() for r in self.all_run_data]
            tasks_for_js[0]["info_text"] = "离线"
            tasks_for_js[0]["target_range_m"] = self.target_range_m

            return {
                "success": True,
                "tasks": tasks_for_js,
                "userInfo": self._get_full_user_info_dict(),
            }
        except Exception as e:
            self.log("导入失败。")
            logging.error(f"导入失败: {e}", exc_info=True)
            return {"success": False, "message": f"导入失败: {e}"}

    def clear_current_task_draft(self):
        """清除当前任务的草稿路径和已生成路径"""
        logging.info(
            "API调用: clear_current_task_draft - 清除当前任务的草稿路径和生成路径"
        )
        if self.current_run_idx == -1 or not (
            0 <= self.current_run_idx < len(self.all_run_data)
        ):
            return {"success": False, "message": "未选择任务"}
        run = self.all_run_data[self.current_run_idx]
        run.draft_coords = []
        run.run_coords = []
        run.total_run_distance_m = 0
        run.total_run_time_s = 0
        logging.info(f"已清除任务的草稿路径和运行数据: 任务名称={run.run_name}")
        return {"success": True}

    def enter_multi_account_mode(self):
        """切换到多账号模式（增强：先打断单账号运行）"""
        # 先停止单账号任何运行中的任务/线程
        try:
            if hasattr(self, "stop_run_flag") and isinstance(
                self.stop_run_flag, threading.Event
            ):
                self.stop_run_flag.set()
            # 清空路径规划回调，避免误回传
            for key, (path_result, completion_event) in list(
                self.path_gen_callbacks.items()
            ):
                path_result["error"] = "模式切换（进入多账号）已取消"
                try:
                    completion_event.set()
                except Exception:
                    pass
            self.path_gen_callbacks.clear()
            # 通知前端停止单账号UI（可选）
            if self.window:
                try:
                    self.window.evaluate_js("onRunStopped()")
                except Exception:
                    pass
        except Exception:
            logging.debug(
                "enter_multi_account_mode pre-stop single failed (non-fatal)."
            )

        self.log("进入多账号模式。")
        self.is_multi_account_mode = True
        self._update_multi_global_buttons()

        # 发送账号列表到前端（修复：页面刷新后账号列表丢失的问题）
        session_id = getattr(self, "_web_session_id", None)
        if session_id and socketio:
            try:
                accounts_data = []
                for username, acc in self.accounts.items():
                    accounts_data.append(
                        {
                            "username": username,
                            "name": (
                                acc.user_data.name if acc.user_data.name else username
                            ),
                            "status_text": acc.status_text,
                            "summary": acc.summary,
                            "params": acc.params,
                        }
                    )
                socketio.emit(
                    "accounts_updated", {"accounts": accounts_data}, room=session_id
                )
            except Exception as e:
                logging.error(f"Failed to emit accounts_updated on mode entry: {e}")

        try:
            self.stop_multi_auto_refresh.clear()
            if (
                self.multi_auto_refresh_thread is None
                or not self.multi_auto_refresh_thread.is_alive()
            ):
                self.multi_auto_refresh_thread = threading.Thread(
                    target=self._multi_auto_attendance_worker, daemon=True
                )
                self.multi_auto_refresh_thread.start()
        except Exception as e:
            self.log(f"启动多账号自动刷新线程失败: {e}")

        # [BUG修复] 进入多账号模式后立即保存会话状态，确保账号列表被持久化
        # 这样即使程序重启，也能恢复多账号列表
        if session_id:
            try:
                save_session_state(session_id, self, force_save=True)
                logging.info(f"进入多账号模式：已保存会话状态到持久化存储")
            except Exception as e:
                logging.error(f"进入多账号模式：保存会话状态失败: {e}")

        return {"success": True, "params": self.global_params}

    def exit_multi_account_mode(self):
        """退出多账号模式，返回单用户登录页（增强：彻底停止所有执行）"""
        # 发送全局停止并终止所有账号线程
        try:
            self.multi_stop_all_accounts()
            # 等待线程尽量退出
            for acc in list(self.accounts.values()):
                try:
                    if acc.worker_thread and acc.worker_thread.is_alive():
                        acc.stop_event.set()
                        acc.worker_thread.join(timeout=1.0)
                except Exception:
                    pass
        except Exception:
            logging.debug(
                "exit_multi_account_mode: stop all accounts failed (non-fatal)."
            )

        # 清空路径规划回调，避免延迟回传
        for key, (path_result, completion_event) in list(
            self.path_gen_callbacks.items()
        ):
            path_result["error"] = "模式切换（退出多账号）已取消"
            try:

                completion_event.set()
            except Exception:
                pass
        self.path_gen_callbacks.clear()

        try:
            self.stop_multi_auto_refresh.set()
            if (
                self.multi_auto_refresh_thread
                and self.multi_auto_refresh_thread.is_alive()
            ):
                self.multi_auto_refresh_thread.join(timeout=1.0)
            self.multi_auto_refresh_thread = None
        except Exception as e:
            logging.warning(f"停止多账号自动刷新线程失败: {e}")

        # 重置所有状态（包含 accounts 清理）
        self._init_state_variables()
        self._load_global_config()
        self.log("已退出多账号模式。")

        # [BUG修复] 退出多账号模式后立即保存会话状态，清空多账号列表
        # 确保重启后不会恢复多账号模式
        session_id = getattr(self, "_web_session_id", None)
        if session_id:
            try:
                save_session_state(session_id, self, force_save=True)
                logging.info(f"退出多账号模式：已清空会话中的账号列表并保存")
            except Exception as e:
                logging.error(f"退出多账号模式：保存会话状态失败: {e}")

        return {"success": True}

    def enter_single_account_mode(self):
        """进入单账号模式（增强：先停止多账号运行）"""
        # 如果有多账号线程，先全停
        try:
            self.multi_stop_all_accounts()
            # 等待线程尽量退出
            for acc in list(getattr(self, "accounts", {}).values()):
                try:
                    if acc.worker_thread and acc.worker_thread.is_alive():
                        acc.stop_event.set()
                        acc.worker_thread.join(timeout=1.0)
                except Exception:
                    pass
        except Exception:
            logging.debug("enter_single_account_mode: stop multi failed (non-fatal).")

        # 清空路径规划回调
        for key, (path_result, completion_event) in list(
            self.path_gen_callbacks.items()
        ):
            path_result["error"] = "模式切换（进入单账号）已取消"
            try:
                completion_event.set()
            except Exception:
                pass
        self.path_gen_callbacks.clear()

        self.is_multi_account_mode = False
        self.log("进入单账号模式。")
        return {"success": True}

    def exit_single_account_mode(self):
        """
        退出单账号模式

        功能说明：
        - 用于移动端退出单账号模式，返回会话选择界面
        - 清理当前会话状态，但保留认证信息
        - 停止所有正在运行的任务

        返回:
            dict: {"success": True} 表示退出成功
        """
        try:
            # 停止当前运行的任务
            if hasattr(self, "stop_event"):
                self.stop_event.set()

            # 如果有工作线程，等待其结束
            if (
                hasattr(self, "worker_thread")
                and self.worker_thread
                and self.worker_thread.is_alive()
            ):
                self.worker_thread.join(timeout=1.0)

            # 清空路径规划回调，避免延迟回传
            if hasattr(self, "path_gen_callbacks"):
                for key, (path_result, completion_event) in list(
                    self.path_gen_callbacks.items()
                ):
                    path_result["error"] = "退出单账号模式已取消"
                    try:
                        completion_event.set()
                    except Exception:
                        pass
                self.path_gen_callbacks.clear()

            self.log("已退出单账号模式")
            return {"success": True}
        except Exception as e:
            logging.error(f"退出单账号模式失败: {e}", exc_info=True)
            return {"success": False, "message": f"退出失败: {str(e)}"}

    def get_session_mode_info(self):
        """获取会话模式信息（单账号/多账号），用于页面刷新时恢复状态"""
        mode_info = {
            "success": True,
            "is_multi_account_mode": getattr(self, "is_multi_account_mode", False),
            "school_account_logged_in": getattr(self, "login_success", False),
            "is_offline_mode": getattr(self, "is_offline_mode", False),
        }

        # 如果是多账号模式，返回更多信息
        if getattr(self, "is_multi_account_mode", False):
            mode_info["multi_account_count"] = len(getattr(self, "accounts", {}))
            mode_info["multi_account_usernames"] = list(
                getattr(self, "accounts", {}).keys()
            )
            mode_info["global_params"] = getattr(self, "global_params", {})

            # 返回账号详细信息（修复：页面刷新时恢复账号列表）
            accounts_data = []
            for username, acc in getattr(self, "accounts", {}).items():
                accounts_data.append(
                    {
                        "username": username,
                        "name": acc.user_data.name if acc.user_data.name else username,
                        "status_text": acc.status_text,
                        "summary": acc.summary,
                        "params": acc.params,
                    }
                )
            mode_info["accounts"] = accounts_data
        else:
            # 单账号模式信息
            mode_info["has_tasks"] = len(getattr(self, "all_run_data", [])) > 0
            mode_info["task_count"] = len(getattr(self, "all_run_data", []))
            mode_info["selected_task_index"] = getattr(self, "current_run_idx", -1)

            # 保存用户数据（用于离线模式恢复）
            if hasattr(self, "user_data") and self.user_data:
                user_data = self.user_data
                mode_info["user_data"] = {
                    "name": getattr(user_data, "name", ""),
                    "phone": getattr(user_data, "phone", ""),
                    "student_id": getattr(user_data, "student_id", ""),
                    "id": getattr(user_data, "id", ""),
                    "username": getattr(user_data, "username", ""),
                    "gender": getattr(user_data, "gender", ""),
                    "school_name": getattr(user_data, "school_name", ""),
                }

        return mode_info

    def multi_get_all_config_users(self):
        """
        获取所有存在配置文件的用户列表，用于前端便捷添加

        功能增强：根据当前认证用户的权限过滤返回结果
        - 如果用户有school_accounts权限，则可以看到该认证用户名下管理的所有学校账号
        - 如果没有特定权限，则只返回空列表
        - 这确保了用户只能访问自己有权限的配置数据

        返回:
            dict: {"users": [用户名列表]}
        """
        # 获取所有存在.ini配置文件的用户名列表
        all_users = sorted(
            [
                os.path.splitext(f)[0]
                for f in os.listdir(self.user_dir)
                if f.endswith(".ini")
            ]
        )

        # 权限过滤：根据当前认证用户的school_accounts权限过滤
        # 只返回当前认证用户有权限访问的账号
        filtered_users = []

        if hasattr(self, "auth_username") and self.auth_username:
            # 加载当前认证用户管理的school_accounts
            # _load_user_school_accounts返回格式：{school_username: {"password": "xxx", "ua": "xxx"}, ...}
            school_accounts = self._load_user_school_accounts(self.auth_username)

            # 只返回在school_accounts中存在的用户
            # 这确保了用户只能看到自己有权限访问的学校账号配置
            for username in all_users:
                if username in school_accounts:
                    filtered_users.append(username)

            logging.debug(
                f"用户 {self.auth_username} 可访问的配置用户: {len(filtered_users)}/{len(all_users)}"
            )
        else:
            # 如果没有认证用户信息，返回空列表（安全起见）
            logging.warning("multi_get_all_config_users: 没有认证用户信息，返回空列表")

        return {"users": filtered_users}

    def multi_load_accounts_from_config(self):
        """模式一：从所有.ini配置文件加载账号"""
        self.log("正在从配置文件加载账号列表...")
        users = sorted(
            [
                os.path.splitext(f)[0]
                for f in os.listdir(self.user_dir)
                if f.endswith(".ini")
            ]
        )
        loaded_count = 0
        accounts_missing_password = []
        for username in users:
            if username not in self.accounts:
                # 内部调用 multi_add_account 并检查其返回值
                add_result = self.multi_add_account(username, "")
                if add_result and add_result.get("action") == "request_password":
                    # 修正：存储完整的对象(包含username和tag)
                    accounts_missing_password.append(
                        {
                            "username": add_result.get("username"),
                            "tag": add_result.get("tag"),
                        }
                    )
                elif add_result and add_result.get("success"):
                    loaded_count += 1
        self.log(f"已加载 {loaded_count} 个账号。")
        if accounts_missing_password:
            self.log(
                f"发现 {len(accounts_missing_password)} 个账号缺少密码，等待用户手动添加。"
            )
        self._update_multi_global_buttons()

        # # 批量加载后立即触发一次“刷新全部”，便于自动拉取状态与汇总
        # try:
        #     self.multi_refresh_all_statuses()
        # except Exception:
        #     logging.error(f"触发刷新全部失败: {traceback.format_exc()}")

        final_status = self.multi_get_all_accounts_status()
        final_status["accounts_missing_password"] = accounts_missing_password
        return final_status

    def multi_add_account(self, username, password, tag=None, params=None):
        """模式二：手动或选择性添加账号

        Args:
            username: 账号用户名
            password: 账号密码
            tag: 账号标记（备注/标签），可选
            params: 额外的参数配置（可选，防止前端传参报错）
        """
        if username in self.accounts:
            # 如果账号已存在，智能处理密码更新或从文件刷新
            acc = self.accounts[username]

            # [新增] 如果传入了params，尝试更新参数
            if params and isinstance(params, dict):
                for k, v in params.items():
                    if k in acc.params:
                        acc.params[k] = v

            # 场景1: 提供了新的、非空的密码 (来自导入或手动输入)。
            # 则更新内存和文件中的密码。
            if password and acc.password != password:
                acc.password = password
                self._save_config(username, password)
                self.log(f"已更新账号 [{username}] 的密码。")
            # 场景2: 未提供密码 (来自下拉框重复添加)。
            # 此时从.ini文件实时重新加载密码，确保使用的是最新的（例如刚刚导入的）。
            else:
                self.log(f"账号 [{username}] 已存在，正在从配置文件刷新...")
                reloaded_password = self._load_config(username)
                if reloaded_password:
                    acc.password = reloaded_password

            # 更新标记（如果提供了新的标记）
            if tag is not None:
                acc.tag = str(tag)
                self._save_account_tag(username, acc.tag)
                self.log(f"已更新账号 [{username}] 的标记：{acc.tag}。")

            # 统一执行后续的强制刷新逻辑，以新密码或从文件加载的最新密码来重新验证
            try:
                # UI反馈为“刷新中…”
                self._update_account_status_js(acc, status_text="刷新中...")
                # 清理会话与登录态，强制走登录分支
                try:
                    acc.api_client.session.cookies.clear()
                except Exception:
                    pass
                acc.user_data.id = ""  # 标记为未登录，从而在刷新线程中执行登录流程
                # 启动刷新线程
                threading.Thread(
                    target=self._multi_refresh_worker, args=(acc,), daemon=True
                ).start()
            except Exception:
                logging.error(f"更新账号后触发刷新失败: {traceback.format_exc()}")
            # 刷新全局按钮状态并返回最新账号状态列表
            self._update_multi_global_buttons()
            return self.multi_get_all_accounts_status([{"success": True}])

        # 创建账号会话（注意：若稍后判定密码为空，将撤销）
        # 加载已保存的标记（如果有）
        loaded_tag = self._load_account_tag(username)
        final_tag = tag if tag is not None else (loaded_tag if loaded_tag else "")
        self.accounts[username] = AccountSession(
            username, password, self, tag=final_tag
        )

        # 尝试从 .ini 加载 UA/参数/密码（如果存在）
        loaded_password = self._load_config(username)

        # 如果加载不到UA，则生成一个新的
        if not self.accounts[username].device_ua:
            self.accounts[username].device_ua = ApiClient.generate_random_ua()

        # 最终确定密码：优先使用传入的新密码；否则使用 .ini 中的密码；否则空
        final_password = password or (loaded_password or "")
        self.accounts[username].password = final_password

        # 若最终密码仍为空，则弹出前端模态框让用户补充密码，并撤销本次添加
        if not final_password:
            # 撤销创建的会话，避免半添加状态
            try:
                del self.accounts[username]
            except Exception:
                pass
            self.log(f"账号 {username} 缺少密码，已弹出输入框以完善密码。")
            # [修正] 返回一个特定动作，由前端JS处理弹窗
            # 修正：同时返回tag，以便前端预填充
            return {
                "success": False,
                "message": "缺少密码",
                "action": "request_password",
                "username": username,
                "tag": final_tag,
            }

        # 检查是否需要首次验证
        # 如果导入的密码与已有配置文件中的密码不同，或者配置文件不存在，则需要首次验证
        ini_path = os.path.join(self.user_dir, f"{username}.ini")
        needs_verification = False

        if password and loaded_password and password != loaded_password:
            # 密码冲突：导入的密码与配置文件中的密码不同
            needs_verification = True
            self.log(f"账号 {username} 密码与配置文件不一致，需要首次登录验证。")
        elif password and not loaded_password:
            # 新账号：配置文件不存在或没有密码
            needs_verification = True
            self.log(f"账号 {username} 是新添加的账号，需要首次登录验证。")

        if needs_verification:
            # 标记为需要验证，不保存密码到配置文件
            self.accounts[username].is_first_login_verified = False
            self.accounts[username].is_verifying = True
            # 只保存 UA 和参数，不保存密码
            try:
                self._save_config(
                    username, password=None, ua=self.accounts[username].device_ua
                )
            except Exception:
                logging.warning(f"保存配置失败（将继续运行）：{traceback.format_exc()}")
        else:
            # 使用已有的密码，直接标记为已验证
            self.accounts[username].is_first_login_verified = True
            self.accounts[username].is_verifying = False
            # 保存完整配置
            try:
                self._save_config(
                    username,
                    self.accounts[username].password,
                    self.accounts[username].device_ua,
                )
            except Exception:
                logging.warning(f"保存配置失败（将继续运行）：{traceback.format_exc()}")

        self.log(f"已添加账号: {username}")
        # 添加账号后立即刷新“全部开始/全部停止”按钮状态
        self._update_multi_global_buttons()

        # 修正：使用 SocketIO 向特定会话发送“列表已更新”事件
        session_id = getattr(self, "_web_session_id", None)
        if session_id and socketio:
            try:
                current_accounts = self.multi_get_all_accounts_status().get(
                    "accounts", []
                )
                # 发送一个自定义事件 'accounts_updated'，前端JS需要监听这个事件
                socketio.emit(
                    "accounts_updated", {"accounts": current_accounts}, room=session_id
                )
            except Exception as e:
                logging.error(f"SocketIO emit 'accounts_updated' failed: {e}")

        # 为“刚添加的账号”立即启动刷新线程（自动登录 + 拉摘要）
        try:
            threading.Thread(
                target=self._multi_refresh_worker,
                args=(self.accounts[username],),
                daemon=True,
            ).start()
        except Exception:
            logging.error(f"启动刷新线程失败: {traceback.format_exc()}")

        if hasattr(self, "_web_session_id") and self._web_session_id:
            save_session_state(self._web_session_id, self, force_save=True)

        return self.multi_get_all_accounts_status([{"success": True}])

    def multi_remove_account(self, username):
        """移除一个账号"""
        if username in self.accounts:
            # 如果该账号正在运行，先停止它
            if (
                self.accounts[username].worker_thread
                and self.accounts[username].worker_thread.is_alive()
            ):
                self.accounts[username].stop_event.set()
            del self.accounts[username]
            self.log(f"已移除账号: {username}")
        # 统一刷新多账号全局按钮状态
        self._update_multi_global_buttons()
        if hasattr(self, "_web_session_id") and self._web_session_id:
            save_session_state(self._web_session_id, self, force_save=True)
        return self.multi_get_all_accounts_status()

    def multi_refresh_all_statuses(self):
        """(多线程)刷新所有账号的任务状态和统计信息"""
        # 【多账号自动刷新】记录刷新请求
        # 原因：记录刷新调用可以帮助追踪系统行为，便于调试和性能分析
        # 记录会话UUID可以区分不同用户的请求，便于多用户环境下的问题排查
        session_uuid = session.get("uuid", "unknown")
        logging.info(
            f"[多账号自动刷新] 收到刷新请求，会话UUID: {session_uuid}, 当前账号数量: {len(self.accounts) if self.accounts else 0}"
        )

        if not self.accounts:
            self.log("账号列表为空，无需刷新。")
            return {"success": True}

        self.log("正在刷新所有账号状态...")
        for acc in self.accounts.values():
            is_running = bool(acc.worker_thread and acc.worker_thread.is_alive())
            # 仅当账号未在运行时才提示“刷新中...”
            if not is_running:
                self._update_account_status_js(acc, status_text="刷新中...")
            # 运行中的账号走保留状态模式
            threading.Thread(
                target=self._multi_refresh_worker,
                args=(acc, True if is_running else False),
                daemon=True,
            ).start()

        self._update_multi_global_buttons()
        return {"success": True}

    def multi_refresh_single_status(self, username: str):
        """刷新指定账号的状态与摘要（单账号）"""
        if username not in self.accounts:
            return {"success": False, "message": "账号不存在"}
        acc = self.accounts[username]

        # 若账号正在运行任务，仍允许运行刷新线程，只要刷新线程自身不调用执行逻辑
        try:
            # 立刻标记UI状态
            self._update_account_status_js(acc, status_text="刷新中...")
            # 启动单独刷新线程（复用已有的 _multi_refresh_worker）
            threading.Thread(
                target=self._multi_refresh_worker, args=(acc,), daemon=True
            ).start()
            return {"success": True}
        except Exception as e:
            logging.error(f"启动单账号刷新失败: {e}", exc_info=True)
            self._update_account_status_js(acc, status_text="刷新出错")
            return {"success": False, "message": "启动刷新失败"}

    def _multi_refresh_worker(self, acc: AccountSession, preserve_status: bool = False):
        """用于刷新的单个账号工作线程
        - preserve_status=True 时：若账号正在运行，不改写 status_text，只更新 name 与 summary
        """
        try:
            # 更新最后刷新时间戳
            acc.last_refresh_time = time.time()

            # 动态判断是否需要保留状态（仅当账号当前正在运行且调用方要求保留时）
            preserve_now = preserve_status and bool(
                acc.worker_thread and acc.worker_thread.is_alive()
            )

            # 1) 登录（或确保已登录）
            if not acc.user_data.id:
                if not acc.device_ua:
                    acc.device_ua = ApiClient.generate_random_ua()

                # 标记正在验证
                if not acc.is_first_login_verified:
                    acc.is_verifying = True
                    if not preserve_now:
                        self._update_account_status_js(acc, status_text="首次验证中...")

                login_resp = self._queued_login(acc, respect_global_stop=False)
                if not login_resp or not login_resp.get("success"):
                    # 登录失败
                    if not acc.is_first_login_verified:
                        # 首次验证失败
                        acc.is_verifying = False
                        acc.is_first_login_verified = False
                        if not preserve_now:
                            self._update_account_status_js(
                                acc, status_text="验证失败(密码错误)"
                            )
                        acc.log(f"首次登录验证失败，密码可能不正确。")
                    else:
                        # 已验证账号的登录失败
                        if not preserve_now:
                            self._update_account_status_js(
                                acc, status_text="刷新失败(登录错误)"
                            )
                    return

                data = login_resp.get("data", {})
                user_info = data.get("userInfo", {})
                acc.user_data.name = user_info.get("name", "")
                acc.user_data.id = user_info.get("id", "")
                acc.user_data.student_id = user_info.get("account", "")

                # 首次登录验证成功，保存密码到配置文件
                if not acc.is_first_login_verified:
                    acc.is_first_login_verified = True
                    acc.is_verifying = False
                    try:
                        # 保存密码、UA和参数到配置文件
                        self._save_config(acc.username, acc.password, acc.device_ua)
                        acc.log(f"首次登录验证成功，密码已保存到配置文件。")
                    except Exception as e:
                        logging.error(f"保存密码到配置文件失败: {e}", exc_info=True)
                else:
                    # 写回 UA/参数（如有）
                    ini_path = os.path.join(self.user_dir, f"{acc.username}.ini")
                    if os.path.exists(ini_path):
                        self._save_config(acc.username)

                # 更新名字（允许）
                # 【修正】同时更新状态文本为“获取数据...”，避免一直显示“正在登录”
                self._update_account_status_js(
                    acc, name=acc.user_data.name, status_text="获取数据..."
                )

            # 2) 拉取任务并汇总
            self._multi_fetch_and_summarize_tasks(acc)

            # 2.5) 拉取签到统计
            if not preserve_now:  # 仅在非保留状态（即主动刷新）时才获取签到
                self._multi_fetch_attendance_stats(acc)

            # 3) 决定最终状态文本（仅当不保留状态时才改 status_text）
            if not preserve_now:
                exe_cnt = acc.summary.get("executable", 0)
                not_started_cnt = acc.summary.get("not_started", 0)

                if exe_cnt > 0:
                    final_status = f"有 {exe_cnt} 个任务可执行"
                    acc.has_pending_tasks = True
                elif not_started_cnt > 0:
                    final_status = "无任务可执行"
                    acc.has_pending_tasks = False
                else:
                    final_status = "无任务可执行"
                    acc.has_pending_tasks = False

                # 如果当前是错误态，则保留，不覆盖
                if self._should_preserve_status(
                    acc.status_text, new_status=final_status
                ):
                    self._update_account_status_js(acc, summary=acc.summary)
                else:
                    self._update_account_status_js(
                        acc, status_text=final_status, summary=acc.summary
                    )

            acc.log("状态刷新完成。")

            # [BUG修复] 账号刷新完成后保存会话状态（延迟保存，避免过于频繁）
            # 只在主动刷新（不保留状态）时保存，避免运行中的账号频繁保存
            if (
                not preserve_now
                and hasattr(self, "_web_session_id")
                and self._web_session_id
            ):
                # 使用线程延迟保存，避免阻塞刷新线程
                def delayed_save():
                    time.sleep(2)  # 延迟2秒，等待所有刷新完成
                    try:
                        save_session_state(self._web_session_id, self, force_save=True)
                        logging.debug(f"账号 {acc.username} 刷新完成后已保存会话状态")
                    except Exception as e:
                        logging.error(f"延迟保存会话状态失败: {e}")

                threading.Thread(target=delayed_save, daemon=True).start()

        except Exception as e:
            logging.error(f"Error refreshing {acc.username}: {traceback.format_exc()}")
            # 仅当不保留状态时才显示出错文案
            if not preserve_status:
                self._update_account_status_js(acc, status_text="刷新出错")

    def multi_remove_selected_accounts(self, usernames: list[str]):
        """根据用户名列表移除多个账号"""
        if not usernames:
            return self.multi_get_all_accounts_status()

        removed_count = 0
        for username in usernames:
            if username in self.accounts:
                # 如果账号正在运行，先停止它
                if (
                    self.accounts[username].worker_thread
                    and self.accounts[username].worker_thread.is_alive()
                ):
                    self.accounts[username].stop_event.set()
                del self.accounts[username]
                removed_count += 1

        self.log(f"移除了 {removed_count} 个选定账号。")
        self._update_multi_global_buttons()
        if hasattr(self, "_web_session_id") and self._web_session_id:
            save_session_state(self._web_session_id, self, force_save=True)

        return self.multi_get_all_accounts_status()

    def multi_remove_all_accounts(self):
        """一键移除所有账号"""
        if not self.accounts:
            return self.multi_get_all_accounts_status()

        # 停止所有正在运行的线程
        self.multi_stop_all_accounts()

        count = len(self.accounts)
        self.accounts.clear()
        self.log(f"已移除全部 {count} 个账号。")
        self._update_multi_global_buttons()
        if hasattr(self, "_web_session_id") and self._web_session_id:
            save_session_state(self._web_session_id, self, force_save=True)
        return self.multi_get_all_accounts_status()

    def multi_get_all_accounts_status(self, addition=None):
        """获取所有账号的当前状态，用于刷新前端UI"""
        status_list = []
        # 1. 遍历生成账号列表
        for acc in self.accounts.values():
            # --- 新增：序列化任务列表供前端筛选 ---
            tasks_simple = []
            if hasattr(acc, "all_run_data"):
                for r in acc.all_run_data:
                    # 只包含计算状态所需的字段，减少数据量
                    tasks_simple.append(
                        {
                            "status": getattr(r, "status", 0),
                            "start_time": getattr(r, "start_time", ""),
                            "end_time": getattr(r, "end_time", ""),
                            # 调用现有的 _get_task_info_text 方法获取 "已过期" / "开始于..." 等文本
                            "info_text": self._get_task_info_text(r),
                        }
                    )

            status_list.append(
                {
                    "username": acc.username,
                    "name": acc.user_data.name or "---",
                    "status_text": acc.status_text,
                    "summary": acc.summary,
                    "tag": acc.tag,
                    "tasks": tasks_simple,
                    # 【新增】返回实时状态数据供前端轮询
                    # 使用 getattr 避免属性不存在时报错
                    "current_position": getattr(acc, "current_position", None),
                    "progress_pct": getattr(acc, "progress_pct", 0),
                    "progress_text": getattr(acc, "progress_text", ""),
                    "progress_extra": getattr(acc, "progress_extra", ""),
                }
            )

        # 2. 构建基础返回对象
        response = {"accounts": status_list}

        # 3. 处理传入的补全内容 (addition)
        # 你的调用方式是: self.multi_get_all_accounts_status([{"success": True}])
        if addition:
            if isinstance(addition, list):
                # 如果传入的是列表，遍历并将字典项更新到 response 中
                for item in addition:
                    if isinstance(item, dict):
                        response.update(item)
            elif isinstance(addition, dict):
                # 如果直接传入的是字典，直接更新
                response.update(addition)
        response["success"] = True
        return response

    def multi_download_import_template(self):
        """下载导入模板（账号、密码、标记），支持 Web模式直接返回文件内容"""
        try:
            headers = ["账号", "密码", "标记"]

            # Web模式：生成xlsx文件到内存，返回base64编码的内容
            wb = openpyxl.Workbook()
            sh = wb.active
            sh.title = "模板"
            sh.append(headers)

            # 保存到内存流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)

            # 转换为base64
            file_content = base64.b64encode(output.read()).decode("utf-8")
            filename = f"账号导入模板_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"

            self.log(f"模板已生成：{filename}")
            return {
                "success": True,
                "filename": filename,
                "content": file_content,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        except Exception as e:
            self.log(f"模板生成失败：{e}")
            logging.error(f"Template generation failed: {traceback.format_exc()}")
            return {"success": False, "message": f"生成失败: {e}"}

    def multi_import_accounts(self, filename, base64_content):
        """从文件导入账号密码，支持 .xlsx/.xls/.csv（仅Web模式，从内存流处理）

        Args:
            filename: 文件名（从前端传入）
            base64_content: Base64编码的文件内容（从前端传入）
        """
        try:
            # 解码Base64内容到内存
            file_data = base64.b64decode(base64_content)
            file_stream = io.BytesIO(file_data)

            # 确定文件扩展名
            ext = os.path.splitext(filename)[1].lower()

            logging.info(
                f"正在从内存处理上传的文件 {filename}（大小：{len(file_data)} 字节）"
            )
        except Exception as e:
            logging.error(f"解码Base64内容失败: {e}")
            return {"success": False, "message": f"文件处理失败: {e}"}

        try:
            imported = 0
            seen_usernames: set[str] = (
                set()
            )  # 本次导入会话内去重，避免同一文件重复账号多次导入

            if ext == ".xlsx":
                # 从内存流加载工作簿
                try:
                    wb = openpyxl.load_workbook(
                        file_stream, data_only=True, read_only=True, keep_links=False
                    )
                except TypeError as e:
                    # 针对个别环境样式解析异常的兜底
                    warnings.warn(f"样式解析失败，已忽略样式: {e}")
                    file_stream.seek(0)  # 重置流位置
                    wb = openpyxl.load_workbook(
                        file_stream,
                        data_only=True,
                        read_only=True,
                        keep_links=False,
                        keep_vba=False,
                    )

                sh = wb.active
                skipped_no_password = []  # 收集无密码且 .ini 无密码的账号
                # 从第2行开始，默认第1行为表头，避免重复处理与表头导入
                for row in sh.iter_rows(min_row=2, values_only=True):
                    if not row or len(row) < 1:
                        continue
                    username = str(row[0] or "").strip()
                    password = str(row[1] or "").strip() if len(row) > 1 else ""
                    # 支持第三列：标记（可选）
                    tag = None
                    if len(row) > 2 and row[2]:
                        tag = str(row[2]).strip()

                    if not username:
                        continue
                    # 本次导入内去重
                    if username in seen_usernames:
                        continue
                    seen_usernames.add(username)

                    # 1. 尝试从 .ini 兜底密码
                    loaded_password = self._load_config(username)
                    # 2. 确定最终密码
                    final_password = password or (loaded_password or "")

                    if not final_password:
                        # 3. 只有当导入文件和.ini都没有密码时，才跳过
                        skipped_no_password.append(username)
                        continue  # 跳过本账号，留给用户手动补密码

                    # 4. 使用 final_password 和 tag 添加
                    self.multi_add_account(username, final_password, tag=tag)
                    imported += 1

            elif ext == ".xls":
                # xlrd支持从内存流读取
                file_stream.seek(0)  # 重置流位置
                book = xlrd.open_workbook(file_contents=file_stream.read())
                sh = book.sheet_by_index(0)
                skipped_no_password = []
                for r in range(1, sh.nrows):
                    username = str(sh.cell_value(r, 0) or "").strip()
                    password = ""
                    if sh.ncols >= 2:
                        password = str(sh.cell_value(r, 1) or "").strip()
                    # 支持第三列：标记（可选）
                    tag = None
                    if sh.ncols >= 3:
                        tag_val = sh.cell_value(r, 2)
                        if tag_val:
                            tag = str(tag_val).strip()

                    if username:
                        if username in seen_usernames:
                            continue
                        seen_usernames.add(username)

                        loaded_password = self._load_config(username)
                        final_password = password or (loaded_password or "")
                        if not final_password:
                            skipped_no_password.append(username)
                            continue

                        self.multi_add_account(username, final_password, tag=tag)
                        imported += 1

            elif ext == ".csv":
                skipped_no_password = []
                # 从内存流读取CSV
                file_stream.seek(0)  # 重置流位置
                # 将字节流转换为文本流
                text_stream = io.TextIOWrapper(
                    file_stream, encoding="utf-8-sig", newline=""
                )
                reader = csv.reader(text_stream)

                first_row = True
                for row in reader:
                    if not row or len(row) < 1:
                        continue
                    # 跳过可能的表头
                    if first_row and str(row[0]).strip() in (
                        "账号",
                        "用户名",
                        "username",
                        "user",
                    ):
                        first_row = False
                        continue
                    first_row = False
                    username = (row[0] or "").strip()
                    password = (row[1] or "").strip() if len(row) > 1 else ""
                    # 支持第三列：标记（可选）
                    tag = None
                    if len(row) > 2 and row[2]:
                        tag = row[2].strip()

                    if username:
                        if username in seen_usernames:
                            continue
                        seen_usernames.add(username)

                        loaded_password = self._load_config(username)
                        final_password = password or (loaded_password or "")
                        if not final_password:
                            skipped_no_password.append(username)
                            continue

                        self.multi_add_account(username, final_password, tag=tag)
                        imported += 1

            else:
                return {"success": False, "message": f"不支持的导入格式: {ext}"}

            # 导入汇总日志
            self.log(f"成功导入 {imported} 个账号。")
            if skipped_no_password:
                # 前端弹窗提醒需要手动补密码
                msg = "以下账号缺少密码，已跳过导入。请在多账号控制台手动添加并输入密码：\n" + "\n".join(
                    skipped_no_password[:20]
                )
                # 提示过长时仅显示前 20 条，避免 UI 过载
                try:
                    if self.window:
                        self.window.evaluate_js(f"alert({json.dumps(msg)})")
                except Exception:
                    logging.debug("Alert skipped_no_password failed (non-fatal).")
                self.log(
                    f"缺少密码的账号（共 {len(skipped_no_password)}）：{', '.join(skipped_no_password)}"
                )

            return self.multi_get_all_accounts_status()

        except Exception as e:
            self.log(f"导入失败: {e}")
            logging.error(f"导入多账号配置失败，详细错误信息: {traceback.format_exc()}")
            return {"success": False, "message": f"导入失败: {e}"}

    def multi_export_accounts_summary(self):
        """导出多账号汇总，支持 Web模式直接返回文件内容"""
        try:
            headers = [
                "账号",
                "姓名",
                "状态",
                "总任务数",
                "已完成",
                "未开始任务数",
                "可执行任务数",
                "已过期任务数",
            ]

            rows = []
            for acc in sorted(self.accounts.values(), key=lambda x: x.username):
                s = acc.summary
                rows.append(
                    [
                        acc.username,
                        acc.user_data.name or "---",
                        acc.status_text,
                        s.get("total", 0),
                        s.get("completed", 0),
                        s.get("not_started", 0),
                        s.get("executable", 0),
                        s.get("expired", 0),
                    ]
                )

            # Web模式：生成xlsx文件到内存，返回base64编码的内容
            wb = openpyxl.Workbook()
            sh = wb.active
            sh.title = "任务汇总"
            sh.append(headers)
            for r in rows:
                sh.append(r)

            # 自动列宽
            for col in sh.columns:
                max_len = 0
                col_letter = col[0].column_letter
                for cell in col:
                    v = "" if cell.value is None else str(cell.value)
                    max_len = max(max_len, len(v))
                sh.column_dimensions[col_letter].width = max_len + 2

            # 保存到内存流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)

            # 转换为base64
            file_content = base64.b64encode(output.read()).decode("utf-8")
            filename = f"跑步任务汇总_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"

            self.log(f"汇总信息已导出到 {filename}")
            return {
                "success": True,
                "filename": filename,
                "content": file_content,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        except Exception as e:
            self.log(f"导出失败: {e}")
            logging.error(f"Export accounts summary failed: {traceback.format_exc()}")
            return {"success": False, "message": f"导出失败: {e}"}

    def multi_get_account_params(self, username):
        """
        获取指定账号的参数配置。

        功能说明：
        在多账号模式下，获取单个账号的完整参数配置字典。
        用于Web界面显示账号配置或进行参数修改前的查询。

        参数:
            username (str): 账号用户名

        返回:
            dict: 包含以下字段：
                - success (bool): 操作是否成功
                - params (dict): 账号参数字典（成功时）
                - message (str): 错误信息（失败时）

        使用示例:
            result = api.multi_get_account_params("user123")
            if result["success"]:
                print(result["params"])
        """
        if username in self.accounts:
            return {"success": True, "params": self.accounts[username].params}
        return {"success": False, "message": "账号不存在"}

    def multi_update_account_param(self, username, key, value):
        """
        更新指定账号的单个参数值。

        功能说明：
        动态修改账号的配置参数，支持类型自动转换和配置持久化。
        修改后立即保存到配置文件，确保重启后配置不丢失。

        类型转换规则：
        - bool类型：支持多种表示方式（'true', '1', 't', 'yes'等）
        - 其他类型：根据原始参数类型自动转换（int, float, str等）

        参数:
            username (str): 账号用户名
            key (str): 参数键名（必须是已存在的参数）
            value: 新的参数值（将自动转换为正确类型）

        返回:
            dict: 包含以下字段：
                - success (bool): 操作是否成功
                - message (str): 错误信息（失败时）

        异常处理:
            - ValueError: 类型转换失败
            - TypeError: 类型不兼容

        ⚠️ 注意事项：
        1. 只能修改已存在的参数，不能添加新参数
        2. 类型必须与原始参数类型兼容
        3. 修改会立即保存到磁盘

        使用示例:
            # 修改布尔参数
            api.multi_update_account_param("user1", "auto_run", "true")
            # 修改数值参数
            api.multi_update_account_param("user1", "speed", 1.5)
        """
        if username not in self.accounts:
            return {"success": False, "message": "账号不存在"}

        acc = self.accounts[username]
        target_params = acc.params
        if key in target_params:
            try:
                # 获取原始参数类型，用于类型转换
                original_type = type(target_params[key])
                # 布尔类型特殊处理：支持多种表示方式
                if original_type is bool:
                    target_params[key] = (
                        bool(value)
                        if isinstance(value, bool)
                        else str(value).lower() in ("true", "1", "t", "yes")
                    )
                else:
                    # 其他类型：强制转换为原始类型
                    target_params[key] = original_type(value)

                # 保存配置到文件（持久化）
                self._save_config(username, self.accounts[username].password)
                self.log(f"已更新账号 [{username}] 的参数 {key}。")

                # [BUG修复] 账号参数更新后保存会话状态
                if hasattr(self, "_web_session_id") and self._web_session_id:
                    save_session_state(self._web_session_id, self, force_save=True)

                return {"success": True}
            except (ValueError, TypeError) as e:
                # 类型转换失败，返回错误
                return {"success": False, "message": str(e)}
        # 参数不存在
        return {"success": False, "message": "Unknown parameter"}

    def multi_start_single_account(self, username, run_only_incomplete: bool = True):
        """
        启动指定账号的任务执行线程。

        功能说明：
        在多账号模式下启动单个账号的自动任务执行。
        创建独立的工作线程，不阻塞主线程和其他账号。

        执行流程：
        1. 验证账号存在性
        2. 检查是否已在运行（避免重复启动）
        3. 清除停止标志，准备运行
        4. 创建daemon工作线程
        5. 更新UI状态

        参数:
            username (str): 要启动的账号用户名
            run_only_incomplete (bool): 是否只执行未完成的任务
                - True: 跳过已完成的任务，只执行新任务或失败任务
                - False: 执行所有任务，包括已完成的（重新执行）

        返回:
            dict: 包含以下字段：
                - success (bool): 操作是否成功
                - message (str): 错误信息（失败时）

        线程安全：
        - 使用stop_event控制线程生命周期
        - daemon线程确保主程序退出时自动清理
        - multi_run_stop_flag全局停止控制

        ⚠️ 注意事项：
        1. 重复启动会被拒绝（返回失败）
        2. 线程异常会被_multi_account_worker内部捕获
        3. 启动后无法修改run_only_incomplete参数
        """
        if username not in self.accounts:
            return {"success": False, "message": "账号不存在"}
        acc = self.accounts[username]
        if acc.worker_thread and acc.worker_thread.is_alive():
            self.log(f"账号 {username} 已在运行中。")
            return {"success": False, "message": "该账号已在运行"}

        acc.stop_event.clear()
        # 进入运行态
        if self.multi_run_stop_flag.is_set():
            self.multi_run_stop_flag.clear()
        # 使用传入的 run_only_incomplete 复选框状态
        acc.worker_thread = threading.Thread(
            target=self._multi_account_worker,
            args=(acc, 0, bool(run_only_incomplete)),
            daemon=True,
        )
        acc.worker_thread.start()
        self.log(f"已启动账号: {username}")
        self._update_account_status_js(acc, status_text="排队等待...")
        self._update_multi_global_buttons()
        return {"success": True}

    def multi_stop_single_account(self, username):
        """
        停止指定账号的任务执行线程。

        功能说明：
        向账号的工作线程发送停止信号，优雅地终止任务执行。
        使用异步监视器等待线程完全退出后清理资源。

        停止流程：
        1. 验证账号存在性
        2. 检查线程是否在运行
        3. 设置stop_event信号
        4. 启动监视线程等待工作线程退出
        5. 线程退出后更新UI状态为"待命"

        设计特点：
        - 非阻塞：使用独立监视线程，不阻塞主线程
        - 优雅停止：通过Event信号，让线程自己退出
        - 资源清理：线程退出后自动清理worker_thread句柄
        - 状态同步：实时更新UI状态显示

        监视器(_watch_stop)机制：
        - 每200ms检查一次线程状态
        - 线程退出后立即清理和更新UI
        - daemon线程确保不会阻止程序退出
        - 捕获所有异常，避免监视器崩溃

        ⚠️ 注意事项：
        1. 停止是异步的，可能需要几秒钟完成
        2. 如果线程未在运行，返回失败但不报错
        3. 强制停止可能导致任务状态不完整
        """
        acc = self.accounts.get(username)
        if not acc:
            return {"success": False, "message": f"账号 {username} 不存在"}

        if acc.worker_thread and acc.worker_thread.is_alive():
            acc.stop_event.set()
            self.log(f"已向账号 {username} 发送停止信号。")
            self._update_account_status_js(acc, status_text="正在停止...")
            self._update_multi_global_buttons()

            # 监视该账号的工作线程退出，退出后立即刷新UI与按钮状态
            def _watch_stop():
                try:
                    while acc.worker_thread and acc.worker_thread.is_alive():
                        time.sleep(0.2)
                    # 线程已退出，清理句柄并刷新状态
                    acc.worker_thread = None
                    # 若用户主动停止，统一回到“待命”
                    self._update_account_status_js(acc, status_text="待命")
                    self._update_multi_global_buttons()
                except Exception:
                    logging.debug(
                        "Stop watcher encountered a non-fatal error.", exc_info=True
                    )

            threading.Thread(target=_watch_stop, daemon=True).start()

            return {"success": True}
        else:
            self._update_account_status_js(acc, status_text="待命")
            self._update_multi_global_buttons()
            return {"success": False, "message": "该账号未在运行"}

    def multi_start_all_accounts(
        self, min_delay, max_delay, use_delay, run_only_incomplete
    ):
        """一键启动所有账号的任务"""
        # 账号为空：直接失败
        if not self.accounts:
            self.log("账号列表为空，无法开始。请先添加账号。")
            return {
                "success": False,
                "message": "账号列表为空，无法开始。请先添加账号。",
            }

        # 仅当“所有账号都在运行中”才阻止
        total_accounts = len(self.accounts)
        running_count = sum(
            1
            for acc in self.accounts.values()
            if acc.worker_thread and acc.worker_thread.is_alive()
        )
        if total_accounts > 0 and running_count == total_accounts:
            return {"success": False, "message": "任务已在运行中"}

        # 允许为未运行账号继续启动（不再用全局停止标志作为唯一门槛）
        self.log("开始执行所有账号...")
        self._update_multi_global_buttons()
        # 若之前已在运行（multi_run_stop_flag 已清除），无需重复清除；否则清除以表明进入“运行态”
        if self.multi_run_stop_flag.is_set():
            self.multi_run_stop_flag.clear()

        account_list = list(self.accounts.values())
        num_accounts = len(account_list)
        delays = [0] * num_accounts

        if use_delay and num_accounts > 0 and max_delay >= min_delay:
            try:
                delays = [
                    random.uniform(min_delay, max_delay) for _ in range(num_accounts)
                ]
            except ValueError:
                delays = [
                    random.uniform(min_delay, max_delay) for _ in range(num_accounts)
                ]

        random.shuffle(account_list)

        started_threads = 0
        for i, acc in enumerate(account_list):
            # 已在运行的账号跳过，仅启动未运行账号
            if acc.worker_thread and acc.worker_thread.is_alive():
                acc.log("已在运行，本次'全部开始'将跳过此账号。")
                continue

            delay = delays[i] if use_delay else 0
            acc.stop_event.clear()
            acc.worker_thread = threading.Thread(
                target=self._multi_account_worker,
                args=(acc, delay, run_only_incomplete),
                daemon=True,
            )
            acc.worker_thread.start()
            started_threads += 1

        # 如果这次没有任何账号被启动（所有账号已在运行或无可执行任务）
        if started_threads == 0:
            # 保持标志位为“运行中”或“停止”的合理状态：
            # - 若此前有运行中的账号，则 multi_run_stop_flag 可能已清除，无需更改；
            # - 若此前标志为停止，则维持停止态，给出用户提示。
            self.log("当前没有可启动的账号任务。")
            return {"success": False, "message": "当前没有可启动的账号任务。"}

        self._update_multi_global_buttons()
        return {"success": True}

    def multi_stop_all_accounts(self):
        """停止所有账号的运行"""
        logging.info("API调用: multi_stop_all_accounts - 停止所有多账号任务的运行")
        # 账号为空的情况，直接提示，无需切状态
        if not self.accounts:
            self.log("当前无账号，无需停止。")
            # 保持一致性：确保全局停止标志为“已停止”
            self.multi_run_stop_flag.set()
            return {"success": False, "message": "当前无账号，无需停止。"}

        if self.multi_run_stop_flag.is_set():
            return {"success": True}

        self.log("正在发送停止信号...")
        self.multi_run_stop_flag.set()
        for acc in self.accounts.values():
            acc.stop_event.set()
        self._update_multi_global_buttons()
        self.log("所有任务将在当前步骤完成后停止。")
        self._update_multi_global_buttons()

        time.sleep(1)

        self._update_multi_global_buttons()
        return {"success": True}

    def _update_account_status_js(
        self,
        acc: AccountSession,
        status_text: str = None,
        summary: dict = None,
        name: str = None,
        progress_pct: int | None = None,
        progress_text: str | None = None,
        progress_extra: str | None = None,
    ):
        """一个辅助函数，用于向前端发送状态更新"""
        # 修正：使用 SocketIO 向特定会话发送更新，而不是 self.window
        session_id = getattr(self, "_web_session_id", None)
        if not session_id or not socketio:
            logging.debug(
                f"跳过账号状态更新（_update_account_status_js），账号: {acc.username}，原因: 缺少会话ID或socketio未初始化"
            )
            return  # 如果没有会话ID或socketio未初始化，则无法发送

        update_data = {}
        if status_text is not None:
            acc.status_text = status_text
            update_data["status_text"] = status_text
        if summary is not None:
            acc.summary = summary
            update_data["summary"] = summary
        if name is not None:
            update_data["name"] = name

        # 进度条更新
        if progress_pct is not None:
            # 【新增】保存到实例属性
            acc.progress_pct = int(progress_pct)
            update_data["progress_pct"] = int(progress_pct)
        if progress_text is not None:
            # 【新增】保存到实例属性
            acc.progress_text = progress_text
            update_data["progress_text"] = progress_text
        if progress_extra is not None:
            # 【新增】保存到实例属性
            acc.progress_extra = progress_extra
            update_data["progress_extra"] = progress_extra

        if update_data:
            try:
                # 发送一个自定义事件到该 session_id 对应的房间
                socketio.emit(
                    "multi_status_update",
                    {"username": acc.username, "data": update_data},
                    room=session_id,
                )
                # [修复] 使用 time.sleep 替代 socketio.sleep，避免 greenlet.error
                time.sleep(0.001)  # 强制交出控制权，确保状态更新立即发送
            except Exception as e:
                logging.error(f"SocketIO emit 'multi_status_update' failed: {e}")

        # _update_multi_global_buttons 也需要用 socketio
        self._update_multi_global_buttons()

    def _update_multi_global_buttons(self):
        """根据当前多账号状态刷新“全部开始/全部停止/返回登录页”按钮的可用性"""
        # 修正：使用 SocketIO 向特定会话发送更新
        session_id = getattr(self, "_web_session_id", None)
        if not session_id or not socketio:
            logging.debug(
                "跳过多账号全局按钮更新（_update_multi_global_buttons），原因: 缺少会话ID或socketio未初始化"
            )
            return

        # 仅统计仍有任务可执行的账号（active）
        active_accounts = []
        for acc in self.accounts.values():
            total = acc.summary.get("total", 0)
            expired = acc.summary.get("expired", 0)
            not_started = acc.summary.get("not_started", 0)
            executable = acc.summary.get("executable", 0)
            # 候选任务：已开始且未截止（无论是否已完成）
            candidates = max(0, total - expired - not_started)
            has_tasks = (
                (executable > 0) if self.multi_run_only_incomplete else (candidates > 0)
            )
            if has_tasks:
                active_accounts.append(acc)

        total_active = len(active_accounts)
        running_count = sum(
            1
            for acc in active_accounts
            if acc.worker_thread and acc.worker_thread.is_alive()
        )

        # 四种状态规则：
        # 1) 无账号 或 无active账号：start=禁用, stop=禁用, exit=启用
        # 2) 有active且不是全部在运行：start=启用, stop=启用, exit=禁用
        # 3) 全部active都在运行：start=禁用, stop=启用, exit=禁用
        if total_active == 0:
            # 无账号或无可执行任务
            start_disabled = True
            stop_disabled = True
            exit_disabled = False
        elif running_count == 0:
            # 有账号但没有任何账号在执行任务
            start_disabled = False
            stop_disabled = True
            exit_disabled = False
        elif running_count == total_active:
            # 全部 active 账号都在运行
            start_disabled = True
            stop_disabled = False
            exit_disabled = True
        else:
            # 部分账号在运行
            start_disabled = False
            stop_disabled = False
            exit_disabled = True

        # 推送到前端
        try:
            socketio.emit(
                "multi_global_buttons_update",
                {
                    "start_disabled": start_disabled,
                    "stop_disabled": stop_disabled,
                    "exit_disabled": exit_disabled,
                },
                room=session_id,
            )
        except Exception as e:
            logging.error(f"SocketIO emit 'multi_global_buttons_update' failed: {e}")

    def _queued_login(
        self, acc: AccountSession, respect_global_stop: bool = True
    ) -> dict | None:
        """
        多账号模式下的“排队登录”（参数化是否尊重全局停止标志）：
        - 使用全局信号量 multi_login_lock 将登录并发固定为 1
        - 在排队等待期间，若收到停止信号（可选尊重 multi_run_stop_flag），立即退出
        - 进入队列前给出UI提示“排队登录...”
        """
        try:
            self._update_account_status_js(acc, status_text="排队登录...")
        except Exception:
            pass

        # 循环尝试获取登录槽位，期间尊重停止事件
        while True:
            # 刷新线程登录不受全局停止影响；任务执行阶段登录继续尊重全局停止
            if acc.stop_event.is_set() or (
                respect_global_stop and self.multi_run_stop_flag.is_set()
            ):
                return None
            # 尝试以短超时获取锁，便于及时响应停止
            acquired = self.multi_login_lock.acquire(timeout=0.5)
            if acquired:
                break
        try:
            # 二次检查停止（同样按参数决定是否尊重全局停止）
            if acc.stop_event.is_set() or (
                respect_global_stop and self.multi_run_stop_flag.is_set()
            ):
                return None

            # 【修正】获取锁后，立即更新状态为“正在登录”，防止一直显示排队
            self._update_account_status_js(acc, status_text="正在登录...")

            # 执行实际登录请求
            return acc.api_client.login(acc.username, acc.password)
        finally:
            try:
                self.multi_login_lock.release()
            except Exception:
                pass

    def _multi_fetch_and_summarize_tasks(self, acc: AccountSession):
        """(辅助函数) 为单个账号获取任务列表并计算统计信息（按任务ID去重）"""
        acc.all_run_data = []
        seen_keys: set[str] = set()  # 记录已见过的 errandId（与其他处保持一致）
        offset = 0
        dup_count = 0  # 可选：统计重复条数

        while True:
            if acc.stop_event.is_set():
                return
            resp = acc.api_client.get_run_list(acc.user_data.id, offset)
            if not resp or not resp.get("success"):
                acc.log("获取任务列表失败。")
                break

            tasks = resp.get("data", {}).get("errandList", [])
            if not tasks:
                break

            for td in tasks:
                # 构造稳健唯一键（兼容 errandId 缺失 / 同一 errandId 不同 schedule 或时间）
                eid = td.get("errandId") or ""
                es = td.get("errandSchedule") or ""
                st = td.get("startTime") or ""
                et = td.get("endTime") or ""
                unique_key = f"{eid}|{es}|{st}|{et}"

                if unique_key in seen_keys:
                    dup_count += 1
                    continue
                seen_keys.add(unique_key)

                run = RunData()
                run.run_name = td.get("eName")

                # 规范化 status（防止字符串/布尔等造成后续比较错误）
                try:
                    run.status = int(td.get("isExecute") or 0)
                except (TypeError, ValueError):
                    run.status = (
                        1
                        if str(td.get("isExecute")).strip().lower()
                        in ("1", "true", "yes")
                        else 0
                    )

                run.errand_id = eid
                run.errand_schedule = es
                run.start_time = st
                run.end_time = et
                acc.all_run_data.append(run)

                # 临时调试日志（上线后可删除）
                logging.info(
                    f"[{acc.username}] Parsed task {eid!r}: raw_isExecute={td.get('isExecute')!r} -> status={run.status}"
                )

            offset += len(tasks)
            if len(tasks) < 10:
                break

        if dup_count > 0:
            logging.info(
                f"[{acc.username}] Task de-dup: {dup_count} duplicates skipped (by errandId)."
            )

        # --- 任务分类统计重构 ---
        total = len(acc.all_run_data)
        completed = 0
        expired = 0
        executable = 0
        not_started = 0

        now = datetime.datetime.now()
        ignore_time = acc.params.get("ignore_task_time", True)

        for r in acc.all_run_data:
            # 1. 首先处理已完成的任务
            if r.status == 1:
                completed += 1
                # 如果全局开关开启了“仅执行未完成”，则已完成的任务不再视为可执行
                if self.multi_run_only_incomplete:
                    continue
                # 如果“仅执行未完成”为False，则已完成的任务继续向下进行时间检查，可能计入可执行

            # 2. 对任务进行时间分类 (status != 1 或者 status == 1 且允许重跑)
            start_dt, end_dt = None, None
            try:
                if r.start_time:
                    start_dt = datetime.datetime.strptime(
                        r.start_time, "%Y-%m-%d %H:%M:%S"
                    )
            except (ValueError, TypeError):
                start_dt = None
            try:
                if r.end_time:
                    end_dt = datetime.datetime.strptime(r.end_time, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                end_dt = None

            # 检查是否过期
            if end_dt:
                is_expired = end_dt.date() < now.date() if ignore_time else end_dt < now
                if is_expired:
                    expired += 1
                    continue

            # 检查是否未开始
            if start_dt:
                is_not_started = (
                    now.date() < start_dt.date() if ignore_time else now < start_dt
                )
                if is_not_started:
                    not_started += 1
                    continue

            # 剩余的未完成任务即为可执行
            executable += 1

        acc.summary.update(
            {
                "total": total,
                "completed": completed,
                "pending": total - completed,
                "not_started": not_started,
                "executable": executable,
                "expired": expired,
            }
        )

        # 未开始任务仅在摘要中展示，不应影响“全部开始/停止”按钮或地图标记逻辑
        acc.has_pending_tasks = executable > 0

    def _multi_fetch_attendance_stats(self, acc: AccountSession):
        """(多账号) 获取单个账号的签到统计"""
        if not acc.user_data.id:
            return  # 尚未登录

        try:
            list_resp = acc.api_client.get_notice_list(offset=0, limit=20, type_id=0)
            if not (list_resp and list_resp.get("success")):
                acc.log("获取通知列表失败 (用于签到统计)")
                return

            notices = list_resp.get("data", {}).get("noticeList", [])
            att_pending = 0
            att_completed = 0
            att_expired = 0

            for notice in notices:
                is_attendance = notice.get(
                    "image"
                ) == "attendance" or "签到" in notice.get("title", "")
                if is_attendance and notice.get("id"):
                    roll_call_id = notice["id"]
                    info_resp = acc.api_client.get_roll_call_info(
                        roll_call_id, acc.user_data.id
                    )

                    status = -2
                    finished = 0
                    if info_resp and info_resp.get("success"):
                        data = info_resp.get("data", {})
                        roll_call_info = data.get("rollCallInfo", {})
                        status = roll_call_info.get("status")
                        finished = data.get("attendFinish")

                    # --- 应用新逻辑 ---
                    if status == -1:
                        att_expired += 1
                    elif status != -1 and (finished == 1 or finished is True):
                        att_completed += 1
                    else:  # status != -1 and finished == 0
                        att_pending += 1

            # 更新到账号的 summary
            acc.summary.update(
                {
                    "att_pending": att_pending,
                    "att_completed": att_completed,
                    "att_expired": att_expired,
                }
            )
            logging.debug(
                f"[{acc.username}] 签到统计: 待签{att_pending}, 完成{att_completed}, 过期{att_expired}"
            )

        except Exception as e:
            acc.log(f"刷新签到统计时出错: {e}")
            logging.error(
                f"[{acc.username}] Failed to fetch attendance stats: {e}", exc_info=True
            )

    def multi_path_generation_callback(self, username: str, success: bool, data: any):
        """接收来自JS的路径规划结果并唤醒对应线程"""
        if username in self.path_gen_callbacks:
            path_result, completion_event = self.path_gen_callbacks.pop(username)
            if success:
                path_result["path"] = data
            else:
                path_result["error"] = data
            completion_event.set()

    def _multi_account_worker(
        self, acc: AccountSession, delay: float, run_only_incomplete: bool
    ):
        try:
            if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                self._update_account_status_js(acc, status_text="已取消")
                return

            # 检查是否需要重新登录和刷新任务列表
            # 如果20秒内已经刷新过（例如首次验证刚完成），则跳过登录和任务刷新，直接使用已有数据
            current_time = time.time()
            time_since_last_refresh = current_time - acc.last_refresh_time
            skip_refresh = (
                time_since_last_refresh < 20
                and acc.user_data.id
                and len(acc.all_run_data) > 0
            )

            if skip_refresh:
                acc.log(
                    f"距离上次刷新仅 {time_since_last_refresh:.1f} 秒，跳过重复刷新，直接使用已有数据。"
                )
            else:
                self._update_account_status_js(acc, status_text="登录中...")
                if not acc.device_ua:
                    acc.device_ua = ApiClient.generate_random_ua()

                # 登录前再次检查是否已被停止
                if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已中止")
                    self._update_multi_global_buttons()
                    return

                login_resp = self._queued_login(acc)

                # 登录返回后立即检查是否已被停止（避免继续向下流程）
                if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已中止")
                    self._update_multi_global_buttons()
                    return

                if not login_resp or not login_resp.get("success"):
                    msg = (
                        login_resp.get("message", "未知错误")
                        if login_resp
                        else "网络错误"
                    )
                    self._update_account_status_js(acc, status_text=f"登录失败: {msg}")
                    return

                data = login_resp.get("data", {})
                user_info = data.get("userInfo", {})
                acc.user_data.name = user_info.get("name", "")
                acc.user_data.id = user_info.get("id", "")
                acc.user_data.student_id = user_info.get("account", "")
                acc.log("登录成功。")
                self._update_account_status_js(
                    acc, status_text="分析任务", name=acc.user_data.name
                )

                if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已中止")
                    return

                self._multi_fetch_and_summarize_tasks(acc)
                self._update_account_status_js(acc, summary=acc.summary)

                # 更新刷新时间戳
                acc.last_refresh_time = time.time()

            tasks_to_run_candidates = []
            now = datetime.datetime.now()
            ignore_time = acc.params.get("ignore_task_time", True)
            acc.log(
                f"分析任务参数: ignore_task_time={ignore_time}, run_only_incomplete={run_only_incomplete}"
            )
            for r in acc.all_run_data:
                # 解析时间
                start_dt = None
                end_dt = None
                try:
                    if r.start_time:
                        start_dt = datetime.datetime.strptime(
                            r.start_time, "%Y-%m-%d %H:%M:%S"
                        )
                except (ValueError, TypeError):
                    start_dt = None
                try:
                    if r.end_time:
                        end_dt = datetime.datetime.strptime(
                            r.end_time, "%Y-%m-%d %H:%M:%S"
                        )
                except (ValueError, TypeError):
                    end_dt = None

                # 排除过期
                if end_dt:
                    is_expired = (
                        end_dt.date() < now.date() if ignore_time else end_dt < now
                    )
                    if is_expired:
                        continue

                # 排除未开始
                if start_dt:
                    is_not_started = (
                        now.date() < start_dt.date() if ignore_time else now < start_dt
                    )
                    if is_not_started:
                        continue

                tasks_to_run_candidates.append(r)

            tasks_to_run = (
                [t for t in tasks_to_run_candidates if t.status == 0]
                if run_only_incomplete
                else tasks_to_run_candidates
            )

            acc.log(
                f"任务筛选结果: 候选任务={len(tasks_to_run_candidates)}, 待执行任务={len(tasks_to_run)}"
            )

            if not tasks_to_run:
                self._update_account_status_js(acc, status_text="无任务可执行")
                self._update_multi_global_buttons()
                return
            else:
                acc.has_pending_tasks = True  # 有任务可执行

            tasks_executed_count = 0  # 跟踪实际执行的任务数

            if delay > 0:
                end_time = time.time() + delay
                while time.time() < end_time:
                    if acc.stop_event.is_set() or self.multi_run_stop_flag.is_set():
                        self._update_account_status_js(acc, status_text="已中止")
                        self._update_multi_global_buttons()
                        return
                    remaining = end_time - time.time()
                    self._update_account_status_js(
                        acc, status_text=f"延迟 {remaining:.0f}s"
                    )
                    time.sleep(1)

            for i, run_data in enumerate(tasks_to_run):
                if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已中止")
                    self._update_multi_global_buttons()
                    break

                task_name_short = (
                    run_data.run_name[:10] + "..."
                    if len(run_data.run_name) > 10
                    else run_data.run_name
                )

                # 任务开始：显示初始进度 0%
                self._update_account_status_js(
                    acc,
                    status_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short}",
                    progress_pct=0,
                    progress_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short} · 0%",
                    progress_extra="",
                )

                acc.log(f"开始执行任务: {run_data.run_name}")

                # 获取详情前检查停止
                if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已中止")
                    break

                details_resp = acc.api_client.get_run_details(
                    run_data.errand_id, acc.user_data.id, run_data.errand_schedule
                )
                if not (details_resp and details_resp.get("success")):
                    acc.log(f"获取任务详情失败，跳过。")
                    continue

                details = details_resp.get("data", {}).get("errandDetail", {})
                waypoints = [
                    (float(p["lon"]), float(p["lat"]))
                    for p in details.get("geoCoorList", [])
                    if p.get("lon") is not None
                ]
                if not waypoints:
                    # 任务25: 记录无打卡点日志，便于追溯
                    task_name = details.get("title", run_data.run_name)
                    acc.log(f"跳过: 任务 '{task_name}' 无打卡点")
                    continue
                run_data.target_points = waypoints

                # 使用 chrome_pool 进行路径规划（Web 模式）
                api_path_coords = None

                global chrome_pool
                if not chrome_pool:
                    acc.log("错误: Chrome浏览器池不可用，无法进行路径规划。")
                    continue

                try:
                    acc.log("正在调用高德地图API进行路径规划...")

                    # 获取会话ID（用于chrome_pool）
                    session_id = getattr(self, "_web_session_id", None)
                    if not session_id:
                        acc.log(
                            "错误: 无法获取会话ID（_web_session_id 属性不存在），跳过任务。"
                        )
                        logging.error(
                            f"多账号模式缺少 _web_session_id 属性，账号: {acc.username}"
                        )
                        continue

                    # 获取高德地图API密钥（优化：使用全局缓存）
                    if not hasattr(self, "_amap_key_cached"):
                        config = configparser.ConfigParser()
                        config.read(CONFIG_FILE, encoding="utf-8")
                        self._amap_key_cached = config.get(
                            "Map", "amap_js_key", fallback=""
                        )
                        logging.info(f"已加载高德地图API密钥配置（缓存至实例）")

                    amap_key = self._amap_key_cached
                    if not amap_key:
                        acc.log("错误: 未配置高德地图API密钥，请在config.ini中设置。")
                        continue

                    # 获取Chrome上下文
                    ctx = chrome_pool.get_context(session_id)
                    page = ctx["page"]

                    # 检查是否已加载AMap SDK（优化：避免重复加载）
                    amap_loaded = False
                    try:
                        amap_loaded = page.evaluate("typeof AMapLoader !== 'undefined'")
                    except Exception as e:
                        # 可能是页面刚创建，AMapLoader 还未定义，这是正常情况
                        logging.debug(f"检查AMap SDK时出错（可能尚未加载）: {e}")

                    if not amap_loaded:
                        # 加载高德地图SDK
                        page.goto("about:blank")
                        page.set_content(
                            """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="utf-8">
                            <script type="text/javascript" src="https://webapi.amap.com/loader.js"></script>
                        </head>
                        <body></body>
                        </html>
                        """
                        )

                        # 等待AMap加载（优化：添加明确的错误处理）
                        try:
                            page.wait_for_function(
                                "typeof AMapLoader !== 'undefined'", timeout=10000
                            )
                        except Exception as e:
                            acc.log(f"错误: 加载高德地图SDK超时或失败: {str(e)}")
                            continue

                    # 执行路径规划JavaScript
                    path_coords = chrome_pool.execute_js(
                        session_id,
                        """
                        (async (arg) => {
                            const waypointsPy = arg[0];
                            const apiKey = arg[1];
                            const pythonParams = arg[2];

                            async function planPath(waypointsPy, apiKey, pythonParams) {
                                if (typeof AMapLoader === 'undefined') {
                                    return {error: 'AMapLoader not loaded'};
                                }

                                try {
                                    await AMapLoader.load({
                                        "key": apiKey,
                                        "version": "2.0",
                                        "plugins": ["AMap.Walking"]
                                    });
                                } catch (e) {
                                    return {error: 'AMapLoader.load failed: ' + (e ? e.message : 'Unknown error')};
                                }

                                if (typeof AMap.Walking === 'undefined') {
                                    return {error: 'AMap.Walking plugin failed to load'};
                                }

                                const useFallback = pythonParams.api_fallback_line ?? false;
                                const maxRetries = pythonParams.api_retries ?? 2;
                                const retryDelayMs = (pythonParams.api_retry_delay_s ?? 0.5) * 1000;
                                const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

                                const searchSegment = (start, end, walkingInstance) => new Promise((resolve) => {
                                    walkingInstance.search(start, end, (status, result) => {
                                        if (status === 'complete' && result.routes?.length > 0) {
                                            const p = []; 
                                            result.routes[0].steps.forEach(s => s.path.forEach(pt => p.push({ lng: pt.lng, lat: pt.lat })));
                                            resolve({ path: p });
                                        } else {
                                            let errorInfo = 'Unknown Error';
                                            if (status === 'error') {
                                                errorInfo = result?.info || status;
                                            } else if (status === 'no_data') {
                                                errorInfo = 'No path found (no_data)';
                                            } else {
                                                errorInfo = status;
                                            }
                                            resolve({ error: 'Path planning failed: ' + errorInfo });
                                        }
                                    });
                                });

                                const all_path = [];
                                const waypoints = waypointsPy.map(p => new AMap.LngLat(p[0], p[1]));
                                const walking = new AMap.Walking({ map: null, panel: "", hideMarkers: true });

                                if (waypoints.length < 2) {
                                    return {error: 'Waypoints must be at least 2.'};
                                }

                                for (let i = 0; i < waypoints.length - 1; i++) {
                                    const realStart = waypoints[i];
                                    const realEnd = waypoints[i + 1];
                                    
                                    let attempts = 0;
                                    let segmentResult = null;
                                    let segmentPath = null;

                                    while (attempts <= maxRetries) {
                                        if (attempts > 0) {
                                            await sleep(retryDelayMs);
                                        }
                                        
                                        segmentResult = await searchSegment(realStart, realEnd, walking);
                                        
                                        if (segmentResult.path) {
                                            segmentPath = segmentResult.path;
                                            break;
                                        }
                                        
                                        attempts++;
                                    }

                                    if (segmentPath) {
                                        const areCoordsEqual = (c1, c2) => Math.abs(c1.lng - c2.lng) < 1e-6 && Math.abs(c1.lat - c2.lat) < 1e-6;
                                        if (i > 0) {
                                            all_path.push(...segmentPath.slice(1));
                                        } else {
                                            all_path.push(...segmentPath);
                                        }
                                        if (i === waypoints.length - 2) { 
                                            if (segmentPath.length > 0 && !areCoordsEqual(segmentPath[segmentPath.length - 1], { lng: realEnd.lng, lat: realEnd.lat })) {
                                                all_path.push({ lng: realEnd.lng, lat: realEnd.lat });
                                            }
                                        }
                                    } else {
                                        if (useFallback) {
                                            const lastPoint = all_path.length > 0 ? all_path[all_path.length - 1] : null;
                                            if (!lastPoint || (Math.abs(lastPoint.lng - realStart.lng) > 1e-6 || Math.abs(lastPoint.lat - realStart.lat) > 1e-6)) {
                                                all_path.push({ lng: realStart.lng, lat: realStart.lat });
                                            }
                                            all_path.push({ lng: realEnd.lng, lat: realEnd.lat });
                                        } else {
                                            return {error: `Segment ${i+1} failed after ${maxRetries+1} attempts: ${segmentResult.error}`};
                                        }
                                    }
                                }
                                
                                return {path: all_path};
                            }

                            return await planPath(waypointsPy, apiKey, pythonParams);
                        })
                        """,
                        waypoints,
                        amap_key,
                        acc.params,
                    )

                    if path_coords and "path" in path_coords:
                        api_path_coords = path_coords["path"]
                        acc.log(f"路径规划成功，共 {len(api_path_coords)} 个点。")
                    else:
                        error_msg = (
                            path_coords.get("error", "未知错误")
                            if path_coords
                            else "无响应"
                        )
                        acc.log(f"路径规划失败: {error_msg}")
                        continue

                except Exception as e:
                    logging.error(f"Chrome浏览器池路径规划失败: {e}", exc_info=True)
                    acc.log(f"路径规划异常: {str(e)}")
                    continue

                if not api_path_coords:
                    acc.log("路径规划失败，跳过任务。")
                    continue

                # [Debug] 输出规划点数
                logging.debug(
                    f"[{acc.username}] 路径规划返回点数: {len(api_path_coords)}"
                )

                min_t_m, max_t_m, min_d_m = (
                    acc.params.get("min_time_m", 20),
                    acc.params.get("max_time_m", 30),
                    acc.params.get("min_dist_m", 2000),
                )

                final_path_dedup = []
                last_coord = None
                for p in api_path_coords:
                    # 修正BUG：同时兼容 'lng' 和 'lon' 两种经度键名
                    longitude = p.get("lng", p.get("lon"))
                    if longitude is None:
                        continue  # 如果经度不存在，则跳过这个点
                    coord = (longitude, p["lat"])
                    if coord != last_coord:
                        final_path_dedup.append(coord)
                        last_coord = coord

                if not final_path_dedup:
                    acc.log("路径处理失败：无有效坐标点。")
                    continue

                # [Debug] 输出去重后点数
                logging.debug(
                    f"[{acc.username}] 路径去重后点数: {len(final_path_dedup)}"
                )

                target_time_s = random.uniform(min_t_m * 60, max_t_m * 60)
                target_dist_m = random.uniform(min_d_m, min_d_m * 1.15)
                cumulative = [0.0]
                for idx_c in range(len(final_path_dedup) - 1):
                    cumulative.append(
                        cumulative[-1]
                        + self._calculate_distance_m(
                            final_path_dedup[idx_c][0],
                            final_path_dedup[idx_c][1],
                            final_path_dedup[idx_c + 1][0],
                            final_path_dedup[idx_c + 1][1],
                        )
                    )

                final_geo_path = self._get_path_for_distance(
                    final_path_dedup, cumulative, target_dist_m
                )
                final_cumulative = [0.0]
                for idx_c in range(len(final_geo_path) - 1):
                    final_cumulative.append(
                        final_cumulative[-1]
                        + self._calculate_distance_m(
                            final_geo_path[idx_c][0],
                            final_geo_path[idx_c][1],
                            final_geo_path[idx_c + 1][0],
                            final_geo_path[idx_c + 1][1],
                        )
                    )

                actual_total_dist = final_cumulative[-1] if final_cumulative else 0.0
                if actual_total_dist == 0:
                    acc.log("路径计算距离为0，跳过。")
                    continue

                # [Debug] 输出计算结果
                acc.log(
                    f"路径计算完成: 目标距离 {actual_total_dist:.1f}m, 目标耗时 {target_time_s:.1f}s"
                )

                avg_speed = actual_total_dist / target_time_s
                new_run_coords = []
                start = final_geo_path[0]
                new_run_coords.append(
                    self._gps_random_offset(start[0], start[1], acc.params) + (0,)
                )
                t_elapsed, d_covered = 0.0, 0.0

                while t_elapsed < target_time_s:
                    interval = min(
                        random.uniform(
                            acc.params["interval_ms"] * 0.9,
                            acc.params["interval_ms"] * 1.1,
                        )
                        / 1000.0,
                        target_time_s - t_elapsed,
                    )
                    if interval <= 0.1:
                        break

                    d_covered = min(
                        d_covered
                        + random.uniform(avg_speed * 0.9, avg_speed * 1.1) * interval,
                        actual_total_dist,
                    )
                    lon, lat = self._get_point_at_distance(
                        final_geo_path, final_cumulative, d_covered
                    )
                    lon_o, lat_o = self._gps_random_offset(lon, lat, acc.params)
                    new_run_coords.append((lon_o, lat_o, int(interval * 1000)))
                    t_elapsed += interval
                    if d_covered >= actual_total_dist:
                        break

                run_data.run_coords = new_run_coords
                run_data.total_run_distance_m = d_covered
                run_data.total_run_time_s = t_elapsed

                # [Debug] 输出轨迹生成结果
                acc.log(f"已生成模拟轨迹: {len(new_run_coords)} 个GPS点")

                tasks_executed_count += 1  # 任务已通过所有检查，准备执行

                run_data.trid = f"{acc.user_data.student_id}{int(time.time() * 1000)}"
                start_time_ms = str(int(time.time() * 1000))
                submission_successful = True
                # 总点数用于进度计算（更高频率的进度更新）
                total_points = max(1, len(run_data.run_coords))

                # [Debug] 检查点数是否为0
                if total_points <= 1:
                    acc.log("警告: 生成的轨迹点数过少，无法执行任务。")
                    continue

                for chunk_idx in range(0, len(run_data.run_coords), 40):
                    # [Debug] 记录执行进度
                    logging.debug(
                        f"[{acc.username}] 执行进度: {chunk_idx}/{len(run_data.run_coords)}"
                    )
                    if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                        submission_successful = False
                        break

                    chunk = run_data.run_coords[chunk_idx : chunk_idx + 40]
                    processed_points = chunk_idx  # 从当前分块起始已处理的点数
                    for lon, lat, dur_ms in chunk:
                        if self.multi_run_stop_flag.is_set() or acc.stop_event.is_set():
                            submission_successful = False
                            break

                        # 位置与前端地图更新（使用 SocketIO）
                        session_id = getattr(self, "_web_session_id", None)

                        # 【新增】将当前坐标保存到对象实例，供前端轮询拉取
                        acc.current_position = {"lon": lon, "lat": lat}

                        if session_id and socketio:
                            try:
                                # (保持原有的emit逻辑以兼容可能的WebSocket连接)
                                socketio.emit(
                                    "multi_position_update",
                                    {
                                        "username": acc.username,
                                        "lon": lon,
                                        "lat": lat,
                                        "name": acc.user_data.name,
                                    },
                                    room=session_id,
                                )
                                # [修复] 使用 time.sleep 替代 socketio.sleep，避免 greenlet.error
                                time.sleep(0.001)  # 强制交出控制权，确保消息立即发送
                            except Exception as e:
                                logging.debug(
                                    f"Failed to emit multi_position_update: {e}"
                                )

                        # 等待当前点的“上报时长”（保持原有逻辑）
                        if acc.stop_event.wait(timeout=dur_ms / 1000.0):
                            submission_successful = False
                            break

                        # 每个点完成后实时推进进度（仅更新进度相关字段，避免频繁改写状态文本）
                        processed_points += 1
                        try:
                            pct = int(processed_points * 100 / total_points)
                            self._update_account_status_js(
                                acc,
                                progress_pct=pct,
                                progress_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short} · {pct}%",
                                progress_extra=f"{processed_points}/{total_points} 点",
                            )
                        except Exception:
                            pass

                    if not submission_successful:
                        break

                    # # 按已处理点数推送进度百分比
                    # try:
                    #     total_points = max(1, len(run_data.run_coords))
                    #     processed_points = min(total_points, chunk_idx + len(chunk))
                    #     pct = int(processed_points * 100 / total_points)
                    #     self._update_account_status_js(
                    #         acc,
                    #         status_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short}",
                    #         progress_pct=pct,
                    #         progress_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short} · {pct}%",
                    #         progress_extra=f"{processed_points}/{total_points} 点"
                    #     )
                    # except Exception:
                    #     pass

                    is_final_chunk = chunk_idx + 40 >= len(run_data.run_coords)
                    if not self._submit_chunk(
                        run_data,
                        chunk,
                        start_time_ms,
                        is_final_chunk,
                        chunk_idx,
                        acc.api_client,
                        acc.user_data,
                    ):
                        submission_successful = False
                        break

                if submission_successful:
                    acc.log(f"任务 {run_data.run_name} 数据提交完毕，等待服务器确认...")
                    time.sleep(3)
                    self._finalize_run(run_data, -1, acc.api_client)
                    run_data.status = 1
                    self._multi_fetch_and_summarize_tasks(acc)
                    self._update_account_status_js(acc, summary=acc.summary)
                    acc.log(f"任务 {run_data.run_name} 执行流程完成。")
                    # 任务完成后置为 100%
                    self._update_account_status_js(
                        acc,
                        status_text="任务已完成",
                        progress_pct=100,
                        progress_text=f"运行 {i+1}/{len(tasks_to_run)}: {task_name_short} · 100%",
                        progress_extra="",
                    )
                else:
                    acc.log(f"任务 {run_data.run_name} 执行被中止。")
                    # 中止时维持当前进度文本（不强制 100）
                    self._update_account_status_js(acc, status_text="已中止")

                if i < len(tasks_to_run) - 1:
                    wait_time = random.uniform(
                        acc.params["task_gap_min_s"], acc.params["task_gap_max_s"]
                    )
                    should_break_worker = False
                    end_time = time.time() + wait_time
                    while time.time() < end_time:
                        if acc.stop_event.is_set() or self.multi_run_stop_flag.is_set():
                            should_break_worker = True
                            break
                        remaining = end_time - time.time()
                        self._update_account_status_js(
                            acc, status_text=f"等待 {remaining:.0f}s"
                        )
                        time.sleep(1)
                    if should_break_worker:
                        self._update_account_status_js(acc, status_text="已中止")
                        break

            if not acc.stop_event.is_set():
                if tasks_executed_count == 0:
                    # 如果没有执行任何任务（全部跳过）
                    self._update_account_status_js(acc, status_text="无任务可执行")
                else:
                    # 至少执行了一个任务
                    self._update_account_status_js(acc, status_text="全部完成")

        except Exception:
            logging.error(
                f"Error in worker for {acc.username}: {traceback.format_exc()}"
            )
            self._update_account_status_js(acc, status_text="执行出错")
        finally:
            try:
                acc.worker_thread = None
                if acc.stop_event.is_set():
                    self._update_account_status_js(acc, status_text="已停止")
                else:
                    # 保留错误/中止/网络错误等状态，不回落为“待命”
                    if not self._should_preserve_status(
                        acc.status_text, new_status="待命"
                    ):
                        # 仅当当前状态是临时运行态或空状态时才回落为“待命”
                        if (
                            acc.status_text
                            in (
                                "登录中...",
                                "排队登录...",
                                "已启动",
                                "分析任务",
                                "运行",
                                "等待",
                            )
                            or not acc.status_text
                        ):
                            self._update_account_status_js(acc, status_text="待命")

            except Exception:
                logging.debug(
                    "Finalize worker status update failed (non-fatal).", exc_info=True
                )
            finally:
                self._update_multi_global_buttons()

    def _get_device_sign_code(self, username):
        """生成或获取设备标识码 (signCode)"""
        # 方案1：使用固定的 UUID (每次运行可能不同，但同一用户会话内可能一致)
        # return str(uuid.uuid4())
        # 方案2：尝试更稳定的标识 (可能需要额外库或权限)
        # try:
        #     # mac 地址 (可能需要 pip install getmac)
        #     import getmac
        #     mac = getmac.get_mac_address()
        #     if mac: return mac
        # except ImportError:
        #     pass
        # 方案3：基于用户名和固定字符串生成 UUID (同一用户始终一致)
        # return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"zslf_runner_{username}"))
        # 方案4：简单模拟 trid 格式 (不保证唯一性)
        # return f"{username}_dev_{int(time.time() * 100)}"
        # 方案5：直接使用随机 UUID
        return str(uuid.uuid4())

    def _fetch_server_attendance_radius_if_needed(
        self, client: ApiClient, acc: AccountSession | None = None
    ):
        """
        (辅助函数) 检查并获取服务器签到半径。
        - 单账号模式: 缓存到 self.server_attendance_radius_m
        - 多账号模式: 缓存到 acc.server_attendance_radius_m
        """
        log_func = acc.log if acc else self.log
        cache_duration_s = 3600  # 缓存1小时

        # 确定使用哪个缓存
        if acc:
            last_fetch_time = acc.last_radius_fetch_time
            current_radius = acc.server_attendance_radius_m
        else:
            last_fetch_time = self.last_radius_fetch_time
            current_radius = self.server_attendance_radius_m

        # 检查缓存是否有效
        if time.time() - last_fetch_time < cache_duration_s and current_radius > 0:
            logging.debug(f"使用缓存的服务器签到半径值: {current_radius}米")
            return current_radius

        log_func("正在获取服务器签到半径...")
        new_radius = 0.0
        try:
            resp = client.get_attendance_radius()
            if resp and resp.get("success"):
                info_list = resp.get("data", {}).get("info", [])
                if info_list and isinstance(info_list, list) and len(info_list) > 0:
                    radius_str = info_list[0].get("code")
                    new_radius = float(radius_str)
                    if new_radius <= 0:
                        log_func("服务器返回半径为0，启用精确签到。")
                        new_radius = 0.0
                    else:
                        log_func(f"服务器签到半径更新为: {new_radius} 米")
                else:
                    log_func("服务器未返回半径信息，默认为精确签到。")
            else:
                log_func("获取半径API失败，默认为精确签到。")
        except Exception as e:
            log_func(f"获取半径时出错: {e}，默认为精确签到。")
            logging.error(f"Failed to fetch attendance radius: {e}", exc_info=True)

        # 更新缓存
        if acc:
            acc.server_attendance_radius_m = new_radius
            acc.last_radius_fetch_time = time.time()
        else:
            self.server_attendance_radius_m = new_radius
            self.last_radius_fetch_time = time.time()

        return new_radius

    def trigger_attendance(
        self,
        roll_call_id: str,
        target_coords: tuple[float, float],
        location_choice: str = "random",
        specific_coords: tuple[float, float] | None = None,
        is_makeup: bool = False,
        acc: AccountSession | None = None,
    ):
        """
        (已重构) 触发签到流程。
        - acc: (可选) 在多账号模式下传入 AccountSession。

        Args:
            roll_call_id: 签到活动的 ID.
            target_coords: 签到目标的坐标 (经度, 纬度).
            location_choice: 'random' (在目标点范围内随机) 或 'specific' (使用 specific_coords).
            specific_coords: 当 location_choice 为 'specific' 时使用的具体坐标 (经度, 纬度).
            is_makeup: 是否为补签。
            acc: (可选) 在多账号模式下传入 AccountSession。
        """

        # 确定上下文 (单账号 vs 多账号)
        if acc:
            client = acc.api_client
            log_func = acc.log
            user = acc.user_data
            params = acc.params
        elif not self.is_multi_account_mode:
            client = self.api_client
            log_func = self.log
            user = self.user_data
            params = self.params
        else:
            self.log("trigger_attendance 在多账号模式下被错误调用（未传入acc）")
            return {"success": False, "message": "多账号模式内部错误"}

        if not user.id:
            log_func("用户未登录，无法签到。")
            return {"success": False, "message": "用户未登录"}

        log_func(f"正在处理签到: {roll_call_id}")

        # 1. 获取服务器最大半径 (使用新函数，带缓存)
        server_radius_m = self._fetch_server_attendance_radius_if_needed(client, acc)
        is_precise_checkin = server_radius_m <= 0

        # 2. 检查当前签到状态 (使用你的新逻辑)
        try:
            info_resp = client.get_roll_call_info(roll_call_id, user.id)
            if info_resp and info_resp.get("success"):
                data = info_resp.get("data", {})
                roll_call_info = data.get("rollCallInfo", {})

                status = roll_call_info.get("status")  # 关键字段1: -1=过期, 0=进行中
                finished = data.get("attendFinish")  # 关键字段2: 1=已签, 0=未签

                # 逻辑: 只要 status == -1，就是已过期且未签到
            if status == -1:
                if not is_makeup:
                    # 如果不是补签，则按原逻辑阻止
                    log_func("此签到任务已过期（status=-1）。")
                    return {"success": False, "message": "任务已过期"}
                else:
                    # 如果是补签，则记录日志并继续
                    log_func(f"任务 {roll_call_id} 已过期，正在尝试[补签]...")

                # 逻辑: 只有 status != -1 且 finished == 1 才算完成
                if status != -1 and (finished == 1 or finished is True):
                    log_func("你已经签到过了 (status!=-1 and attendFinish=1)。")
                    return {"success": True, "message": "已签到"}

                # (其他情况，如 status=0 and finished=0，都视为 "待签到"，流程继续)
                log_func("任务状态：待签到。")

            else:
                log_func("获取签到信息失败，将继续尝试签到...")
        except Exception as e:
            log_func(f"检查签到状态时出错: {e}，将继续尝试...")
            logging.error(f"Error checking roll call status: {e}", exc_info=True)

        # 3. 确定签到坐标
        final_lon, final_lat = 0.0, 0.0
        target_lon, target_lat = target_coords

        if location_choice == "specific" and specific_coords:
            final_lon, final_lat = specific_coords
            log_func(f"使用指定坐标签到: ({final_lon:.6f}, {final_lat:.6f})")

        elif location_choice == "random":
            # 默认为精确签到
            radius_for_random = 0.0

            if not is_precise_checkin:
                # 仅在服务器允许范围签到时，才计算随机半径
                user_radius_m = params.get("attendance_user_radius_m", 40)
                # 随机半径不能超过服务器的半径
                radius_for_random = max(0.0, min(user_radius_m, server_radius_m))

            if radius_for_random <= 0:
                # 精确签到
                final_lon, final_lat = target_lon, target_lat
                log_func(
                    f"精确签到模式：使用目标点坐标签到: ({final_lon:.6f}, {final_lat:.6f})"
                )
            else:
                # 范围随机签到
                angle = random.uniform(0, 2 * math.pi)
                # 在 0 到 1 倍的 *有效半径* 内随机
                radius_ratio = random.uniform(0, 1.0)
                radius_m = radius_for_random * radius_ratio

                offset_lon = (radius_m * math.cos(angle)) / 102834.74
                offset_lat = (radius_m * math.sin(angle)) / 111712.69

                final_lon = target_lon + offset_lon
                final_lat = target_lat + offset_lat
                log_func(
                    f"在 {radius_for_random:.1f} 米范围内随机生成坐标签到: ({final_lon:.6f}, {final_lat:.6f})"
                )

        else:
            log_func("无效的位置选择，无法签到。")
            return {"success": False, "message": "无效的位置选择"}

        # 4. 计算实际距离
        actual_distance = self._calculate_distance_m(
            final_lon, final_lat, target_lon, target_lat
        )
        log_func(f"签到点距离目标点 {actual_distance:.2f} 米。")

        # 5. 获取设备标识码
        sign_code = self._get_device_sign_code(user.username)

        # 6. 准备提交负载
        if is_makeup:
            # 补签负载
            payload = {
                "rollCallId": roll_call_id,
                "userId": user.id,
                "coordinate": f"{final_lon},{final_lat}",
                "distance": int(actual_distance),  # 转为整数
                "status": 2,  # 1=正常, 2=补签 (如果补签状态码不是2，请修改这里)
                "signCode": sign_code,
                "reason": "补签",  # 补签时填写原因
            }
            log_func("使用[补签]负载提交...")
        else:
            # 正常签到负载
            payload = {
                "rollCallId": roll_call_id,
                "userId": user.id,
                "coordinate": f"{final_lon},{final_lat}",
                "distance": int(actual_distance),  # 转为整数
                "status": 1,  # 1 表示成功签到
                "signCode": sign_code,
                "reason": "",  # 签到时为空
            }
            log_func("使用[正常签到]负载提交...")

        # 7. 提交签到
        try:
            log_func("正在提交签到...")
            submit_resp = client.submit_attendance(payload)
            if submit_resp and submit_resp.get("success"):
                log_func("签到成功！")
                logging.info(f"Attendance submitted successfully for {roll_call_id}")
                return {"success": True, "message": "签到成功"}
            else:
                msg = (
                    submit_resp.get("message", "未知错误")
                    if submit_resp
                    else "网络错误"
                )
                log_func(f"签到失败: {msg}")
                logging.warning(
                    f"Attendance submission failed for {roll_call_id}: {msg}"
                )
                return {"success": False, "message": f"签到失败: {msg}"}
        except Exception as e:
            log_func(f"提交签到时出错: {e}")
            logging.error(f"提交签到请求时发生错误，异常信息: {e}", exc_info=True)
            return {"success": False, "message": f"提交签到时出错: {e}"}

    # --- 获取通知功能 ---

    def get_notifications(
        self,
        is_auto_refresh: bool = False,
        request_limit: int = None,
        request_offset: int = 0,
    ):
        """
        (已重构) 获取未读通知数量和通知列表。
        - 附加基于新逻辑的签到状态。
        - (自动签到逻辑已移至 _check_and_trigger_auto_attendance)
        - 支持分段加载：可指定 request_limit 和 request_offset 参数

        Args:
            is_auto_refresh: 是否为自动刷新调用
            request_limit: 请求的最大通知数量（None表示获取全部）
            request_offset: 请求的起始偏移量（默认为0）

        Returns:
            包含 success、unreadCount、notices、hasMore、totalCount 的字典
        """
        logging.info(
            f"API调用: get_notifications - 获取用户通知消息列表 (limit={request_limit}, offset={request_offset})"
        )
        if not self.user_data.id or self.is_multi_account_mode:
            return {"success": False, "message": "仅单账号登录模式可用"}

        # 【修复 Requirement 13】离线模式下直接返回空白通知列表，不读取缓存
        if self.is_offline_mode:
            return {"success": True, "data": {"unreadNumber": 0, "notices": []}}

        try:
            # 1. 获取未读数量
            count_resp = self.api_client.get_unread_notice_count()
            unread_count = 0
            if count_resp and count_resp.get("success"):
                unread_count = count_resp.get("data", {}).get("unreadNumber", 0)

            # 2. 【重构】获取通知 - 支持分段加载
            all_notices = []
            offset = request_offset
            limit = 10  # 每次向服务器请求的批次大小
            total_fetched = 0

            # 如果指定了 request_limit，则只获取指定数量的通知
            if request_limit is not None:
                # 计算需要获取多少批次
                while total_fetched < request_limit:
                    # 计算本次请求应该获取多少条
                    batch_size = min(limit, request_limit - total_fetched)

                    list_resp = self.api_client.get_notice_list(
                        offset=offset, limit=batch_size, type_id=0
                    )
                    if list_resp and list_resp.get("success"):
                        current_notices = list_resp.get("data", {}).get(
                            "noticeList", []
                        )
                        if not current_notices:
                            # 没有更多通知了，退出循环
                            break
                        all_notices.extend(current_notices)
                        total_fetched += len(current_notices)
                        offset += len(current_notices)
                        # 如果返回的通知数小于请求的批次大小，说明没有更多数据了
                        if len(current_notices) < batch_size:
                            break
                    else:
                        self.log("获取通知列表时失败。")
                        break
            else:
                # 原有逻辑：获取所有通知
                while True:
                    list_resp = self.api_client.get_notice_list(
                        offset=offset, limit=limit, type_id=0
                    )
                    if list_resp and list_resp.get("success"):
                        current_notices = list_resp.get("data", {}).get(
                            "noticeList", []
                        )
                        if not current_notices:
                            # 没有更多通知了，退出循环
                            break
                        all_notices.extend(current_notices)
                        offset += limit
                        # 如果返回的通知数小于请求的 limit，说明是最后一页
                        if len(current_notices) < limit:
                            break
                    else:
                        self.log("获取通知列表时失败。")
                        # 发生错误时中断，避免无限循环
                        break

            notices = all_notices

            # 3. 【重构】遍历通知，仅为签到任务附加状态
            if notices:
                logging.debug(f"正在为 {len(notices)} 条通知附加签到状态...")
                for notice in notices:
                    try:
                        is_attendance = notice.get(
                            "image"
                        ) == "attendance" or "签到" in notice.get("title", "")
                        if is_attendance and notice.get("id"):
                            roll_call_id = notice["id"]

                            info_resp = self.api_client.get_roll_call_info(
                                roll_call_id, self.user_data.id
                            )

                            status = -2  # 默认为未知
                            finished = 0

                            if info_resp and info_resp.get("success"):
                                data = info_resp.get("data", {})
                                roll_call_info = data.get("rollCallInfo", {})
                                status = roll_call_info.get(
                                    "status"
                                )  # -1=过期, 0=进行中
                                finished = data.get("attendFinish")  # 1=已签, 0=未签

                            # 附加新字段到 notice 对象
                            notice["attendance_finished"] = finished
                            notice["attendance_status_code"] = status

                            if status == -1:
                                notice["attendance_code"] = -1  # 已过期
                            elif status != -1 and (finished == 1 or finished is True):
                                notice["attendance_code"] = 1  # 已签到
                            else:
                                notice["attendance_code"] = 0  # 待签到

                    except Exception as e:
                        logging.warning(
                            f"附加签到状态失败 (ID: {notice.get('id')}): {e}"
                        )

            # 判断是否还有更多通知
            # 如果请求了 request_limit 条，且实际获取的数量等于 request_limit，
            # 说明可能还有更多数据（需要再次请求确认）
            has_more = False
            if request_limit is not None and len(notices) >= request_limit:
                # 尝试peek下一条，看是否还有数据
                peek_resp = self.api_client.get_notice_list(
                    offset=offset, limit=1, type_id=0
                )
                if peek_resp and peek_resp.get("success"):
                    peek_notices = peek_resp.get("data", {}).get("noticeList", [])
                    has_more = len(peek_notices) > 0

            if not is_auto_refresh:
                self.log(
                    f"获取到 {unread_count} 条未读通知，本次返回 {len(notices)} 条通知。"
                )

            # 【新增】如果这是首次加载（offset=0）且获取了5条或更多通知，更新缓存
            if request_offset == 0 and len(notices) >= 5:
                self.cached_notifications = {
                    "notices": notices[:5],  # 只缓存前5条
                    "unreadCount": unread_count,
                    "cached_at": time.time(),
                }
                logging.debug(
                    f"已更新缓存通知：{len(self.cached_notifications['notices'])} 条"
                )

            return {
                "success": True,
                "unreadCount": unread_count,
                "notices": notices,
                "hasMore": has_more,
                "totalCount": offset,  # 当前已扫描到的总数
                "returnedCount": len(notices),  # 本次返回的数量
            }
        except Exception as e:
            self.log(f"获取通知失败: {e}")
            logging.error(f"get_notifications failed: {e}", exc_info=True)
            return {"success": False, "message": str(e)}

    def get_cached_notifications(self):
        """获取缓存的通知（用于快速显示）"""
        logging.info("API调用: get_cached_notifications - 获取缓存的通知")

        if hasattr(self, "cached_notifications") and self.cached_notifications:
            # 检查缓存是否过期（超过5分钟）
            cached_at = self.cached_notifications.get("cached_at", 0)
            age_seconds = time.time() - cached_at

            if age_seconds < 300:  # 5分钟内的缓存有效
                logging.debug(f"返回缓存的通知，缓存年龄: {age_seconds:.1f}秒")
                return {
                    "success": True,
                    "cached": True,
                    "unreadCount": self.cached_notifications.get("unreadCount", 0),
                    "notices": self.cached_notifications.get("notices", []),
                    "cached_at": cached_at,
                }
            else:
                logging.debug(f"缓存已过期（{age_seconds:.1f}秒），返回空")

        return {"success": True, "cached": False, "notices": []}

    def mark_notification_read(self, notice_id):
        """(单账号) 将指定ID的通知设为已读"""
        logging.info(
            f"API调用: mark_notification_read - 标记通知为已读，通知ID: {notice_id}"
        )
        if not self.user_data.id or self.is_multi_account_mode:
            return {"success": False, "message": "仅单账号登录模式可用"}

        resp = self.api_client.mark_notice_as_read(notice_id)
        if resp and resp.get("success"):
            return {"success": True}
        else:
            return {"success": False, "message": resp.get("message", "标记已读失败")}

    def _auto_refresh_worker(self):
        """(单账号) 后台自动刷新通知和签到的线程 (已修复)"""
        while not self.stop_auto_refresh.is_set():
            try:
                # --- 修复：从循环顶部移除 is_enabled 检查 ---

                # 1. 检查是否满足运行条件（已登录 且 处于单账号模式）
                if not self.user_data.id or self.is_multi_account_mode:
                    # 如果未登录或在多账号模式，则休眠
                    # (使用 wait 替代 sleep 以便快速响应停止)
                    if self.stop_auto_refresh.wait(timeout=5.0):
                        break  # 收到停止信号
                    continue  # 回去重新检查登录状态

                # --- 修复：移除 "Bug 2" 相关的300秒长休眠逻辑 ---
                # if not is_enabled: ... continue ...

                # 2. 线程应始终按 'refresh_interval_s' 频率运行

                # 读取刷新间隔，并设置合理的默认值和最小值
                refresh_interval_s = self.params.get(
                    "auto_attendance_refresh_s", 30
                )  # 默认30秒
                # 确保间隔不小于一个最小值，例如15秒，防止过高频率
                refresh_interval_s = max(15, refresh_interval_s)

                # 再次检查登录状态
                if self.is_multi_account_mode or not self.user_data.id:
                    continue

                # --- 关键修复：在执行操作前，才读取最新的 is_enabled 状态 ---
                is_enabled = self.params.get("auto_attendance_enabled", False)

                # 3. 只有在启用时才执行自动签到和通知刷新
                if is_enabled:
                    self.log("(后台) 自动签到已启用，正在检查...")
                    self._check_and_trigger_auto_attendance(self)

                    # 4. 获取通知并推送到UI (仅在启用自动签到时执行)
                    self.log("正在自动刷新通知 (后台)...")
                    result = self.get_notifications(
                        is_auto_refresh=True
                    )  # (修复：传入True以避免日志重复)

                    # [BUG 修复]：替换 self.window 为 socketio.emit
                    if result.get("success"):
                        # 修复：使用 SocketIO 向特定会话推送更新，而不是 self.window
                        session_id = getattr(self, "_web_session_id", None)
                        # 确保 socketio 变量在全局可用 (它在 start_web_server 中定义)
                        if session_id and "socketio" in globals():
                            try:
                                # 发送一个自定义事件，前端JS需要监听这个事件
                                globals()["socketio"].emit(
                                    "onNotificationsUpdated", result, room=session_id
                                )
                                logging.debug(
                                    f"[_auto_refresh_worker] 已向会话 {session_id[:8]} 推送通知更新"
                                )
                            except Exception as e:
                                logging.error(
                                    f"[_auto_refresh_worker] SocketIO推送通知失败: {e}",
                                    exc_info=True,
                                )
                        elif not session_id:
                            logging.warning(
                                f"[_auto_refresh_worker] 无法推送通知：未找到 _web_session_id"
                            )
                        else:
                            logging.warning(
                                f"[_auto_refresh_worker] 无法推送通知：socketio 实例不可用"
                            )
                else:
                    # 如果未启用，则不执行任何操作也不记录日志，保持安静
                    pass

                # 问题15修复：刷新完成后等待，减轻服务器负担
                self.log(f"自动刷新完成，等待 {refresh_interval_s} 秒后再次刷新...")
                # 使用 wait() 替代 time.sleep()，以便在等待期间可以被 'stop_auto_refresh.set()' 立即中断
                if self.stop_auto_refresh.wait(timeout=refresh_interval_s):
                    break  # 如果在等待时收到停止信号，则退出循环

            except Exception as e:
                self.log(f"自动刷新线程出错: {e}")
                logging.error(f"Auto-refresh worker error: {e}", exc_info=True)
                # 修复：使用 wait() 替换 time.sleep() 以便能被立即停止
                if self.stop_auto_refresh.wait(timeout=60):
                    break  # 如果在等待时收到停止信号，则退出循环

        logging.info("Auto-refresh worker stopped.")

    def _check_and_trigger_auto_attendance(self, context: "Api | AccountSession"):
        """
        (辅助函数) 检查并执行单个上下文(Api或AccountSession)的自动签到。
        """
        # 1. 确定上下文
        if isinstance(context, AccountSession):
            client = context.api_client
            log_func = context.log
            user = context.user_data
            params = context.params
            # 多账号模式下，使用账号自己的参数来判断是否启用
            if not params.get("auto_attendance_enabled", False):
                return
        else:  # context is Api (self)
            client = self.api_client
            log_func = self.log
            user = self.user_data
            params = self.params
            # 单账号模式下，也使用自己的参数判断
            if not params.get("auto_attendance_enabled", False):
                return

        if not user.id:
            log_func("用户未登录，跳过自动签到。")
            return

        log_func("(后台) 正在检查自动签到任务...")

        try:
            list_resp = client.get_notice_list(offset=0, limit=20, type_id=0)
            if not (list_resp and list_resp.get("success")):
                log_func("获取通知列表失败，跳过自动签到。")
                return

            notices = list_resp.get("data", {}).get("noticeList", [])
            if not notices:
                log_func("(后台) 通知列表为空。")
                return

            triggered_count = 0
            for notice in notices:
                is_attendance = notice.get(
                    "image"
                ) == "attendance" or "签到" in notice.get("title", "")
                if not (is_attendance and notice.get("id")):
                    continue

                roll_call_id = notice["id"]
                info_resp = client.get_roll_call_info(roll_call_id, user.id)

                status = -2
                finished = 0
                if info_resp and info_resp.get("success"):
                    data = info_resp.get("data", {})
                    roll_call_info = data.get("rollCallInfo", {})
                    status = roll_call_info.get("status")  # -1=过期, 0=进行中
                    finished = data.get("attendFinish")  # 1=已签, 0=未签

                # 检查是否为 "待签到" (进行中 且 未完成)
                if status != -1 and not (finished == 1 or finished is True):
                    log_func(
                        f"检测到待签到任务 '{notice.get('title')}'，正在自动签到..."
                    )
                    coords_str = notice.get("updateBy", "").split(",")
                    if len(coords_str) == 2:
                        try:
                            target_lat, target_lon = float(coords_str[0]), float(
                                coords_str[1]
                            )
                            target_coords = (target_lon, target_lat)

                            # 关键：调用 trigger_attendance
                            auto_result = self.trigger_attendance(
                                roll_call_id,
                                target_coords,
                                "random",
                                specific_coords=None,
                                is_makeup=False,  # 自动签到总是尝试正常签到
                                acc=(
                                    context
                                    if isinstance(context, AccountSession)
                                    else None
                                ),
                            )

                            if auto_result.get("success"):
                                log_func(f"自动签到 '{notice.get('title')}' 成功。")
                                triggered_count += 1
                            else:
                                log_func(
                                    f"自动签到 '{notice.get('title')}' 失败: {auto_result.get('message', '')}"
                                )
                        except Exception as e:
                            log_func(f"签到坐标解析或执行失败: {e}")
                    else:
                        log_func("签到通知坐标格式错误，跳过。")

            if triggered_count == 0:
                log_func("(后台) 未发现待处理的签到任务。")

        except Exception as e:
            log_func(f"自动签到检查时出错: {e}")
            logging.error(
                f"[_check_and_trigger_auto_attendance] Error: {e}", exc_info=True
            )

    def _multi_auto_attendance_worker(self):
        """(多账号) 后台自动刷新和签到所有账号的线程"""
        while not self.stop_multi_auto_refresh.wait(timeout=1.0):
            try:
                if (
                    not self.is_multi_account_mode
                    or not self.global_params.get("auto_attendance_enabled", False)
                    or not self.accounts
                ):
                    # 如果未启用、或不在多账号模式、或没账号，则休眠
                    time.sleep(5)
                    continue

                # 读取刷新间隔
                refresh_interval_s = self.global_params.get("auto_attendance_refresh_s")

                self.log(f"(多账号) 自动签到: 等待 {refresh_interval_s} 秒...")
                if self.stop_multi_auto_refresh.wait(timeout=refresh_interval_s):
                    break  # 收到停止信号

                if not self.is_multi_account_mode or not self.global_params.get(
                    "auto_attendance_enabled", False
                ):
                    continue

                self.log("(多账号) 正在为所有账号执行后台签到检查...")

                # 迭代当前账号列表的快照
                accounts_to_check = list(self.accounts.values())

                for acc in accounts_to_check:
                    if self.stop_multi_auto_refresh.is_set():
                        break  # 检查过程中被停止

                    # 检查该账号是否也启用了自动签到 (从它自己的参数里读)
                    if acc.params.get("auto_attendance_enabled", False):
                        if acc.user_data.id:
                            self._check_and_trigger_auto_attendance(acc)
                            # 刷新该账号的签到统计 (这会更新UI)
                            self._multi_fetch_attendance_stats(acc)
                            self._update_account_status_js(acc, summary=acc.summary)
                            # 简单延迟，避免API风暴
                            time.sleep(random.uniform(1.0, 3.0))
                        else:

                            acc.log("(后台) 尚未登录，跳过自动签到检查。")
                    else:

                        acc.log("(后台) 自动签到未在此账号上启用，跳过。")

            except Exception as e:
                self.log(f"(多账号) 自动签到线程出错: {e}")
                logging.error(f"Multi-auto-attendance worker error: {e}", exc_info=True)
                time.sleep(60)

        logging.info("Multi-auto-attendance worker stopped.")

    def _normalize_status_flag(self, v) -> int:
        """将后端返回的各种 isExecute 表达式规范为 0 或 1"""
        try:
            if v is None:
                return 0
            if isinstance(v, bool):
                return 1 if v else 0
            s = str(v).strip()
            if s == "":
                return 0
            # 纯数字字符串
            if s.isdigit():
                return 1 if int(s) == 1 else 0
            # 常见布尔文本
            if s.lower() in ("true", "yes", "y", "1"):
                return 1
            return 0
        except Exception:
            return 0

    def _should_preserve_status(self, status: str, new_status: str = None) -> bool:
        """
        判断当前状态是否应保留。
        - 如果当前是错误/中止态，则保留，除非新状态明确表示成功或完成。
        """
        if not status:
            return False
        s = str(status).strip()
        error_keywords = (
            "登录失败",
            "刷新失败",
            "执行出错",
            "网络错误",
            "已中止",
            "已停止",
        )

        # 如果当前是错误态
        if any(k in s for k in error_keywords):
            # 只有当新状态是“登录成功”“全部完成”“无任务可执行”等明确的成功/完成态时，才允许覆盖
            if new_status and new_status in (
                "登录成功",
                "全部完成",
                "无任务可执行",
                "待命",
            ):
                return False
            return True
        return False


# ==============================================================================
# 4. 前端界面 (HTML/CSS/JS)
# ==============================================================================


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容 PyInstaller 打包和开发环境"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def check_port_available(host, port):
    """检查端口是否可用"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
    except OSError:
        return False


IP_CACHE_FILE = os.path.join("logs", "ip_location_cache.json")
ip_location_cache = {}  # 内存缓存
ip_cache_lock = threading.Lock()  # 线程安全锁
CACHE_DURATION_SECONDS = 86400  # 缓存有效期：1天


def _load_ip_cache():
    """启动时加载IP归属地缓存文件"""
    global ip_location_cache
    if not os.path.exists(IP_CACHE_FILE):
        logging.info("[IP缓存] 缓存文件不存在，将创建新缓存")
        return

    with ip_cache_lock:
        try:
            with open(IP_CACHE_FILE, "r", encoding="utf-8") as f:
                ip_location_cache = json.load(f)
            logging.info(f"[IP缓存] 成功加载 {len(ip_location_cache)} 条IP缓存记录")
        except (json.JSONDecodeError, OSError) as e:
            logging.warning(f"[IP缓存] 加载缓存文件失败: {e}，将创建新缓存")
            ip_location_cache = {}


def _save_ip_cache():
    """保存IP归属地缓存到文件（线程安全）"""
    with ip_cache_lock:
        try:
            # 确保logs目录存在
            os.makedirs(os.path.dirname(IP_CACHE_FILE), exist_ok=True)
            # 创建缓存的临时副本以进行写入
            cache_copy = ip_location_cache.copy()

            with open(IP_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_copy, f, indent=2, ensure_ascii=False)
            logging.debug("[IP缓存] IP缓存已保存到文件")
        except OSError as e:
            logging.error(f"[IP缓存] 保存缓存文件失败: {e}")
        except Exception as e:
            logging.error(f"[IP缓存] 序列化缓存数据失败: {e}")


def update_session_activity(session_id):
    """更新会话活动时间"""
    with session_activity_lock:
        session_activity[session_id] = time.time()


def update_session_activity(session_id):
    """更新会话活动时间（线程安全）"""
    if not session_id:
        return
    with session_activity_lock:
        session_activity[session_id] = time.time()
        logging.debug(f"[会话活跃] 更新会话 {session_id} 的活跃时间")


def cleanup_session(session_id, reason="manual"):
    """清理指定会话（支持指定原因）"""
    # 跳过无效的session_id
    if not session_id or session_id == "null" or session_id.strip() == "":
        logging.debug(f"跳过清理无效会话ID: '{session_id}'")
        return

    logging.info(f"清理会话: {session_id} (原因: {reason})")
    cleanup_inactive_session(session_id)


def cleanup_inactive_session(session_id):
    """清理不活跃的会话"""
    # 跳过无效的session_id
    if not session_id or session_id == "null" or session_id.strip() == "":
        logging.debug(f"跳过清理无效会话ID: '{session_id}'")
        return

    try:
        logging.info(f"清理不活跃会话: {session_id}")

        # 从内存中移除会话
        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]

                # 停止运行中的任务
                if hasattr(api_instance, "stop_run_flag"):
                    api_instance.stop_run_flag.set()

                # 如果是注册用户，取消会话关联并使token失效
                if hasattr(api_instance, "auth_username") and not getattr(
                    api_instance, "is_guest", True
                ):
                    username = api_instance.auth_username
                    auth_system.unlink_session_from_user(username, session_id)
                    # 使token失效
                    token_manager.invalidate_token(username, session_id)
                    logging.info(f"已使用户 {username} 的会话 {session_id} 的token失效")

                del web_sessions[session_id]

        # 删除会话文件

        session_hash = hashlib.sha256(session_id.encode()).hexdigest()
        session_file = os.path.join(SESSION_STORAGE_DIR, f"{session_hash}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
            logging.info(f"已删除会话文件: {session_hash}")

        # 从活动追踪中移除
        with session_activity_lock:
            if session_id in session_activity:
                del session_activity[session_id]

        # 从索引中移除
        index = _load_session_index()
        if session_id in index:
            del index[session_id]
            _save_session_index(index)

        logging.info(f"会话清理完成: {session_id}")
    except Exception as e:
        logging.error(f"清理会话失败 {session_id} {e}")


def monitor_session_inactivity():
    """
    监控会话不活跃状态并清理
    """
    # 从config.ini读取配置参数
    check_interval = 60
    inactivity_timeout = 300

    try:
        if os.path.exists("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            if config.has_section("System"):
                check_interval = config.getint(
                    "System", "session_monitor_check_interval", fallback=60
                )
                inactivity_timeout = config.getint(
                    "System", "session_inactivity_timeout", fallback=300
                )
    except Exception as e:
        logging.warning(f"读取会话监控配置失败，使用默认值: {e}")

    while True:
        try:
            time.sleep(check_interval)
            current_time = time.time()
            inactive_sessions_to_cleanup = []
            active_sessions_to_update = []

            # 1. 获取当前所有会话的快照（避免长时间持有锁）
            with web_sessions_lock:
                sessions_snapshot = list(web_sessions.items())

            for session_id, api_instance in sessions_snapshot:
                if not api_instance:
                    continue

                # --- 尝试读取最后活跃时间，如果没有定义，就定义为当前时间 ---
                with session_activity_lock:
                    if session_id not in session_activity:
                        session_activity[session_id] = current_time
                    last_activity = session_activity[session_id]

                has_background_activity = False

                # --- 检查单账号模式下是否有正在执行的跑步任务 ---
                if (
                    hasattr(api_instance, "stop_run_flag")
                    and not api_instance.stop_run_flag.is_set()
                ):
                    has_background_activity = True
                    logging.debug(f"[会话监控] {session_id} 单账号跑步任务执行中")

                # --- 检查多账号模式下是否有正在执行的跑步任务 ---
                if (
                    hasattr(api_instance, "multi_run_stop_flag")
                    and not api_instance.multi_run_stop_flag.is_set()
                ):
                    has_background_activity = True
                    logging.debug(f"[会话监控] {session_id} 多账号跑步任务执行中")

                # --- 检查后台自动签到配置 ---
                is_multi = getattr(api_instance, "is_multi_account_mode", False)

                if is_multi:
                    # 多账号模式：检查是否有账号 且 开启了自动签到
                    accounts = getattr(api_instance, "accounts", {})
                    global_params = getattr(api_instance, "multi_global_params", {})
                    auto_attendance = global_params.get(
                        "auto_attendance_enabled", False
                    )
                    logging.debug(
                        f"[会话监控] {session_id} 多账号模式自动签到状态: {auto_attendance}, 账号数: {len(accounts)}"
                    )
                    if accounts and auto_attendance:
                        has_background_activity = True
                        logging.debug(f"[会话监控] {session_id} 多账号自动签到开启中")
                else:
                    # 单账号模式：检查是否开启了自动签到
                    params = getattr(api_instance, "params", {})
                    auto_attendance = params.get("auto_attendance_enabled", False)
                    logging.debug(
                        f"[会话监控] {session_id} 单账号模式自动签到状态: {auto_attendance}"
                    )

                    if auto_attendance:
                        has_background_activity = True
                        logging.debug(f"[会话监控] {session_id} 单账号自动签到开启中")

                # --- 结果处理 ---
                if has_background_activity:
                    # 如果有后台活动，加入更新队列
                    active_sessions_to_update.append(session_id)
                    logging.debug(f"[会话监控] {session_id} 有后台任务，更新活跃时间")
                elif (current_time - last_activity) > inactivity_timeout:
                    logging.debug(f"[会话监控] {session_id} 超过不活跃超时阈值")
                    # 既无前台活跃也无后台任务，且超时
                    inactive_sessions_to_cleanup.append(session_id)
                else:
                    logging.debug(
                        f"[会话监控] {session_id} 仍在活跃期内，上次活跃时间: {current_time - last_activity:.1f}秒前"
                    )

            # 2. 批量更新活跃会话
            if active_sessions_to_update:
                with session_activity_lock:
                    for sid in active_sessions_to_update:
                        session_activity[sid] = current_time

            # 3. 批量清理过期会话
            if inactive_sessions_to_cleanup:
                logging.info(
                    f"[会话监控] 发现 {len(inactive_sessions_to_cleanup)} 个超时且无后台任务的会话，准备清理"
                )
                for sid in inactive_sessions_to_cleanup:
                    cleanup_inactive_session(sid)

        except Exception as e:
            logging.error(f"会话监控线程错误: {e}", exc_info=True)


# 启动会话监控线程


def start_session_monitor():
    """启动会话不活跃监控"""
    monitor_thread = threading.Thread(target=monitor_session_inactivity, daemon=True)
    monitor_thread.start()
    logging.info("会话监控线程已启动")


# 会话持久化函数


def _load_session_index():
    """加载会话索引文件"""
    try:
        if os.path.exists(SESSION_INDEX_FILE):
            with open(SESSION_INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning(f"加载会话索引失败: {e}")
    return {}


def _save_session_index(index):
    """保存会话索引文件"""
    try:
        with open(SESSION_INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"保存会话索引失败: {e}")


def save_session_state(session_id, api_instance, force_save=False):
    """
    将会话状态保存到文件（完整版：保存所有应用状态包括离线任务数据）

    Args:
        session_id: 会话UUID
        api_instance: Api实例
        force_save: 强制保存，即使距离上次保存时间很短
    """
    if not session_id or session_id == "null":
        logging.warning(f"拒绝保存会话：无效的 session_id: '{session_id}'")
        # 可以在这里根据需要决定是否要抛出异常或返回特定值
        return  # 直接返回，不执行后续保存逻辑
    try:
        # 修复Windows路径长度限制：使用SHA256哈希作为文件名
        # 2048位UUID(512字符)会导致Windows文件名过长错误
        session_hash = hashlib.sha256(session_id.encode()).hexdigest()
        session_file = os.path.join(SESSION_STORAGE_DIR, f"{session_hash}.json")

        # 线程安全：获取或创建此会话文件的锁
        with session_file_locks_lock:
            if session_hash not in session_file_locks:
                session_file_locks[session_hash] = threading.Lock()
            file_lock = session_file_locks[session_hash]

        # 使用文件锁保护并发写入
        with file_lock:
            # 防抖：避免过于频繁的保存（除非强制保存）
            if not force_save:
                last_save_time = getattr(api_instance, "_last_session_save_time", 0)
                if time.time() - last_save_time < 2.0:  # 最少间隔2秒
                    return

            # 记录本次保存时间
            api_instance._last_session_save_time = time.time()

            # 基础状态
            state = {
                "session_id": session_id,  # 在文件内容中保存完整的UUID
                # 更明确的命名：学校账号是否已登录
                "school_account_logged_in": getattr(
                    api_instance, "login_success", False
                ),
                # 保留兼容性
                "login_success": getattr(api_instance, "login_success", False),
                "user_info": getattr(api_instance, "user_info", None),
                "created_at": getattr(api_instance, "_session_created_at", time.time()),
                "last_accessed": time.time(),
                "last_saved": time.time(),  # 最后保存时间
            }

            # 增强：保存认证信息
            if hasattr(api_instance, "auth_username"):
                state["auth_username"] = api_instance.auth_username
                state["auth_group"] = getattr(api_instance, "auth_group", "guest")
                state["is_guest"] = getattr(api_instance, "is_guest", False)
                state["is_authenticated"] = getattr(
                    api_instance, "is_authenticated", False
                )

            # 增强：保存用户配置参数
            if hasattr(api_instance, "params"):
                # 复制 params 字典以进行修改
                params_to_save = api_instance.params.copy()
                # 从要保存到会话的字典中移除 amap_js_key
                # amap_js_key 只应存在于 config.ini 中
                if "amap_js_key" in params_to_save:
                    del params_to_save["amap_js_key"]

                state["params"] = params_to_save

            # 增强：保存User-Agent
            if hasattr(api_instance, "device_ua"):
                state["device_ua"] = api_instance.device_ua

            # 增强：保存缓存的通知（用于快速显示）
            if hasattr(api_instance, "cached_notifications"):
                state["cached_notifications"] = api_instance.cached_notifications

            # 增强：保存用户数据
            if hasattr(api_instance, "user_data") and api_instance.user_data:
                user_data = api_instance.user_data
                state["user_data"] = {
                    "name": getattr(user_data, "name", ""),
                    "phone": getattr(user_data, "phone", ""),
                    "student_id": getattr(user_data, "student_id", ""),
                    "id": getattr(user_data, "id", ""),
                    "username": getattr(user_data, "username", ""),
                    "gender": getattr(user_data, "gender", ""),
                    "school_name": getattr(user_data, "school_name", ""),
                }

            # 增强：保存任务选择状态
            if hasattr(api_instance, "current_run_idx"):
                state["current_run_idx"] = api_instance.current_run_idx

            # 保存完整的任务列表（包括所有离线任务字段）
            if hasattr(api_instance, "all_run_data") and api_instance.all_run_data:
                loaded_tasks = []
                for run_data in api_instance.all_run_data:
                    task_dict = {
                        # 任务基本信息
                        "run_name": getattr(run_data, "run_name", ""),
                        "errand_id": getattr(run_data, "errand_id", ""),
                        "errand_schedule": getattr(run_data, "errand_schedule", ""),
                        "status": getattr(run_data, "status", 0),
                        "start_time": getattr(run_data, "start_time", ""),
                        "end_time": getattr(run_data, "end_time", ""),
                        "upload_time": getattr(run_data, "upload_time", ""),
                        "total_run_time_s": getattr(run_data, "total_run_time_s", 0.0),
                        "total_run_distance_m": getattr(
                            run_data, "total_run_distance_m", 0.0
                        ),
                        # 离线任务完整数据（核心）
                        "target_points": getattr(run_data, "target_points", []),
                        "target_point_names": getattr(
                            run_data, "target_point_names", ""
                        ),
                        "recommended_coords": getattr(
                            run_data, "recommended_coords", []
                        ),
                        "draft_coords": getattr(run_data, "draft_coords", []),
                        "run_coords": getattr(run_data, "run_coords", []),
                        # 运行时状态
                        "target_sequence": getattr(run_data, "target_sequence", 0),
                        "is_in_target_zone": getattr(
                            run_data, "is_in_target_zone", False
                        ),
                        "trid": getattr(run_data, "trid", ""),
                        "details_fetched": getattr(run_data, "details_fetched", False),
                        "distance_covered_m": getattr(
                            run_data, "distance_covered_m", 0.0
                        ),
                    }
                    loaded_tasks.append(task_dict)
                state["loaded_tasks"] = loaded_tasks

            # 保存运行状态
            state["is_offline_mode"] = getattr(api_instance, "is_offline_mode", False)

            if (
                hasattr(api_instance, "api_client")
                and api_instance.api_client.session.cookies
            ):
                try:
                    # 将 CookieJar 转换为可序列化的字典
                    state["api_cookies"] = requests.utils.dict_from_cookiejar(
                        api_instance.api_client.session.cookies
                    )
                    logging.debug(
                        f"会话保存: 正在保存 {len(state['api_cookies'])} 个 API Cookies..."
                    )
                except Exception as e:
                    logging.warning(f"会话保存: 保存 API Cookies 失败: {e}")

            # 保存多账号模式状态
            state["is_multi_account_mode"] = getattr(
                api_instance, "is_multi_account_mode", False
            )

            # 如果是多账号模式，保存多账号相关信息
            if getattr(api_instance, "is_multi_account_mode", False):

                # 保存全局参数
                if hasattr(api_instance, "global_params"):
                    global_params_to_save = api_instance.global_params.copy()
                    if "amap_js_key" in global_params_to_save:
                        del global_params_to_save["amap_js_key"]
                    state["multi_global_params"] = global_params_to_save
                else:
                    state["multi_global_params"] = {}

                # 保存每个账号的状态（精简版，只保存恢复所需的核心信息）
                multi_account_states = {}
                accounts = getattr(api_instance, "accounts", {})
                for username, account_session in accounts.items():
                    try:
                        account_state = {
                            # 'username': username, # 键名就是 username，无需重复
                            "status_text": getattr(
                                account_session, "status_text", "待命"
                            ),
                            # [新增] 显式保存验证状态，防止重启后重置为False
                            "is_first_login_verified": getattr(
                                account_session, "is_first_login_verified", False
                            ),
                            "school_account_logged_in": bool(
                                getattr(account_session, "user_data", None)
                                and getattr(account_session.user_data, "id", "")
                            )
                            and getattr(
                                account_session, "is_first_login_verified", False
                            ),
                            # [BUG 修复] 必须保存 summary 字典，UI 恢复依赖此信息
                            "summary": getattr(account_session, "summary", {}),
                        }

                        # 保存账号特定参数（如果有）
                        if hasattr(account_session, "params"):
                            account_state["params"] = account_session.params

                        multi_account_states[username] = account_state

                    except Exception as e:
                        logging.warning(f"保存账号 {username} 状态时出错: {e}")
                        continue

                state["multi_account_states"] = multi_account_states
                # 保存已加载的账号列表（用户名列表）
                state["multi_account_usernames"] = list(
                    getattr(api_instance, "accounts", {}).keys()
                )

                # 保存全局参数
                if hasattr(api_instance, "global_params"):
                    global_params_to_save = api_instance.global_params.copy()
                    if "amap_js_key" in global_params_to_save:
                        del global_params_to_save["amap_js_key"]
                    state["multi_global_params"] = global_params_to_save
                else:
                    state["multi_global_params"] = {}

                # 保存每个账号的状态（精简版，只保存恢复所需的核心信息）
                multi_account_states = {}
                accounts = getattr(api_instance, "accounts", {})
                for username, account_session in accounts.items():
                    try:
                        account_state = {
                            # 'username': username, # 键名就是 username，无需重复
                            "status_text": getattr(
                                account_session, "status_text", "待命"
                            ),
                            "school_account_logged_in": bool(
                                getattr(account_session, "user_data", None)
                                and getattr(account_session.user_data, "id", "")
                            )
                            and getattr(
                                account_session, "is_first_login_verified", False
                            ),
                            # [BUG 修复] 必须保存 summary 字典，UI 恢复依赖此信息
                            "summary": getattr(account_session, "summary", {}),
                        }

                        # 保存账号特定参数（如果有）
                        if hasattr(account_session, "params"):
                            account_state["params"] = account_session.params

                        multi_account_states[username] = account_state

                    except Exception as e:
                        logging.warning(f"保存账号 {username} 状态时出错: {e}")
                        continue

                state["multi_account_states"] = multi_account_states

                # 保存多账号控制面板信息（仪表盘信息）
                state["multi_dashboard_info"] = {
                    "total_accounts": len(accounts),
                    "running_accounts": sum(
                        1
                        for acc in accounts.values()
                        if getattr(acc, "is_running", False)
                    ),
                    "logged_in_accounts": sum(
                        1
                        for acc in accounts.values()
                        if getattr(acc, "login_success", False)
                    ),
                    "total_tasks": sum(
                        len(getattr(acc, "all_run_data", []))
                        for acc in accounts.values()
                    ),
                    "completed_tasks": sum(
                        sum(
                            1
                            for task in getattr(acc, "all_run_data", [])
                            if getattr(task, "status", 0) == 1
                        )
                        for acc in accounts.values()
                    ),
                }

            # 单账号模式的仪表盘信息
            if not getattr(api_instance, "is_multi_account_mode", False):
                # 统计任务信息
                all_tasks = getattr(api_instance, "all_run_data", [])
                state["dashboard_info"] = {
                    "total_tasks": len(all_tasks),
                    "completed_tasks": sum(
                        1 for task in all_tasks if getattr(task, "status", 0) == 1
                    ),
                    "pending_tasks": sum(
                        1 for task in all_tasks if getattr(task, "status", 0) == 0
                    ),
                    "selected_task_index": getattr(api_instance, "current_run_idx", -1),
                    "is_offline_mode": getattr(api_instance, "is_offline_mode", False),
                    "school_account_logged_in": getattr(
                        api_instance, "login_success", False
                    ),
                }

                # 添加当前选中任务的信息（如果有）
                if (
                    hasattr(api_instance, "current_run_idx")
                    and api_instance.current_run_idx >= 0
                ):
                    if hasattr(
                        api_instance, "all_run_data"
                    ) and api_instance.current_run_idx < len(api_instance.all_run_data):
                        current_task = api_instance.all_run_data[
                            api_instance.current_run_idx
                        ]
                        state["dashboard_info"]["current_task"] = {
                            "run_name": getattr(current_task, "run_name", ""),
                            "status": getattr(current_task, "status", 0),
                            "total_distance": getattr(
                                current_task, "total_run_distance_m", 0.0
                            ),
                            "total_time": getattr(
                                current_task, "total_run_time_s", 0.0
                            ),
                            "has_path": len(getattr(current_task, "run_coords", []))
                            > 0,
                        }

            # 增强：保存停止标志状态
            if hasattr(api_instance, "stop_run_flag"):
                state["stop_run_flag_set"] = api_instance.stop_run_flag.is_set()

            # 增强：保存UI状态（如果存在）
            if hasattr(api_instance, "ui_state"):
                state["ui_state"] = api_instance.ui_state

            # 增强：保存用户设置（如果存在）
            if hasattr(api_instance, "user_settings"):
                state["user_settings"] = api_instance.user_settings

            # 写入文件
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

            # 更新索引文件：存储完整UUID到SHA256哈希的映射
            index = _load_session_index()
            index[session_id] = session_hash
            _save_session_index(index)

            tasks_count = len(state.get("loaded_tasks", []))
            logging.debug(
                f"会话状态已保存: {session_id} (任务数:{tasks_count}, 选中索引:{state.get('current_run_idx', -1)})"
            )
    except Exception as e:
        logging.error(f"保存会话状态失败: {e}", exc_info=True)


def load_session_state(session_id):
    """从文件加载会话状态"""
    try:
        # 优化：首先从索引文件查找哈希，避免每次都计算
        index = _load_session_index()

        # 如果索引中存在，直接使用索引中的哈希值
        if session_id in index:
            session_hash = index[session_id]
            logging.debug(
                f"从索引找到会话哈希: {session_id[:32]}... -> {session_hash[:16]}..."
            )
        else:
            # 索引中不存在，计算哈希值（兼容旧文件或索引损坏情况）
            session_hash = hashlib.sha256(session_id.encode()).hexdigest()
            logging.debug(
                f"索引中未找到，计算会话哈希: {session_id[:32]}... -> {session_hash[:16]}..."
            )

        session_file = os.path.join(SESSION_STORAGE_DIR, f"{session_hash}.json")

        if os.path.exists(session_file):
            # 线程安全：获取或创建此会话文件的锁
            with session_file_locks_lock:
                if session_hash not in session_file_locks:
                    session_file_locks[session_hash] = threading.Lock()
                file_lock = session_file_locks[session_hash]

            # 使用文件锁保护并发读取
            with file_lock:
                with open(session_file, "r", encoding="utf-8") as f:
                    state = json.load(f)

            # 验证加载的UUID是否匹配
            if state.get("session_id") == session_id:
                # 检查会话是否过期（7天未访问）
                last_accessed = state.get("last_accessed", 0)
                session_age_days = (time.time() - last_accessed) / 86400  # 转换为天数
                max_age_days = 7  # 会话最大保留7天

                if session_age_days > max_age_days:
                    logging.warning(
                        f"[会话管理] 会话已过期 --> 会话ID: {session_id[:32]}..., 最后访问: {session_age_days:.1f}天前, 最大保留期限: {max_age_days}天, 将被自动清理"
                    )
                    # 删除过期的会话文件
                    try:
                        os.remove(session_file)
                        logging.info(f"[会话管理] 已删除过期会话文件: {session_file}")
                    except Exception as remove_err:
                        logging.error(f"[会话管理] 删除过期会话文件失败: {remove_err}")
                    return None  # 返回None，表示会话不存在或已过期

                tasks_count = len(state.get("loaded_tasks", []))
                logging.info(
                    f"[会话管理] 从文件加载会话 --> 会话ID: {session_id[:32]}..., 登录状态: {state.get('login_success')}, 任务数: {tasks_count}, 最后访问: {session_age_days:.1f}天前"
                )
                return state
            else:
                logging.warning(f"[会话管理] 会话文件UUID不匹配，忽略")
    except Exception as e:
        logging.error(f"[会话管理] 加载会话状态失败 --> 错误: {e}", exc_info=True)
    return None


def cleanup_expired_sessions():
    """
    清理过期的会话文件（7天未访问）

    此函数遍历所有会话文件，删除超过7天未访问的会话。
    """
    try:
        if not os.path.exists(SESSION_STORAGE_DIR):
            return

        max_age_days = 7
        max_age_seconds = max_age_days * 86400
        current_time = time.time()
        cleaned_count = 0
        error_count = 0

        logging.info(f"[会话清理] 开始清理过期会话 --> 最大保留期限: {max_age_days}天")

        for filename in os.listdir(SESSION_STORAGE_DIR):
            if not filename.endswith(".json") or filename == "_index.json":
                continue

            session_file = os.path.join(SESSION_STORAGE_DIR, filename)

            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    state = json.load(f)

                last_accessed = state.get("last_accessed", 0)
                if current_time - last_accessed > max_age_seconds:
                    session_id = state.get("session_id", "unknown")[:32]
                    age_days = (current_time - last_accessed) / 86400

                    os.remove(session_file)
                    cleaned_count += 1
                    logging.info(
                        f"[会话清理] 已删除过期会话 --> 会话ID: {session_id}..., 文件: {filename}, 年龄: {age_days:.1f}天"
                    )

            except Exception as e:
                error_count += 1
                logging.debug(
                    f"[会话清理] 处理会话文件失败 --> 文件: {filename}, 错误: {e}"
                )

        logging.info(
            f"[会话清理] 清理完成 --> 已删除: {cleaned_count}个过期会话, 错误: {error_count}个"
        )

    except Exception as e:
        logging.error(f"[会话清理] 清理过期会话失败 --> 错误: {e}", exc_info=True)


def restore_session_to_api_instance(api_instance, state):
    """
    将保存的会话状态恢复到Api实例

    Args:
        api_instance: Api实例
        state: 从文件加载的状态字典
    """
    try:
        # 恢复认证信息
        if "auth_username" in state:
            api_instance.auth_username = state["auth_username"]
            api_instance.auth_group = state.get("auth_group", "guest")
            api_instance.is_guest = state.get("is_guest", False)
            api_instance.is_authenticated = state.get("is_authenticated", False)

        # 恢复登录状态和用户信息
        if "login_success" in state:
            api_instance.login_success = state["login_success"]
        if "user_info" in state:
            api_instance.user_info = state["user_info"]

        # 恢复用户配置参数
        if "params" in state:
            api_instance.params = state["params"]

        # 恢复User-Agent
        if "device_ua" in state:
            api_instance.device_ua = state["device_ua"]

        # 恢复缓存的通知
        if "cached_notifications" in state:
            api_instance.cached_notifications = state["cached_notifications"]

        # 恢复用户数据
        if "user_data" in state:
            user_data_dict = state["user_data"]
            api_instance.user_data.name = user_data_dict.get("name", "")
            api_instance.user_data.phone = user_data_dict.get("phone", "")
            api_instance.user_data.student_id = user_data_dict.get("student_id", "")
            api_instance.user_data.id = user_data_dict.get("id", "")
            api_instance.user_data.username = user_data_dict.get("username", "")
            api_instance.user_data.gender = user_data_dict.get("gender", "")
            api_instance.user_data.school_name = user_data_dict.get("school_name", "")

        # 恢复任务列表
        if "loaded_tasks" in state:
            api_instance.all_run_data = []
            for task_dict in state["loaded_tasks"]:
                run_data = RunData()
                # 任务基本信息
                run_data.run_name = task_dict.get("run_name", "")
                run_data.errand_id = task_dict.get("errand_id", "")
                run_data.errand_schedule = task_dict.get("errand_schedule", "")
                run_data.status = task_dict.get("status", 0)
                run_data.start_time = task_dict.get("start_time", "")
                run_data.end_time = task_dict.get("end_time", "")
                run_data.upload_time = task_dict.get("upload_time", "")
                run_data.total_run_time_s = task_dict.get("total_run_time_s", 0.0)
                run_data.total_run_distance_m = task_dict.get(
                    "total_run_distance_m", 0.0
                )

                # 离线任务完整数据
                run_data.target_points = [
                    tuple(p) for p in task_dict.get("target_points", [])
                ]
                run_data.target_point_names = task_dict.get("target_point_names", "")
                run_data.recommended_coords = [
                    tuple(p) for p in task_dict.get("recommended_coords", [])
                ]
                run_data.draft_coords = [
                    tuple(p) for p in task_dict.get("draft_coords", [])
                ]
                run_data.run_coords = [
                    tuple(p) for p in task_dict.get("run_coords", [])
                ]

                # 运行时状态
                run_data.target_sequence = task_dict.get("target_sequence", 0)
                run_data.is_in_target_zone = task_dict.get("is_in_target_zone", False)
                run_data.trid = task_dict.get("trid", "")
                run_data.details_fetched = task_dict.get("details_fetched", False)
                run_data.distance_covered_m = task_dict.get("distance_covered_m", 0.0)

                api_instance.all_run_data.append(run_data)

        # 恢复任务选择状态
        if "current_run_idx" in state:
            api_instance.current_run_idx = state["current_run_idx"]

        # 恢复离线模式标志
        if "is_offline_mode" in state:
            api_instance.is_offline_mode = state["is_offline_mode"]

        # 恢复多账号模式状态
        if "is_multi_account_mode" in state:
            api_instance.is_multi_account_mode = state["is_multi_account_mode"]

            # 如果是多账号模式，恢复多账号相关数据
            if state["is_multi_account_mode"]:
                # 恢复全局参数
                if "multi_global_params" in state:
                    api_instance.global_params = state["multi_global_params"]

                # 恢复账号列表的基本信息（修复：页面刷新后账号列表丢失）
                if "multi_account_states" in state:
                    multi_account_states = state["multi_account_states"]

                    logging.info(
                        f"会话恢复：找到 {len(multi_account_states)} 个账号状态，正在重建..."
                    )

                    for username, account_state in multi_account_states.items():
                        if username not in api_instance.accounts:
                            try:
                                # [BUG 修复] 启动时重建 AccountSession 实例
                                # 1. 从 .ini 文件加载该账号的密码 (必须)
                                #    _load_config 也会加载 .ini 中的 params 和 ua,
                                #    但我们稍后会用会话中保存的 params 覆盖它。
                                loaded_password = api_instance._load_config(username)

                                # 2. 从 .ini 加载 tag
                                loaded_tag = api_instance._load_account_tag(username)

                                # 3. 正确创建 AccountSession 实例
                                #    (Api 实例本身就是 api_bridge)
                                acc = AccountSession(
                                    username=username,
                                    password=loaded_password
                                    or "",  # 如果 .ini 没有密码，则为空
                                    api_bridge=api_instance,
                                    tag=loaded_tag or "",
                                )

                                # 4. 恢复会话中保存的状态
                                acc.status_text = account_state.get(
                                    "status_text", "待命"
                                )

                                # 优先使用会话中保存的 params，其次是刚从 .ini 加载的，最后是全局
                                acc.params = account_state.get("params", acc.params)

                                # [BUG 修复] 恢复会话中保存的 summary
                                acc.summary = account_state.get(
                                    "summary",
                                    {
                                        "total": 0,
                                        "completed": 0,
                                        "not_started": 0,
                                        "executable": 0,
                                        "expired": 0,
                                        "att_pending": 0,
                                        "att_completed": 0,
                                        "att_expired": 0,
                                    },
                                )

                                # 恢复 user_data (如果已登录过)
                                if account_state.get("school_account_logged_in", False):
                                    acc.login_success = True
                                    # (user_data 字段在 AccountSession 初始化时是空的,
                                    #  下次刷新 _multi_refresh_worker 时会自动填充)

                                # 5. 添加到 Api 实例的 accounts 字典中
                                api_instance.accounts[username] = acc
                                logging.info(
                                    f"会话恢复：成功重建账号 {username} (密码从 .ini 加载)"
                                )

                            except Exception as e:
                                logging.error(
                                    f"会话恢复：重建账号 {username} 失败: {e}",
                                    exc_info=True,
                                )
                                continue  # 跳过这个损坏的账号

                # --- 启动后立即刷新所有已恢复账号的状态 ---
                if len(api_instance.accounts) > 0:
                    logging.info(
                        f"会话恢复：正在为 {len(api_instance.accounts)} 个已恢复的账号启动后台刷新..."
                    )
                    for acc_session in api_instance.accounts.values():
                        try:
                            # 为每个账号启动一个独立的刷新工作线程
                            # preserve_status=False 确保UI显示“刷新中...”
                            # 我们使用 threading.Thread，因为 _multi_refresh_worker 内部的
                            # eventlet/socketio 调用会在需要时自动“绿化”这个线程。
                            threading.Thread(
                                target=api_instance._multi_refresh_worker,
                                args=(
                                    acc_session,
                                    False,
                                ),  # False 表示不保留旧状态，强制刷新
                                daemon=True,
                                name=f"RestoreRefresh-{acc_session.username}",  # 为线程添加名称
                            ).start()
                        except Exception as thread_err:
                            logging.error(
                                f"会话恢复：启动账号 {acc_session.username} 的刷新线程失败: {thread_err}",
                                exc_info=True,
                            )
                # --- [BUG修复结束] ---

                logging.info(
                    f"会话恢复：检测到多账号模式，已恢复 {len(api_instance.accounts)} 个账号"
                )

        # 恢复停止标志状态
        if "stop_run_flag_set" in state:
            if state["stop_run_flag_set"]:
                api_instance.stop_run_flag.set()
            else:
                api_instance.stop_run_flag.clear()

        # 恢复UI状态
        if "ui_state" in state:
            api_instance.ui_state = state["ui_state"]

        # 恢复用户设置
        if "user_settings" in state:
            api_instance.user_settings = state["user_settings"]

        # 恢复 API Client Cookies (用于拉取通知等)
        if "api_cookies" in state and state["api_cookies"]:
            try:
                cookies_dict = state["api_cookies"]
                # 将 cookie 字典加载回 session
                api_instance.api_client.session.cookies = (
                    requests.utils.cookiejar_from_dict(cookies_dict)
                )
                logging.info(
                    f"会话恢复: 成功恢复 {len(cookies_dict)} 个 API Cookies (shiroCookie等)。"
                )
            except Exception as e:
                logging.warning(f"会话恢复: 恢复 API Cookies 失败: {e}")

        # 恢复自动签到后台线程 (如果启用)
        # 单账号模式
        if not api_instance.is_multi_account_mode and api_instance.params.get(
            "auto_attendance_enabled", False
        ):
            api_instance.stop_auto_refresh.clear()
            api_instance.auto_refresh_thread = threading.Thread(
                target=api_instance._auto_refresh_worker, daemon=True
            )
            api_instance.auto_refresh_thread.start()
            logging.info(f"会话恢复: 已重启单账号自动签到后台线程")

        # 多账号模式
        if api_instance.is_multi_account_mode and api_instance.global_params.get(
            "auto_attendance_enabled", False
        ):
            api_instance.stop_multi_auto_refresh.clear()
            api_instance.multi_auto_refresh_thread = threading.Thread(
                target=api_instance._multi_auto_attendance_worker, daemon=True
            )
            api_instance.multi_auto_refresh_thread.start()
            logging.info(f"会话恢复: 已重启多账号自动签到后台线程")

        logging.info(
            f"会话状态恢复完成: 任务数={len(api_instance.all_run_data)}, 选中索引={api_instance.current_run_idx}, 多账号模式={api_instance.is_multi_account_mode}"
        )

    except Exception as e:
        logging.error(f"恢复会话状态失败: {e}", exc_info=True)


def get_captcha_original_width(html_content):
    """
    【移动端验证码缩放】获取验证码的原始宽度

    功能说明:
        - 从HTML中解析验证码结构（行数、列数）
        - 从CSS中提取单个像素的宽度
        - 计算总宽度 = 列数 × 单个像素宽度

    参数:
        html_content (str): 验证码HTML内容

    返回:
        float: 验证码原始宽度（像素），解析失败返回None

    示例:
        原始HTML: 46列 × 10px/像素 = 460px总宽度
        原始HTML: 40列 × 12px/像素 = 480px总宽度
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # 获取容器和像素span
        container = soup.find("div")
        if not container:
            return None

        spans = container.find_all("span")
        if not spans:
            return None

        pixel_classes = list(set([s.get("class")[0] for s in spans if s.get("class")]))
        if not pixel_classes:
            return None

        # 计算列数（统计第一行有多少个span）
        first_line_spans = 0
        for child in container.contents:
            if child.name == "br":
                break
            if child.name == "span":
                first_line_spans += 1

        num_cols = first_line_spans
        if num_cols == 0:
            return None

        # 从CSS中提取单个像素宽度
        style_tag = soup.find("style")
        if not style_tag:
            return None

        css_text = style_tag.string
        sample_pixel_class = pixel_classes[0]
        container_class = container.get("class")[0]  # 获取容器类名

        # 正则匹配width
        # 【修正】优先匹配容器下的span样式
        w_match = re.search(
            rf"\.{container_class}\s+span[^}}]*width\s*:\s*(\d+(\.\d+)?)px", css_text
        )

        if not w_match:
            # 备用：匹配像素类样式
            w_match = re.search(
                rf"\.{sample_pixel_class}[^}}]*width\s*:\s*(\d+(\.\d+)?)px", css_text
            )

        if not w_match:
            # 如果都匹配不到，假设默认值 (通常 scale_factor=2 时是 6px)
            # 或者返回 None 让后续逻辑处理
            return None

        old_pixel_w = float(w_match.group(1))

        # 计算总宽度 = 列数 × 单个像素宽度
        original_width = num_cols * old_pixel_w

        logging.debug(
            f"[get_captcha_original_width] 列数={num_cols}, 像素宽度={old_pixel_w}px, 总宽度={original_width}px"
        )

        return original_width

    except Exception as e:
        logging.error(f"[get_captcha_original_width] 解析失败: {e}")
        return None


def resize_captcha_html(html_content, target_width):
    """
    自动分析并调整像素验证码HTML的大小 (Grid Layout 增强版 - 修正Padding/Border计算)。
    """
    try:
        target_width = float(target_width)  # 确保是数字
        soup = BeautifulSoup(html_content, "html.parser")

        # 1. 获取容器
        container = soup.find("div")
        if not container:
            logging.warning("[resize_captcha_html] 无法找到容器 div")
            return html_content

        container_class = container.get("class")[0]

        # 2. 解析 CSS 内容
        style_tag = soup.find("style")
        if not style_tag:
            return html_content

        css_text = style_tag.string

        # --- 步骤 A: 智能解析布局参数 (Grid 优先) ---

        num_cols = 0
        old_pixel_w = 0.0
        old_pixel_h = 0.0
        old_gap = 0.0

        # 解析 Grid 列数和宽
        grid_match = re.search(
            r"grid-template-columns\s*:\s*repeat\(\s*(\d+)\s*,\s*(\d+(?:\.\d+)?)\s*px\s*\)",
            css_text,
            re.IGNORECASE,
        )

        if grid_match:
            num_cols = int(grid_match.group(1))
            old_pixel_w = float(grid_match.group(2))
            logging.info(
                f"[验证码缩放] 检测到 CSS Grid 布局: {num_cols} 列, 原始宽 {old_pixel_w}px"
            )
        else:
            # 备用方案（略，你的场景主要是Grid）
            pass

        if num_cols == 0:
            logging.error("[resize_captcha_html] 无法解析列数，跳过缩放")
            return html_content

        # 解析 Gap
        gap_match = re.search(
            rf"\.{container_class}\s*\{{.*?\bgap\s*:\s*(\d+(?:\.\d+)?)px",
            css_text,
            re.DOTALL | re.IGNORECASE,
        )
        if gap_match:
            old_gap = float(gap_match.group(1))

        # 解析高度
        h_match = re.search(
            rf"\.{container_class}\s+span[^}}]*?height\s*:\s*(\d+(\.\d+)?)px",
            css_text,
            re.IGNORECASE,
        )
        if h_match:
            old_pixel_h = float(h_match.group(1))
        else:
            old_pixel_h = old_pixel_w

        # --- 新增步骤: 解析 Padding 和 Border (修正的核心) ---
        padding_w = 0.0
        border_w = 0.0

        # 解析 Padding (匹配 padding: 10px 格式)
        pad_match = re.search(
            rf"\.{container_class}\s*\{{.*?\bpadding\s*:\s*(\d+(?:\.\d+)?)px",
            css_text,
            re.DOTALL | re.IGNORECASE,
        )
        if pad_match:
            padding_w = float(pad_match.group(1)) * 2  # 左右两边

        # 解析 Border (匹配 border: 1px ... 格式)
        bor_match = re.search(
            rf"\.{container_class}\s*\{{.*?\bborder\s*:\s*(\d+(?:\.\d+)?)px",
            css_text,
            re.DOTALL | re.IGNORECASE,
        )
        if bor_match:
            border_w = float(bor_match.group(1)) * 2  # 左右两边

        # --- 步骤 B: 计算缩放比例 ---

        # 原始 Grid 内容宽度 (仅内容)
        original_grid_width = (num_cols * old_pixel_w) + ((num_cols - 1) * old_gap)

        if original_grid_width <= 0:
            return html_content

        # 计算有效可用宽度 (扣除装饰)
        available_grid_width = target_width - padding_w - border_w

        if available_grid_width <= 0:
            logging.warning(f"[验证码缩放] 目标宽度过小，无法容纳Padding/Border")
            return html_content

        # 修正后的缩放系数
        scale_ratio = available_grid_width / original_grid_width

        # --- [新增] 约束：只允许缩小，不允许放大 ---
        if scale_ratio >= 1.0:
            logging.info(
                f"[验证码缩放] 目标宽度 ({target_width}px) 足以容纳原始尺寸，跳过放大 (Ratio: {scale_ratio:.2f})"
            )
            return html_content
        # ---------------------------------------

        new_pixel_w = old_pixel_w * scale_ratio
        new_pixel_h = old_pixel_h * scale_ratio
        new_gap = old_gap * scale_ratio

        logging.info(
            f"[验证码缩放] Scaling: {scale_ratio:.4f} | Pad/Bor: {padding_w}/{border_w} | Target Grid: {available_grid_width:.2f}px"
        )

        # --- 步骤 C: 执行替换 ---

        new_css = css_text

        # 1. 替换 grid-template-columns
        new_css = re.sub(
            r"(grid-template-columns\s*:\s*repeat\(\s*\d+\s*,\s*)(\d+(?:\.\d+)?)px",
            rf"\g<1>{new_pixel_w:.4f}px",
            new_css,
            flags=re.IGNORECASE,
        )

        # 2. 替换 gap
        if old_gap >= 0:  # 即使是0也要替换，防止原有是1px
            new_css = re.sub(
                rf"(\.{container_class}\s*\{{.*?\bgap\s*:\s*)(\d+(?:\.\d+)?)px",
                rf"\g<1>{new_gap:.4f}px",
                new_css,
                flags=re.DOTALL | re.IGNORECASE,
            )

        # 3. 替换 span width/height (通用匹配，防止漏掉)
        # 替换 width
        new_css = re.sub(
            rf"(\.{container_class}\s+span[^}}]*?width\s*:\s*)(\d+(\.\d+)?)px",
            rf"\g<1>{new_pixel_w:.4f}px",
            new_css,
            flags=re.IGNORECASE,
        )
        # 替换 height
        new_css = re.sub(
            rf"(\.{container_class}\s+span[^}}]*?height\s*:\s*)(\d+(\.\d+)?)px",
            rf"\g<1>{new_pixel_h:.4f}px",
            new_css,
            flags=re.IGNORECASE,
        )

        # 4. 替换单独像素类 (ekzfv, desiz)
        spans = container.find_all("span")
        pixel_classes = set([s.get("class")[0] for s in spans if s.get("class")])

        for p_class in pixel_classes:
            new_css = re.sub(
                rf"(\.{p_class}[^}}]*?(?<![-\w])width\s*:\s*)(\d+(\.\d+)?)px",
                rf"\g<1>{new_pixel_w:.4f}px",
                new_css,
                flags=re.IGNORECASE,
            )
            new_css = re.sub(
                rf"(\.{p_class}[^}}]*?(?<![-\w])height\s*:\s*)(\d+(\.\d+)?)px",
                rf"\g<1>{new_pixel_h:.4f}px",
                new_css,
                flags=re.IGNORECASE,
            )

        style_tag.string = new_css
        return str(soup)

    except Exception as e:
        logging.error(f"[resize_captcha_html] 调整失败: {e}", exc_info=True)
        return html_content


def load_all_sessions(args):
    """启动时加载所有持久化会话"""
    if not os.path.exists(SESSION_STORAGE_DIR):
        return

    # 加载或重建索引文件
    index = _load_session_index()
    new_index = {}

    successful_sessions = {}

    loaded_count = 0
    for filename in os.listdir(SESSION_STORAGE_DIR):
        if filename == "_index.json":
            continue

        if filename.endswith(".json"):
            session_file = os.path.join(SESSION_STORAGE_DIR, filename)
            session_id = None  # 先声明 session_id
            session_hash = filename[:-5]
            try:
                # 尝试读取文件基本信息
                with open(session_file, "r", encoding="utf-8") as f:
                    state = json.load(f)

                session_id = state.get("session_id")
                if not session_id:
                    raise ValueError(f"文件 {filename} 缺少 session_id")

                # 检查会话是否过期
                last_accessed = state.get("last_accessed", 0)
                if time.time() - last_accessed > 7 * 24 * 3600:
                    logging.info(
                        f"清理过期会话: {session_id[:8]}... (文件: {filename})"
                    )
                    try:
                        os.remove(session_file)
                    except Exception as remove_err:
                        logging.error(f"删除过期会话文件 {filename} 失败: {remove_err}")
                    continue  # 过期则跳过，不尝试恢复

                # --- 尝试恢复完整状态 ---
                api_instance = Api(args)
                api_instance._session_created_at = state.get("created_at", time.time())

                # 【关键修复】恢复会话ID，否则socketio推送无法找到房间
                api_instance._web_session_id = session_id

                # restore_session_to_api_instance 现在包含恢复 login_success 等所有状态
                restore_session_to_api_instance(api_instance, state)

                # --- 如果成功恢复 ---
                logging.info(
                    f"成功恢复会话: {session_id}... (用户: {api_instance.auth_username if hasattr(api_instance, 'auth_username') else 'Unknown'}, 文件: {filename})"
                )
                web_sessions[session_id] = api_instance  # 加入内存
                session_activity[session_id] = last_accessed  # 恢复活动时间
                successful_sessions[session_id] = (
                    session_hash  # 记录成功加载的会话及其哈希
                )
                loaded_count += 1

            except (
                json.JSONDecodeError,
                ValueError,
                KeyError,
                TypeError,
                AttributeError,
            ) as e:
                # 加载或恢复过程中发生任何错误
                # 可以关闭 exc_info 避免过多日志
                logging.error(
                    f"加载或恢复会话文件 {filename} 失败: {e}", exc_info=False
                )
                logging.warning(f"将删除损坏的/无法恢复的会话文件: {filename}")
                try:
                    os.remove(session_file)  # 删除损坏的文件
                except Exception as remove_err:
                    logging.error(f"删除损坏的会话文件 {filename} 失败: {remove_err}")
                # 不将失败的会话加入 web_sessions 或 successful_sessions
                continue  # 继续处理下一个文件
            except Exception as e:  # 捕获其他意外错误
                logging.error(
                    f"处理会话文件 {filename} 时发生未知错误: {e}", exc_info=True
                )
                try:
                    os.remove(session_file)  # 也尝试删除
                except Exception as remove_err:
                    logging.error(
                        f"删除未知错误的会话文件 {filename} 失败: {remove_err}"
                    )
                continue

    # 保存重建的索引（只包含成功加载的会话）
    if successful_sessions:
        # 使用 successful_sessions 作为新的索引内容
        _save_session_index(successful_sessions)
        logging.info(f"会话索引已更新，包含 {len(successful_sessions)} 个有效会话")
    elif not any(
        f.endswith(".json") and f != "_index.json"
        for f in os.listdir(SESSION_STORAGE_DIR)
    ):
        # 如果 sessions 目录为空 (除了 index)，则清空 index 文件
        _save_session_index({})
        logging.info("会话目录为空，已清空会话索引。")

    # 保存重建的索引（清理过期条目）
    if new_index:
        _save_session_index(new_index)
        logging.debug(f"会话索引已更新，包含 {len(new_index)} 个有效会话")

    if loaded_count > 0:
        logging.info(f"共加载 {loaded_count} 个持久化会话")


# Playwright浏览器池管理


class BackgroundTaskManager:
    """管理服务器端后台任务执行"""

    def __init__(self):
        self.tasks = {}  # {session_id: task_info}
        self.lock = threading.Lock()
        self.task_storage_dir = os.path.join(
            os.path.dirname(__file__), "background_tasks"
        )
        if not os.path.exists(self.task_storage_dir):
            os.makedirs(self.task_storage_dir)
        logging.info("BackgroundTaskManager initialized")

    def _get_task_file_path(self, session_id):
        """获取任务状态文件路径"""
        task_hash = hashlib.sha256(session_id.encode()).hexdigest()
        return os.path.join(self.task_storage_dir, f"{task_hash}.json")

    def save_task_state(self, session_id, task_state):
        """保存任务状态到文件"""
        task_file = self._get_task_file_path(session_id)
        try:
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump(task_state, f, indent=2, ensure_ascii=False)
            logging.debug(f"后台任务状态已保存，会话ID: {session_id}")
        except Exception as e:
            logging.error(f"保存后台任务状态失败: {e}")

    def load_task_state(self, session_id):
        """从文件加载任务状态"""
        task_file = self._get_task_file_path(session_id)
        if not os.path.exists(task_file):
            return None
        try:
            with open(task_file, "r", encoding="utf-8") as f:
                task_state = json.load(f)
            logging.debug(f"后台任务状态已加载，会话ID: {session_id}")
            return task_state
        except Exception as e:
            logging.error(f"加载后台任务状态失败: {e}")
            return None

    def start_background_task(
        self, session_id, api_instance, task_indices, auto_generate=False
    ):
        """启动后台任务执行"""
        with self.lock:
            # 初始化任务状态
            task_state = {
                "session_id": session_id,
                "total_tasks": len(task_indices),
                "completed_tasks": 0,
                "current_task_index": 0,
                "task_indices": task_indices,
                "auto_generate": auto_generate,
                "status": "running",
                "start_time": time.time(),
                "last_update": time.time(),
                "progress_percent": 0,
                "current_task_progress": 0,
                "singleProcessedPoints": 0,  # 已处理的GPS点数
                "singleTotalPoints": 0,  # 总GPS点数
            }

            self.tasks[session_id] = task_state
            self.save_task_state(session_id, task_state)

            # 启动后台线程执行任务
            thread = threading.Thread(
                target=self._execute_tasks_background,
                args=(session_id, api_instance, task_indices, auto_generate),
                daemon=True,
            )
            thread.start()

            logging.info(
                f"后台任务已启动，会话ID前缀: {session_id[:8]}, 总任务数: {len(task_indices)}"
            )
            return {
                "success": True,
                "message": f"已启动后台任务，共{len(task_indices)}个任务",
            }

    def _execute_tasks_background(
        self, session_id, api_instance, task_indices, auto_generate
    ):
        """后台执行任务的线程函数"""
        try:
            tasks_executed = 0  # 追踪实际执行的任务数量

            for i, task_idx in enumerate(task_indices):
                # 检查是否需要停止
                with self.lock:
                    if session_id not in self.tasks:
                        logging.info(f"后台任务已取消，会话ID前缀: {session_id[:8]}")
                        return

                    task_state = self.tasks[session_id]
                    if task_state.get("status") == "stopped":
                        logging.info(f"后台任务已停止，会话ID前缀: {session_id[:8]}")
                        return

                # 更新当前任务
                with self.lock:
                    task_state["current_task_index"] = i
                    task_state["last_update"] = time.time()
                    self.save_task_state(session_id, task_state)

                # 执行单个任务
                logging.info(
                    f"正在执行后台任务 {i+1}/{len(task_indices)}，会话ID前缀: {session_id[:8]}"
                )
                run_data = api_instance.all_run_data[task_idx]

                # 如果需要自动生成路径
                if auto_generate and not run_data.run_coords:
                    logging.info(
                        f"正在为任务自动生成路径: 任务名称={run_data.run_name}"
                    )
                    try:
                        # 确保已加载任务详情，拿到打卡点
                        if not run_data.details_fetched:
                            logging.info(
                                f"正在获取任务详细信息: {run_data.run_name}..."
                            )
                            details_resp = api_instance.get_task_details(task_idx)
                            if not details_resp.get("success"):
                                logging.error(
                                    f"获取任务详情失败，任务名称: {run_data.run_name}，错误信息: {details_resp.get('message', '未知错误')}"
                                )
                                continue
                            run_data = api_instance.all_run_data[task_idx]
                            logging.info(f"任务详情获取成功: {run_data.run_name}")

                        if not run_data.target_points:

                            logging.warning(
                                f"[跳过任务] 任务 '{run_data.run_name}' 因缺少打卡点 (0个) 而无法自动生成路径。请检查学校平台任务设置。"
                            )

                            continue

                        logging.info(
                            f"任务包含 {len(run_data.target_points)} 个目标打卡点: {run_data.run_name}"
                        )

                        # 使用Chrome池进行服务器端路径规划
                        waypoints = run_data.target_points
                        logging.info(
                            f"正在规划路径，包含 {len(waypoints)} 个路点，任务名称: {run_data.run_name}"
                        )
                        logging.info(
                            f"Waypoints: {waypoints[:3]}..."
                            if len(waypoints) > 3
                            else f"Waypoints: {waypoints}"
                        )

                        # 必须在调用Chrome池之前获取 Key
                        amap_key = ""
                        try:
                            # 确保 configparser 和 os 已在文件顶部导入
                            if os.path.exists(CONFIG_FILE):
                                cfg = configparser.ConfigParser()
                                cfg.read(CONFIG_FILE, encoding="utf-8")
                                amap_key = cfg.get("Map", "amap_js_key", fallback="")
                                if not amap_key:
                                    # 兼容旧版配置
                                    amap_key = cfg.get(
                                        "System", "AmapJsKey", fallback=""
                                    )

                            if amap_key:
                                logging.info(f"已从 {CONFIG_FILE} 实时加载 AMap Key。")
                            else:
                                logging.error(
                                    f"无法为 {run_data.run_name} 自动规划路径：实时读取 {CONFIG_FILE} 失败，[Map] -> amap_js_key 缺失或为空。"
                                )
                                # 标记任务状态为错误并跳过
                                with self.lock:
                                    task_state["status"] = "error"
                                    task_state["error"] = (
                                        "缺少高德地图API Key (实时读取失败)"
                                    )
                                    self.save_task_state(session_id, task_state)
                                continue  # 跳过此任务

                        except Exception as e:
                            logging.error(
                                f"实时读取 AMap Key 时发生错误: {e}", exc_info=True
                            )
                            with self.lock:
                                task_state["status"] = "error"
                                task_state["error"] = f"读取Config.ini失败: {e}"
                                self.save_task_state(session_id, task_state)
                            continue

                        # 调用Chrome池执行路径规划
                        global chrome_pool
                        if not chrome_pool:
                            logging.error("Chrome浏览器池不可用，无法进行路径规划！")
                            continue

                        if chrome_pool:
                            try:
                                logging.info(
                                    f"正在获取Chrome浏览器上下文，会话ID前缀: {session_id[:8]}..."
                                )
                                # 获取页面并确保加载了AMap
                                ctx = chrome_pool.get_context(session_id)
                                page = ctx["page"]
                                logging.info("Chrome浏览器上下文获取成功")

                                # 首先加载包含AMap的页面
                                logging.info("正在向Chrome页面加载高德地图SDK...")
                                page.goto("about:blank")
                                page.set_content(
                                    """
                                <!DOCTYPE html>
                                <html>
                                <head>
                                    <meta charset="utf-8">
                                    <script type="text/javascript" src="https://webapi.amap.com/loader.js"></script>
                                </head>
                                <body></body>
                                </html>
                                """
                                )

                                # 等待AMap加载 (修复：等待 AMapLoader 加载完成)
                                logging.info(
                                    "等待高德地图加载器(AMapLoader)加载完成..."
                                )
                                page.wait_for_function(
                                    "typeof AMapLoader !== 'undefined'", timeout=10000
                                )
                                logging.info("高德地图加载器在Chrome上下文中加载成功")

                                # 使用Chrome池执行AMap路径规划JavaScript
                                logging.info(
                                    f"正在Chrome浏览器中执行路径规划JavaScript代码..."
                                )

                                # BUG修复：将JS代码块包装在 (async (arg) => { ... }) IIFE 中
                                # 并且使用与 index.html 中 getWalkingPath 相同的“迭代分段请求”逻辑
                                path_coords = chrome_pool.execute_js(
                                    session_id,
                                    """
                                    (async (arg) => {
                                        const waypointsPy = arg[0]; // 这是Python传入的 [[lon, lat], ...]
                                        const apiKey = arg[1];
                                        const pythonParams = arg[2]; // <--- 读取 Python 传入的参数

                                        // 1. 定义辅助函数 (planPath)
                                        async function planPath(waypointsPy, apiKey, pythonParams) {
                                            
                                            // 1.1 确保 AMapLoader (来自 loader.js) 存在
                                            if (typeof AMapLoader === 'undefined') {
                                                return {error: 'AMapLoader not loaded'};
                                            }

                                            // 1.2 调用 AMapLoader.load 并传入 key
                                            try {
                                                await AMapLoader.load({
                                                    "key": apiKey,
                                                    "version": "2.0",
                                                    "plugins": ["AMap.Walking"]
                                                });
                                            } catch (e) {
                                                return {error: 'AMapLoader.load failed: ' + (e ? e.message : 'Unknown error')};
                                            }

                                            // 1.3 检查 AMap.Walking 插件是否真的加载成功
                                            if (typeof AMap.Walking === 'undefined') {
                                                return {error: 'AMap.Walking plugin failed to load'};
                                            }

                                            // 1.4 ★ 步骤 2 修复：从 pythonParams 读取重试和回退设置
                                            const useFallback = pythonParams.api_fallback_line ?? false;
                                            const maxRetries = pythonParams.api_retries ?? 2;
                                            const retryDelayMs = (pythonParams.api_retry_delay_s ?? 0.5) * 1000;
                                            const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

                                            // 1.5 定义分段搜索函数 (同 index.html)
                                            const searchSegment = (start, end, walkingInstance) => new Promise((resolve) => {
                                                walkingInstance.search(start, end, (status, result) => {
                                                    if (status === 'complete' && result.routes?.length > 0) {
                                                        const p = []; 
                                                        result.routes[0].steps.forEach(s => s.path.forEach(pt => p.push({ lng: pt.lng, lat: pt.lat })));
                                                        resolve({ path: p }); // 返回成功路径
                                                    } else {
                                                        let errorInfo = 'Unknown Error';
                                                        if (status === 'error') {
                                                            if (result && result.info) {
                                                                errorInfo = result.info;
                                                            } else if (result) {
                                                                try { errorInfo = JSON.stringify(result); } catch (e) { errorInfo = result.toString(); }
                                                            } else {
                                                                errorInfo = status;
                                                            }
                                                        } else if (status === 'no_data') {
                                                            errorInfo = 'No path found (no_data)';
                                                        } else {
                                                            errorInfo = status; // 如 "CUQPS_HAS_EXCEEDED_THE_LIMIT"
                                                        }
                                                        resolve({ error: 'Path planning failed: ' + errorInfo }); // 返回错误
                                                    }
                                                });
                                            });

                                            // 1.6 ★ 步骤 2 修复：迭代执行路径规划 (增加重试循环)
                                            const all_path = [];
                                            const waypoints = waypointsPy.map(p => new AMap.LngLat(p[0], p[1]));
                                            const walking = new AMap.Walking({ map: null, panel: "", hideMarkers: true });

                                            if (waypoints.length < 2) {
                                                return {error: 'Waypoints must be at least 2.'};
                                            }

                                            for (let i = 0; i < waypoints.length - 1; i++) {
                                                const realStart = waypoints[i];
                                                const realEnd = waypoints[i + 1];
                                                
                                                let attempts = 0;
                                                let segmentResult = null;
                                                let segmentPath = null; // 存储成功的路径

                                                // --- 增加重试循环 (来自 index.html) ---
                                                while (attempts <= maxRetries) {
                                                    if (attempts > 0) {
                                                        await sleep(retryDelayMs); // 等待后重试
                                                    }
                                                    
                                                    segmentResult = await searchSegment(realStart, realEnd, walking);
                                                    
                                                    if (segmentResult.path) { // 检查 .path 是否存在 (成功)
                                                        segmentPath = segmentResult.path;
                                                        break; // 成功，退出重试循环
                                                    }
                                                    
                                                    // 失败，记录最后一次错误 (将在重试用尽时使用)
                                                    // (不需要 console.log，Python端会记录最终错误)
                                                    
                                                    attempts++;
                                                }
                                                // --- 结束重试循环 ---

                                                if (segmentPath) {
                                                    // 成功: 拼接路径
                                                    const areCoordsEqual = (c1, c2) => Math.abs(c1.lng - c2.lng) < 1e-6 && Math.abs(c1.lat - c2.lat) < 1e-6;
                                                    if (i > 0) {
                                                        all_path.push(...segmentPath.slice(1));
                                                    } else {
                                                        all_path.push(...segmentPath);
                                                    }
                                                    if (i === waypoints.length - 2) { 
                                                        if (segmentPath.length > 0 && !areCoordsEqual(segmentPath[segmentPath.length - 1], { lng: realEnd.lng, lat: realEnd.lat })) {
                                                            all_path.push({ lng: realEnd.lng, lat: realEnd.lat });
                                                        }
                                                    }
                                                } else {
                                                    // 失败: 检查回退
                                                    if (useFallback) {
                                                        // 使用直线回退 (确保连接性)
                                                        const lastPoint = all_path.length > 0 ? all_path[all_path.length - 1] : null;
                                                        if (!lastPoint || (Math.abs(lastPoint.lng - realStart.lng) > 1e-6 || Math.abs(lastPoint.lat - realStart.lat) > 1e-6)) {
                                                            all_path.push({ lng: realStart.lng, lat: realStart.lat });
                                                        }
                                                        all_path.push({ lng: realEnd.lng, lat: realEnd.lat });
                                                    } else {
                                                        // 不回退，整个规划失败
                                                        return {error: `Segment ${i+1} failed after ${maxRetries+1} attempts: ${segmentResult.error}`};
                                                    }
                                                }
                                            }
                                            
                                            // 成功
                                            return {path: all_path};
                                        }

                                        // 2. 调用辅助函数并返回结果
                                        return await planPath(waypointsPy, apiKey, pythonParams);
                                    })
                                    """,
                                    waypoints,
                                    amap_key,
                                    api_instance.params,  # <--- 步骤 1 修复：传入参数
                                )

                                logging.info(
                                    f"路径规划JavaScript返回结果: 类型={type(path_coords)}, 包含'path'键={'是' if (path_coords and 'path' in path_coords) else '否'}"
                                )

                                if path_coords and "path" in path_coords:
                                    api_path_coords = path_coords["path"]
                                    logging.info(
                                        f"路径规划成功，包含 {len(api_path_coords)} 个坐标点"
                                    )

                                    # 使用后端生成 run_coords
                                    p = api_instance.params
                                    logging.info(
                                        f"正在生成运动模拟数据，参数: 最小时长={p.get('min_time_m', 20)}分钟, 最大时长={p.get('max_time_m', 30)}分钟, 最小距离={p.get('min_dist_m', 2000)}米"
                                    )
                                    gen_resp = api_instance.auto_generate_path_with_api(
                                        api_path_coords,
                                        p.get("min_time_m", 20),
                                        p.get("max_time_m", 30),
                                        p.get("min_dist_m", 2000),
                                    )

                                    logging.info(
                                        f"auto_generate_path_with_api函数返回: 成功={gen_resp.get('success')}"
                                    )

                                    if gen_resp.get("success"):
                                        # 将生成结果回填到当前任务
                                        run_data.run_coords = gen_resp["run_coords"]
                                        run_data.total_run_distance_m = gen_resp[
                                            "total_dist"
                                        ]
                                        run_data.total_run_time_s = gen_resp[
                                            "total_time"
                                        ]
                                        logging.info(
                                            f"路径自动生成成功，任务: {run_data.run_name}，坐标点数: {len(gen_resp['run_coords'])}, 总距离: {gen_resp['total_dist']}米, 总时长: {gen_resp['total_time']}秒"
                                        )

                                        with self.lock:
                                            if session_id in self.tasks:
                                                task_state = self.tasks[session_id]
                                                task_state["last_update"] = time.time()

                                                # 填充前端 pollBackgroundTaskStatus 所需的关键"总览"数据
                                                task_state["estimated_total_time_s"] = (
                                                    run_data.total_run_time_s
                                                )
                                                task_state[
                                                    "estimated_total_distance_m"
                                                ] = run_data.total_run_distance_m

                                                # 填充路径和打卡点数据，以便 checkBackgroundTaskOnLoad (页面刷新)
                                                # 和 pollBackgroundTaskStatus (地图绘制) 可以恢复地图
                                                task_state["target_points"] = (
                                                    run_data.target_points
                                                    if hasattr(
                                                        run_data, "target_points"
                                                    )
                                                    else []
                                                )
                                                task_state["target_point_names"] = (
                                                    run_data.target_point_names
                                                    if hasattr(
                                                        run_data, "target_point_names"
                                                    )
                                                    else ""
                                                )
                                                task_state["recommended_coords"] = (
                                                    run_data.recommended_coords
                                                    if hasattr(
                                                        run_data, "recommended_coords"
                                                    )
                                                    else []
                                                )
                                                task_state["run_coords"] = (
                                                    run_data.run_coords
                                                    if hasattr(run_data, "run_coords")
                                                    else []
                                                )

                                                # 填充点数信息
                                                total_points = len(run_data.run_coords)
                                                task_state["singleTotalPoints"] = (
                                                    total_points
                                                )
                                                # 尚未开始
                                                task_state["singleProcessedPoints"] = 0

                                                # 立即保存此状态
                                                self.save_task_state(
                                                    session_id, task_state
                                                )

                                    else:
                                        logging.error(
                                            f"生成运动坐标序列失败: {gen_resp.get('message')}"
                                        )
                                        continue
                                else:
                                    error_msg = (
                                        path_coords.get("error", "Unknown error")
                                        if path_coords
                                        else "No response from path planning"
                                    )
                                    logging.error(
                                        f"任务路径规划失败，任务名称: {run_data.run_name}，错误信息: {error_msg}"
                                    )
                                    continue
                            except Exception as e:
                                logging.error(
                                    f"Chrome浏览器池路径规划失败，任务名称: {run_data.run_name}，异常信息: {e}",
                                    exc_info=True,
                                )
                                continue
                        else:
                            logging.error("Chrome浏览器池不可用，无法进行路径规划")
                            continue

                    except Exception as e:
                        logging.error(f"自动生成路径失败，异常信息: {e}", exc_info=True)
                        continue

                # 检查任务是否有路径
                if not run_data.run_coords:
                    logging.warning(f"任务没有可用路径，跳过执行: {run_data.run_name}")
                    # 跳过此任务，继续执行下一个任务
                    continue

                # 计算任务索引（修正 task_idx 未定义错误）
                try:
                    task_idx = api_instance.all_run_data.index(run_data)
                except ValueError:
                    task_idx = -1

                # 设置当前任务状态
                # 注意：多账号模式不使用 self.current_run_idx (单账号专用)
                run_data.target_sequence = 0  # ✓ 从0开始（0-based索引）
                run_data.is_in_target_zone = False

                # 确保当前账号的停止标志已清除 (修正 api_instance 未定义错误)
                if hasattr(api_instance, "stop_run_flag"):
                    api_instance.stop_run_flag.clear()

                # 创建完成事件
                finished_event = threading.Event()

                # 执行任务（使用实际的提交线程）
                try:
                    # 调用实际的执行逻辑
                    thread = threading.Thread(
                        target=api_instance._run_submission_thread,  # 使用 api_instance 调用方法
                        args=(
                            run_data,
                            task_idx,
                            api_instance.api_client,  # 使用 api_instance 的 api_client
                            False,
                            finished_event,
                        ),
                        daemon=True,
                    )
                    thread.start()

                    # 标记正在执行此任务
                    tasks_executed += 1

                    # 等待任务完成或超时（最多等待任务预计时间的2倍）
                    total_time_s = sum(p[2] for p in run_data.run_coords) / 1000.0
                    timeout = max(total_time_s * 2, 300)  # 至少5分钟

                    # 监控任务进度并更新状态
                    start_wait = time.time()
                    while not finished_event.is_set():
                        if time.time() - start_wait > timeout:
                            logging.warning(f"任务执行超时: {run_data.run_name}")
                            api_instance.stop_run_flag.set()
                            break

                        # 更新当前任务进度
                        with self.lock:
                            if hasattr(run_data, "current_point_index"):
                                total_points = len(run_data.run_coords)
                                current_progress = int(
                                    run_data.current_point_index / total_points * 100
                                )
                                task_state["current_task_progress"] = current_progress
                                task_state["last_update"] = time.time()

                                # 添加点数进度信息（供前端直接使用）
                                current_idx = run_data.current_point_index
                                task_state["singleProcessedPoints"] = current_idx
                                task_state["singleTotalPoints"] = total_points

                                # 添加详细的任务数据（供前端完整恢复任务状态）
                                task_state["target_points"] = (
                                    run_data.target_points
                                    if hasattr(run_data, "target_points")
                                    else []
                                )
                                task_state["target_point_names"] = (
                                    run_data.target_point_names
                                    if hasattr(run_data, "target_point_names")
                                    else ""
                                )
                                task_state["recommended_coords"] = (
                                    run_data.recommended_coords
                                    if hasattr(run_data, "recommended_coords")
                                    else []
                                )
                                task_state["run_coords"] = (
                                    run_data.run_coords
                                    if hasattr(run_data, "run_coords")
                                    else []
                                )

                                # 添加打卡点进度信息

                                server_target_sequence_0based = getattr(
                                    run_data, "target_sequence", 0
                                )
                                task_state["checked_targets_count"] = (
                                    server_target_sequence_0based + 1
                                )  # 统一为 1-based

                                task_state["total_targets_count"] = (
                                    len(run_data.target_points)
                                    if hasattr(run_data, "target_points")
                                    else 0
                                )

                                # 添加时间和距离信息
                                task_state["elapsed_time_s"] = (
                                    time.time() - start_wait
                                )  # 当前已用时间（秒）
                                task_state["current_distance_m"] = getattr(
                                    run_data, "distance_covered_m", 0
                                )  # 当前已跑距离（米）
                                task_state["estimated_total_time_s"] = getattr(
                                    run_data, "total_run_time_s", 0
                                )  # 预计总时间（秒）
                                task_state["estimated_total_distance_m"] = getattr(
                                    run_data, "total_run_distance_m", 0
                                )  # 预计总距离（米）

                                # 添加实时位置数据
                                if current_idx > 0 and current_idx <= total_points:
                                    coord = run_data.run_coords[current_idx - 1]
                                    task_state["current_position"] = {
                                        "lon": coord[0],
                                        "lat": coord[1],
                                        "distance": getattr(
                                            run_data, "distance_covered_m", 0
                                        ),
                                        "target_sequence": getattr(
                                            run_data, "target_sequence", 0
                                        ),
                                        "point_index": current_idx,  # 添加点索引用于前端进度计算
                                    }

                        # 每5秒保存一次状态
                        if int(time.time() - start_wait) % 5 == 0:
                            with self.lock:
                                self.save_task_state(session_id, task_state)

                        time.sleep(1)

                    # 等待线程结束
                    thread.join(timeout=10)

                except Exception as e:
                    logging.error(f"任务执行失败，异常信息: {e}", exc_info=True)

                # 更新完成状态
                with self.lock:
                    task_state["completed_tasks"] = i + 1
                    task_state["progress_percent"] = int(
                        (i + 1) / len(task_indices) * 100
                    )
                    task_state["current_task_progress"] = 100
                    task_state["last_update"] = time.time()
                    self.save_task_state(session_id, task_state)

                logging.info(
                    f"任务 {i+1}/{len(task_indices)} 已完成，会话ID前缀: {session_id[:8]}"
                )

            # 所有任务完成 - 仅当至少执行了一个任务时
            if tasks_executed > 0:
                with self.lock:
                    task_state["status"] = "completed"
                    task_state["last_update"] = time.time()
                    self.save_task_state(session_id, task_state)

                logging.info(f"所有后台任务已完成，会话ID前缀: {session_id[:8]}")
            else:
                # 没有任务被执行
                with self.lock:
                    if task_state.get("status") != "error":  # 不覆盖错误状态
                        task_state["status"] = "error"
                        # 根据是否启用自动生成，设置不同的错误消息
                        if auto_generate:
                            task_state["error"] = "自动生成路径失败，请尝试手动生成路径"
                        else:
                            task_state["error"] = "所有任务都没有路径，请先生成路径"
                        task_state["last_update"] = time.time()
                        self.save_task_state(session_id, task_state)
                if auto_generate:
                    logging.error(
                        f"没有任务被执行，会话ID前缀: {session_id[:8]} - 所有自动生成路径尝试均失败"
                    )
                else:
                    logging.warning(
                        f"没有任务被执行，会话ID前缀: {session_id[:8]} - 没有可用的路径"
                    )

        except Exception as e:
            logging.error(f"后台任务执行失败，异常信息: {e}", exc_info=True)
            with self.lock:
                if session_id in self.tasks:
                    self.tasks[session_id]["status"] = "error"
                    self.tasks[session_id]["error"] = str(e)
                    self.save_task_state(session_id, self.tasks[session_id])

    def get_task_status(self, session_id):
        """获取任务状态"""
        with self.lock:
            # 先从内存中获取
            if session_id in self.tasks:
                return self.tasks[session_id]

        # 如果内存中没有，从文件加载
        task_state = self.load_task_state(session_id)
        if task_state:
            with self.lock:
                self.tasks[session_id] = task_state
            return task_state

        return None

    def stop_task(self, session_id):
        """停止后台任务"""
        with self.lock:
            if session_id in self.tasks:
                self.tasks[session_id]["status"] = "stopped"
                self.save_task_state(session_id, self.tasks[session_id])
                logging.info(f"后台任务已停止，会话ID前缀: {session_id[:8]}")
                return {"success": True, "message": "后台任务已停止"}
            return {"success": False, "message": "未找到运行中的后台任务"}

    def cleanup_old_tasks(self, max_age_hours=24):
        """清理旧的任务状态文件"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600

            for filename in os.listdir(self.task_storage_dir):
                if not filename.endswith(".json"):
                    continue

                filepath = os.path.join(self.task_storage_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        task_state = json.load(f)

                    last_update = task_state.get("last_update", 0)
                    if current_time - last_update > max_age_seconds:
                        os.remove(filepath)
                        logging.info(f"已删除旧的任务状态文件: {filename}")
                except Exception as e:
                    logging.warning(f"处理任务文件失败，文件名: {filename}，错误: {e}")
        except Exception as e:
            logging.error(f"清理旧任务文件失败，异常信息: {e}")


class MicroPixelCaptcha:

    FONT = {
        "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
        "N": ["10001", "11001", "10101", "10101", "10011", "10001", "10001"],
        "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
        "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
        "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
        "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
        "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
        "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
        "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
        "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
        "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
        "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
        "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
        "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
        "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
        "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
        "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
        "Y": ["10001", "10001", "10001", "01010", "00100", "00100", "00100"],
        "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
        "0": ["01110", "10011", "10101", "10101", "10101", "11001", "01110"],
        "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
        "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
        "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
        "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
        "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
        "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
        "7": ["11111", "00001", "00010", "00100", "00100", "00100", "00100"],
        "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
        "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    }

    def _random_string(self, length: int) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def generate(
        self, length: int = 4, scale_factor: int = 2, noise_level: float = 0.08
    ):
        """
        生成高密度微像素验证码
        :param length: 验证码字符数
        :param scale_factor: 细分倍数 (建议2或3)
        :param noise_level: 噪点比例
        """
        code = "".join(random.choices(list(self.FONT.keys()), k=length))

        # 1. 构建基础逻辑行
        char_patterns = [self.FONT.get(c, ["11111"] * 7) for c in code]
        base_rows = ["0".join(row_tuple) for row_tuple in zip(*char_patterns)]

        # 2. 像素细分与扩展
        expanded_bit_string = []
        for row in base_rows:
            # 水平扩展
            expanded_row_str = "".join([bit * scale_factor for bit in row])
            # 垂直扩展
            for _ in range(scale_factor):
                expanded_bit_string.append(expanded_row_str)

        full_bit_stream = "".join(expanded_bit_string)

        # 3. 计算 Grid 布局参数
        logic_width = length * 5 + (length - 1)
        grid_cols = logic_width * scale_factor

        # 4. 生成 HTML 像素块
        cls_con = self._random_string(10)
        cls_bg = self._random_string(5)
        cls_fg = self._random_string(5)

        pixels = []
        for bit in full_bit_stream:
            is_fg = bit == "1"
            if random.random() < noise_level:
                is_fg = not is_fg

            pixels.append(f'<span class="{cls_fg if is_fg else cls_bg}"></span>')

        html_content = "".join(pixels)

        # 5. CSS 样式优化 (黑白风格)
        pixel_size = 12 // scale_factor
        if pixel_size < 4:
            pixel_size = 4

        # 6. 计算实际渲染尺寸
        # 验证码总行数固定为7（字体高度）
        grid_rows = 7 * scale_factor
        # 宽度计算：列数 * (像素大小 + 间隙) - 最后一个间隙 + 两侧padding + 两侧border
        captcha_width = grid_cols * (pixel_size + 1) - 1 + 2 * 10 + 2 * 1
        # 高度计算：行数 * (像素大小 + 间隙) - 最后一个间隙 + 两侧padding + 两侧border
        captcha_height = grid_rows * (pixel_size + 1) - 1 + 2 * 10 + 2 * 1

        css = f"""<style>
.{cls_con}{{
    display:grid;
    grid-template-columns:repeat({grid_cols}, {pixel_size}px);
    gap:1px;
    background:#000;
    padding:10px;
    width:fit-content;
    border:1px solid #333;
}}
.{cls_con} span{{
    width:{pixel_size}px;
    height:{pixel_size}px;
    display:block;
    border-radius:0;
}}
.{cls_bg}{{background:#000;}}
.{cls_fg}{{background:#fff;}}
</style>"""

        full_html = f'<div class="{cls_con}">{html_content}</div>{css}'
        return code, full_html, captcha_width, captcha_height


class ChromeBrowserPool:
    """管理服务器端Chrome浏览器实例，用于执行JS计算 (线程本地安全模式)"""

    def __init__(self, headless=True, max_instances=5):
        self.headless = headless
        self.max_instances = max_instances
        # self.playwright = None # 移除
        # self.browser = None # 移除
        # self.contexts = {}  # 移除
        # self.lock = threading.Lock() # 移除

        # 使用 threading.local() 存储线程私有的资源
        self.thread_local = threading.local()
        # _initialize() 将在每个线程首次使用时调用
        # self._initialize() # 移除

    def _initialize_for_thread(self):
        """在每个线程中首次使用时初始化Playwright和浏览器"""
        # 检查当前线程是否已经初始化
        if not hasattr(self.thread_local, "playwright"):
            try:
                logging.info(
                    f"正在为线程 {threading.current_thread().name} 初始化 Playwright..."
                )
                self.thread_local.playwright = sync_playwright().start()
                self.thread_local.browser = (
                    self.thread_local.playwright.chromium.launch(
                        headless=self.headless,
                        args=["--no-sandbox", "--disable-setuid-sandbox"],
                    )
                )
                # contexts 也是线程私有的
                self.thread_local.contexts = {}
                logging.info(
                    f"Chrome浏览器已为线程 {threading.current_thread().name} 启动 (headless={self.headless})"
                )
            except Exception as e:
                logging.error(
                    f"为线程 {threading.current_thread().name} 启动Chrome失败: {e}",
                    exc_info=True,
                )
                raise

    def get_context(self, session_id):
        """获取或创建指定会话的浏览器上下文（线程安全）"""
        # 确保当前线程已初始化
        self._initialize_for_thread()

        # 从当前线程的存储中获取 contexts
        contexts = self.thread_local.contexts

        if session_id not in contexts:
            # 从当前线程的存储中获取 browser
            browser = self.thread_local.browser
            # 创建新的浏览器上下文
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            )
            page = context.new_page()
            contexts[session_id] = {"context": context, "page": page}
            logging.info(
                f"为会话 {session_id} 在线程 {threading.current_thread().name} 中创建Chrome上下文"
            )
        return contexts[session_id]

    def execute_js(self, session_id, script, *args):
        """在指定会话的Chrome中执行JavaScript代码（线程安全）"""
        try:
            # 确保当前线程已初始化（如果尚未初始化）
            self._initialize_for_thread()
            # get_context 已经是线程安全的
            ctx = self.get_context(session_id)
            page = ctx["page"]
            # 修复BUG：Playwright的evaluate方法只接受一个 'arg' 参数。
            # 必须将所有Python参数 (*args) 包装成一个列表 (list(args))
            # 传递给 'arg'，以便在JS中作为 arguments[0], arguments[1] 等访问。
            result = page.evaluate(script, list(args))
            return result
        except Exception as e:
            logging.error(
                f"执行JS失败 (session={session_id}, thread={threading.current_thread().name}): {e}",
                exc_info=True,
            )
            return None

    def close_context(self, session_id):
        """关闭指定会话的浏览器上下文（线程安全）"""
        # 检查当前线程是否有资源
        if not hasattr(self.thread_local, "contexts"):
            return  # 此线程未初始化，无需关闭

        contexts = self.thread_local.contexts
        if session_id in contexts:
            try:
                ctx = contexts[session_id]
                ctx["context"].close()
                del contexts[session_id]
                logging.info(
                    f"关闭会话 {session_id} 在线程 {threading.current_thread().name} 中的Chrome上下文"
                )
            except Exception as e:
                logging.error(f"关闭上下文失败: {e}")

    def cleanup_thread(self):
        """清理当前线程的所有Playwright资源"""
        # 检查当前线程是否有资源
        if hasattr(self.thread_local, "playwright"):
            try:
                logging.info(
                    f"正在清理线程 {threading.current_thread().name} 的 Playwright 资源..."
                )
                contexts = getattr(self.thread_local, "contexts", {})
                # 1. 关闭所有上下文
                for session_id, ctx in contexts.items():
                    try:
                        ctx["context"].close()
                    except Exception as e:
                        logging.warning(f"关闭会话 {session_id} 上下文失败: {e}")
                self.thread_local.contexts.clear()

                # 2. 关闭浏览器
                if hasattr(self.thread_local, "browser"):
                    self.thread_local.browser.close()

                # 3. 停止 Playwright
                self.thread_local.playwright.stop()

                # 4. 清理 thread_local 属性
                del self.thread_local.playwright
                del self.thread_local.browser
                del self.thread_local.contexts

                logging.info(
                    f"线程 {threading.current_thread().name} 的 Playwright 资源清理完毕。"
                )
            except Exception as e:
                logging.error(
                    f"清理线程 {threading.current_thread().name} 资源时出错: {e}",
                    exc_info=True,
                )


def _cleanup_playwright():
    """
    在程序退出时清理Playwright资源。

    功能说明：
    - 这是一个注册在atexit的清理函数，确保程序退出时正确关闭所有浏览器实例
    - 防止遗留的浏览器进程占用系统资源

    清理流程：
    1. 检查chrome_pool全局实例是否存在
    2. 调用chrome_pool.cleanup()关闭所有浏览器
    3. 记录清理结果

    异常处理：
    - 使用try-except捕获清理过程中的所有异常
    - exc_info=False避免在退出时打印完整堆栈（可能引起混淆）
    - 只记录错误，不重新抛出，确保程序正常退出

    设计考虑：
    - 使用global访问chrome_pool而不是参数传递，因为atexit不支持参数
    - 判空检查避免未初始化时的错误

    使用场景：
    - 正常退出（Ctrl+C、关闭终端）
    - 异常退出（未捕获的异常）
    - 系统信号（SIGTERM等）

    注意：
    - 此函数由atexit.register()自动调用，不需手动调用
    - 执行时机在Python解释器关闭前
    """
    global chrome_pool
    if chrome_pool:
        logging.info("捕获到程序退出信号，正在清理 Playwright 资源...")
        try:
            # 修正：调用线程本地的清理方法 cleanup_thread()，而不是不存在的 cleanup()
            chrome_pool.cleanup_thread()
            logging.info("Playwright浏览器自动化框架资源清理完成")
        except Exception as e:
            # 在退出时尽量不抛出新异常，只记录错误
            logging.error(f"清理 Playwright 资源时发生错误: {e}", exc_info=False)
    else:
        logging.debug("Playwright 池未初始化，无需清理。")


def start_background_auto_attendance(args):
    """
    在服务器启动时扫描所有.ini配置文件，为启用自动签到的账号启动后台工作线程。

    功能说明：
    - 自动发现并加载所有启用了auto_attendance_enabled的账号配置
    - 根据账号数量智能选择单账号或多账号模式
    - 在后台守护线程中持续运行，无需用户干预

    工作模式：

    **单账号模式**（只有1个启用自动签到的账号）：
    - 为该账号创建独立的Api实例
    - 启动单独的_auto_refresh_worker线程
    - 资源占用更少，适合个人使用

    **多账号模式**（2个或更多账号）：
    - 所有账号共享一个Api实例
    - 启动_multi_auto_attendance_worker统一管理
    - 更高效的资源利用，适合批量管理

    执行流程：
    1. 扫描SCHOOL_ACCOUNTS_DIR目录中的所有.ini文件
    2. 读取每个文件的配置，检查auto_attendance_enabled参数
    3. 收集所有启用自动签到的账号信息
    4. 根据账号数量选择模式并启动相应的后台线程

    参数说明：
    - args: 命令行参数对象，包含--no-auto-start等配置

    异常处理：
    - 单个账号加载失败不影响其他账号
    - 登录失败会记录错误但不终止服务
    - 所有异常都会记录到日志中

    全局变量：
    - _background_service_api: 保持Api实例存活的引用（单账号模式）
    - chrome_pool: 共享的浏览器池（如果需要）

    设计考虑：
    - 使用daemon线程确保主程序退出时自动停止
    - 临时创建Api实例仅用于读取配置，避免资源浪费
    - 账号信息缓存在内存中，避免重复读取文件

    注意事项：
    - 此函数应在Flask服务器启动前调用
    - 需要确保SCHOOL_ACCOUNTS_DIR目录存在且有读权限
    - 账号的.ini文件必须包含密码和auto_attendance_enabled配置

    """
    try:
        logging.info("正在启动后台自动签到服务...")

        accounts_dir = SCHOOL_ACCOUNTS_DIR

        if not os.path.exists(accounts_dir):
            logging.warning(f"后台签到：未找到账号目录 {accounts_dir}，跳过。")
            return

        # 收集所有启用自动签到的账号
        enabled_accounts = []

        for filename in os.listdir(accounts_dir):
            if filename.endswith(".ini"):
                username = os.path.splitext(filename)[0]
                try:
                    # 临时创建一个Api实例来加载配置
                    temp_api = Api(args)
                    password = temp_api._load_config(username)

                    if not password:
                        logging.debug(
                            f"后台签到：跳过账号 {username}，因为未在 {filename} 中找到密码。"
                        )
                        continue

                    # 检查是否启用了自动签到
                    if temp_api.params.get("auto_attendance_enabled", False):
                        enabled_accounts.append(
                            {
                                "username": username,
                                "password": password,
                                "params": dict(temp_api.params),
                            }
                        )
                        logging.info(f"后台签到：找到启用自动签到的账号: {username}")
                    else:
                        logging.debug(
                            f"后台签到：账号 {username} 未启用自动签到，跳过。"
                        )

                except Exception as e:
                    logging.error(
                        f"后台签到：加载账号 {username} 失败: {e}", exc_info=True
                    )

        if not enabled_accounts:
            logging.info("后台签到：未找到启用自动签到的账号。")
            return

        # 根据账号数量选择模式
        if len(enabled_accounts) == 1:
            # 单账号模式：为该账号创建独立的Api实例
            account = enabled_accounts[0]
            logging.info(f"后台签到：使用单账号模式，账号: {account['username']}")

            service_api = Api(args)
            service_api.is_multi_account_mode = False
            service_api.params = account["params"]

            # 执行登录
            try:
                login_result = service_api.login(
                    account["username"], account["password"]
                )
                if login_result.get("success"):
                    logging.info(f"后台签到：账号 {account['username']} 登录成功")

                    # 启动单账号自动刷新线程
                    service_api.stop_auto_refresh.clear()
                    service_api.auto_refresh_thread = threading.Thread(
                        target=service_api._auto_refresh_worker,
                        daemon=True,
                        name=f"BackgroundAttendance-{account['username']}",
                    )
                    service_api.auto_refresh_thread.start()

                    # 保持实例存活
                    globals()["_background_service_api"] = service_api
                    logging.info(f"后台签到：单账号模式启动成功")
                else:
                    logging.error(
                        f"后台签到：账号 {account['username']} 登录失败: {login_result.get('message')}"
                    )
            except Exception as e:
                logging.error(
                    f"后台签到：账号 {account['username']} 登录时发生错误: {e}",
                    exc_info=True,
                )

        else:
            # 多账号模式：所有账号共享一个Api实例
            logging.info(f"后台签到：使用多账号模式，共 {len(enabled_accounts)} 个账号")

            service_api = Api(args)
            service_api.is_multi_account_mode = True
            service_api._load_global_config()
            service_api.global_params["auto_attendance_enabled"] = True

            # 为每个账号创建AccountSession
            for account in enabled_accounts:
                try:
                    acc_session = AccountSession(
                        account["username"], account["password"], service_api
                    )
                    acc_session.params = account["params"]
                    service_api.accounts[account["username"]] = acc_session
                except Exception as e:
                    logging.error(
                        f"后台签到：创建账号会话失败 {account['username']}: {e}",
                        exc_info=True,
                    )

            # 启动多账号自动刷新线程
            service_api.stop_multi_auto_refresh.clear()
            service_api.multi_auto_refresh_thread = threading.Thread(
                target=service_api._multi_auto_attendance_worker,
                daemon=True,
                name="BackgroundAttendanceWorker-Multi",
            )
            service_api.multi_auto_refresh_thread.start()

            # 保持实例存活
            globals()["_background_service_api"] = service_api
            logging.info(
                f"后台签到：多账号模式启动成功，已加载 {len(service_api.accounts)} 个账号"
            )

    except Exception as e:
        logging.error(f"启动后台自动签到服务时发生严重错误: {e}", exc_info=True)


# ============================================================================
# SSL/HTTPS 配置和证书管理相关函数
# 这些函数用于加载、验证和管理SSL证书，支持HTTPS服务
# ============================================================================


def load_ssl_config():
    """
    从config.ini文件加载SSL配置。

    功能说明：
    1. 读取配置文件中的[SSL]节
    2. 解析SSL相关的配置项（启用状态、证书路径、仅HTTPS模式等）
    3. 返回配置字典供后续使用

    返回值：
        dict: 包含SSL配置的字典，键包括：
            - ssl_enabled (bool): 是否启用SSL
            - ssl_cert_path (str): 证书文件路径
            - ssl_key_path (str): 私钥文件路径
            - https_only (bool): 是否仅允许HTTPS访问
        如果配置文件不存在或读取失败，返回默认配置（SSL禁用）
    """
    # 定义配置文件路径（相对于程序根目录）
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")

    # 创建配置解析器对象
    config = configparser.ConfigParser()

    # 默认的SSL配置（向后兼容，默认禁用SSL）
    # 这确保了即使没有配置文件，程序也能正常以HTTP模式运行
    default_config = {
        "ssl_enabled": False,  # 默认不启用SSL
        "ssl_cert_path": "ssl/fullchain.pem",  # 默认证书路径
        "ssl_key_path": "ssl/privkey.key",  # 默认密钥路径
        "https_only": False,  # 默认允许HTTP访问
    }

    try:
        # 尝试读取配置文件
        # 如果文件不存在，read()方法会返回空列表，不会抛出异常
        if not os.path.exists(config_file):
            logging.warning(f"配置文件 {config_file} 不存在，使用默认SSL配置（禁用）")
            return default_config

        # 读取配置文件内容
        config.read(config_file, encoding="utf-8")

        # 检查[SSL]节是否存在
        if not config.has_section("SSL"):
            logging.warning("配置文件中未找到[SSL]节，使用默认SSL配置（禁用）")
            return default_config

        # 从配置文件中读取各项配置，使用getboolean和get方法
        # getboolean会自动将'true'/'false'字符串转换为布尔值
        ssl_config = {
            "ssl_enabled": config.getboolean("SSL", "ssl_enabled", fallback=False),
            "ssl_cert_path": config.get(
                "SSL", "ssl_cert_path", fallback="ssl/fullchain.pem"
            ),
            "ssl_key_path": config.get(
                "SSL", "ssl_key_path", fallback="ssl/privkey.key"
            ),
            "https_only": config.getboolean("SSL", "https_only", fallback=False),
        }

        # 记录加载的配置信息（不记录路径细节，避免泄露敏感信息）
        logging.info(
            f"SSL配置加载成功: enabled={ssl_config['ssl_enabled']}, https_only={ssl_config['https_only']}"
        )

        return ssl_config

    except Exception as e:
        # 如果读取配置文件时发生任何错误，记录错误并返回默认配置
        # 这样可以确保程序不会因为配置问题而崩溃
        logging.error(f"加载SSL配置时发生错误: {e}，使用默认配置（禁用SSL）")
        return default_config


def save_ssl_config(ssl_config):
    """
    将SSL配置保存到config.ini文件。

    参数：
        ssl_config (dict): 包含SSL配置的字典，键应包括：
            - ssl_enabled (bool): 是否启用SSL
            - ssl_cert_path (str): 证书文件路径
            - ssl_key_path (str): 私钥文件路径
            - https_only (bool): 是否仅允许HTTPS访问

    返回值：
        bool: 保存成功返回True，失败返回False
    """
    # 定义配置文件路径
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")

    # 创建配置解析器对象
    config = configparser.ConfigParser()

    try:
        # 读取完整的 config.ini 文件到 ConfigParser 对象
        # 这样可以保留所有现有的节和配置项，而不仅仅是 [SSL] 节
        if os.path.exists(config_file):
            config.read(config_file, encoding="utf-8")
        else:
            # 如果配置文件不存在，使用默认配置初始化
            logging.warning("config.ini 文件不存在，将创建新的配置文件")
            config = _get_default_config()

        # 确保[SSL]节存在，如果不存在则创建
        if not config.has_section("SSL"):
            config.add_section("SSL")

        # 将字典中的配置写入到[SSL]节
        # 布尔值会自动转换为'true'/'false'字符串
        config.set(
            "SSL", "ssl_enabled", str(ssl_config.get("ssl_enabled", False)).lower()
        )
        config.set(
            "SSL", "ssl_cert_path", ssl_config.get("ssl_cert_path", "ssl/fullchain.pem")
        )
        config.set(
            "SSL", "ssl_key_path", ssl_config.get("ssl_key_path", "ssl/privkey.key")
        )
        config.set(
            "SSL", "https_only", str(ssl_config.get("https_only", False)).lower()
        )

        # 使用 _write_config_with_comments 函数写入配置文件
        # 这个函数会保留所有注释和配置项，不会造成数据丢失
        _write_config_with_comments(config, config_file)

        logging.info("SSL配置已成功保存到配置文件")
        return True

    except Exception as e:
        # 记录保存失败的错误信息
        logging.error(f"保存SSL配置时发生错误: {e}")
        return False


def validate_ssl_certificate(cert_path, key_path):
    """
    验证SSL证书文件和密钥文件是否有效。

    功能说明：
    1. 检查证书文件和密钥文件是否存在
    2. 检查文件是否可读
    3. 验证证书格式和有效期（基础验证）
    4. 检查证书和密钥是否匹配

    参数：
        cert_path (str): 证书文件路径（相对或绝对路径）
        key_path (str): 密钥文件路径（相对或绝对路径）

    返回值：
        tuple: (bool, str, dict)
            - bool: 验证是否通过
            - str: 错误消息（验证通过时为空字符串）
            - dict: 证书信息字典（验证通过时包含证书详细信息，失败时为空）
    """
    # 如果路径是相对路径，转换为相对于程序根目录的绝对路径
    if not os.path.isabs(cert_path):
        cert_path = os.path.join(os.path.dirname(__file__), cert_path)
    if not os.path.isabs(key_path):
        key_path = os.path.join(os.path.dirname(__file__), key_path)

    # 1. 检查证书文件是否存在
    if not os.path.exists(cert_path):
        error_msg = f"证书文件不存在: {cert_path}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 2. 检查密钥文件是否存在
    if not os.path.exists(key_path):
        error_msg = f"密钥文件不存在: {key_path}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 3. 检查证书文件是否可读
    if not os.access(cert_path, os.R_OK):
        error_msg = f"证书文件不可读（权限不足）: {cert_path}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 4. 检查密钥文件是否可读
    if not os.access(key_path, os.R_OK):
        error_msg = f"密钥文件不可读（权限不足）: {key_path}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 5. 尝试读取证书文件内容，验证基本格式
    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert_content = f.read()
            # 检查是否包含PEM格式的标识头
            if "-----BEGIN CERTIFICATE-----" not in cert_content:
                error_msg = f"证书文件格式无效（不是PEM格式）: {cert_path}"
                logging.error(error_msg)
                return False, error_msg, {}
    except Exception as e:
        error_msg = f"读取证书文件时发生错误: {e}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 6. 尝试读取密钥文件内容，验证基本格式
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            key_content = f.read()
            # 检查是否包含PEM格式的标识头（支持多种私钥格式）
            valid_key_headers = [
                "-----BEGIN PRIVATE KEY-----",
                "-----BEGIN RSA PRIVATE KEY-----",
                "-----BEGIN EC PRIVATE KEY-----",
                "-----BEGIN DSA PRIVATE KEY-----",
            ]
            if not any(header in key_content for header in valid_key_headers):
                error_msg = f"密钥文件格式无效（不是PEM格式）: {key_path}"
                logging.error(error_msg)
                return False, error_msg, {}
    except Exception as e:
        error_msg = f"读取密钥文件时发生错误: {e}"
        logging.error(error_msg)
        return False, error_msg, {}

    # 7. 尝试使用OpenSSL库解析证书并提取信息（如果可用）
    # 注意：这里使用基础的文件验证，更复杂的证书验证需要pyOpenSSL库
    cert_info = {
        "cert_path": cert_path,
        "key_path": key_path,
        "valid": True,
        "message": "证书文件格式验证通过",
    }

    # 尝试导入ssl模块进行更详细的验证（Python标准库）
    try:
        import ssl

        # 使用ssl.SSLContext来加载证书，这会进行更严格的验证
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)

        # 如果没有抛出异常，说明证书和密钥匹配且有效
        cert_info["message"] = "证书和密钥验证通过，可以安全使用"
        logging.info(f"SSL证书验证成功: {cert_path}")

    except Exception as e:
        # 如果ssl模块验证失败，记录警告但不阻止使用
        # 因为某些环境可能没有完整的SSL支持
        error_msg = f"SSL证书深度验证失败: {e}，但基础格式验证已通过"
        logging.warning(error_msg)
        cert_info["message"] = error_msg
        # 仍然返回True，因为基础验证已通过

    return True, "", cert_info


def get_ssl_certificate_info(cert_path):
    """
    获取SSL证书的详细信息（如有效期、颁发者、主题等）。

    参数：
        cert_path (str): 证书文件路径

    返回值：
        dict: 包含证书详细信息的字典，失败时返回空字典
    """
    # 如果路径是相对路径，转换为绝对路径
    if not os.path.isabs(cert_path):
        cert_path = os.path.join(os.path.dirname(__file__), cert_path)

    # 默认返回值
    cert_info = {}

    try:
        # 导入ssl和OpenSSL相关模块
        import ssl
        from datetime import datetime

        # 读取证书文件
        with open(cert_path, "rb") as f:
            cert_data = f.read()

        # 使用ssl模块解析证书
        # 注意：这需要证书是PEM格式
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend

        # 加载证书
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # 提取证书信息
        cert_info = {
            "subject": cert.subject.rfc4514_string(),  # 证书主题（服务器域名等）
            "issuer": cert.issuer.rfc4514_string(),  # 颁发者
            "version": cert.version.name,  # 证书版本
            "serial_number": str(cert.serial_number),  # 序列号
            "not_before": cert.not_valid_before_utc.isoformat(),  # 生效日期
            "not_after": cert.not_valid_after_utc.isoformat(),  # 过期日期
            "is_expired": datetime.now()
            > cert.not_valid_after_utc.replace(tzinfo=None),  # 是否已过期
        }

        # 提取SAN（Subject Alternative Names）扩展
        try:
            san_ext = cert.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            cert_info["san"] = [name.value for name in san_ext.value]
        except x509.ExtensionNotFound:
            cert_info["san"] = []

        logging.info(f"成功获取证书信息: {cert_path}")

    except ImportError:
        # 如果cryptography库不可用，使用简化的方法
        logging.warning("cryptography库不可用，无法获取详细的证书信息")
        cert_info = {
            "error": "需要安装cryptography库才能查看详细证书信息",
            "install_hint": "pip install cryptography",
        }
    except Exception as e:
        # 记录错误但不抛出异常
        logging.error(f"获取证书信息时发生错误: {e}")
        cert_info = {"error": f"读取证书信息失败: {str(e)}"}

    return cert_info


def start_web_server(args_param):
    """
    启动Flask Web服务器主函数，集成SocketIO实时通信和Chrome浏览器自动化。
    """
    global chrome_pool, background_task_manager, web_sessions, web_sessions_lock, session_file_locks, session_file_locks_lock, session_activity, session_activity_lock, args

    # ========== 新增：记录服务器启动时间 ==========
    # 使用全局变量记录服务器启动时间，用于计算运行时长（uptime）
    # time.time() 返回当前时间的时间戳（自1970年1月1日以来的秒数）
    global server_start_time
    server_start_time = time.time()
    # 记录启动时间到日志（使用人类可读的格式）
    logging.info(
        f"服务器启动时间: {datetime.datetime.fromtimestamp(server_start_time).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    # ========== 结束：服务器启动时间记录 ==========

    # Make args available globally for Flask routes
    # 将命令行参数存储为全局变量，供Flask路由函数访问
    args = args_param

    # 用于速率限制的简单内存缓存
    global cache
    cache = {}
    # 用于存储待验证短信验证码
    global sms_verification_codes
    sms_verification_codes = {}

    # --- 显式初始化/重置内存锁状态 ---
    # 重置所有会话相关的全局变量，防止程序重启后出现状态污染
    web_sessions = {}
    web_sessions_lock = threading.Lock()
    session_file_locks = {}
    session_file_locks_lock = threading.Lock()
    session_activity = {}
    session_activity_lock = threading.Lock()
    logging.info("内存锁和会话状态已重置。")
    # --- 结束新增 ---

    # 初始化Chrome浏览器池
    try:
        chrome_pool = ChromeBrowserPool(headless=getattr(args, "headless", True))
        logging.info("Chrome浏览器池初始化成功")
        atexit.register(_cleanup_playwright)
        logging.info("已注册 Playwright 退出清理函数。")
    except Exception as e:
        logging.error(f"无法初始化Chrome浏览器池: {e}")
        sys.exit(1)

    # 初始化后台任务管理器
    try:
        background_task_manager = BackgroundTaskManager()
        logging.info("后台任务管理器初始化成功")

        logging.info("程序启动：正在清理所有历史后台任务记录（内存和文件）...")
        cleaned_files_count = 0
        if background_task_manager and hasattr(
            background_task_manager, "task_storage_dir"
        ):
            task_dir = background_task_manager.task_storage_dir
            if os.path.exists(task_dir):
                # 清理内存
                with background_task_manager.lock:
                    background_task_manager.tasks.clear()
                # 清理文件
                for filename in os.listdir(task_dir):
                    if filename.endswith(".json"):
                        file_path = os.path.join(task_dir, filename)
                        try:
                            os.remove(file_path)
                            cleaned_files_count += 1
                        except Exception as e:
                            logging.error(f"无法删除后台任务文件 {filename}: {e}")
            logging.info(
                f"已清空后台任务管理器内存状态，并删除了 {cleaned_files_count} 个任务状态文件。"
            )
        else:
            logging.warning(
                "无法清理后台任务文件：BackgroundTaskManager 或其 task_storage_dir 未定义。"
            )

    except Exception as e:
        logging.error(f"无法初始化后台任务管理器: {e}")
        sys.exit(1)

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)  # 生成安全的密钥
    CORS(app)  # 允许跨域请求

    # 声明 socketio 为全局变量
    global socketio
    # 初始化 SocketIO
    socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

    # 会话配置
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=7)  # 会话保持7天

    # ===== 登录验证装饰器 =====
    def login_required(f):
        """
        一个装饰器，用于验证用户是否已登录。
        它检查 X-Session-ID，验证会话，并将用户信息存储在 g 对象中。
        """

        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            session_id = request.headers.get("X-Session-ID", "")
            api_instance = None
            is_authenticated = False
            auth_username = None

            # 1. 检查会话ID是否存在且在内存中
            if session_id:
                with web_sessions_lock:
                    if session_id in web_sessions:
                        api_instance = web_sessions[session_id]
                        # 检查是否已通过认证（非游客或已登录的系统用户）
                        is_authenticated = getattr(
                            api_instance, "is_authenticated", False
                        )
                        auth_username = getattr(api_instance, "auth_username", None)

            # 2. 如果未认证，返回401
            if not is_authenticated or not api_instance or not auth_username:
                return jsonify({"success": False, "message": "未登录或会话无效"}), 401

            # 3. 检查是否为游客
            if getattr(api_instance, "is_guest", False):
                return jsonify({"success": False, "message": "游客无权访问此功能"}), 403

            # 4. 认证成功，将用户信息存入g (Flask的请求上下文)
            g.user = auth_username
            g.api_instance = api_instance

            # 5. 执行原始的路由函数
            return f(*args, **kwargs)

        return decorated_function

    # ===============================

    # ============================================================
    # IP封禁全局检查 - before_request拦截器
    # 在所有请求之前执行，检查IP是否被封禁
    # ============================================================
    @app.before_request
    def check_ip_ban_before_request():
        """
        全局IP封禁检查拦截器
        """
        # 获取客户端IP地址
        client_ip = request.remote_addr

        # 跳过静态资源和健康检查端点（这些不需要IP封禁检查）
        # 静态资源路径示例：/static/, /css/, /js/, /default_avatar.png
        if (
            request.path.startswith("/static/")
            or request.path.startswith("/css/")
            or request.path.startswith("/js/")
            or request.path == "/health"
            or request.path.endswith(".png")
            or request.path.endswith(".jpg")
            or request.path.endswith(".ico")
        ):
            return None  # 允许请求继续处理

        # 检查IP是否被全局封禁（scope='all'）
        # check_ip_ban函数定义在下方，用于检查IP封禁列表
        is_banned = check_ip_ban(client_ip, scope="all")

        if is_banned:
            # IP被全局封禁，返回封禁提示页面
            logging.warning(
                f"[IP封禁] 全局封禁拦截：IP {client_ip} 尝试访问 {request.path}"
            )

            # 返回HTML格式的封禁提示页面（使用简单的内联HTML）
            banned_html = (
                """
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>访问被拒绝</title>
                <style>
                    body {
                        font-family: 'Microsoft YaHei', Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                        color: #333;
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 15px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    h1 {
                        color: #e74c3c;
                        font-size: 48px;
                        margin: 0 0 20px 0;
                    }
                    p {
                        font-size: 18px;
                        color: #555;
                        line-height: 1.6;
                    }
                    .ip {
                        background: #f8f9fa;
                        padding: 10px;
                        border-radius: 5px;
                        font-family: monospace;
                        color: #495057;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚫 访问被拒绝</h1>
                    <p>您的IP地址已被系统封禁。</p>
                    <p>如有疑问，请联系系统管理员。</p>
                    <div class="ip">您的IP: """
                + client_ip
                + """</div>
                </div>
            </body>
            </html>
            """
            )
            return make_response(banned_html, 403)

        # IP未被封禁，允许请求继续处理
        return None

    # ====================
    # 认证相关API路由
    # ====================

    # ====================
    # 辅助函数：线程安全的会话管理
    # ====================

    def get_session_user_safe(
        session_id, required_permission=None, require_super_admin=False
    ):
        """
        【并发安全辅助函数】线程安全地获取会话用户信息并验证权限

        功能说明：
        1. 使用锁保护web_sessions字典的并发访问
        2. 验证会话有效性和用户认证状态
        3. 提取用户信息（在锁保护范围内）
        4. 释放锁后执行权限检查（避免长时间持锁）

        参数:
            session_id (str): 会话ID，从请求头X-Session-ID获取
            required_permission (str, optional): 需要检查的权限名称，如'manage_users'
            require_super_admin (bool, optional): 是否要求超级管理员权限

        返回:
            tuple: (success: bool, result: dict或Response)
            - 成功时: (True, {"username": str, "group": str, "api_instance": object})
            - 失败时: (False, jsonify({...})) - 可直接返回给前端的错误响应

        使用示例：
            success, result = get_session_user_safe(session_id, 'manage_users')
            if not success:
                return result  # 返回错误响应
            username = result['username']  # 使用用户信息

        线程安全说明：
        - 函数内部使用web_sessions_lock确保线程安全
        - 只在锁内访问web_sessions字典和api_instance属性
        - 耗时的权限检查操作在锁外执行，避免阻塞其他请求
        """
        # 使用锁保护对共享资源web_sessions的访问
        with web_sessions_lock:
            # 验证会话ID的存在性和有效性
            if not session_id or session_id not in web_sessions:
                # 返回401未授权错误
                return False, jsonify({"success": False, "message": "未授权"}), 401

            # 从会话字典中获取API实例对象
            api_instance = web_sessions[session_id]

            # 检查用户是否已通过认证（是否有auth_username属性）
            if not hasattr(api_instance, "auth_username"):
                # 返回401未登录错误
                return False, jsonify({"success": False, "message": "未登录"}), 401

            # 在锁保护范围内提取用户信息
            # 这样可以确保读取的是一致的状态，避免竞态条件
            user_info = {
                "username": api_instance.auth_username,
                "group": getattr(api_instance, "auth_group", "user"),
                "api_instance": api_instance,  # 某些情况下可能需要完整的实例
            }
        # 锁已释放，现在可以安全地执行耗时操作

        # 如果要求超级管理员权限
        if require_super_admin:
            if user_info["group"] != "super_admin":
                # 返回403权限不足错误
                return (
                    False,
                    jsonify({"success": False, "message": "仅超级管理员可执行此操作"}),
                    403,
                )

        # 如果需要检查特定权限
        if required_permission:
            # 调用权限系统检查用户是否拥有指定权限
            # 这个操作可能较耗时（需要查询配置文件），所以在锁外执行
            if not auth_system.check_permission(
                user_info["username"], required_permission
            ):
                # 返回403权限不足错误
                return (
                    False,
                    jsonify(
                        {
                            "success": False,
                            "message": f"权限不足：需要 {required_permission} 权限",
                        }
                    ),
                    403,
                )

        # 验证通过，返回成功和用户信息
        return True, user_info, 200

    @app.route("/auth/register", methods=["POST"])
    def auth_register():
        """
        用户注册API端点（已升级支持手机号、昵称、头像）。
        """
        try:

            # 确保 configparser 和 os 模块已在文件顶部导入
            config = configparser.ConfigParser()
            if os.path.exists(CONFIG_FILE):
                config.read(CONFIG_FILE, encoding="utf-8")

            # 1. 解析请求数据（支持JSON和表单两种方式）
            content_type = request.headers.get("Content-Type", "").lower()

            if "application/json" in content_type:
                # 备用：如果请求是纯 JSON (没有头像上传)
                data = request.get_json() or {}
            else:
                # 核心：处理 multipart/form-data 或 x-www-form-urlencoded
                # request.form 会自动解析 FormData 中的文本字段。
                data = request.form.to_dict()

            # 2. 提取基本字段并去除首尾空格
            auth_username = data.get("auth_username", "").strip()
            auth_password = data.get("auth_password", "").strip()
            phone = data.get("phone", "").strip()
            nickname = data.get("nickname", "").strip()
            sms_code = data.get("sms_code", "").strip()
            captcha_input = data.get("captcha", "").strip()  # 获取用户输入的验证码
            captcha_id = data.get("captcha_id", "").strip()  # 获取验证码ID

            # 3. 验证图形验证码（必须首先验证，防止恶意注册）
            is_captcha_valid, captcha_error_msg = verify_captcha(
                captcha_id, captcha_input
            )
            if not is_captcha_valid:
                return jsonify({"success": False, "message": captcha_error_msg})

            # 4. 验证必填字段
            if not auth_username or not auth_password:
                return jsonify({"success": False, "message": "用户名和密码不能为空"})

            # 5. 验证用户名不包含中文字符（防止显示和排序问题）
            if re.search(r"[\u4e00-\u9fff]", auth_username):
                return jsonify({"success": False, "message": "用户名不能包含中文字符"})

            # 6. 验证手机号格式（如果提供）
            if phone and not re.match(r"^1[3-9]\d{9}$", phone):
                return jsonify({"success": False, "message": "手机号格式不正确"})

            # 7. 校验短信验证码（如果启用了注册验证功能）
            if (
                config.get(
                    "Features", "enable_phone_registration_verify", fallback="false"
                ).lower()
                == "true"
            ):
                if not phone:
                    return jsonify({"success": False, "message": "注册需要填写手机号"})
                if not sms_code:
                    return jsonify({"success": False, "message": "请输入短信验证码"})

                # 查找验证码记录
                code_verified = False
                if phone in sms_verification_codes:
                    stored_code, expires_at = sms_verification_codes[phone]

                    if time.time() > expires_at:
                        # 验证码过期
                        del sms_verification_codes[phone]
                        return jsonify(
                            {"success": False, "message": "验证码已过期，请重新获取"}
                        )

                    if stored_code == sms_code:
                        # 验证成功
                        code_verified = True
                        del sms_verification_codes[phone]  # 验证码一次性使用

                if not code_verified:
                    return jsonify({"success": False, "message": "验证码错误或已过期"})

            # 8. 处理头像上传（如果提供）
            avatar_url = "default_avatar.png"  # 默认头像
            avatar_file = request.files.get("avatar")
            avatar_sha256_hash = None  # 用于注册后更新索引

            if avatar_file and avatar_file.filename:
                # 验证文件类型（仅允许图片）
                allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}
                file_ext = avatar_file.filename.rsplit(".", 1)[-1].lower()
                if file_ext not in allowed_extensions:
                    return jsonify(
                        {
                            "success": False,
                            "message": "头像文件格式不支持，请使用png/jpg/gif",
                        }
                    )

                # 读取文件内容
                file_content = avatar_file.read()

                # 验证文件大小（限制5MB）
                max_size = 5 * 1024 * 1024  # 5MB
                if len(file_content) > max_size:
                    return (
                        jsonify(
                            {
                                "success": False,
                                "message": "文件过大，请上传小于5MB的图片",
                            }
                        ),
                        400,
                    )

                try:
                    # 使用PIL打开图片并转换为PNG格式
                    img = Image.open(io.BytesIO(file_content))

                    # 转换为RGB模式（PNG不支持CMYK等模式）
                    if img.mode in ("RGBA", "LA", "P"):
                        pass  # 保留透明度
                    elif img.mode != "RGB":
                        img = img.convert("RGB")

                    # 将图片转换为PNG格式的字节流
                    png_buffer = io.BytesIO()
                    img.save(png_buffer, format="PNG", optimize=True)
                    png_content = png_buffer.getvalue()

                    # 计算SHA256哈希
                    avatar_sha256_hash = hashlib.sha256(png_content).hexdigest()

                    # 创建存储目录 (修正路径)
                    images_dir = os.path.join("system_accounts", "images")
                    os.makedirs(images_dir, exist_ok=True)

                    # 保存为PNG文件 (修正文件名)
                    filename = f"{avatar_sha256_hash}.png"
                    filepath = os.path.join(images_dir, filename)

                    with open(filepath, "wb") as f:
                        f.write(png_content)

                    # 更新索引文件，记录为 "Guest" (用户请求)
                    index_file = os.path.join(images_dir, "_index.json")
                    try:
                        if os.path.exists(index_file):
                            with open(index_file, "r", encoding="utf-8") as f:
                                index_data = json.load(f)
                        else:
                            index_data = {
                                "version": "1.0",
                                "description": "用户头像索引文件",
                                "files": {},
                            }

                        ip_address = request.headers.get(
                            "X-Forwarded-For", request.remote_addr
                        )

                        # 添加/更新文件信息，用户名为 "Guest"
                        index_data["files"][filename] = {
                            "username": "Guest",  # <--- 修正：注册时标记为Guest
                            "upload_time": time.time(),
                            "upload_time_str": datetime.datetime.now().isoformat(),
                            "ip_address": ip_address,
                            "original_filename": avatar_file.filename,
                            "file_size": len(png_content),
                            "sha256": avatar_sha256_hash,
                        }

                        with open(index_file, "w", encoding="utf-8") as f:
                            json.dump(index_data, f, indent=2, ensure_ascii=False)

                        logging.info(
                            f"访客 (注册前) 从 {ip_address} 上传头像: {filename}"
                        )
                    except Exception as e:
                        logging.error(f"注册时更新头像索引失败: {e}", exc_info=True)
                        # 索引失败不应阻止注册，继续

                    # 构建正确的头像URL (修正URL)
                    avatar_url = f"/api/avatar/{filename}"

                except Exception as e:
                    logging.error(f"注册时处理头像失败: {e}", exc_info=True)
                    return (
                        jsonify(
                            {"success": False, "message": f"图片处理失败: {str(e)}"}
                        ),
                        500,
                    )

            # 8. 调用auth_system.register_user()执行注册逻辑
            # 传递额外参数：phone, nickname, avatar_url
            result = auth_system.register_user(
                auth_username,
                auth_password,
                phone=phone,
                nickname=nickname or auth_username,  # 默认昵称为用户名
                avatar_url=avatar_url,
            )

            # 9. (新) 注册成功后，更新头像索引中的用户名
            if result.get("success") and avatar_sha256_hash:
                try:
                    images_dir = os.path.join("system_accounts", "images")
                    index_file = os.path.join(images_dir, "_index.json")
                    filename = f"{avatar_sha256_hash}.png"

                    if os.path.exists(index_file):
                        # 此处需要加锁，以防并发写入索引文件
                        # 假设 auth_system.lock 可用于此目的
                        with auth_system.lock:
                            with open(index_file, "r", encoding="utf-8") as f:
                                index_data = json.load(f)

                            # 查找由Guest上传的、匹配哈希值的条目
                            if (
                                filename in index_data.get("files", {})
                                and index_data["files"][filename].get("username")
                                == "Guest"
                            ):
                                # 更新用户名为新注册的用户名
                                index_data["files"][filename][
                                    "username"
                                ] = auth_username

                                with open(index_file, "w", encoding="utf-8") as f:
                                    json.dump(
                                        index_data, f, indent=2, ensure_ascii=False
                                    )

                                logging.info(
                                    f"头像索引已更新：文件 {filename} 的所有者已从 'Guest' 更新为 '{auth_username}'"
                                )
                            else:
                                logging.warning(
                                    f"注册后尝试更新头像索引：未找到匹配的 'Guest' 条目 (文件: {filename})"
                                )
                except Exception as e:
                    logging.error(f"注册成功后更新头像索引失败: {e}", exc_info=True)
                    # 索引更新失败不影响注册成功响应

            return jsonify(result)

        except Exception as e:
            app.logger.error(f"[注册] 处理异常：{str(e)}")
            return jsonify({"success": False, "message": "注册失败，请稍后重试"})

    @app.route("/auth/login", methods=["POST"])
    def auth_login():
        """
        用户登录认证API端点。
        """
        global config

        # 加载配置以检查功能开关
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE, encoding="utf-8")

        data = request.get_json() or {}

        # --- 提取所有可能的字段 ---
        auth_phone = data.get("auth_phone", "").strip()
        auth_username = data.get("auth_username", "").strip()
        auth_password = data.get("auth_password", "").strip()
        sms_code = data.get("auth_sms_code", "").strip()
        two_fa_code = data.get("two_fa_code", "").strip()
        captcha_input = data.get("captcha", "").strip()  # 获取用户输入的验证码
        captcha_id = data.get("captcha_id", "").strip()  # 获取验证码ID

        # 验证图形验证码（在所有登录尝试前进行验证，增强安全性）
        is_captcha_valid, captcha_error_msg = verify_captcha(captcha_id, captcha_input)
        if not is_captcha_valid:
            return jsonify({"success": False, "message": captcha_error_msg})

        session_id = request.headers.get("X-Session-ID", "")
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr) or ""
        user_agent = request.headers.get("User-Agent", "")

        # 此处不能分配新 session_id，登录时必须使用客户端提供的 ID

        auth_result = None
        target_username = None  # 用于2FA和日志记录

        # 模式1: 手机号 + 验证码
        if auth_phone and sms_code:
            target_username = auth_system.find_user_by_phone(auth_phone)
            if not target_username:
                return jsonify({"success": False, "message": "该手机号未注册"})

            logging.info(f"[登录] 模式: 手机号/验证码 (用户: {target_username})")

            if (
                config.get("Features", "enable_phone_login", fallback="false").lower()
                != "true"
            ):
                return jsonify({"success": False, "message": "手机号登录功能未启用"})
            if (
                config.get("Features", "enable_sms_service", fallback="false").lower()
                != "true"
            ):
                return jsonify({"success": False, "message": "短信服务未启用"})

            # 验证短信验证码
            global sms_verification_codes
            stored_code_info = sms_verification_codes.get(auth_phone)
            if not stored_code_info:
                return jsonify({"success": False, "message": "请先获取验证码"})

            code_value, expires_at = stored_code_info
            if time.time() > expires_at:
                del sms_verification_codes[auth_phone]
                return jsonify(
                    {"success": False, "message": "验证码已过期，请重新获取"}
                )

            if code_value != sms_code:
                return jsonify({"success": False, "message": "验证码错误"})

            # 验证码正确，清除
            del sms_verification_codes[auth_phone]

            # 检查2FA
            user_file = auth_system.get_user_file_path(target_username)
            if os.path.exists(user_file):
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                if user_data.get("2fa_enabled", False):
                    if not two_fa_code:
                        # 需要2FA
                        return jsonify(
                            {
                                "success": True,
                                "message": "需要2FA验证码",
                                "requires_2fa": True,
                                "auth_username": target_username,
                            }
                        )
                    if not auth_system.verify_2fa(target_username, two_fa_code):
                        auth_system._log_login_attempt(
                            target_username, False, ip_address, user_agent, "2fa_failed"
                        )
                        return jsonify({"success": False, "message": "2FA验证码错误"})

            # 登录成功 (短信 + 2FA通过)
            # 手动构建 auth_result
            auth_result = {
                "success": True,
                "auth_username": target_username,
                "group": auth_system.get_user_group(target_username),
                "is_guest": False,
                "message": "登录成功",
            }
            auth_system._log_login_attempt(
                target_username, True, ip_address, user_agent, "SMS code login"
            )

        # 模式2: 手机号 + 密码
        elif auth_phone and auth_password:
            target_username = auth_system.find_user_by_phone(auth_phone)
            if not target_username:
                return jsonify({"success": False, "message": "该手机号未注册"})

            logging.info(f"[登录] 模式: 手机号/密码 (用户: {target_username})")

            if (
                config.get("Features", "enable_phone_login", fallback="false").lower()
                != "true"
            ):
                return jsonify({"success": False, "message": "手机号登录功能未启用"})

            # 调用authenticate进行密码和2FA验证
            auth_result = auth_system.authenticate(
                target_username, auth_password, ip_address, user_agent, two_fa_code
            )

        # 模式3: 用户名 + 密码
        elif auth_username and auth_password:
            target_username = auth_username
            logging.info(f"[登录] 模式: 用户名/密码 (用户: {target_username})")

            # 调用authenticate进行密码和2FA验证
            auth_result = auth_system.authenticate(
                target_username, auth_password, ip_address, user_agent, two_fa_code
            )

        # 模式4: 游客 (特殊处理)
        elif auth_username == "guest" and not auth_password:
            logging.info(f"[登录] 模式: 游客")
            auth_result = auth_system.authenticate(
                auth_username, auth_password, ip_address, user_agent, two_fa_code
            )

        else:
            return jsonify({"success": False, "message": "无效的登录凭据"})

        if not auth_result:
            return jsonify({"success": False, "message": "认证时发生未知错误"})

        # 如果需要2FA (来自密码验证)
        if auth_result.get("requires_2fa"):
            return jsonify(auth_result)

        # 如果登录失败 (密码错误, 2FA错误等)
        if not auth_result.get("success"):
            return jsonify(auth_result)

        # 将认证信息附加到会话
        # 使用锁保护web_sessions字典的并发访问
        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]
            else:
                api_instance = Api(args)
                api_instance._session_created_at = time.time()
                api_instance._web_session_id = session_id
                web_sessions[session_id] = api_instance

            api_instance.auth_username = auth_result["auth_username"]
            api_instance.auth_group = auth_result["group"]
            api_instance.is_guest = auth_result.get("is_guest", False)
            api_instance.is_authenticated = True

            # 如果是注册用户（非游客），处理会话关联
            cleanup_message = ""
            if not auth_result.get("is_guest", False):
                try:
                    # 检查并强制执行会话数量限制
                    old_sessions, cleanup_message = (
                        auth_system.check_single_session_enforcement(
                            auth_username, session_id
                        )
                    )

                    # 清理旧会话（如果超出限制）- 使用后台线程异步清理，不阻塞登录响应
                    if old_sessions:

                        def cleanup_old_sessions_async():
                            for old_sid in old_sessions:
                                try:
                                    cleanup_session(old_sid, "session_limit_exceeded")
                                except Exception as e:
                                    logging.error(
                                        f"后台清理旧会话失败 {old_sid[:16]}...: {e}"
                                    )

                        cleanup_thread = threading.Thread(
                            target=cleanup_old_sessions_async, daemon=True
                        )
                        cleanup_thread.start()

                    # 关联新会话到用户账号
                    auth_system.link_session_to_user(auth_username, session_id)

                    # 记录审计日志
                    if session_id == "" or session_id is None or session_id == "null":
                        audit_details = f"登录成功"
                    else:
                        audit_details = f"登录成功，会话ID: {session_id}"
                    if cleanup_message:
                        audit_details += f"; {cleanup_message}"

                    auth_system.log_audit(
                        auth_username,
                        "user_login",
                        audit_details,
                        ip_address,
                        session_id,
                    )
                except Exception as e:
                    # 即使会话管理失败，也不应阻止登录
                    logging.error(f"会话管理过程出错，但继续登录流程: {e}")
                    cleanup_message = ""

            try:
                save_session_state(session_id, api_instance, force_save=True)
            except Exception as e:
                logging.error(f"保存会话状态失败: {e}")

        # 如果是注册用户，返回已保存的会话ID列表
        user_sessions = []
        max_sessions = 1
        if not auth_result.get("is_guest", False):
            try:
                user_sessions = auth_system.get_user_sessions(auth_username)
                user_details = auth_system.get_user_details(auth_username)
                if user_details:
                    max_sessions = user_details.get("max_sessions", 1)
            except Exception as e:
                logging.error(f"获取用户会话信息失败: {e}")
                user_sessions = []
                max_sessions = 1

        # 生成会话限制提示信息
        session_limit_info = ""
        if max_sessions == 1:
            session_limit_info = "您的账号为单会话模式，新登录将自动清理所有旧会话"
        elif max_sessions == -1:
            session_limit_info = "您的账号为无限会话模式，可以创建任意数量的会话"
        else:
            session_limit_info = f"您的账号最多可以同时保持{max_sessions}个活跃会话，超出时将自动清理最旧的会话"

        # ===== 生成和存储Token (仅非游客) =====
        token = None
        kicked_sessions = []
        if not auth_result.get("is_guest", False) and session_id:
            try:
                # 1. 生成2048位token
                token = token_manager.create_token(auth_username, session_id)

                # 2. 检测多设备登录
                kicked_sessions = token_manager.detect_multi_device_login(
                    auth_username, session_id
                )

                # 3. 清理过期token
                token_manager.cleanup_expired_tokens(auth_username)

                # 4. 踢出旧设备（使token失效并清理会话）
                if kicked_sessions:
                    for old_sid in kicked_sessions:
                        # 使token失效
                        token_manager.invalidate_token(auth_username, old_sid)
                        # 清理会话
                        # cleanup_session(old_sid, "logged_in_elsewhere")

                    logging.info(
                        f"用户 {auth_username} 从新设备登录，检测到 {len(kicked_sessions)} 个其他活跃会话。"
                    )
            except Exception as e:
                # 即使token管理失败，也不应阻止登录流程
                logging.error(f"Token管理过程出错，但继续登录流程: {e}")
                token = None
                kicked_sessions = []

        try:
            response_data = {
                "success": True,
                "session_id": session_id,  # 修正：返回session_id给前端
                "auth_username": auth_result["auth_username"],
                "group": auth_result["group"],
                "is_guest": auth_result.get("is_guest", False),
                "user_sessions": user_sessions,  # 用于状态恢复
                "max_sessions": max_sessions,
                "session_limit_info": session_limit_info,
                "avatar_url": auth_result.get("avatar_url", ""),
                "theme": auth_result.get("theme", "light"),
                "token": token,  # 返回token给前端
                "kicked_sessions_count": len(kicked_sessions),  # 踢出的设备数量
            }

            # 添加清理提示（如果有）
            if cleanup_message:
                response_data["cleanup_message"] = cleanup_message

            # 添加多设备登录提示
            if kicked_sessions:
                response_data["multi_device_warning"] = (
                    f"检测到该账号在其他 {len(kicked_sessions)} 个设备上登录，已自动登出旧设备"
                )

            # 创建响应并设置Cookie (仅非游客)
            response = jsonify(response_data)
            if token:
                # 设置1小时过期的httponly cookie
                response.set_cookie(
                    "auth_token",
                    value=token,
                    max_age=3600,  # 1小时
                    httponly=True,  # 防止JavaScript访问
                    secure=False,  # 开发环境设为False，生产环境应为True
                    samesite="Lax",
                )

            return response
        except Exception as e:
            # 最后的安全网：即使响应创建失败，也返回基本的成功响应
            logging.error(f"创建登录响应失败: {e}")
            return jsonify(
                {
                    "success": True,
                    "session_id": session_id,
                    "auth_username": auth_result.get("auth_username", auth_username),
                    "group": auth_result.get("group", "user"),
                    "is_guest": False,
                }
            )

    @app.route("/auth/guest_login", methods=["POST"])
    def auth_guest_login():
        """
        游客登录API - 无需密码的快速访问入口。
        """
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"})

        # 更新会话活动时间
        update_session_activity(session_id)

        # 检查是否允许游客登录
        if not auth_system.config.getboolean(
            "Guest", "allow_guest_login", fallback=True
        ):
            return jsonify({"success": False, "message": "系统不允许游客登录"})

        # 创建游客会话
        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]
            else:
                api_instance = Api(args)
                api_instance._session_created_at = time.time()
                api_instance._web_session_id = session_id
                web_sessions[session_id] = api_instance

            api_instance.auth_username = "guest"
            api_instance.auth_group = "guest"
            api_instance.is_guest = True
            api_instance.is_authenticated = True

            save_session_state(session_id, api_instance, force_save=True)

        return jsonify(
            {
                "success": True,
                "auth_username": "guest",
                "group": "guest",
                "is_guest": True,
            }
        )

    @app.route("/auth/logout", methods=["POST"])
    def auth_logout():
        """
        用户登出API - 安全退出系统并清理所有会话数据。

        功能说明：
        - 终止用户的当前会话
        - 使token失效（防止重放攻击）
        - 清除浏览器cookie
        - 释放服务器端资源

        请求格式：
        - 方法：POST
        - 路径：/auth/logout
        - 请求头：
          * X-Session-ID: 要登出的会话标识符（必需）
        - 请求体：无需

        响应格式：
        {
          "success": true,
          "message": "登出成功"
        }

        响应头：
        - Set-Cookie: auth_token=; Max-Age=0（清除cookie）

        处理流程：
        1. 从请求头获取session_id
        2. 验证session_id存在性
        3. 获取用户信息（用户名、是否游客）
        4. 如果是注册用户，使其token失效：
           - 调用token_manager.invalidate_token()
           - 记录登出事件到日志
        5. 清理服务器端会话：
           - 从web_sessions移除会话
           - 关闭Api实例资源
           - 删除会话持久化文件
        6. 清除客户端cookie（auth_token）
        7. 返回成功响应

        安全特性：
        - Token失效机制：防止token被重复使用
        - Cookie清除：防止浏览器自动重新登录
        - 资源释放：避免会话泄漏
        - 审计日志：记录登出时间和原因

        游客处理：
        - 游客用户没有token，只清理会话即可
        - 不记录游客的登出事件

        错误情况：
        - 缺少session_id：返回400错误
        - 会话不存在：仍然返回成功（幂等性）

        注意：
        - 此接口幂等性强，重复调用不会出错
        - 登出后前端应导航到登录页
        - 多标签页的其他标签会话也会失效
        - 调用cleanup_session时原因设为"user_logout"

        使用场景：
        - 用户主动点击"退出"按钮
        - 会话超时后的强制登出
        - 安全策略要求的定期重新认证
        """
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 400

        # 获取用户信息
        username = None
        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]
                if hasattr(api_instance, "auth_username"):
                    username = api_instance.auth_username
                    is_guest = getattr(api_instance, "is_guest", True)

                    # 如果是非游客用户，使token失效
                    if not is_guest and username:
                        token_manager.invalidate_token(username, session_id)
                        logging.info(
                            f"用户 {username} 登出，session: {session_id[:16]}..."
                        )

        # 清理会话
        cleanup_session(session_id, "user_logout")

        # 创建响应并清除cookies
        response = jsonify({"success": True, "message": "登出成功"})
        response.set_cookie("auth_token", "", max_age=0)

        return response

    @app.route("/auth/check_permission", methods=["POST"])
    def auth_check_permission():
        """
        权限检查API - 验证用户是否拥有特定权限。
        """
        # 从请求头中提取会话ID，用于识别当前用户的会话
        session_id = request.headers.get("X-Session-ID", "")
        # 解析请求体中的JSON数据，如果解析失败则返回空字典
        data = request.get_json() or {}
        # 提取要检查的权限名称
        permission = data.get("permission", "")

        # 【并发安全】使用辅助函数进行线程安全的会话验证
        # 这个函数会自动加锁、验证会话、提取用户信息，然后释放锁
        success, result, status_code = get_session_user_safe(session_id)
        if not success:
            # 如果验证失败，返回特殊的权限检查响应格式
            return jsonify({"success": False, "has_permission": False})

        # 提取用户名
        auth_username = result["username"]

        # 执行权限检查（已在锁外，不会阻塞其他请求）
        has_permission = auth_system.check_permission(auth_username, permission)
        return jsonify({"success": True, "has_permission": has_permission})

    @app.route("/auth/switch_session", methods=["POST"])
    def auth_switch_session():
        """
        会话切换API - 在多标签页间切换时更新认证token和cookie。
        """
        current_session_id = request.headers.get(
            "X-Session-ID", ""
        )  # 当前活动窗口的 Session ID
        data = request.get_json() or {}
        target_session_id = data.get(
            "target_session_id", ""
        )  # 用户想要切换到的 Session ID

        if not current_session_id or not target_session_id:
            return jsonify({"success": False, "message": "缺少会话ID参数"}), 400

        # 1. 验证当前用户身份 (基于 current_session_id 和 cookie)
        username = None
        is_guest = True
        auth_username = ""
        with web_sessions_lock:
            if current_session_id in web_sessions:
                api_instance = web_sessions[current_session_id]
                if getattr(api_instance, "is_authenticated", False):
                    username = getattr(api_instance, "auth_username", None)
                    is_guest = getattr(api_instance, "is_guest", True)

        if not username or is_guest:
            return (
                jsonify(
                    {"success": False, "message": "用户未登录或为游客，无法切换会话"}
                ),
                401,
            )

        # 2. 检查 token (这一步是必要的，确保当前操作是合法的)
        token_from_cookie = request.cookies.get("auth_token")
        if not token_from_cookie:
            return jsonify({"success": False, "message": "缺少认证令牌(cookie)"}), 401

        is_valid, reason = token_manager.verify_token(
            username, current_session_id, token_from_cookie
        )
        if not is_valid:
            # 如果当前 token 都无效了，直接要求重新登录
            logging.warning(
                f"切换会话失败：用户 {username} 的当前会话 {current_session_id[:8]} token 无效 ({reason})"
            )
            response_data = {
                "success": False,
                "message": f"当前认证已失效({reason})，请重新登录",
                "need_login": True,
            }
            response = make_response(jsonify(response_data), 401)
            response.set_cookie("auth_token", "", max_age=0)  # 清除无效 cookie
            return response

        # 3. 为目标会话生成新 Token
        # 注意：即使目标会话已存在 token，这里也生成一个新的，以确保安全性和一致性
        new_token_for_target = token_manager.create_token(username, target_session_id)
        logging.info(
            f"用户 {username} 切换会话：为目标会话 {target_session_id[:8]} 生成新 token"
        )

        # 4. 创建响应，并设置新的 auth_token cookie
        response_data = {"success": True, "message": "Token已更新，可以跳转"}
        response = make_response(jsonify(response_data))
        response.set_cookie(
            "auth_token",
            value=new_token_for_target,
            max_age=3600,  # 1 小时
            httponly=True,
            secure=False,  # 开发环境 False，生产环境 True
            samesite="Lax",
        )

        # 5. （可选但推荐）确保目标会话状态存在于内存或文件中
        with web_sessions_lock:
            if target_session_id not in web_sessions:
                # 尝试从文件加载，如果文件不存在或加载失败，也没关系，
                # 因为 /uuid=<target_id> 路由会处理新会话的创建
                state = load_session_state(target_session_id)
                if state:
                    target_api_instance = Api(args)
                    target_api_instance._web_session_id = target_session_id
                    restore_session_to_api_instance(target_api_instance, state)
                    web_sessions[target_session_id] = target_api_instance
                    logging.info(
                        f"切换会话时，预加载目标会话 {target_session_id[:8]} 状态成功"
                    )
                else:
                    logging.warning(
                        f"切换会话时，目标会话 {target_session_id[:8]} 状态文件不存在或加载失败，将在访问时创建"
                    )

        return response

    @app.route("/auth/admin/list_users", methods=["GET"])
    def auth_admin_list_users():
        """
        列出所有用户信息。
        """
        # 从请求头中提取会话ID
        session_id = request.headers.get("X-Session-ID", "")

        # 【并发安全修复】使用锁保护web_sessions字典访问
        with web_sessions_lock:
            # 验证会话ID的存在性和有效性
            if not session_id or session_id not in web_sessions:
                return jsonify({"success": False, "message": "未授权"})

            # 从会话字典中获取API实例
            api_instance = web_sessions[session_id]
            # 检查是否已认证登录
            if not hasattr(api_instance, "auth_username"):
                return jsonify({"success": False, "message": "未登录"})

            # 在锁保护范围内提取用户名，确保线程安全
            auth_username = api_instance.auth_username

        # 在释放锁后执行权限检查（耗时操作不应在锁内）
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"})

        # 获取用户列表并返回
        users = auth_system.list_users()
        return jsonify({"success": True, "users": users})

    @app.route("/auth/admin/update_user_group", methods=["POST"])
    def auth_admin_update_user_group():
        """
        修改用户所属的权限组。
        """
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        target_username = data.get("target_username", "")
        new_group = data.get("new_group", "")

        if new_group == "super_admin":
            return jsonify({"success": False, "message": "不允许分配超级管理员组"})

        super_admin = auth_system.config.get("Admin", "super_admin", fallback="admin")
        if target_username == super_admin:
            return jsonify(
                {"success": False, "message": "不允许修改超级管理员用户组的用户"}
            )

        # 验证会话ID和用户认证状态
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权"})

        # 【并发安全修复】使用锁保护web_sessions字典访问
        # 这是一个竞态条件的关键点：多个请求可能同时读取会话字典
        with web_sessions_lock:
            # 从会话字典中获取API实例
            api_instance = web_sessions[session_id]
            # 检查用户是否已认证登录
            if not hasattr(api_instance, "auth_username"):
                return jsonify({"success": False, "message": "未登录"})

            # 在锁保护范围内提取用户名，确保数据一致性
            auth_username = api_instance.auth_username

        # 在锁外执行权限检查，避免长时间持有锁
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"})

        # 执行用户组更新操作
        result = auth_system.update_user_group(target_username, new_group)
        return jsonify(result)

    @app.route("/auth/admin/list_groups", methods=["GET"])
    def auth_admin_list_groups():
        """
        管理员API - 列出所有权限组及其权限配置。
        """
        # 从请求头提取会话ID
        session_id = request.headers.get("X-Session-ID", "")

        # 【并发安全修复】在访问共享资源web_sessions前加锁
        with web_sessions_lock:
            # 验证会话ID的有效性
            if not session_id or session_id not in web_sessions:
                return jsonify({"success": False, "message": "未授权"})

            # 从会话字典获取API实例
            api_instance = web_sessions[session_id]
            # 检查用户认证状态
            if not hasattr(api_instance, "auth_username"):
                return jsonify({"success": False, "message": "未登录"})

            # 提取用户名（在锁保护范围内）
            auth_username = api_instance.auth_username

        # 在锁外执行权限检查（不阻塞其他请求）
        if not auth_system.check_permission(auth_username, "manage_permissions"):
            return jsonify({"success": False, "message": "权限不足"})

        # 获取原始权限组配置
        raw_groups = auth_system.get_all_groups()

        # --- 自动补全缺失权限逻辑 ---
        groups = copy.deepcopy(raw_groups)

        # 1. 收集系统当前所有已知的权限键名（）
        all_permission_keys = set()
        for g_data in groups.values():
            perms = g_data.get("permissions", {})
            all_permission_keys.update(perms.keys())

        # 2. 遍历所有组，补全缺失的权限字段，默认为 False
        for g_key, g_data in groups.items():
            if "permissions" not in g_data:
                g_data["permissions"] = {}

            current_perms = g_data["permissions"]
            for key in all_permission_keys:
                if key not in current_perms:
                    current_perms[key] = False

        return jsonify({"success": True, "groups": groups})

    @app.route("/auth/admin/create_group", methods=["POST"])
    def auth_admin_create_group():
        """创建权限组"""
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        # 去除首尾空格
        # 验证必填参数
        group_name = data.get("group_name", "").strip()
        display_name = data.get("display_name", "").strip()
        permissions = data.get("permissions", {})

        # 【并发安全修复】使用锁保护会话字典访问
        with web_sessions_lock:
            # 验证会话有效性
            if not session_id or session_id not in web_sessions:
                return jsonify({"success": False, "message": "未授权"})

            # 获取API实例
            api_instance = web_sessions[session_id]
            # 验证用户已登录
            if not hasattr(api_instance, "auth_username"):
                return jsonify({"success": False, "message": "未登录"})

            # 检查是否为超级管理员（需要访问auth_group属性）
            # 在锁保护范围内进行检查，确保读取的是一致的状态
            if api_instance.auth_group != "super_admin":
                return jsonify(
                    {"success": False, "message": "仅超级管理员可创建权限组"}
                )
        # 锁已释放，可以执行后续的业务逻辑

        # 问题7修复：验证必填字段不能为空
        if not group_name:
            return jsonify(
                {"success": False, "message": "权限组标识（group_name）不能为空"}
            )

        if not display_name:
            return jsonify(
                {"success": False, "message": "权限组名称（display_name）不能为空"}
            )

        # 执行权限组创建操作
        result = auth_system.create_permission_group(
            group_name, permissions, display_name
        )
        return jsonify(result)

    @app.route("/auth/admin/update_group", methods=["POST"])
    def auth_admin_update_group():
        """更新权限组（支持group_key和group_name参数）"""
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        # 兼容group_key和group_name两种参数名
        group_name = data.get("group_key") or data.get("group_name", "")
        permissions = data.get("permissions", {})

        # 预先验证权限组名称（防止修改超级管理员组）
        if group_name == "super_admin":
            return jsonify({"success": False, "message": "不允许修改超级管理员组"})

        # 【并发安全修复】使用锁保护会话字典的并发访问
        with web_sessions_lock:
            # 验证会话存在性
            if not session_id or session_id not in web_sessions:
                return jsonify({"success": False, "message": "未授权"})

            # 从会话字典获取API实例
            api_instance = web_sessions[session_id]
            # 验证用户已认证
            if not hasattr(api_instance, "auth_username"):
                return jsonify({"success": False, "message": "未登录"})

            # 检查超级管理员权限（auth_group属性访问必须在锁内）
            if api_instance.auth_group != "super_admin":
                return jsonify(
                    {"success": False, "message": "仅超级管理员可更新权限组"}
                )
        # 锁已释放

        # 问题6修复：验证权限组名称
        if not group_name:
            return jsonify({"success": False, "message": "权限组标识不能为空"})

        # 执行权限组更新操作
        result = auth_system.update_permission_group(group_name, permissions)

        # 问题6修复：检查权限组是否存在
        if not result.get("success", False):
            # 如果更新失败，检查是否因为权限组不存在
            if "不存在" in result.get("message", ""):
                return jsonify(
                    {"success": False, "message": f"权限组 '{group_name}' 不存在"}
                )

        return jsonify(result)

    @app.route("/auth/admin/delete_group", methods=["POST"])
    def auth_admin_delete_group():
        """超级管理员：删除权限组"""
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        group_name = data.get("group_name", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权"})

        api_instance = web_sessions[session_id]
        if not hasattr(api_instance, "auth_username"):
            return jsonify({"success": False, "message": "未登录"})

        # 检查是否为超级管理员
        if api_instance.auth_group != "super_admin":
            return jsonify({"success": False, "message": "仅超级管理员可删除权限组"})

        result = auth_system.delete_permission_group(group_name)
        return jsonify(result)

    @app.route("/auth/admin/get_user_permissions", methods=["POST"])
    def auth_admin_get_user_permissions():
        """管理员：获取用户的完整权限列表"""
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        target_username = data.get("username", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_permissions"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 获取用户的完整权限列表（包含差分化权限）
        all_permissions = auth_system.get_user_permissions(target_username)

        # 获取用户所属的权限组
        group = auth_system.get_user_group(target_username)

        # 获取权限组的基础权限
        group_permissions = (
            auth_system.permissions["permission_groups"]
            .get(group, {})
            .get("permissions", {})
        )

        # 获取用户的差分权限信息
        user_custom = auth_system.permissions.get("user_custom_permissions", {}).get(
            target_username, {}
        )
        added_list = user_custom.get("added", [])
        removed_list = user_custom.get("removed", [])

        # 将差分权限数组转换为对象格式（前端需要）
        added_permissions = {perm: True for perm in added_list}
        removed_permissions = {perm: True for perm in removed_list}

        return jsonify(
            {
                "success": True,
                "group": group,
                "all_permissions": all_permissions,
                "group_permissions": group_permissions,
                "added_permissions": added_permissions,
                "removed_permissions": removed_permissions,
            }
        )

    @app.route("/auth/admin/set_user_permission", methods=["POST"])
    def auth_admin_set_user_permission():
        """管理员：为用户设置自定义权限（差分化存储）

        支持两种模式：
        1. 单个权限设置：传递 permission 和 grant 参数
        2. 批量权限设置：传递 added_permissions 和 removed_permissions 对象
        """
        session_id = request.headers.get("X-Session-ID", "")
        data = request.get_json() or {}
        target_username = data.get("username", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_permissions"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 检查是批量更新还是单个更新
        added_permissions = data.get("added_permissions", {})
        removed_permissions = data.get("removed_permissions", {})

        if added_permissions or removed_permissions:
            # 批量更新模式
            try:
                # 清空用户的差分权限，然后设置新的
                if "user_custom_permissions" not in auth_system.permissions:
                    auth_system.permissions["user_custom_permissions"] = {}

                auth_system.permissions["user_custom_permissions"][target_username] = {
                    "added": list(added_permissions.keys()),
                    "removed": list(removed_permissions.keys()),
                }

                auth_system._save_permissions()

                # 记录审计日志
                ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
                auth_system.log_audit(
                    auth_username,
                    "set_user_permissions_batch",
                    f"批量更新用户 {target_username} 的差分权限: 添加{len(added_permissions)}个, 移除{len(removed_permissions)}个",
                    ip_address,
                    session_id,
                )

                return jsonify({"success": True, "message": "权限已更新"})
            except Exception as e:
                logging.error(f"批量更新权限失败: {e}", exc_info=True)
                return (
                    jsonify({"success": False, "message": f"更新失败: {str(e)}"}),
                    500,
                )
        else:
            # 单个权限更新模式（兼容旧代码）
            permission = data.get("permission", "")
            grant = data.get("grant", False)

            if not permission:
                # return jsonify({"success": False, "message": "缺少permission参数"}), 400
                logging.info(
                    f"管理员 {auth_username} 尝试为用户 {target_username} 设置权限时，缺少 permission 参数"
                )
                try:
                    # 清空用户的差分权限，然后设置新的
                    if "user_custom_permissions" not in auth_system.permissions:
                        auth_system.permissions["user_custom_permissions"] = {}

                    auth_system.permissions["user_custom_permissions"][
                        target_username
                    ] = {"added": [], "removed": []}

                    auth_system._save_permissions()

                    # 记录审计日志
                    ip_address = request.headers.get(
                        "X-Forwarded-For", request.remote_addr
                    )
                    auth_system.log_audit(
                        auth_username,
                        "set_user_permissions_batch",
                        f"批量更新用户 {target_username} 的差分权限: 清空用户的差分权限",
                        ip_address,
                        session_id,
                    )

                    return jsonify({"success": True, "message": "权限已更新"})
                except Exception as e:
                    logging.error(f"批量更新权限失败: {e}", exc_info=True)
                    return (
                        jsonify({"success": False, "message": f"更新失败: {str(e)}"}),
                        500,
                    )

            result = auth_system.set_user_custom_permission(
                target_username, permission, grant
            )

            # 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "set_user_permission",
                f'为用户 {target_username} {"授予" if grant else "移除"} 权限: {permission}',
                ip_address,
                session_id,
            )

            return jsonify(result)

    @app.route("/auth/get_config", methods=["GET"])
    def auth_get_config():
        """
        获取认证配置（用于前端显示）
        使用 _get_config_value 辅助函数安全地读取配置，避免 ValueError 崩溃
        """
        # 安全地读取 allow_guest_login 配置，使用 _get_config_value 辅助函数
        # type_func 参数设置为 lambda 函数，用于处理布尔值转换
        # 支持 'true', 'yes', '1', 'on' 等多种格式
        allow_guest_login = _get_config_value(
            auth_system.config,
            "Guest",
            "allow_guest_login",
            type_func=lambda x: str(x).lower()
            in ("true", "yes", "1", "on"),  # 布尔值转换逻辑
            fallback=True,  # 默认值为 True
        )

        # 安全地读取 amap_js_key 配置
        amap_js_key = _get_config_value(
            auth_system.config,
            "Map",
            "amap_js_key",
            type_func=str,  # 字符串类型
            fallback="",  # 默认值为空字符串
        )

        return jsonify(
            {
                "success": True,
                "allow_guest_login": allow_guest_login,
                "amap_js_key": amap_js_key,
            }
        )

    @app.route("/auth/check_uuid_type", methods=["POST"])
    def auth_check_uuid_type():
        """
        检查UUID类型：游客UUID、系统账号UUID或未知UUID
        用于实现访问控制和会话验证
        """
        data = request.json
        check_uuid = data.get("uuid", "")

        if not check_uuid:
            return jsonify({"success": False, "message": "UUID参数缺失"}), 400

        # UUID格式验证 - 标准UUID v4格式

        uuid_pattern = re.compile(
            r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$",
            re.IGNORECASE,
        )
        if not uuid_pattern.match(check_uuid):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "无效的UUID格式，请使用标准UUID v4格式",
                    }
                ),
                400,
            )

        # 检查会话文件是否存在
        session_file = get_session_file_path(check_uuid)
        file_exists = os.path.exists(session_file)
        logging.debug(
            f"/auth/check_uuid_type: Checking UUID {check_uuid[:8]}..., File path: {session_file}, Exists: {file_exists}"
        )  # 新增日志

        if not file_exists:
            return jsonify(
                {
                    "success": True,
                    "uuid_type": "unknown",
                    "message": "UUID不存在 (文件未找到)",  # 更明确的消息
                }
            )

        # 读取会话文件判断类型 - 使用文件锁避免并发问题

        max_retries = 3
        retry_delay = 0.1

        # 在循环开始前尝试导入 fcntl (仅非Windows)
        fcntl = None

        for attempt in range(max_retries):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    # 加共享锁（读锁），仅当 fcntl 可用时
                    if fcntl:  # <- 添加判断
                        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        session_data = json.load(f)
                    finally:
                        # 释放锁，仅当 fcntl 可用时
                        if fcntl:  # <- 添加判断
                            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

                # 检查是否为游客会话
                is_guest = session_data.get("is_guest", False)
                auth_username = session_data.get("auth_username", "")

                if is_guest or auth_username == "guest":
                    return jsonify(
                        {"success": True, "uuid_type": "guest", "message": "游客UUID"}
                    )
                elif auth_username:
                    return jsonify(
                        {
                            "success": True,
                            "uuid_type": "system_account",
                            "auth_username": auth_username,
                            "message": "系统账号UUID",
                        }
                    )
                else:
                    logging.warning(
                        f"/auth/check_uuid_type: 文件 {session_file} 存在但内容无法识别用户类型 (auth_username='{auth_username}', is_guest={is_guest})，返回 unknown"
                    )  # 新增日志
                    return jsonify(
                        {
                            "success": True,
                            "uuid_type": "unknown",
                            "message": "未知类型UUID (内容无法识别)",  # 更明确的消息
                        }
                    )
            except (IOError, OSError) as e:
                # 文件锁定或IO错误，重试
                if attempt < max_retries - 1:

                    time.sleep(retry_delay)
                    continue
                else:
                    logging.error(f"读取会话文件失败（已重试{max_retries}次）: {e}")
                    return (
                        jsonify(
                            {"success": False, "message": "读取会话失败，请稍后重试"}
                        ),
                        500,
                    )
            except json.JSONDecodeError as e:
                logging.error(f"会话文件JSON解析失败: {e}")
                return jsonify({"success": False, "message": "会话数据损坏"}), 500
            except Exception as e:
                logging.error(f"检查UUID类型失败: {e}")
                return (
                    jsonify({"success": False, "message": f"服务器错误: {str(e)}"}),
                    500,
                )

    @app.route("/auth/2fa/generate", methods=["POST"])
    def auth_2fa_generate():
        """生成2FA密钥"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        if not getattr(api_instance, "is_authenticated", False):
            return jsonify({"success": False, "message": "未认证"}), 401

        auth_username = getattr(api_instance, "auth_username", "")
        if auth_username == "guest":
            return jsonify({"success": False, "message": "游客不支持2FA"}), 403

        result = auth_system.generate_2fa_secret(auth_username)
        return jsonify(result)

    @app.route("/auth/2fa/enable", methods=["POST"])
    def auth_2fa_enable():
        """启用2FA"""
        data = request.get_json() or {}
        verification_code = data.get("code", "").strip()
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        if not getattr(api_instance, "is_authenticated", False):
            return jsonify({"success": False, "message": "未认证"}), 401

        auth_username = getattr(api_instance, "auth_username", "")
        result = auth_system.enable_2fa(auth_username, verification_code)
        return jsonify(result)

    @app.route("/auth/2fa/verify", methods=["POST"])
    def auth_2fa_verify():
        """测试验证2FA代码（用于用户测试2FA是否工作正常）"""
        data = request.get_json() or {}
        verification_code = data.get("code", "").strip()
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        if not getattr(api_instance, "is_authenticated", False):
            return jsonify({"success": False, "message": "未认证"}), 401

        auth_username = getattr(api_instance, "auth_username", "")
        if auth_username == "guest":
            return jsonify({"success": False, "message": "游客不支持2FA"}), 403

        # 验证2FA代码
        if auth_system.verify_2fa(auth_username, verification_code):
            return jsonify({"success": True, "message": "验证码正确"})
        else:
            return jsonify({"success": False, "message": "验证码错误"})

    @app.route("/auth/2fa/disable", methods=["POST"])
    def auth_2fa_disable():
        """关闭2FA"""
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        if not getattr(api_instance, "is_authenticated", False):
            return jsonify({"success": False, "message": "未认证"}), 401

        auth_username = getattr(api_instance, "auth_username", "")
        if auth_username == "guest":
            return jsonify({"success": False, "message": "游客不支持2FA"}), 403

        # 禁用2FA
        user_file = auth_system.get_user_file_path(auth_username)
        if os.path.exists(user_file):
            try:
                with auth_system.lock:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)

                    user_data["2fa_enabled"] = False
                    # 可选：也可以删除2fa_secret，但保留它允许用户稍后重新启用
                    # user_data['2fa_secret'] = None

                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2, ensure_ascii=False)

                logging.info(f"用户 {auth_username} 已关闭2FA")
                return jsonify({"success": True, "message": "2FA已关闭"})
            except Exception as e:
                logging.error(f"关闭2FA失败: {e}", exc_info=True)
                return (
                    jsonify({"success": False, "message": f"关闭失败: {str(e)}"}),
                    500,
                )
        else:
            return jsonify({"success": False, "message": "用户不存在"}), 404

    @app.route("/auth/2fa/verify_login", methods=["POST"])
    def auth_2fa_verify_login():
        """验证2FA代码并完成登录（用于登录流程中的2FA验证）"""
        data = request.get_json() or {}
        auth_username = data.get("auth_username", "").strip()
        verification_code = data.get("code", "").strip()

        if not auth_username:
            return jsonify({"success": False, "message": "缺少用户名"}), 400

        if not verification_code:
            return jsonify({"success": False, "message": "缺少验证码"}), 400

        # 验证2FA代码
        if not auth_system.verify_2fa(auth_username, verification_code):
            logging.warning(f"2FA登录验证失败: {auth_username}")
            return jsonify({"success": False, "message": "验证码错误"})

        # 2FA验证成功，创建会话
        session_id = str(uuid.uuid4())
        api_instance = Api(args)
        api_instance._session_created_at = time.time()
        api_instance._web_session_id = session_id
        api_instance.is_authenticated = True
        api_instance.auth_username = auth_username

        # 获取用户组信息
        user_group = auth_system.get_user_group(auth_username)
        api_instance.auth_group = user_group

        # 检查是否为游客
        is_guest = auth_username == "guest"
        api_instance.is_guest = is_guest

        # 保存会话
        web_sessions[session_id] = api_instance

        # 更新用户最后登录时间
        user_file = auth_system.get_user_file_path(auth_username)
        if os.path.exists(user_file):
            try:
                with auth_system.lock:
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)

                    user_data["last_login"] = time.time()
                    if "session_ids" not in user_data:
                        user_data["session_ids"] = []
                    if session_id not in user_data["session_ids"]:
                        user_data["session_ids"].append(session_id)

                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logging.error(f"更新用户登录信息失败: {e}", exc_info=True)

        # 生成token（非游客）
        token = None
        if not is_guest:
            try:
                token = token_manager.create_token(auth_username, session_id)
                token_manager.cleanup_expired_tokens(auth_username)
            except Exception as e:
                logging.error(f"Token管理过程出错: {e}")
                token = None

        logging.info(f"用户 {auth_username} 通过2FA验证登录成功")

        response_data = {
            "success": True,
            "message": "2FA验证成功",
            "session_id": session_id,
            "is_guest": is_guest,
            "token": token,
        }

        # 创建响应并设置Cookie（非游客）
        response = jsonify(response_data)
        if token:
            response.set_cookie(
                "auth_token",
                value=token,
                max_age=3600,  # 1小时
                httponly=True,
                secure=False,
                samesite="Lax",
            )

        return response

    @app.route("/auth/admin/create_user", methods=["POST"])
    def auth_admin_create_user():
        """管理员：创建新用户"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        new_username = data.get("username", "")
        password = data.get("password", "")
        group = data.get("group", "user")

        if not new_username or not password:
            return jsonify({"success": False, "message": "用户名和密码不能为空"})

        result = auth_system.register_user(new_username, password, group)

        # 记录审计日志
        if result.get("success"):
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "create_user",
                f"创建新用户: {new_username} (组: {group})",
                ip_address,
                session_id,
            )

        return jsonify(result)

    @app.route("/auth/admin/ban_user", methods=["POST"])
    def auth_admin_ban_user():
        """管理员：封禁用户"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        target_username = data.get("username", "")

        result = auth_system.ban_user(target_username)

        # 记录审计日志
        if result.get("success"):
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "ban_user",
                f"封禁用户: {target_username}",
                ip_address,
                session_id,
            )

        return jsonify(result)

    @app.route("/auth/admin/unban_user", methods=["POST"])
    def auth_admin_unban_user():
        """管理员：解封用户"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        target_username = data.get("username", "")

        result = auth_system.unban_user(target_username)

        # 记录审计日志
        if result.get("success"):
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "unban_user",
                f"解封用户: {target_username}",
                ip_address,
                session_id,
            )

        return jsonify(result)

    @app.route("/auth/admin/delete_user", methods=["POST"])
    def auth_admin_delete_user():
        """管理员：删除用户"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        target_username = data.get("username", "")

        result = auth_system.delete_user(target_username)

        # 记录审计日志
        if result.get("success"):
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "delete_user",
                f"删除用户: {target_username}",
                ip_address,
                session_id,
            )

        return jsonify(result)

    @app.route("/auth/admin/force_reset_password", methods=["POST"])
    def auth_admin_force_reset_password():
        """
        管理员API：强制重置用户密码。
        """
        # 1. 验证会话
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 2. 检查权限 (假设重置密码需要 'manage_users' 权限)
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 3. 获取参数 (匹配 index.html L7158 的调用)
        data = request.json
        target_username = data.get("target_username", "")
        new_password = data.get("new_password", "")

        if not target_username or not new_password:
            return jsonify({"success": False, "message": "缺少用户名或新密码"}), 400

        # 4. 执行重置 (调用 main.py L2174 中已定义的 auth_system.reset_user_password)
        result = auth_system.reset_user_password(target_username, new_password)

        # 5. 记录审计日志
        if result.get("success"):
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "force_reset_password",  # 审计动作
                f"强制重置了用户 {target_username} 的密码",
                ip_address,
                session_id,
            )

        return jsonify(result)

    @app.route("/api/admin/users/<username>/basic_info", methods=["PUT"])
    def api_admin_update_user_basic_info(username):
        """
        问题8修复：管理员或用户本人：更新用户基本信息

        功能说明：
        允许管理员或用户本人更新基本信息（如昵称）

        URL参数:
            username: 要更新的用户名

        请求体参数（JSON）:
            nickname: 新昵称（可选）

        权限要求:
            - 管理员可以更新任何用户的信息
            - 普通用户只能更新自己的信息

        返回:
            操作结果
        """
        # 获取会话ID
        session_id = request.headers.get("X-Session-ID", "")
        # 验证会话
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        # 获取API实例和当前用户信息
        api_instance = web_sessions[session_id]
        current_username = getattr(api_instance, "auth_username", "")

        # 检查权限：管理员可以更新任何用户，普通用户只能更新自己
        is_admin = auth_system.check_permission(current_username, "manage_users")
        if not is_admin and current_username != username:
            return (
                jsonify(
                    {"success": False, "message": "权限不足：您只能修改自己的信息"}
                ),
                403,
            )

        # 获取请求数据
        data = request.get_json() or {}
        nickname = data.get("nickname", "").strip()  # 获取昵称并去除空格

        # 验证昵称不能为空
        if not nickname:
            return jsonify({"success": False, "message": "昵称不能为空"}), 400

        try:
            # 获取用户文件路径
            user_file_path = auth_system.get_user_file_path(username)

            # 检查用户是否存在
            if not os.path.exists(user_file_path):
                return jsonify({"success": False, "message": "用户不存在"}), 404

            # 读取用户数据
            with open(user_file_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)

            # 更新昵称
            user_data["nickname"] = nickname

            # 保存更新后的用户数据
            with open(user_file_path, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                current_username,
                "update_basic_info",
                f"更新用户 {username} 的昵称为: {nickname}",
                ip_address,
                session_id,
            )

            # 返回成功响应
            return jsonify(
                {
                    "success": True,
                    "message": "基本信息更新成功",
                    "data": {"username": username, "nickname": nickname},
                }
            )

        except Exception as e:
            # 捕获异常并记录日志
            app.logger.error(f"[更新基本信息] 失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500

    @app.route("/auth/admin/update_user_nickname", methods=["POST"])
    @login_required
    def auth_admin_update_user_nickname():
        """
        新功能：管理员强制修改用户昵称

        权限要求:
            - 管理员权限 ('manage_users')

        请求体参数（JSON）:
            username: 要更新的用户名
            nickname: 新昵称

        返回:
            操作结果
        """
        try:
            # 1. 获取当前登录用户 (来自 @login_required 装饰器设置的 g.user)
            current_username = g.user

            # 2. 检查管理员权限
            if not auth_system.check_permission(current_username, "manage_users"):
                return (
                    jsonify({"success": False, "message": "权限不足：需要管理员权限"}),
                    403,
                )

            # 3. 获取请求数据
            data = request.get_json() or {}
            target_username = data.get("username", "").strip()
            new_nickname = data.get("nickname", "").strip()

            # 4. 验证参数
            if not target_username:
                return jsonify({"success": False, "message": "缺少用户名参数"}), 400

            if not new_nickname:
                return jsonify({"success": False, "message": "新昵称不能为空"}), 400

            # 5. 获取用户文件路径
            user_file_path = auth_system.get_user_file_path(target_username)

            if not os.path.exists(user_file_path):
                return jsonify({"success": False, "message": "用户不存在"}), 404

            # 6. 读取、更新、保存用户数据
            # (使用 auth_system.lock 确保文件操作的线程安全)
            with auth_system.lock:
                with open(user_file_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                user_data["nickname"] = new_nickname

                with open(user_file_path, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 7. 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                current_username,
                "admin_update_nickname",
                f"管理员 {current_username} 更新了用户 {target_username} 的昵称为: {new_nickname}",
                ip_address,
                g.api_instance._web_session_id if hasattr(g, "api_instance") else "",
            )

            # 8. 返回成功响应
            return jsonify(
                {
                    "success": True,
                    "message": "昵称更新成功",
                    "data": {"username": target_username, "nickname": new_nickname},
                }
            )

        except Exception as e:
            app.logger.error(f"[管理员更新昵称] 失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500

    @app.route("/auth/admin/update_user_phone", methods=["POST"])
    def auth_admin_update_user_phone():
        """
        问题4修复：管理员更新用户手机号
        任务 3/3：落实一个手机号只能绑定一个账号

        功能说明：
        允许管理员更新用户的手机号（验证码非必需）

        请求体参数（JSON）:
            username: 要更新的用户名
            new_phone: 新手机号
            sms_code: 验证码（可选，管理员操作不强制）

        权限要求:
            - 管理员权限

        返回:
            操作结果
        """
        # 获取会话ID
        session_id = request.headers.get("X-Session-ID", "")
        # 验证会话
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        # 获取API实例和当前用户信息
        api_instance = web_sessions[session_id]
        current_username = getattr(api_instance, "auth_username", "")

        # 检查管理员权限
        if not auth_system.check_permission(current_username, "manage_users"):
            return (
                jsonify({"success": False, "message": "权限不足：需要管理员权限"}),
                403,
            )

        # 获取请求数据
        data = request.get_json() or {}
        username = data.get("username", "").strip()  # 目标用户
        new_phone = data.get("new_phone", "").strip()
        sms_code = data.get("sms_code", "").strip()  # 管理员操作时，sms_code可选

        # 验证参数
        if not username:
            return jsonify({"success": False, "message": "缺少用户名参数"}), 400

        if not new_phone:
            return jsonify({"success": False, "message": "新手机号不能为空"}), 400

        # 验证手机号格式
        import re

        if not re.match(r"^1[3-9]\d{9}$", new_phone):
            return jsonify({"success": False, "message": "手机号格式不正确"}), 400

        try:
            # 获取用户文件路径
            user_file_path = auth_system.get_user_file_path(username)

            # 检查用户是否存在
            if not os.path.exists(user_file_path):
                return jsonify({"success": False, "message": "用户不存在"}), 404

            # 管理员修改时，允许将手机号绑定到目标用户，即使该手机号已绑定到其他人
            auth_system.unbind_phone_from_user(new_phone, except_username=username)

            # 读取用户数据
            # (使用 AuthSystem 的锁确保文件操作的线程安全)
            with auth_system.lock:
                with open(user_file_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                # 更新手机号
                user_data["phone"] = new_phone

                # 保存更新后的用户数据
                with open(user_file_path, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                current_username,
                "admin_update_phone",
                f"管理员 {current_username} 更新了用户 {username} 的手机号为: {new_phone}",
                ip_address,
                session_id,
            )

            # 返回成功响应
            return jsonify(
                {
                    "success": True,
                    "message": "手机号更新成功",
                    "data": {"username": username, "phone": new_phone},
                }
            )

        except Exception as e:
            # 捕获异常并记录日志
            app.logger.error(f"[管理员更新手机号] 失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500

    @app.route("/auth/admin/login_logs", methods=["GET"])
    def auth_admin_login_logs():
        """获取登录日志（管理员）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_group = getattr(api_instance, "auth_group", "guest")

        # 只有管理员和超级管理员可以查看
        if auth_group not in ["admin", "super_admin"]:
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 获取参数
        username = request.args.get("username", None)
        limit = int(request.args.get("limit", 100))

        logs = auth_system.get_login_history(username, limit)
        return jsonify({"success": True, "logs": logs})

    @app.route("/auth/admin/get_user_school_accounts", methods=["GET"])
    def auth_admin_get_user_school_accounts():
        """获取指定认证用户的所有 school_account（管理员或有 auto_fill_password 权限）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_group = getattr(api_instance, "auth_group", "guest")
        auth_username = getattr(api_instance, "auth_username", None)

        # 检查权限：管理员或有 auto_fill_password 权限
        has_permission = False
        if auth_group in ["admin", "super_admin"]:
            has_permission = True
        elif auth_username:
            has_permission = auth_system.check_permission(
                auth_username, "auto_fill_password"
            )

        if not has_permission:
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 获取参数：要查询的用户名（如果不提供，则查询当前用户自己的）
        target_username = request.args.get("username", auth_username)

        # 如果是普通用户（非管理员），只能查询自己的
        if (
            auth_group not in ["admin", "super_admin"]
            and target_username != auth_username
        ):
            return jsonify({"success": False, "message": "只能查询自己的账户"}), 403

        # 加载 school_accounts
        accounts = api_instance._load_user_school_accounts(target_username)

        return jsonify(
            {"success": True, "username": target_username, "accounts": accounts}
        )

    @app.route("/auth/admin/get_all_users_school_accounts", methods=["GET"])
    def auth_admin_get_all_users_school_accounts():
        """获取所有认证用户的 school_account 列表（管理员或有 auto_fill_password 权限）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_group = getattr(api_instance, "auth_group", "guest")
        auth_username = getattr(api_instance, "auth_username", None)

        # 检查权限：管理员或有 auto_fill_password 权限
        has_permission = False
        if auth_group in ["admin", "super_admin"]:
            has_permission = True
        elif auth_username:
            has_permission = auth_system.check_permission(
                auth_username, "auto_fill_password"
            )

        if not has_permission:
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 扫描 user_accounts 目录，获取所有用户的 school_accounts
        user_accounts_dir = os.path.join(SCHOOL_ACCOUNTS_DIR, "user_accounts")
        all_users_accounts = {}

        if os.path.exists(user_accounts_dir):
            for filename in os.listdir(user_accounts_dir):
                if filename.endswith(".json"):
                    username = filename[:-5]  # 去掉 .json 后缀
                    try:
                        file_path = os.path.join(user_accounts_dir, filename)
                        with open(file_path, "r", encoding="utf-8") as f:
                            accounts = json.load(f)
                        all_users_accounts[username] = accounts
                    except Exception as e:
                        logging.error(
                            f"读取用户 {username} 的 school_accounts 失败: {e}"
                        )

        return jsonify({"success": True, "all_accounts": all_users_accounts})

    # ========== 新增：School Account 管理API（保存/添加） ==========
    @app.route("/api/admin/school_account/save", methods=["POST"])
    def api_admin_school_account_save():
        """
        保存或添加 School Account（PC端管理面板CRUD支持）。

        功能说明：
        - 允许管理员或有权限的用户保存/更新学校账户信息
        - 支持添加新账户和更新现有账户
        - 数据包括：用户名、密码、UA（User-Agent）

        请求参数（JSON）：
        - auth_username: 认证用户名（所属用户）
        - school_username: 学校账户用户名
        - password: 学校账户密码
        - ua: User-Agent字符串（可选）

        权限要求：
        - 管理员可以保存任何用户的账户
        - 普通用户只能保存自己的账户

        返回值：
        - success: 是否成功
        - message: 提示信息
        """
        # ========== 1. 验证会话 ==========
        # 从请求头获取会话ID
        session_id = request.headers.get("X-Session-ID", "")

        # 检查会话是否存在
        if not session_id or session_id not in web_sessions:
            # 会话不存在或已过期，返回401未授权
            return jsonify({"success": False, "message": "未登录或会话无效"}), 401

        # 获取当前用户的API实例
        api_instance = web_sessions[session_id]

        # 获取当前用户的权限信息
        auth_group = getattr(
            api_instance, "auth_group", "guest"
        )  # 用户组（guest/user/admin/super_admin）
        current_auth_username = getattr(
            api_instance, "auth_username", None
        )  # 当前登录的认证用户名

        # ========== 2. 解析请求数据 ==========
        try:
            # 从请求体获取JSON数据
            data = request.get_json()
            if not data:
                # 如果没有提供JSON数据，返回400错误
                return jsonify({"success": False, "message": "缺少请求数据"}), 400

            # 提取必需的字段并去除首尾空格
            auth_username = data.get(
                "auth_username", ""
            ).strip()  # 目标认证用户（账户所属）
            school_username = data.get("school_username", "").strip()  # 学校账户用户名
            password = data.get("password", "").strip()  # 学校账户密码
            ua = data.get("ua", "").strip()  # User-Agent（可选）

            # 验证必填字段
            if not auth_username or not school_username or not password:
                # 如果任何必填字段为空，返回400错误
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "缺少必填字段：auth_username, school_username, password",
                        }
                    ),
                    400,
                )

        except Exception as e:
            # 捕获JSON解析错误或其他异常
            logging.error(f"解析school_account保存请求失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": "请求数据格式错误"}), 400

        # ========== 3. 权限检查 ==========
        # 检查当前用户是否有权限保存指定用户的账户
        is_admin = auth_group in ["admin", "super_admin"]  # 是否是管理员

        # 权限规则：
        # 1. 管理员可以保存任何用户的账户
        # 2. 普通用户只能保存自己的账户（auth_username 必须等于 current_auth_username）
        if not is_admin and auth_username != current_auth_username:
            # 权限不足：普通用户试图保存其他用户的账户
            logging.warning(
                f"用户 {current_auth_username} 试图保存 {auth_username} 的账户，权限不足"
            )
            return (
                jsonify({"success": False, "message": "权限不足：只能保存自己的账户"}),
                403,
            )

        # ========== 4. 加载现有账户数据 ==========
        try:
            # 调用 API 实例的方法加载指定用户的所有 school_accounts
            # 返回格式：{school_username: {"password": "xxx", "ua": "xxx"}, ...}
            accounts = api_instance._load_user_school_accounts(auth_username)

            # 如果 accounts 为 None（不应该发生，但作为防御性编程），初始化为空字典
            if accounts is None:
                accounts = {}

        except Exception as e:
            # 加载失败，记录错误并返回500错误
            logging.error(
                f"加载用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "加载账户数据失败"}), 500

        # ========== 5. 更新或添加账户 ==========
        # 检查该 school_username 是否已存在
        is_new_account = school_username not in accounts

        # 更新账户信息（如果已存在则覆盖，如果不存在则添加）
        accounts[school_username] = {
            "password": password,  # 保存密码
            "ua": ua if ua else "",  # 保存UA，如果未提供则为空字符串
        }

        # 记录操作日志
        action = "添加" if is_new_account else "更新"
        logging.info(
            f"{action} school_account: 认证用户={auth_username}, 学校账户={school_username}, 操作者={current_auth_username}"
        )

        # ========== 6. 保存到文件 ==========
        try:
            # 调用 API 实例的方法将更新后的数据保存到文件
            api_instance._save_user_school_accounts(auth_username, accounts)

            # 保存成功，返回成功响应
            return jsonify(
                {
                    "success": True,
                    "message": f"账户 {school_username} {action}成功",
                    "is_new": is_new_account,  # 告诉前端这是新账户还是更新
                }
            )

        except Exception as e:
            # 保存失败，记录错误并返回500错误
            logging.error(
                f"保存用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "保存账户数据失败"}), 500

    # ========== 新增：School Account 管理API（删除） ==========
    @app.route("/api/admin/school_account/delete", methods=["POST"])
    def api_admin_school_account_delete():
        """
        删除 School Account（PC端管理面板CRUD支持）。

        功能说明：
        - 允许管理员或有权限的用户删除学校账户
        - 从指定认证用户的账户列表中移除指定的学校账户

        请求参数（JSON）：
        - auth_username: 认证用户名（所属用户）
        - school_username: 要删除的学校账户用户名

        权限要求：
        - 管理员可以删除任何用户的账户
        - 普通用户只能删除自己的账户

        返回值：
        - success: 是否成功
        - message: 提示信息
        """
        # ========== 1. 验证会话 ==========
        # 从请求头获取会话ID
        session_id = request.headers.get("X-Session-ID", "")

        # 检查会话是否存在
        if not session_id or session_id not in web_sessions:
            # 会话不存在或已过期，返回401未授权
            return jsonify({"success": False, "message": "未登录或会话无效"}), 401

        # 获取当前用户的API实例
        api_instance = web_sessions[session_id]

        # 获取当前用户的权限信息
        auth_group = getattr(api_instance, "auth_group", "guest")  # 用户组
        current_auth_username = getattr(
            api_instance, "auth_username", None
        )  # 当前登录用户

        # ========== 2. 解析请求数据 ==========
        try:
            # 从请求体获取JSON数据
            data = request.get_json()
            if not data:
                # 如果没有提供JSON数据，返回400错误
                return jsonify({"success": False, "message": "缺少请求数据"}), 400

            # 提取必需的字段并去除首尾空格
            auth_username = data.get("auth_username", "").strip()  # 目标认证用户
            school_username = data.get(
                "school_username", ""
            ).strip()  # 要删除的学校账户

            # 验证必填字段
            if not auth_username or not school_username:
                # 如果任何必填字段为空，返回400错误
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "缺少必填字段：auth_username, school_username",
                        }
                    ),
                    400,
                )

        except Exception as e:
            # 捕获JSON解析错误或其他异常
            logging.error(f"解析school_account删除请求失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": "请求数据格式错误"}), 400

        # ========== 3. 权限检查 ==========
        # 检查当前用户是否有权限删除指定用户的账户
        is_admin = auth_group in ["admin", "super_admin"]  # 是否是管理员

        # 权限规则：
        # 1. 管理员可以删除任何用户的账户
        # 2. 普通用户只能删除自己的账户（auth_username 必须等于 current_auth_username）
        if not is_admin and auth_username != current_auth_username:
            # 权限不足：普通用户试图删除其他用户的账户
            logging.warning(
                f"用户 {current_auth_username} 试图删除 {auth_username} 的账户 {school_username}，权限不足"
            )
            return (
                jsonify({"success": False, "message": "权限不足：只能删除自己的账户"}),
                403,
            )

        # ========== 4. 加载现有账户数据 ==========
        try:
            # 调用 API 实例的方法加载指定用户的所有 school_accounts
            accounts = api_instance._load_user_school_accounts(auth_username)

            # 如果 accounts 为 None，初始化为空字典
            if accounts is None:
                accounts = {}

        except Exception as e:
            # 加载失败，记录错误并返回500错误
            logging.error(
                f"加载用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "加载账户数据失败"}), 500

        # ========== 5. 删除账户 ==========
        # 检查要删除的账户是否存在
        if school_username not in accounts:
            # 账户不存在，返回404错误
            logging.warning(
                f"试图删除不存在的账户: 认证用户={auth_username}, 学校账户={school_username}"
            )
            return (
                jsonify(
                    {"success": False, "message": f"账户 {school_username} 不存在"}
                ),
                404,
            )

        # 从字典中删除该账户
        # 使用 pop() 方法安全地删除键值对
        accounts.pop(school_username)

        # 记录操作日志
        logging.info(
            f"删除 school_account: 认证用户={auth_username}, 学校账户={school_username}, 操作者={current_auth_username}"
        )

        # ========== 6. 保存到文件 ==========
        try:
            # 调用 API 实例的方法将更新后的数据保存到文件
            api_instance._save_user_school_accounts(auth_username, accounts)

            # 删除成功，返回成功响应
            return jsonify(
                {"success": True, "message": f"账户 {school_username} 删除成功"}
            )

        except Exception as e:
            # 保存失败，记录错误并返回500错误
            logging.error(
                f"保存用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "保存账户数据失败"}), 500

    @app.route("/api/admin/school_account/update", methods=["POST"])
    def api_admin_school_account_update():
        """
        更新 School Account（PC端管理面板CRUD支持）。

        功能说明：
        - 允许管理员或有权限的用户更新学校账户的密码和UA
        - 支持修改指定认证用户的学校账户信息

        请求参数（JSON）：
        - auth_username: 认证用户名（所属用户）
        - school_username: 学校账户用户名
        - password: 新密码
        - ua: 新User-Agent（可选）

        权限要求：
        - 管理员可以更新任何用户的账户
        - 普通用户只能更新自己的账户

        返回值：
        - success: 是否成功
        - message: 提示信息
        """
        # ========== 1. 验证会话 ==========
        # 从请求头获取会话ID
        session_id = request.headers.get("X-Session-ID", "")

        # 检查会话是否存在
        if not session_id or session_id not in web_sessions:
            # 会话不存在或已过期，返回401未授权
            return jsonify({"success": False, "message": "未登录或会话无效"}), 401

        # 获取当前用户的API实例
        api_instance = web_sessions[session_id]

        # 获取当前用户的权限信息
        auth_group = getattr(api_instance, "auth_group", "guest")  # 用户组
        current_auth_username = getattr(
            api_instance, "auth_username", None
        )  # 当前登录用户

        # ========== 2. 解析请求数据 ==========
        try:
            # 从请求体获取JSON数据
            data = request.get_json()
            if not data:
                # 如果没有提供JSON数据，返回400错误
                return jsonify({"success": False, "message": "缺少请求数据"}), 400

            # 提取必需的字段并去除首尾空格
            auth_username = data.get("auth_username", "").strip()  # 目标认证用户
            school_username = data.get("school_username", "").strip()  # 学校账户用户名
            password = data.get("password", "").strip()  # 新密码
            ua = data.get("ua", "").strip()  # 新User-Agent（可选）

            # 验证必填字段
            if not auth_username or not school_username or not password:
                # 如果任何必填字段为空，返回400错误
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "缺少必填字段：auth_username, school_username, password",
                        }
                    ),
                    400,
                )

        except Exception as e:
            # 捕获JSON解析错误或其他异常
            logging.error(f"解析school_account更新请求失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": "请求数据格式错误"}), 400

        # ========== 3. 权限检查 ==========
        # 检查当前用户是否有权限更新指定用户的账户
        is_admin = auth_group in ["admin", "super_admin"]  # 是否是管理员

        # 权限规则：
        # 1. 管理员可以更新任何用户的账户
        # 2. 普通用户只能更新自己的账户（auth_username 必须等于 current_auth_username）
        if not is_admin and auth_username != current_auth_username:
            # 权限不足：普通用户试图更新其他用户的账户
            logging.warning(
                f"用户 {current_auth_username} 试图更新 {auth_username} 的账户 {school_username}，权限不足"
            )
            return (
                jsonify({"success": False, "message": "权限不足：只能更新自己的账户"}),
                403,
            )

        # ========== 4. 加载现有账户数据 ==========
        try:
            # 调用 API 实例的方法加载指定用户的所有 school_accounts
            accounts = api_instance._load_user_school_accounts(auth_username)

            # 如果 accounts 为 None，初始化为空字典
            if accounts is None:
                accounts = {}

        except Exception as e:
            # 加载失败，记录错误并返回500错误
            logging.error(
                f"加载用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "加载账户数据失败"}), 500

        # ========== 5. 更新账户 ==========
        # 检查要更新的账户是否存在
        if school_username not in accounts:
            # 账户不存在，返回404错误
            logging.warning(
                f"试图更新不存在的账户: 认证用户={auth_username}, 学校账户={school_username}"
            )
            return (
                jsonify(
                    {"success": False, "message": f"账户 {school_username} 不存在"}
                ),
                404,
            )

        # 更新账户信息
        # 使用新格式（字典）存储密码和UA
        accounts[school_username] = {"password": password, "ua": ua if ua else ""}

        # 记录操作日志
        logging.info(
            f"更新 school_account: 认证用户={auth_username}, 学校账户={school_username}, 操作者={current_auth_username}"
        )

        # ========== 6. 保存到文件 ==========
        try:
            # 调用 API 实例的方法将更新后的数据保存到文件
            api_instance._save_user_school_accounts(auth_username, accounts)

            # 更新成功，返回成功响应
            return jsonify(
                {"success": True, "message": f"账户 {school_username} 更新成功"}
            )

        except Exception as e:
            # 保存失败，记录错误并返回500错误
            logging.error(
                f"保存用户 {auth_username} 的 school_accounts 失败: {e}", exc_info=True
            )
            return jsonify({"success": False, "message": "保存账户数据失败"}), 500

    @app.route("/logs/view", methods=["GET"])
    def view_logs():
        """查看应用日志（管理员）- 分页模式"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_group = getattr(api_instance, "auth_group", "guest")

        # 只有管理员和超级管理员可以查看
        if auth_group not in ["admin", "super_admin"]:
            return jsonify({"success": False, "message": "权限不足"}), 403

        # --- [修复] 分页参数 ---
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 100))
            if page < 1:
                page = 1
            if limit < 1:
                limit = 100
            if limit > 2000:  # 限制每页最多2000行
                limit = 2000
        except ValueError:
            page = 1
            limit = 100

        all_log_content = []
        log_files = []

        # 查找日志目录中的日志文件
        if os.path.exists(LOGIN_LOGS_DIR):
            # [修复] 确保按名称排序，以便'zx-slm-tool.log'在'zx-slm-tool-01.log'之前
            files = sorted(
                [
                    f
                    for f in os.listdir(LOGIN_LOGS_DIR)
                    if f.endswith(".log") or f.endswith(".jsonl")
                ]
            )
            for f in files:
                log_files.append(os.path.join(LOGIN_LOGS_DIR, f))

        # [修复] 读取所有日志文件内容
        # (注意：如果日志文件非常大，这里可能会消耗大量内存)
        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    all_log_content.extend(f.readlines())
            except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
                logging.debug(f"[日志读取] 无法读取日志文件 {log_file}: {e}")
                continue

        # --- [修复] 分页计算 ---
        total_lines = len(all_log_content)
        total_pages = (total_lines + limit - 1) // limit  # 向上取整
        if page > total_pages and total_pages > 0:
            page = total_pages

        # 计算切片索引 (注意：日志是倒序显示的，所以我们从末尾开始取)
        # 例如：共 1000 行, 每页 100.
        # 第1页 (page=1): lines[900:1000] (索引 -100 到末尾)
        # 第2页 (page=2): lines[800:900] (索引 -200 到 -100)

        start_index = max(0, total_lines - (page * limit))
        end_index = total_lines - ((page - 1) * limit)

        # 获取当前页的日志 (从旧到新)
        paginated_logs = all_log_content[start_index:end_index]

        # [修复] 反转列表，使最新的日志在最上面
        paginated_logs.reverse()

        return jsonify(
            {
                "success": True,
                "logs": paginated_logs,  # 返回当前页的行
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_lines": total_lines,
                    "limit": limit,
                },
            }
        )

    @app.route("/auth/admin/reset_password", methods=["POST"])
    def auth_admin_reset_password():
        """重置用户密码（管理员）或修改自己的密码"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")
        auth_group = getattr(api_instance, "auth_group", "guest")

        data = request.json
        target_username = data.get("username", "")
        new_password = data.get("new_password", "")
        old_password = data.get("old_password", "")  # 可选：用于用户自己修改密码时验证

        if not target_username or not new_password:
            return jsonify({"success": False, "message": "参数缺失"})

        # 判断是用户自己修改密码还是管理员重置他人密码
        is_self_change = target_username == auth_username

        if is_self_change:
            # 用户修改自己的密码：需要验证原密码
            if not old_password:
                return jsonify({"success": False, "message": "请提供当前密码"})

            # 验证原密码
            user_file = auth_system.get_user_file_path(auth_username)
            if not os.path.exists(user_file):
                return jsonify({"success": False, "message": "用户不存在"}), 404

            try:
                with open(user_file, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                stored_password = user_data.get("password")
            except Exception as e:
                logging.error(f"读取用户 {auth_username} 密码失败: {e}")
                return jsonify({"success": False, "message": "无法验证密码"}), 500

                # 验证原密码 (修正：使用 _verify_password 并比较 input vs stored)
                if not auth_system._verify_password(old_password, stored_password):
                    return jsonify({"success": False, "message": "当前密码错误"}), 401
        else:
            # 管理员重置他人密码：需要管理权限
            if not auth_system.check_permission(auth_username, "reset_user_password"):
                return jsonify({"success": False, "message": "权限不足"}), 403

        # 执行密码重置
        result = auth_system.reset_user_password(target_username, new_password)
        return jsonify(result)

    @app.route("/auth/user/update_avatar", methods=["POST"])
    def auth_user_update_avatar():
        """更新用户头像（URL方式）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_username or auth_username == "guest":
            return jsonify({"success": False, "message": "游客无法设置头像"})

        data = request.json
        avatar_url = data.get("avatar_url", "")

        result = auth_system.update_user_avatar(auth_username, avatar_url)
        return jsonify(result)

    @app.route("/auth/user/upload_avatar", methods=["POST"])
    def auth_user_upload_avatar():
        """上传用户头像文件（multipart/form-data）"""

        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_username or auth_username == "guest":
            return jsonify({"success": False, "message": "游客无法上传头像"})

        # 检查是否有文件上传
        if "avatar" not in request.files:
            return jsonify({"success": False, "message": "未找到头像文件"}), 400

        file = request.files["avatar"]

        if file.filename == "":
            return jsonify({"success": False, "message": "未选择文件"}), 400

        # 检查文件类型
        allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return (
                jsonify(
                    {"success": False, "message": "不支持的文件格式，请上传图片文件"}
                ),
                400,
            )

        # 读取文件内容
        file_content = file.read()

        # 检查文件大小（限制为5MB）
        max_size = 5 * 1024 * 1024  # 5MB
        if len(file_content) > max_size:
            return (
                jsonify({"success": False, "message": "文件过大，请上传小于5MB的图片"}),
                400,
            )

        try:
            # 使用PIL打开图片并转换为PNG格式
            img = Image.open(io.BytesIO(file_content))

            # 转换为RGB模式（PNG不支持CMYK等模式）
            if img.mode in ("RGBA", "LA", "P"):
                # 保留透明度
                pass
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # 将图片转换为PNG格式的字节流
            png_buffer = io.BytesIO()
            img.save(png_buffer, format="PNG", optimize=True)
            png_content = png_buffer.getvalue()

            # 计算SHA256哈希
            sha256_hash = hashlib.sha256(png_content).hexdigest()

            # 创建存储目录
            images_dir = os.path.join("system_accounts", "images")
            os.makedirs(images_dir, exist_ok=True)

            # 保存为PNG文件
            filename = f"{sha256_hash}.png"
            filepath = os.path.join(images_dir, filename)

            with open(filepath, "wb") as f:
                f.write(png_content)

            # 更新索引文件，记录上传信息
            index_file = os.path.join(images_dir, "_index.json")
            try:
                # 读取现有索引
                if os.path.exists(index_file):
                    with open(index_file, "r", encoding="utf-8") as f:
                        index_data = json.load(f)
                else:
                    index_data = {
                        "version": "1.0",
                        "description": "用户头像索引文件，记录每个文件的上传信息",
                        "files": {},
                    }

                # 获取客户端IP
                ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)

                # 添加/更新文件信息
                index_data["files"][filename] = {
                    "username": auth_username,
                    "upload_time": time.time(),
                    "upload_time_str": datetime.datetime.now().isoformat(),
                    "ip_address": ip_address,
                    "original_filename": file.filename,
                    "file_size": len(png_content),
                    "sha256": sha256_hash,
                }

                # 保存索引
                with open(index_file, "w", encoding="utf-8") as f:
                    json.dump(index_data, f, indent=2, ensure_ascii=False)

                logging.info(
                    f"用户 {auth_username} 从 {ip_address} 上传头像: {filename}"
                )
            except Exception as e:
                logging.error(f"更新头像索引失败: {e}", exc_info=True)
                # 不影响上传流程，继续执行

        except Exception as e:
            return (
                jsonify({"success": False, "message": f"图片处理失败: {str(e)}"}),
                500,
            )

        # 构建头像URL
        avatar_url = f"/api/avatar/{filename}"

        # 更新用户头像
        result = auth_system.update_user_avatar(auth_username, avatar_url)

        if result.get("success"):
            # 返回新的头像URL
            return jsonify(
                {"success": True, "avatar_url": avatar_url, "message": "头像上传成功"}
            )
        else:
            # 如果更新失败，删除已上传的文件和索引
            try:
                os.remove(filepath)
                # 从索引中移除
                if os.path.exists(index_file):
                    with open(index_file, "r", encoding="utf-8") as f:
                        index_data = json.load(f)
                    if filename in index_data.get("files", {}):
                        del index_data["files"][filename]
                        with open(index_file, "w", encoding="utf-8") as f:
                            json.dump(index_data, f, indent=2, ensure_ascii=False)
            except (OSError, PermissionError) as e:
                logging.warning(f"[会话索引] 更新索引文件失败: {e}")
            return jsonify(result)

    @app.route("/default_avatar.png")
    @app.route("/static/default_avatar.png")
    def serve_default_avatar():
        """

        为 default_avatar.png 提供根路径和 /static 路径的访问。

        问题：
        - 注册页面 (auth-reg-avatar-preview) hardcodes /static/default_avatar.png (404)
        - 个人资料 (loadPersonalInfo) 在 avatar_url 为 'default_avatar.png' 时，
          会直接请求 /default_avatar.png (404)

        解决：
        添加这两个路由，统一指向 ./default_avatar.png 文件。
        """
        try:
            # 确保 os 模块已导入
            import os

            # 使用 os.path.dirname(__file__) 确保路径是相对于 main.py 的
            # __file__ 在 main() 中已保证可用
            base_dir = os.path.dirname(__file__)
            default_avatar_path = os.path.join(base_dir, "default_avatar.png")

            if os.path.exists(default_avatar_path):
                # 使用 send_file 发送文件 (必须在顶部导入)
                return send_file(default_avatar_path, mimetype="image/png")
            else:
                logging.warning(f"Default avatar not found at {default_avatar_path}")
                return "Default avatar not found", 404
        except NameError as e:
            # 如果 send_file 未导入 (虽然我们上面修复了，但作为兜底)
            logging.error(f"Serve default avatar failed: {e}. Is send_file imported?")
            return "Server configuration error", 500
        except Exception as e:
            logging.error(f"Error serving default avatar: {e}", exc_info=True)
            return "Server error", 500

    @app.route("/api/avatar/<filename>", methods=["GET"])
    def serve_avatar(filename):
        """提供头像图片服务（需要会话认证，管理员可访问）"""

        if filename == "default_avatar.png":
            return redirect("/default_avatar.png")

        # 验证会话 - 支持从header、cookie或query参数获取session_id
        session_id = (
            request.headers.get("X-Session-ID", "")
            or request.cookies.get("session_id", "")
            or request.args.get("session_id", "")
        )

        # 如果没有会话ID或会话无效，返回401
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        # 获取当前用户信息，检查是否为管理员
        api_instance = web_sessions[session_id]
        current_username = getattr(api_instance, "auth_username", "")
        is_admin = (
            auth_system.check_permission(current_username, "manage_users")
            if current_username
            else False
        )

        # 管理员可以访问所有头像，无需进一步验证
        # 普通用户也可以访问（因为他们已通过会话验证）

        # 问题1修复：特殊处理默认头像文件
        # 默认头像位于项目根目录的default_avatar.png
        if filename == "default_avatar.png":
            default_avatar_path = os.path.join(
                os.path.dirname(__file__), "default_avatar.png"
            )
            if os.path.exists(default_avatar_path):
                try:
                    return send_file(default_avatar_path, mimetype="image/png")
                except Exception as e:
                    return (
                        jsonify(
                            {"success": False, "message": f"读取默认头像失败: {str(e)}"}
                        ),
                        500,
                    )
            else:
                return jsonify({"success": False, "message": "默认头像文件不存在"}), 404

        # 验证文件名格式（只允许PNG文件，且文件名为64字符的十六进制哈希值）
        # 64 chars hash + .png (4 chars)
        if not filename.endswith(".png") or len(filename) != 68:
            return jsonify({"success": False, "message": "无效的文件名"}), 400

        # 构建文件路径
        filepath = os.path.join("system_accounts", "images", filename)

        # 检查文件是否存在
        if not os.path.exists(filepath):
            return jsonify({"success": False, "message": "头像不存在"}), 404

        # 返回图片文件
        try:
            return send_file(filepath, mimetype="image/png")
        except Exception as e:
            return (
                jsonify({"success": False, "message": f"读取文件失败: {str(e)}"}),
                500,
            )

    @app.route("/auth/admin/clear_user_avatar", methods=["POST"])
    def auth_admin_clear_user_avatar():
        """管理员：强制清除用户头像"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查管理权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        target_username = data.get("username", "")

        if not target_username:
            return jsonify({"success": False, "message": "缺少用户名参数"}), 400

        # 获取目标用户的头像URL
        user_details = auth_system.get_user_details(target_username)
        if not user_details:
            return jsonify({"success": False, "message": "用户不存在"}), 404

        old_avatar_url = user_details.get("avatar_url", "")

        # 清除用户头像URL
        result = auth_system.update_user_avatar(target_username, "default_avatar.png")

        if result.get("success"):
            # 如果有旧头像，尝试删除文件和索引（但不强制，因为可能被其他用户共享）
            if old_avatar_url:
                try:
                    # 提取文件名
                    filename = old_avatar_url.split("/")[-1]
                    filepath = os.path.join("system_accounts", "images", filename)
                    index_file = os.path.join(
                        "system_accounts", "images", "_index.json"
                    )

                    # 检查索引中的文件信息
                    if os.path.exists(index_file):
                        with open(index_file, "r", encoding="utf-8") as f:
                            index_data = json.load(f)

                        file_info = index_data.get("files", {}).get(filename, {})

                        # 只有当文件是该用户上传的才删除（避免误删共享头像）
                        if file_info.get("username") == target_username:
                            # 删除文件
                            if os.path.exists(filepath):
                                os.remove(filepath)
                                logging.info(
                                    f"管理员 {auth_username} 删除了用户 {target_username} 的头像文件: {filename}"
                                )

                            # 从索引中移除
                            if filename in index_data.get("files", {}):
                                del index_data["files"][filename]
                                with open(index_file, "w", encoding="utf-8") as f:
                                    json.dump(
                                        index_data, f, indent=2, ensure_ascii=False
                                    )
                        else:
                            logging.info(
                                f"管理员 {auth_username} 清除了用户 {target_username} 的头像URL，但文件由其他用户上传，未删除文件"
                            )

                except Exception as e:
                    logging.error(f"清除头像文件时出错: {e}", exc_info=True)
                    # 不影响主要功能，继续

            # 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                auth_username,
                "clear_user_avatar",
                f"强制清除用户 {target_username} 的头像",
                ip_address,
                session_id,
            )

            return jsonify(
                {"success": True, "message": f"已清除用户 {target_username} 的头像"}
            )
        else:
            return jsonify(result)

    @app.route("/auth/user/update_theme", methods=["POST"])
    def auth_user_update_theme():
        """更新用户主题"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_username or auth_username == "guest":
            return jsonify({"success": False, "message": "游客无法设置主题"})

        data = request.json
        theme = data.get("theme", "light")

        result = auth_system.update_user_theme(auth_username, theme)
        return jsonify(result)

    @app.route("/auth/user/details", methods=["GET"])
    def auth_user_details():
        """获取用户详细信息"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_username or auth_username == "guest":
            return jsonify({"success": False, "message": "游客无详细信息"})

        details = auth_system.get_user_details(auth_username)
        if details:
            return jsonify({"success": True, "user": details})
        return jsonify({"success": False, "message": "用户不存在"})

    @app.route("/auth/user/avatar", methods=["GET"])
    def auth_get_user_avatar():
        """根据用户名获取头像URL（管理员可查询所有用户）

        查询参数:
        - username: 用户名（可选，不提供则返回当前用户）
        """
        session_id = request.headers.get("X-Session-ID", "")
        target_username = request.args.get("username", "")

        # 验证会话
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        api_instance = web_sessions[session_id]
        if not hasattr(api_instance, "auth_username"):
            return jsonify({"success": False, "message": "未登录"}), 401

        current_username = getattr(api_instance, "auth_username", "")
        is_admin = auth_system.check_permission(current_username, "manage_users")

        # 如果没有指定用户名，返回当前用户的头像
        if not target_username:
            target_username = current_username

            if not target_username or target_username == "guest":
                return jsonify(
                    {"success": True, "avatar_url": "", "message": "游客无头像"}
                )

        # 管理员可以查询任何用户的头像
        # 普通用户只能查询自己的头像
        if not is_admin and target_username != current_username:
            return (
                jsonify({"success": False, "message": "权限不足，只能查询自己的头像"}),
                403,
            )

        # 获取指定用户的头像
        details = auth_system.get_user_details(target_username)
        if details:
            return jsonify(
                {
                    "success": True,
                    "avatar_url": details.get("avatar_url", ""),
                    "username": target_username,
                }
            )

        return jsonify({"success": False, "message": "用户不存在", "avatar_url": ""})

    @app.route("/auth/admin/update_max_sessions", methods=["POST"])
    def auth_admin_update_max_sessions():
        """更新用户最大会话数量（管理员）

        请求参数:
        - username: 目标用户名
        - max_sessions: 最大会话数 (1=单会话, >1=指定数量, -1=无限制)
        """
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")
        auth_group = getattr(api_instance, "auth_group", "guest")

        # 检查权限
        if not auth_system.check_permission(auth_username, "manage_users"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        data = request.json
        target_username = data.get("username", "")
        max_sessions = data.get("max_sessions", 1)

        # 验证参数
        if not isinstance(max_sessions, int) or (
            max_sessions < 1 and max_sessions != -1
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "无效的会话数量：必须为正整数或-1（无限制）",
                    }
                ),
                400,
            )

        result = auth_system.update_max_sessions(target_username, max_sessions)

        # 记录审计日志
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        auth_system.log_audit(
            auth_username,
            "update_max_sessions",
            f"修改用户 {target_username} 的最大会话数为: {max_sessions}",
            ip_address,
            session_id,
        )

        return jsonify(result)

    @app.route("/auth/user/sessions", methods=["GET"])
    def auth_user_sessions():
        """获取用户的所有会话"""
        session_id = request.headers.get("X-Session-ID", "")
        api_instance = None
        is_guest = False
        auth_username = ""

        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]
                is_guest = getattr(api_instance, "is_guest", False)
                auth_username = getattr(api_instance, "auth_username", "")
            else:
                # 尝试从文件加载，以应对内存中可能不存在的情况 (例如刚恢复)
                state = load_session_state(session_id)
                if state:
                    # 仅获取必要信息，不创建完整实例
                    is_guest = state.get("is_guest", False)
                    auth_username = state.get("auth_username", "")
                else:
                    # 如果内存和文件都没有，则视为未登录
                    return (
                        jsonify({"success": False, "message": "会话无效或未登录"}),
                        401,
                    )

        sessions_info = []

        if is_guest:
            # 游客模式：只显示当前会话
            logging.debug(
                f"auth_user_sessions: Handling guest session {session_id[:8]}"
            )
            session_file = get_session_file_path(session_id)
            created_at = 0
            last_activity = 0
            login_success_status = False  # 游客没有学校账号登录状态

            if os.path.exists(session_file):
                try:
                    with open(session_file, "r", encoding="utf-8") as f:
                        session_data = json.load(f)
                    created_at = session_data.get("created_at", 0)
                    last_activity = session_data.get(
                        "last_accessed", 0
                    )  # 使用 last_accessed
                except Exception as e:
                    logging.warning(
                        f"Failed to read guest session file {session_file}: {e}"
                    )

            sessions_info.append(
                {
                    "session_id": session_id,
                    # 添加哈希用于显示
                    "session_hash": hashlib.sha256(session_id.encode()).hexdigest()[
                        :16
                    ],
                    "created_at": created_at,
                    "last_activity": last_activity,
                    "is_current": True,  # 游客访问时，这个会话总是当前的
                    "login_success": login_success_status,  # 游客的学校登录状态总是 False
                    "user_data": {"username": "guest"},  # 简单标识
                }
            )
            logging.debug(
                f"auth_user_sessions: Guest session info prepared: {sessions_info}"
            )
            return jsonify(
                {"success": True, "sessions": sessions_info, "max_sessions": -1}
            )

        elif auth_username:
            # 注册用户模式：保持原有逻辑
            logging.debug(
                f"auth_user_sessions: Handling registered user {auth_username}"
            )
            session_ids = auth_system.get_user_sessions(auth_username)
            logging.debug(
                f"auth_user_sessions: Found linked session IDs for {auth_username}: {session_ids}"
            )

            # 获取用户的最大会话数设置
            user_details = auth_system.get_user_details(auth_username)
            max_sessions = user_details.get("max_sessions", 1) if user_details else 1

            for sid in session_ids:
                session_file = get_session_file_path(sid)
                if os.path.exists(session_file):
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            session_data = json.load(f)

                        # 确保加载的数据属于当前用户
                        if session_data.get("auth_username") == auth_username:
                            # 15. 修正多账号模式下的“未登录”状态
                            is_multi_mode = session_data.get(
                                "is_multi_account_mode", False
                            )
                            session_login_success = session_data.get(
                                "login_success", False
                            )  # 单账号模式的状态

                            if is_multi_mode:
                                # 多账号模式：检查是否有任何一个子账号已登录
                                account_states = session_data.get(
                                    "multi_account_states", {}
                                )
                                # 检查是否有任何一个 'school_account_logged_in' 为 True
                                # (这依赖于步骤1中 save_session_state 的修正)
                                session_login_success = any(
                                    acc.get("school_account_logged_in", False)
                                    for acc in account_states.values()
                                )

                            sessions_info.append(
                                {
                                    "session_id": sid,
                                    # 添加哈希
                                    "session_hash": hashlib.sha256(
                                        sid.encode()
                                    ).hexdigest()[:16],
                                    "created_at": session_data.get("created_at", 0),
                                    # 使用 last_accessed
                                    "last_activity": session_data.get(
                                        "last_accessed", 0
                                    ),
                                    "is_current": sid == session_id,
                                    "login_success": session_login_success,  # <-- 使用修正后的状态
                                    "is_multi_account_mode": is_multi_mode,  # <-- 确保传递此标志
                                    "user_data": session_data.get("user_data", {}),
                                }
                            )
                    except Exception as e:
                        logging.warning(
                            f"Failed to read session file {session_file} for user {auth_username}: {e}"
                        )
                        continue  # 跳过损坏的文件
            logging.debug(
                f"auth_user_sessions: Registered user session info prepared: {len(sessions_info)} sessions"
            )
            return jsonify(
                {
                    "success": True,
                    "sessions": sessions_info,
                    "max_sessions": max_sessions,
                }
            )
        else:
            # 既不是游客也不是有效注册用户（理论上不应发生，除非状态异常）
            logging.warning(
                f"auth_user_sessions: Invalid state for session {session_id[:8]} - neither guest nor valid user."
            )
            return jsonify({"success": False, "message": "会话状态异常"}), 500

    @app.route("/auth/user/delete_session", methods=["POST"])
    def auth_user_delete_session():
        """删除用户的一个会话"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_username or auth_username == "guest":
            return jsonify({"success": False, "message": "游客无会话管理"})

        data = request.json
        target_session_id = data.get("session_id", "")

        if not target_session_id:
            return jsonify({"success": False, "message": "会话ID缺失"})

        # 不能删除当前会话
        if target_session_id == session_id:
            return jsonify({"success": False, "message": "不能删除当前会话"})

        # 从用户数据中移除
        auth_system.unlink_session_from_user(auth_username, target_session_id)

        # 删除会话文件
        session_file = get_session_file_path(target_session_id)
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except (FileNotFoundError, PermissionError) as e:
                logging.debug(f"[会话删除] 删除会话文件失败: {e}")

        # 从内存中移除
        with web_sessions_lock:
            if target_session_id in web_sessions:
                del web_sessions[target_session_id]

        return jsonify({"success": True, "message": "会话已删除"})

    @app.route("/auth/user/create_session_persistence", methods=["POST"])
    def auth_user_create_session_persistence():
        """创建会话持久化文件（登录状态下）"""
        session_id = request.headers.get("X-Session-ID", "")

        api_instance = None
        is_guest = True  # 默认假设是游客或未登录

        if session_id:
            with web_sessions_lock:
                if session_id in web_sessions:
                    api_instance = web_sessions[session_id]
                    is_guest = getattr(
                        api_instance, "is_guest", True
                    )  # 检查内存中的实例
                else:
                    # 尝试从文件加载判断是否游客
                    state = load_session_state(session_id)
                    if state:
                        is_guest = state.get("is_guest", True)
                    # else: # 文件不存在，保持 is_guest = True (视为未登录)

        # 如果是游客或根本没有有效的会话实例，则禁止创建
        if is_guest:
            logging.warning(
                f"Attempt by guest session {session_id[:8]} to create persistent session blocked."
            )
            return (
                jsonify({"success": False, "message": "游客不允许创建额外的会话"}),
                403,
            )

        # （确保 api_instance 在非游客情况下是有效的）
        if not api_instance:  # 双重检查，理论上非游客时 api_instance 应该已加载
            return jsonify({"success": False, "message": "会话无效或未登录"}), 401

        auth_username = getattr(api_instance, "auth_username", "")

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 游客也可以创建会话持久化，但不关联到用户账号
        is_guest = getattr(api_instance, "is_guest", False)

        # 获取新的会话ID（从请求中或生成新的）
        data = request.json or {}
        new_session_id = data.get("session_id", "")

        if not new_session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 400

        # 验证UUID格式

        uuid_pattern = re.compile(
            r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$",
            re.IGNORECASE,
        )
        if not uuid_pattern.match(new_session_id):
            return jsonify({"success": False, "message": "无效的UUID格式"}), 400

        # 创建新的API实例，继承当前用户的认证信息
        new_api_instance = Api(args)
        new_api_instance._session_created_at = time.time()
        new_api_instance._web_session_id = new_session_id

        # 继承认证信息
        if hasattr(api_instance, "auth_username"):
            new_api_instance.auth_username = api_instance.auth_username
            new_api_instance.auth_group = getattr(api_instance, "auth_group", "guest")
            new_api_instance.is_guest = is_guest
            new_api_instance.is_authenticated = True

        # 继承参数配置
        if hasattr(api_instance, "params"):
            new_api_instance.params = copy.deepcopy(api_instance.params)

        # 继承User-Agent
        if hasattr(api_instance, "device_ua"):
            new_api_instance.device_ua = api_instance.device_ua

        # 如果是注册用户（非游客），处理会话关联
        cleanup_message = ""
        if not is_guest and auth_username:
            # 检查并强制执行会话数量限制
            old_sessions, cleanup_message = (
                auth_system.check_single_session_enforcement(
                    auth_username, new_session_id
                )
            )

            # 清理旧会话（如果超出限制）- 使用后台线程异步清理，不阻塞响应
            if old_sessions:

                def cleanup_old_sessions_async():
                    for old_sid in old_sessions:
                        try:
                            cleanup_session(old_sid, "session_limit_exceeded")
                        except Exception as e:
                            logging.error(f"后台清理旧会话失败 {old_sid[:16]}...: {e}")

                cleanup_thread = threading.Thread(
                    target=cleanup_old_sessions_async, daemon=True
                )
                cleanup_thread.start()

            # 关联新会话到用户账号
            auth_system.link_session_to_user(auth_username, new_session_id)

            # 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            audit_details = f"创建新会话持久化文件，会话ID: {new_session_id}"
            if cleanup_message:
                audit_details += f"; {cleanup_message}"

            auth_system.log_audit(
                auth_username,
                "create_session_persistence",
                audit_details,
                ip_address,
                session_id,
            )

        # 保存新会话状态到文件
        with web_sessions_lock:
            web_sessions[new_session_id] = new_api_instance
            save_session_state(new_session_id, new_api_instance, force_save=True)

        response_data = {
            "success": True,
            "message": "会话持久化文件已创建",
            "session_id": new_session_id,
        }

        # 添加清理提示（如果有）
        if cleanup_message:
            response_data["cleanup_message"] = cleanup_message

        logging.info(f"用户 {auth_username} 创建新会话持久化: {new_session_id[:32]}...")
        # 创建 Flask 响应对象
        response = make_response(jsonify(response_data))

        # 如果是注册用户（非游客），为其生成新 Token 并设置 Cookie
        if not is_guest and auth_username:
            try:
                # 1. 为新会话生成新 Token
                new_token = token_manager.create_token(auth_username, new_session_id)
                logging.info(f"为新会话 {new_session_id[:8]}... 生成了 Token")

                # 2. 设置 Set-Cookie 响应头
                response.set_cookie(
                    "auth_token",
                    value=new_token,
                    max_age=3600,  # 1 小时
                    httponly=True,  # 关键：防止 JS 访问
                    secure=False,  # 开发环境 False，生产环境应设为 True (需要 HTTPS)
                    samesite="Lax",  # 推荐的 SameSite 策略
                )
                logging.info(
                    f"已为新会话 {new_session_id[:8]}... 设置 auth_token Cookie"
                )

            except Exception as token_err:
                # 记录 Token 生成或 Cookie 设置错误，但不阻止会话创建本身
                logging.error(
                    f"为新会话 {new_session_id[:8]} 生成 Token 或设置 Cookie 时出错: {token_err}",
                    exc_info=True,
                )
                # 可以选择在这里修改 response_data 添加警告信息
                # response_data['warning'] = "Token未能成功设置，后续操作可能需要重新登录"
                # response = make_response(jsonify(response_data)) # 如果需要更新响应内容

        # 返回带有 Set-Cookie (如果适用) 的响应对象
        return response

    @app.route("/auth/admin/all_sessions", methods=["GET"])
    def auth_admin_all_sessions():
        """管理员：获取所有活跃会话（查看所有会话）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not session_id:
            return jsonify({"success": False, "message": "缺少当前会话ID"}), 401

        with web_sessions_lock:
            if session_id not in web_sessions:
                # 尝试从文件加载，如果连文件都没有，那肯定没登录
                state = load_session_state(session_id)
                if not state:
                    return (
                        jsonify({"success": False, "message": "当前会话无效或已过期"}),
                        401,
                    )
                # 如果文件存在，创建一个临时实例来获取用户名
                api_instance = Api(args)
                restore_session_to_api_instance(api_instance, state)
                web_sessions[session_id] = api_instance  # 加载成功后放入内存
                logging.info(f"创建新会话时，按需恢复了发起请求的会话 {session_id[:8]}")
            else:
                api_instance = web_sessions[session_id]

        auth_username = getattr(api_instance, "auth_username", None)
        is_guest = getattr(api_instance, "is_guest", True)

        # 只对非游客用户验证 Token
        if not is_guest and auth_username:
            token_from_cookie = request.cookies.get("auth_token")
            if not token_from_cookie:
                logging.warning(
                    f"用户 {auth_username} 尝试创建会话但缺少 auth_token cookie"
                )
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "缺少认证令牌(cookie)，请重新登录",
                            "need_login": True,
                        }
                    ),
                    401,
                )

            is_valid, reason = token_manager.verify_token(
                auth_username, session_id, token_from_cookie
            )
            if not is_valid:
                logging.warning(
                    f"用户 {auth_username} 尝试创建会话但令牌无效: {reason}"
                )
                # 令牌无效，要求重新登录，并清除无效cookie
                response_data = {
                    "success": False,
                    "message": f"令牌验证失败 ({reason})，请重新登录",
                    "need_login": True,
                }
                response = make_response(jsonify(response_data), 401)
                response.set_cookie("auth_token", "", max_age=0)
                return response
            else:
                # Token有效，刷新它
                token_manager.refresh_token(auth_username, session_id)
                logging.debug(
                    f"用户 {auth_username} (会话 {session_id[:8]}) Token 验证通过并已刷新"
                )
        elif not is_guest and not auth_username:
            # 有会话实例但没有用户名，说明状态异常
            logging.error(f"会话 {session_id[:8]} 存在但缺少用户名，无法创建新会话")
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "当前会话状态异常，请重新登录",
                        "need_login": True,
                    }
                ),
                401,
            )

        # 检查查看所有会话权限
        if not auth_system.check_permission(auth_username, "god_mode"):
            return jsonify({"success": False, "message": "需要查看所有会话权限"}), 403

        # 获取所有会话信息（包括内存中的和磁盘上的）
        all_sessions = []
        session_ids_in_memory = set()

        # 1. 首先获取内存中的会话
        with web_sessions_lock:
            for sid, api in web_sessions.items():
                session_info = {
                    "session_id": sid,
                    "session_hash": hashlib.sha256(sid.encode()).hexdigest()[:16],
                    "auth_username": getattr(api, "auth_username", None),
                    "auth_group": getattr(api, "auth_group", "guest"),
                    "is_authenticated": getattr(api, "is_authenticated", False),
                    "is_guest": getattr(api, "is_guest", False),
                    "created_at": getattr(api, "_session_created_at", 0),
                    "login_success": getattr(api, "login_success", False),
                    "user_info": getattr(api, "user_info", {}),
                    "is_current": sid == session_id,
                    # 添加username字段供前端使用
                    "username": getattr(api, "auth_username", None),
                }
                all_sessions.append(session_info)
                session_ids_in_memory.add(sid)

        # 2. 然后扫描磁盘上的会话文件，添加未在内存中的会话
        try:
            if os.path.exists(SESSION_STORAGE_DIR):
                for filename in os.listdir(SESSION_STORAGE_DIR):
                    if filename == "_index.json" or not filename.endswith(".json"):
                        continue

                    session_file = os.path.join(SESSION_STORAGE_DIR, filename)
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            state = json.load(f)

                        sid = state.get("session_id")
                        if not sid or sid in session_ids_in_memory:
                            continue  # 跳过已在内存中的会话

                        # 15. 修正多账号模式下的“未登录”状态
                        is_multi_mode = state.get("is_multi_account_mode", False)
                        session_login_success = state.get(
                            "login_success", False
                        )  # 单账号模式的状态

                        if is_multi_mode:
                            # 多账号模式：检查是否有任何一个子账号已登录
                            account_states = state.get("multi_account_states", {})
                            # 检查是否有任何一个 'school_account_logged_in' 为 True
                            # (这依赖于步骤1中 save_session_state 的修正)
                            session_login_success = any(
                                acc.get("school_account_logged_in", False)
                                for acc in account_states.values()
                            )

                        # 从文件中读取会话信息
                        session_info = {
                            "session_id": sid,
                            "session_hash": hashlib.sha256(sid.encode()).hexdigest()[
                                :16
                            ],
                            "auth_username": state.get("auth_username", None),
                            "auth_group": state.get("auth_group", "guest"),
                            "is_authenticated": state.get("is_authenticated", False),
                            "is_guest": state.get("is_guest", False),
                            "created_at": state.get("created_at", 0),
                            "login_success": session_login_success,  # <-- 使用修正后的状态
                            "is_multi_account_mode": is_multi_mode,  # <-- 传递多账号模式标志
                            "user_info": state.get("user_info", {}),
                            "is_current": sid == session_id,
                            # 添加username字段供前端使用
                            "username": state.get("auth_username", None),
                        }
                        all_sessions.append(session_info)
                    except Exception as e:
                        logging.warning(f"读取会话文件 {filename} 失败: {e}")
                        continue
        except Exception as e:
            logging.error(f"扫描会话文件目录失败: {e}")

        return jsonify(
            {
                "success": True,
                "sessions": all_sessions,
                "total_count": len(all_sessions),
            }
        )

    @app.route("/auth/admin/destroy_session", methods=["POST"])
    def auth_admin_destroy_session():
        """管理员：强制销毁任意会话（查看所有会话）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查查看所有会话权限
        if not auth_system.check_permission(auth_username, "god_mode"):
            return jsonify({"success": False, "message": "需要查看所有会话权限"}), 403

        data = request.json
        target_session_id = data.get("session_id", "")

        if not target_session_id:
            return jsonify({"success": False, "message": "会话ID缺失"})

        # 不能销毁自己的会话
        if target_session_id == session_id:
            return jsonify({"success": False, "message": "不能销毁当前会话"})

        # 获取目标会话的用户信息（用于日志）
        target_username = "unknown"
        with web_sessions_lock:
            if target_session_id in web_sessions:
                target_api = web_sessions[target_session_id]
                target_username = getattr(target_api, "auth_username", "unknown")

        # 从用户数据中移除会话关联
        if target_username != "unknown" and target_username != "guest":
            auth_system.unlink_session_from_user(target_username, target_session_id)

        # 删除会话文件

        session_hash = hashlib.sha256(target_session_id.encode()).hexdigest()
        session_file = os.path.join(SESSION_STORAGE_DIR, f"{session_hash}.json")
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except (FileNotFoundError, PermissionError) as e:
                logging.debug(f"[会话强制登出] 删除会话文件失败: {e}")

        # 从内存中移除
        with web_sessions_lock:
            if target_session_id in web_sessions:
                del web_sessions[target_session_id]

        # 记录审计日志
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        auth_system.log_audit(
            auth_username,
            "destroy_session",
            f"强制销毁用户 {target_username} 的会话: {target_session_id[:32]}...",
            ip_address,
            session_id,
        )

        return jsonify(
            {"success": True, "message": f"已销毁用户 {target_username} 的会话"}
        )

    @app.route("/auth/admin/audit_logs", methods=["GET"])
    def auth_admin_audit_logs():
        """获取审计日志（管理员）"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "view_audit_logs"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        # 获取参数
        username = request.args.get("username", None)
        action = request.args.get("action", None)
        limit = int(request.args.get("limit", 100))

        logs = auth_system.get_audit_logs(username, action, limit)
        return jsonify({"success": True, "logs": logs})

    # ====================
    # 短信服务API
    # ====================

    @app.route("/api/sms/send_code", methods=["POST"])
    def sms_send_code():
        """
        发送短信验证码API
        功能：向指定手机号发送验证码，用于注册、登录或修改手机号等场景

        请求参数：
        - phone: 手机号（必填）
        - scene: 使用场景（register/login/modify，默认register）

        返回：
        - success: 是否成功
        - message: 提示信息
        - code_id: 验证码ID（用于后续验证）
        """
        try:
            # 检查短信服务总开关
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            if (
                config.get("Features", "enable_sms_service", fallback="false").lower()
                != "true"
            ):
                return jsonify({"success": False, "message": "短信服务未启用"})
            # 1. 获取并验证请求参数
            data = request.get_json() or {}
            phone = data.get("phone", "").strip()
            scene = data.get("scene", "register").strip()  # 使用场景
            captcha_input = data.get("captcha", "").strip()  # 获取用户输入的验证码
            captcha_id = data.get("captcha_id", "").strip()  # 获取验证码ID

            # 2. 验证图形验证码（必须首先验证，防止恶意短信攻击）
            is_captcha_valid, captcha_error_msg = verify_captcha(
                captcha_id, captcha_input
            )
            if not is_captcha_valid:
                return jsonify({"success": False, "message": captcha_error_msg})

            # 3. 验证手机号格式（11位数字，1开头）
            if not phone or not re.match(r"^1[3-9]\d{9}$", phone):
                return jsonify({"success": False, "message": "手机号格式不正确"})

            # 4. 检查发送间隔限制（安全增强）
            sms_interval_seconds = int(
                config.get(
                    "SMS_Service_SMSBao", "send_interval_seconds", fallback="180"
                )
            )
            last_send_key = f"sms_last_send_{phone}"
            last_send_time = cache.get(last_send_key, 0)
            current_time = time.time()

            if (
                last_send_time
                and (current_time - last_send_time) < sms_interval_seconds
            ):
                remaining_seconds = int(
                    sms_interval_seconds - (current_time - last_send_time)
                )
                return jsonify(
                    {
                        "success": False,
                        "message": f"发送过于频繁，请{remaining_seconds}秒后再试",
                        "retry_after": remaining_seconds,
                    }
                )

            # 5. 执行速率限制检查（防止滥用和攻击）
            client_ip = request.remote_addr
            current_date = time.strftime("%Y-%m-%d")

            # 检查IP限制
            ip_limit_key = f"sms_ip_{client_ip}_{current_date}"
            ip_count = cache.get(ip_limit_key, 0)
            ip_limit = int(
                config.get("SMS_Service_SMSBao", "rate_limit_per_ip_day", fallback="20")
            )
            if ip_count >= ip_limit:
                return jsonify(
                    {
                        "success": False,
                        "message": f"IP每日发送次数已达上限({ip_limit}次)",
                    }
                )

            # 检查手机号限制
            phone_limit_key = f"sms_phone_{phone}_{current_date}"
            phone_count = cache.get(phone_limit_key, 0)
            phone_limit = int(
                config.get(
                    "SMS_Service_SMSBao", "rate_limit_per_phone_day", fallback="5"
                )
            )
            if phone_count >= phone_limit:
                return jsonify(
                    {
                        "success": False,
                        "message": f"该手机号每日发送次数已达上限({phone_limit}次)",
                    }
                )

            # 6. 生成6位数字验证码（安全：仅后端存储，不返回前端）
            code = "".join([str(random.randint(0, 9)) for _ in range(6)])

            # 7. 调用短信宝API发送短信
            username = config.get("SMS_Service_SMSBao", "username", fallback="")
            api_key = config.get("SMS_Service_SMSBao", "api_key", fallback="")
            signature = config.get(
                "SMS_Service_SMSBao", "signature", fallback="【电科大跑步助手】"
            )
            code_expire_minutes = int(
                config.get("SMS_Service_SMSBao", "code_expire_minutes", fallback="5")
            )
            template = config.get(
                "SMS_Service_SMSBao",
                "template_register",
                fallback=f"您的验证码是：{{code}}，{code_expire_minutes}分钟内有效。",
            )

            if not username or not api_key:
                return jsonify(
                    {"success": False, "message": "短信服务配置不完整，请联系管理员"}
                )

            # 构造短信内容（签名+模板），支持{code}和{minutes}占位符
            content = signature + template.replace("{code}", code).replace(
                "{minutes}", str(code_expire_minutes)
            )

            # 调用短信宝HTTP API
            import urllib.parse
            import urllib.request

            url = f"http://api.smsbao.com/sms?u={username}&p={api_key}&m={phone}&c={urllib.parse.quote(content)}"

            logging.debug(f"[短信服务] 发送请求到短信宝API: {url}")

            try:
                response = urllib.request.urlopen(url, timeout=10)
                result = response.read().decode("utf-8").strip()

                # 短信宝返回码：0=成功，其他为错误码
                if result == "0":
                    # 7. 存储验证码到缓存（有效期可配置，默认5分钟）
                    # 安全增强：验证码仅存储在后端，不返回前端
                    code_expire_minutes = int(
                        config.get(
                            "SMS_Service_SMSBao", "code_expire_minutes", fallback="5"
                        )
                    )
                    code_expire_seconds = code_expire_minutes * 60

                    # 存储验证码到sms_verification_codes（用于后端验证）
                    sms_verification_codes[phone] = (
                        code,
                        time.time() + code_expire_seconds,
                    )

                    # 更新速率限制计数
                    cache[ip_limit_key] = ip_count + 1
                    cache[phone_limit_key] = phone_count + 1

                    # 更新最后发送时间（用于间隔限制）
                    cache[last_send_key] = current_time

                    # 记录日志（安全：不记录验证码内容）
                    app.logger.info(
                        f"[短信服务] 向 {phone} 发送验证码成功，场景：{scene}，有效期：{code_expire_minutes}分钟"
                    )

                    # 8. 记录短信发送历史到JSON文件
                    try:
                        # 确保log目录存在
                        log_dir = LOGIN_LOGS_DIR
                        os.makedirs(log_dir, exist_ok=True)

                        # 获取会话ID（如果存在）
                        session_id = request.headers.get("X-Session-ID", None)

                        # 确定用户名
                        username = None
                        if scene == "register":
                            # 注册场景：使用手机号作为用户名（因为用户还未创建）
                            username = f"注册用户({phone})"
                        elif scene == "modify":
                            # 修改手机号场景：需要从会话中获取当前用户
                            if g and hasattr(g, "user"):
                                username = g.user
                            else:
                                username = "未知用户"
                        elif scene == "admin_modify":
                            # 管理员修改用户手机号：从请求数据中获取目标用户名
                            username = data.get("target_username", "未知用户")
                        else:
                            # 其他场景（如登录）：尝试从会话获取
                            if g and hasattr(g, "user"):
                                username = g.user
                            else:
                                username = phone  # 使用手机号作为标识

                            # 构建历史记录
                        history_entry = {
                            "username": username,
                            "phone": phone,
                            "scene": scene,
                            "timestamp": time.time(),
                            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "content": content,
                            "ip": client_ip,
                        }
                        # 有条件地添加 session_id（仅当存在且非空时）
                        if (
                            session_id is not None
                            and session_id != ""
                            and session_id != "null"
                        ):
                            history_entry["session_id"] = session_id

                        # 追加到JSON文件（每行一个JSON对象）
                        history_file = os.path.join(log_dir, "sms_history.jsonl")
                        with open(history_file, "a", encoding="utf-8") as f:
                            f.write(
                                json.dumps(history_entry, ensure_ascii=False) + "\n"
                            )

                        app.logger.debug(
                            f"[短信历史] 已记录发送历史: {phone} -> {username}"
                        )

                        # 如果场景是管理员操作，则推送SocketIO更新
                        # 检查是否是管理员在“验证码管理”中
                        if scene in [
                            "admin_modify",
                            "register",
                        ]:  # 假设 register 也可能在管理面板触发
                            # 尝试从 g 对象获取 session_id
                            session_id = getattr(g, "api_instance", None)
                            if session_id:
                                session_id = getattr(
                                    session_id, "_web_session_id", None
                                )

                            if session_id:
                                # 修正：只在 admin_add_manual 场景下触发
                                # send_code 本身不应触发，因为它可能是用户自己注册
                                # 让我们把这个逻辑移到 add_manual_verification_code
                                pass
                            else:
                                # 如果 g.api_instance 不可用（例如非Flask请求上下文），则无法推送
                                logging.debug(
                                    "[SocketIO] sms_send_code：无法获取 session_id，跳过推送"
                                )

                    except Exception as e:
                        # 记录历史失败不应影响主流程
                        app.logger.error(f"[短信历史] 记录失败: {str(e)}")

                    # 安全：返回信息中不包含验证码
                    return jsonify(
                        {
                            "success": True,
                            "message": f"验证码已发送，{code_expire_minutes}分钟内有效",
                            "expire_minutes": code_expire_minutes,
                            "retry_after": sms_interval_seconds,  # 告知前端下次可发送的间隔
                        }
                    )
                else:
                    # 短信宝错误码映射（仅用于日志记录）
                    # 安全策略：不向前端暴露具体错误原因，只记录到日志
                    error_map = {
                        "30": "密码错误",
                        "40": "账号不存在",
                        "41": "余额不足",
                        "42": "账户已过期",
                        "43": "IP地址限制",
                        "50": "内容含有敏感词",
                    }
                    # 将详细错误信息记录到日志（包含错误码和具体原因）
                    detailed_error_msg = error_map.get(
                        result, f"未知错误(错误码:{result})"
                    )
                    app.logger.error(
                        f"[短信服务] 短信宝API返回错误码: {result}, 原因: {detailed_error_msg}, 手机号: {phone}"
                    )

                    # 向前端返回通用错误提示，不暴露具体错误原因
                    # 这样可以防止攻击者通过错误信息探测系统配置
                    return jsonify(
                        {"success": False, "message": "验证码发送失败，请稍后重试"}
                    )

            except Exception as e:
                # 网络或其他异常：详细错误记录到日志，前端显示通用提示
                app.logger.error(
                    f"[短信服务] API调用异常：{str(e)}, 手机号: {phone}", exc_info=True
                )
                # 向前端返回通用错误提示
                return jsonify(
                    {"success": False, "message": "验证码发送失败，请稍后重试"}
                )

        except Exception as e:
            # 请求处理异常：详细错误记录到日志，前端显示通用提示
            app.logger.error(f"[短信服务] 处理请求异常：{str(e)}", exc_info=True)
            # 向前端返回通用错误提示
            return jsonify({"success": False, "message": "验证码发送失败，请稍后重试"})

    @app.route("/sms-reply-webhook", methods=["GET"])
    def sms_reply_webhook():
        """
        接收短信宝的用户回复推送（Webhook）

        短信宝会通过GET请求推送用户回复内容：
        - m: 手机号
        - c: 回复内容（UTF-8编码）

        功能：记录所有用户回复到日志文件，便于后续分析
        """
        try:
            # 1. 获取推送参数
            phone = request.args.get("m", "")  # 手机号
            content = request.args.get("c", "")  # 回复内容（可能需要解码）

            if not phone or not content:
                return "0"  # 短信宝要求返回"0"表示接收成功

            # 2. 解码UTF-8内容（如果需要）
            try:
                import urllib.parse

                content = urllib.parse.unquote(content, encoding="utf-8")
            except:
                pass  # 解码失败则使用原始内容

            # 3. 记录到日志文件（JSONL格式，每行一条记录）
            log_dir = LOGIN_LOGS_DIR
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "sms_replies.jsonl")

            import json

            log_entry = {
                "timestamp": time.time(),
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
                "phone": phone,
                "content": content,
                "ip": request.remote_addr,
            }

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

            app.logger.info(f"[短信回复] 收到用户 {phone} 的回复：{content}")

            # 4. 返回"0"告知短信宝接收成功
            return "0"

        except Exception as e:
            app.logger.error(f"[短信回复] 处理异常：{str(e)}")
            return "0"  # 即使出错也返回0，避免短信宝重复推送

    @app.route("/api/sms/test_send", methods=["POST"])
    @login_required
    def sms_test_send():
        """
        短信测试发送API（管理员专用）
        功能：向指定手机号发送验证码（可指定或随机），用于测试短信配置是否正确

        权限要求：仅管理员可调用

        请求参数：
        - phone: 手机号（必填）
        - code: 验证码（可选，不填则自动生成随机验证码）

        返回：
        - success: 是否成功
        - message: 提示信息
        - code: 发送的验证码（仅测试模式下返回，便于管理员验证）
        """
        try:
            # 1. 验证管理员权限
            current_user = g.user
            if not auth_system.is_super_admin(
                current_user
            ) and not auth_system.is_admin(current_user):
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "权限不足，仅管理员可使用测试功能",
                        }
                    ),
                    403,
                )

            # 2. 检查短信服务总开关
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            if (
                config.get("Features", "enable_sms_service", fallback="false").lower()
                != "true"
            ):
                return jsonify(
                    {"success": False, "message": "短信服务未启用，请先在配置中启用"}
                )

            # 3. 获取并验证手机号
            data = request.get_json() or {}
            phone = data.get("phone", "").strip()
            custom_code = data.get("code", "").strip()  # 获取自定义验证码（可选）

            # 验证手机号格式（11位数字，1开头）
            if not phone or not re.match(r"^1[3-9]\d{9}$", phone):
                return jsonify({"success": False, "message": "手机号格式不正确"})

            # 4. 生成或使用自定义验证码
            if custom_code:
                # 使用管理员指定的验证码
                # 验证码格式检查：只允许数字，长度4-8位
                if not re.match(r"^\d{4,8}$", custom_code):
                    return jsonify(
                        {
                            "success": False,
                            "message": "自定义验证码格式不正确，仅支持4-8位数字",
                        }
                    )
                code = custom_code
            else:
                # 生成6位随机验证码
                import random

                code = "".join([str(random.randint(0, 9)) for _ in range(6)])

            # 5. 读取短信宝配置
            username = config.get("SMS_Service_SMSBao", "username", fallback="")
            api_key = config.get("SMS_Service_SMSBao", "api_key", fallback="")
            signature = config.get(
                "SMS_Service_SMSBao", "signature", fallback="【电科大跑步助手】"
            )
            code_expire_minutes = int(
                config.get("SMS_Service_SMSBao", "code_expire_minutes", fallback="5")
            )

            if not username or not api_key:
                return jsonify(
                    {
                        "success": False,
                        "message": "短信服务配置不完整，请先完善短信宝用户名和API Key",
                    }
                )

            # 6. 构造测试短信内容
            content = (
                signature
                + f"【测试短信】您的验证码是：{code}，{code_expire_minutes}分钟内有效。这是一条测试短信。"
            )

            # 7. 调用短信宝API发送短信
            import urllib.parse
            import urllib.request

            url = f"http://api.smsbao.com/sms?u={username}&p={api_key}&m={phone}&c={urllib.parse.quote(content)}"

            logging.info(f"[短信测试] 管理员 {current_user} 发送测试短信到 {phone}")

            try:
                response = urllib.request.urlopen(url, timeout=10)
                result = response.read().decode("utf-8").strip()

                # 短信宝返回码：0=成功，其他为错误码
                if result == "0":
                    # 记录到短信发送历史
                    try:
                        log_dir = LOGIN_LOGS_DIR
                        os.makedirs(log_dir, exist_ok=True)

                        client_ip = request.remote_addr
                        history_entry = {
                            "username": f"{current_user}(测试)",
                            "phone": phone,
                            "scene": "admin_test",
                            "timestamp": time.time(),
                            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "content": content,
                            "ip": client_ip,
                            "test_code": code,  # 测试模式下记录验证码
                        }

                        history_file = os.path.join(log_dir, "sms_history.jsonl")
                        with open(history_file, "a", encoding="utf-8") as f:
                            f.write(
                                json.dumps(history_entry, ensure_ascii=False) + "\n"
                            )

                        logging.info(
                            f"[短信测试] 已记录测试短信历史: {phone} -> 验证码: {code}"
                        )
                    except Exception as e:
                        logging.error(f"[短信测试] 记录历史失败: {str(e)}")

                    # 测试模式下返回验证码，便于管理员验证
                    return jsonify(
                        {
                            "success": True,
                            "message": f"测试短信发送成功！验证码：{code}",
                            "code": code,  # 仅测试模式下返回
                            "phone": phone,
                        }
                    )
                else:
                    # 短信宝错误码映射
                    error_map = {
                        "30": "密码错误",
                        "40": "账号不存在",
                        "41": "余额不足",
                        "42": "账户已过期",
                        "43": "IP地址限制",
                        "50": "内容含有敏感词",
                    }
                    error_msg = error_map.get(result, f"未知错误(错误码:{result})")
                    logging.error(
                        f"[短信测试] 短信宝API返回错误: {result} - {error_msg}"
                    )
                    return jsonify(
                        {
                            "success": False,
                            "message": f"发送失败：{error_msg}",
                            "error_code": result,
                        }
                    )

            except Exception as e:
                logging.error(f"[短信测试] API调用异常: {str(e)}", exc_info=True)
                return jsonify({"success": False, "message": f"网络错误：{str(e)}"})

        except Exception as e:
            logging.error(f"[短信测试] 处理请求异常: {str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"处理失败：{str(e)}"})

    # ====================
    # 管理员日志查看API
    # ====================

    @app.route("/api/admin/logs/login_history", methods=["GET"])
    @login_required
    def admin_logs_login_history():
        """
        查看用户登录历史记录

        权限要求：管理员或用户本人

        参数：
        - username: 用户名（可选，管理员可查看任意用户，普通用户只能查看自己）
        - limit: 返回条数（默认100）

        返回：登录记录列表
        """
        try:
            # 获取当前登录用户
            current_user = g.user

            # 获取查询参数
            target_username = request.args.get("username", "").strip()
            limit = int(request.args.get("limit", 100))

            # 问题5修复：使用check_permission替代is_admin
            # 权限检查：非管理员只能查看自己的记录
            if not auth_system.check_permission(current_user, "manage_users"):
                if target_username and target_username != current_user:
                    return jsonify({"success": False, "message": "权限不足"}), 403
                target_username = current_user

            # 如果未指定用户名且是管理员，则查看所有用户
            if not target_username:
                if not auth_system.check_permission(current_user, "manage_users"):
                    target_username = current_user

            # --- 调用 AuthSystem 的方法，而不是手动读取错误的文件 ---
            # target_username 在权限检查后，要么是目标用户，要么是管理员(空字符串)，要么是用户自己
            # 如果 target_username 为空字符串 (管理员查看全部)，需转为 None 以匹配 get_login_history

            username_to_query = target_username if target_username else None

            # 调用 auth_system 中正确的方法
            # get_login_history 会返回最近的N条记录（但按时间正序）
            history = auth_system.get_login_history(username_to_query, limit)

            # 前端期望的是倒序（最新的在前），所以我们在这里反转一下
            history.reverse()

            return jsonify(
                {
                    "success": True,
                    "logs": history,  # 改为logs以匹配前端期望
                    "total": len(history),
                }
            )

        except Exception as e:
            app.logger.error(f"[登录历史] 查询失败：{str(e)}")
            return jsonify({"success": False, "message": "查询失败"}), 500

    @app.route("/api/admin/logs/audit", methods=["GET"])
    @login_required
    def admin_logs_audit():
        """
        查看用户审计日志（操作记录）

        权限要求：管理员

        参数：
        - username: 用户名
        - action: 操作类型
        - limit: 返回条数（默认100）

        返回：审计日志列表
        """

        try:
            # 权限检查：仅管理员可访问
            if not auth_system.check_permission(g.user, "view_logs"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 获取查询参数
            username = request.args.get("username", "").strip()
            action = request.args.get("action", "").strip()
            limit = int(request.args.get("limit", 100))

            # 调用AuthSystem的审计日志方法
            logs = auth_system.get_audit_logs(username, action, limit)

            return jsonify({"success": True, "logs": logs, "total": len(logs)})

        except Exception as e:
            app.logger.error(f"[审计日志] 查询失败：{str(e)}")
            return jsonify({"success": False, "message": "查询失败"}), 500

    # ============================================================
    # 任务：系统配置API (config.ini)
    # ============================================================

    def _get_config_value(config, section, key, type_func=str, fallback=None):
        """
        辅助函数：从 configparser 安全地获取值，并应用类型转换。
        如果 key 不存在，返回 fallback。
        """
        if config.has_option(section, key):
            try:
                # 尝试从 config 对象获取并转换
                return type_func(config.get(section, key))
            except (ValueError, TypeError):
                # 转换失败，返回 fallback
                return fallback
        # 选项不存在，返回 fallback
        return fallback

    @app.route("/api/admin/config/load", methods=["GET"])
    @login_required
    def admin_config_load():
        """
        加载 config.ini 中的可配置项
        权限要求: manage_system
        """
        try:
            # 1. 权限检查
            if not auth_system.check_permission(g.user, "manage_system"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 2. 获取默认配置作为回退
            default_config = _get_default_config()

            # 3. 读取当前配置
            config = configparser.ConfigParser()
            # 确保 config.ini 存在（如果不存在，_get_default_config() 逻辑在 auto_init 中已处理)
            if os.path.exists(CONFIG_FILE):
                config.read(CONFIG_FILE, encoding="utf-8")
            else:
                # 如果文件意外丢失，使用默认值
                config = default_config

            # 4. 提取用户请求的特定配置项
            config_data = {
                "Guest": {
                    "allow_guest_login": _get_config_value(
                        config,
                        "Guest",
                        "allow_guest_login",
                        type_func=config.getboolean,
                        fallback=default_config.getboolean(
                            "Guest", "allow_guest_login", fallback=True
                        ),
                    )
                },
                "System": {
                    "session_expiry_days": _get_config_value(
                        config,
                        "System",
                        "session_expiry_days",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "System", "session_expiry_days", fallback=7
                        ),
                    ),
                    "school_accounts_dir": _get_config_value(
                        config,
                        "System",
                        "school_accounts_dir",
                        fallback=default_config.get(
                            "System", "school_accounts_dir", fallback="school_accounts"
                        ),
                    ),
                    "system_accounts_dir": _get_config_value(
                        config,
                        "System",
                        "system_accounts_dir",
                        fallback=default_config.get(
                            "System", "system_accounts_dir", fallback="system_accounts"
                        ),
                    ),
                    "permissions_file": _get_config_value(
                        config,
                        "System",
                        "permissions_file",
                        fallback=default_config.get(
                            "System", "permissions_file", fallback="permissions.json"
                        ),
                    ),
                    "session_monitor_check_interval": _get_config_value(
                        config,
                        "System",
                        "session_monitor_check_interval",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "System", "session_monitor_check_interval", fallback=60
                        ),
                    ),
                    "session_inactivity_timeout": _get_config_value(
                        config,
                        "System",
                        "session_inactivity_timeout",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "System", "session_inactivity_timeout", fallback=300
                        ),
                    ),
                },
                "Logging": {
                    "log_rotation_size_mb": _get_config_value(
                        config,
                        "Logging",
                        "log_rotation_size_mb",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "Logging", "log_rotation_size_mb", fallback=10
                        ),
                    ),
                    "archive_max_size_mb": _get_config_value(
                        config,
                        "Logging",
                        "archive_max_size_mb",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "Logging", "archive_max_size_mb", fallback=500
                        ),
                    ),
                    "log_dir": _get_config_value(
                        config,
                        "Logging",
                        "log_dir",
                        fallback=default_config.get(
                            "Logging", "log_dir", fallback="logs"
                        ),
                    ),
                    "archive_dir": _get_config_value(
                        config,
                        "Logging",
                        "archive_dir",
                        fallback=default_config.get(
                            "Logging", "archive_dir", fallback="logs/archive"
                        ),
                    ),
                },
                "Security": {
                    "password_storage": _get_config_value(
                        config,
                        "Security",
                        "password_storage",
                        fallback=default_config.get(
                            "Security", "password_storage", fallback="plaintext"
                        ),
                    ),
                    "brute_force_protection": _get_config_value(
                        config,
                        "Security",
                        "brute_force_protection",
                        type_func=config.getboolean,
                        fallback=default_config.getboolean(
                            "Security", "brute_force_protection", fallback=True
                        ),
                    ),
                    "login_log_retention_days": _get_config_value(
                        config,
                        "Security",
                        "login_log_retention_days",
                        type_func=config.getint,
                        fallback=default_config.getint(
                            "Security", "login_log_retention_days", fallback=90
                        ),
                    ),
                },
                "Map": {
                    "amap_js_key": _get_config_value(
                        config,
                        "Map",
                        "amap_js_key",
                        fallback=default_config.get("Map", "amap_js_key", fallback=""),
                    )
                },
                "API": {
                    "ip_api_key": _get_config_value(
                        config,
                        "API",
                        "ip_api_key",
                        fallback=default_config.get("API", "ip_api_key", fallback=""),
                    ),
                    "captcha_api_key": _get_config_value(
                        config,
                        "API",
                        "captcha_api_key",
                        fallback=default_config.get(
                            "API", "captcha_api_key", fallback=""
                        ),
                    ),
                },
            }

            return jsonify({"success": True, "config": config_data})

        except Exception as e:
            app.logger.error(f"[系统配置] 加载配置失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": "加载配置失败"}), 500

    @app.route("/api/admin/config/save", methods=["POST"])
    @login_required
    def admin_config_save():
        """
        保存 config.ini 中的可配置项
        权限要求: manage_system
        """
        try:
            # 1. 权限检查
            if not auth_system.check_permission(g.user, "manage_system"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            data = request.get_json() or {}

            # 2. 读取现有配置（必须保留注释和其他未修改项）
            config = configparser.ConfigParser()
            config.optionxform = str  # 保持键的大小写
            if os.path.exists(CONFIG_FILE):
                config.read(CONFIG_FILE, encoding="utf-8")
            else:
                # 如果文件不存在，从默认值创建
                config = _get_default_config()

            # 3. 逐项更新配置
            # 辅助函数：确保节存在
            def ensure_section(cfg, section_name):
                if not cfg.has_section(section_name):
                    cfg.add_section(section_name)

            # [Guest]
            if "Guest" in data and "allow_guest_login" in data["Guest"]:
                ensure_section(config, "Guest")
                config.set(
                    "Guest",
                    "allow_guest_login",
                    str(data["Guest"]["allow_guest_login"]).lower(),
                )

            # [System]
            if "System" in data:
                ensure_section(config, "System")
                system_data = data["System"]
                for key in [
                    "session_expiry_days",
                    "school_accounts_dir",
                    "system_accounts_dir",
                    "permissions_file",
                    "session_monitor_check_interval",
                    "session_inactivity_timeout",
                ]:
                    if key in system_data:
                        config.set("System", key, str(system_data[key]))

            # [Logging]
            if "Logging" in data:
                ensure_section(config, "Logging")
                logging_data = data["Logging"]
                for key in [
                    "log_rotation_size_mb",
                    "archive_max_size_mb",
                    "log_dir",
                    "archive_dir",
                ]:
                    if key in logging_data:
                        config.set("Logging", key, str(logging_data[key]))

            # [Security]
            if "Security" in data:
                ensure_section(config, "Security")
                security_data = data["Security"]
                if "password_storage" in security_data:
                    # 验证 password_storage 是否为允许的值
                    allowed_storage = ["plaintext", "sha256", "bcrypt"]
                    if security_data["password_storage"] in allowed_storage:
                        config.set(
                            "Security",
                            "password_storage",
                            security_data["password_storage"],
                        )
                    else:
                        return (
                            jsonify(
                                {
                                    "success": False,
                                    "message": f"无效的 password_storage 值，必须是 {allowed_storage} 之一",
                                }
                            ),
                            400,
                        )
                if "brute_force_protection" in security_data:
                    config.set(
                        "Security",
                        "brute_force_protection",
                        str(security_data["brute_force_protection"]).lower(),
                    )
                if "login_log_retention_days" in security_data:
                    config.set(
                        "Security",
                        "login_log_retention_days",
                        str(security_data["login_log_retention_days"]),
                    )

            # [Map]
            if "Map" in data and "amap_js_key" in data["Map"]:
                ensure_section(config, "Map")
                config.set("Map", "amap_js_key", data["Map"]["amap_js_key"])

            # [API]
            if "API" in data:
                ensure_section(config, "API")
                api_data = data["API"]
                if "ip_api_key" in api_data:
                    config.set("API", "ip_api_key", api_data["ip_api_key"])
                if "captcha_api_key" in api_data:
                    config.set("API", "captcha_api_key", api_data["captcha_api_key"])

            # 4. 使用 _write_config_with_comments 保存以保留注释
            _write_config_with_comments(config, CONFIG_FILE)

            # 5. 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                g.user,
                "update_system_config",
                "管理员更新了 config.ini 系统配置",
                ip_address,
                g.api_instance._web_session_id if hasattr(g, "api_instance") else "",
            )

            return jsonify({"success": True, "message": "系统配置已保存"})

        except Exception as e:
            app.logger.error(f"[系统配置] 保存配置失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": "保存配置失败"}), 500

    # ====================
    # 前端日志接收API
    # ====================

    @app.route("/api/log_frontend", methods=["POST"])
    def log_frontend():
        """接收前端日志并保存到后端日志文件"""
        try:
            data = request.get_json() or {}
            level = data.get("level", "INFO").upper()
            message = data.get("message", "")
            timestamp = data.get("timestamp", "")
            source = data.get("source", "unknown")

            if (data == None) or (not message):
                return (jsonify({"success": False, "message": "无效的日志数据"}),)

            # 获取 Session ID
            session_id = request.headers.get("X-Session-ID", "UnknownSession")
            # session_id_short = session_id[:8] if session_id else None # 取前8位用于日志

            # 获取 IP 地址 (考虑代理)
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)

            # 获取用户名 (通过 Session ID)
            username = "Guest/Unknown"  # 默认值
            with web_sessions_lock:
                if session_id in web_sessions:
                    api_instance = web_sessions[session_id]
                    # 优先使用 auth_username，如果不存在则尝试 user_data.username
                    username_attr = getattr(api_instance, "auth_username", None)
                    if not username_attr and hasattr(api_instance, "user_data"):
                        username_attr = getattr(
                            api_instance.user_data, "username", None
                        )

                    if username_attr:  # 确保获取到的用户名非空
                        username = username_attr
                    elif getattr(api_instance, "is_guest", False):  # 明确是游客
                        username = "Guest"
                    # 如果 session 存在但无法确定用户名，保留 'Guest/Unknown'

            # 构造新的日志消息，包含 IP、用户名和 Session ID
            log_message = f"[前端日志][IP:{ip_address}][前端时间:{timestamp}][用户:{username}][Session Id:{session_id}][{source}] {message}"

            # 根据级别记录日志
            if level == "DEBUG":
                logging.debug(log_message)
            elif level == "INFO":
                logging.info(log_message)
            elif level == "WARNING" or level == "WARN":
                logging.warning(log_message)
            elif level == "ERROR":
                logging.error(log_message)
            elif level == "CRITICAL":
                logging.critical(log_message)
            else:
                logging.info(log_message)

            return jsonify({"success": True})
        except Exception as e:
            # 在错误日志中也尝试包含 IP 和 Session ID
            session_id_err = request.headers.get("X-Session-ID", "UnknownSession")
            ip_address_err = request.headers.get("X-Forwarded-For", request.remote_addr)
            logging.error(
                f"[前端日志处理错误][IP:{ip_address_err}][Sess:{session_id_err[:8]}] {e}",
                exc_info=True,
            )
            return jsonify({"success": False, "message": str(e)}), 500

    @app.route("/api/auth/check_phone", methods=["POST"])
    def auth_check_phone():
        """
        检查手机号是否已被绑定。

        请求体:
            { "phone": "13800138000" }

        返回:
            { "success": true, "is_bound": true/false, "bound_to_user": "username" (如果已绑定) }
        """
        data = request.get_json() or {}
        phone = data.get("phone", "").strip()

        if not phone or not re.match(r"^1[3-9]\d{9}$", phone):
            return jsonify({"success": False, "message": "手机号格式不正确"})

        try:
            bound_username = auth_system.find_user_by_phone(phone)

            if bound_username:
                return jsonify(
                    {"success": True, "is_bound": True, "bound_to_user": bound_username}
                )
            else:
                return jsonify({"success": True, "is_bound": False})
        except Exception as e:
            logging.error(f"[检查手机号] 失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"服务器内部错误: {e}"}), 500

    # 用户修改自己的手机号
    @app.route("/api/user/update_phone", methods=["POST"])
    @login_required  # 使用装饰器确保用户已登录
    def user_update_phone():
        """
        用户修改自己的手机号。
        - 检查 enable_phone_modification 开关
        - 强制验证短信
        - 强制解绑其他账号
        """
        try:
            # 1. 检查功能开关
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE, encoding="utf-8")
            if (
                config.get(
                    "Features", "enable_phone_modification", fallback="false"
                ).lower()
                != "true"
            ):
                return jsonify(
                    {"success": False, "message": "系统未开启手机号修改功能"}
                )

            # 2. 获取参数
            data = request.get_json() or {}
            new_phone = data.get("new_phone", "").strip()
            sms_code = data.get("sms_code", "").strip()

            if not new_phone or not re.match(r"^1[3-9]\d{9}$", new_phone):
                return jsonify({"success": False, "message": "新手机号格式不正确"})

            if not sms_code:
                return jsonify({"success": False, "message": "请输入短信验证码"})

            # 3. 验证短信验证码
            global sms_verification_codes
            stored_code_info = sms_verification_codes.get(new_phone)

            if not stored_code_info:
                return jsonify({"success": False, "message": "请先获取验证码"})

            stored_code, expires_at = stored_code_info

            if time.time() > expires_at:
                del sms_verification_codes[new_phone]
                return jsonify(
                    {"success": False, "message": "验证码已过期，请重新获取"}
                )

            if stored_code != sms_code:
                return jsonify({"success": False, "message": "验证码错误"})

            # 验证成功，删除验证码
            del sms_verification_codes[new_phone]

            # 4. 获取当前用户名
            current_username = g.user

            # 5. 强制解绑该手机号（如果被其他人绑定）
            auth_system.unbind_phone_from_user(
                new_phone, except_username=current_username
            )

            # 6. 更新当前用户的手机号
            user_file_path = auth_system.get_user_file_path(current_username)
            if not os.path.exists(user_file_path):
                return jsonify({"success": False, "message": "当前用户文件不存在"}), 404

            with auth_system.lock:
                with open(user_file_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)

                user_data["phone"] = new_phone

                with open(user_file_path, "w", encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)

            # 7. 记录审计日志
            ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
            auth_system.log_audit(
                current_username,
                "user_update_phone",
                f"用户 {current_username} 成功修改手机号为: {new_phone}",
                ip_address,
                g.api_instance._web_session_id,
            )

            return jsonify(
                {"success": True, "message": "手机号修改成功", "new_phone": new_phone}
            )

        except Exception as e:
            app.logger.error(f"[用户修改手机号] 失败：{str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500

    # IP封禁数据存储文件路径
    IP_BANS_FILE = os.path.join("logs", "ip_bans.json")

    @app.route("/api/admin/ip_bans", methods=["GET"])
    @login_required
    def get_ip_bans():
        """
        获取IP封禁列表

        权限要求：管理员
        返回：所有IP封禁规则列表
        """
        try:
            # 问题5修复：使用check_permission替代is_admin
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 问题11修复：自动创建文件和目录
            # 如果logs目录不存在，自动创建
            if not os.path.exists("logs"):
                os.makedirs("logs", exist_ok=True)

            # 读取封禁列表
            if os.path.exists(IP_BANS_FILE):
                with open(IP_BANS_FILE, "r", encoding="utf-8") as f:
                    bans = json.load(f)
            else:
                # 如果文件不存在，自动创建空列表
                bans = []

            return jsonify({"success": True, "bans": bans})
        except Exception as e:
            app.logger.error(f"[IP封禁] 获取列表失败：{str(e)}")
            return jsonify({"success": False, "message": "获取列表失败"}), 500

    @app.route("/api/admin/ip_bans", methods=["POST"])
    @login_required
    def add_ip_ban():
        """
        添加IP封禁规则

        权限要求：管理员
        参数：
        - target: 封禁目标（IP/IP段/城市）
        - type: 类型（ip/cidr/city）
        - scope: 范围（all/messages_only）
        """
        try:
            # 问题5修复：使用check_permission替代is_admin
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            data = request.get_json() or {}
            target = data.get("target", "").strip()
            ban_type = data.get("type", "ip")
            scope = data.get("scope", "all")

            if not target:
                return jsonify({"success": False, "message": "封禁目标不能为空"})

            # 问题11修复：确保目录存在
            if not os.path.exists("logs"):
                os.makedirs("logs", exist_ok=True)

            # 读取现有封禁列表
            if os.path.exists(IP_BANS_FILE):
                with open(IP_BANS_FILE, "r", encoding="utf-8") as f:
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
                "created_by": g.user,
            }
            bans.append(new_ban)

            # 保存
            os.makedirs(os.path.dirname(IP_BANS_FILE), exist_ok=True)
            with open(IP_BANS_FILE, "w", encoding="utf-8") as f:
                json.dump(bans, f, indent=2, ensure_ascii=False)

            app.logger.info(
                f"[IP封禁] {g.user} 添加封禁规则：{target} ({ban_type}, {scope})"
            )
            return jsonify({"success": True, "message": "封禁规则已添加"})
        except Exception as e:
            app.logger.error(f"[IP封禁] 添加规则失败：{str(e)}")
            return jsonify({"success": False, "message": "添加失败"}), 500

    @app.route("/api/admin/ip_bans/<ban_id>", methods=["DELETE"])
    @login_required
    def delete_ip_ban(ban_id):
        """
        删除IP封禁规则

        权限要求：管理员
        参数：
        - ban_id: 封禁规则ID
        """
        try:
            # 问题5修复：使用check_permission替代is_admin
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            if not os.path.exists(IP_BANS_FILE):
                return jsonify({"success": False, "message": "封禁列表不存在"})

            with open(IP_BANS_FILE, "r", encoding="utf-8") as f:
                bans = json.load(f)

            # 过滤掉要删除的规则
            original_count = len(bans)
            bans = [b for b in bans if b["id"] != ban_id]

            if len(bans) == original_count:
                return jsonify({"success": False, "message": "封禁规则不存在"})

            with open(IP_BANS_FILE, "w", encoding="utf-8") as f:
                json.dump(bans, f, indent=2, ensure_ascii=False)

            app.logger.info(f"[IP封禁] {g.user} 删除封禁规则：{ban_id}")
            return jsonify({"success": True, "message": "封禁规则已删除"})
        except Exception as e:
            app.logger.error(f"[IP封禁] 删除规则失败：{str(e)}")
            return jsonify({"success": False, "message": "删除失败"}), 500

    @app.route("/api/admin/check_ip_ban", methods=["POST"])
    def check_ip_ban_api():
        """
        检查IP封禁状态API

        功能说明：
            供前端调用，检查当前客户端IP是否被封禁。
            前端在切换到留言板标签或发表留言前调用此接口。

        请求参数：
            - scope: 检查范围（'all'或'messages_only'），可选，默认为'all'

        返回：
            {
                "success": True,
                "is_banned": True/False  # true表示IP被封禁
            }
        """
        try:
            # 获取客户端IP地址
            client_ip = request.remote_addr

            # 获取检查范围（默认为'all'）
            data = request.get_json() or {}
            scope = data.get("scope", "all")

            # 调用check_ip_ban函数进行检查
            is_banned = check_ip_ban(client_ip, scope=scope)

            return jsonify({"success": True, "is_banned": is_banned})
        except Exception as e:
            app.logger.error(f"[IP封禁] 检查失败：{str(e)}")
            # 出错时默认返回未被封禁（避免误伤用户）
            return jsonify({"success": True, "is_banned": False})

    def check_ip_ban(ip_address, scope="all"):
        """
        检查IP是否被封禁

        参数：
        - ip_address: 要检查的IP地址
        - scope: 检查范围（all或具体功能如messages_only）

        返回：True表示被封禁，False表示未被封禁
        """
        if not os.path.exists(IP_BANS_FILE):
            return False

        try:
            with open(IP_BANS_FILE, "r", encoding="utf-8") as f:
                bans = json.load(f)

            for ban in bans:
                # 检查scope是否匹配
                if ban["scope"] != "all" and ban["scope"] != scope:
                    continue

                if ban["type"] == "ip":
                    # 单个IP匹配
                    if ip_address == ban["target"]:
                        return True
                elif ban["type"] == "range":
                    # IP范围匹配
                    try:
                        # 解析范围，例如 "192.168.1.1-192.168.1.100"
                        start_ip_str, end_ip_str = ban["target"].split("-")

                        # 使用 ipaddress 模块将IP转换为整数
                        start_ip = int(ipaddress.ip_address(start_ip_str.strip()))
                        end_ip = int(ipaddress.ip_address(end_ip_str.strip()))
                        current_ip = int(ipaddress.ip_address(ip_address))

                        # 检查当前IP是否在范围内
                        if start_ip <= current_ip <= end_ip:
                            return True
                    except (ValueError, TypeError) as e:
                        # 记录解析错误，但继续检查其他规则
                        app.logger.warning(
                            f"[IP封禁] 解析IP范围失败: {ban['target']}, 错误: {e}"
                        )
                        pass
                elif ban["type"] == "city":
                    # 城市匹配（需要IP归属地查询，这里简化处理）
                    pass

            return False
        except Exception as e:
            app.logger.error(f"[IP封禁] 检查失败：{str(e)}")
            return False

    # ====================
    # 任务20：短信服务配置API
    # ====================

    @app.route("/api/admin/sms/config", methods=["GET"])
    @login_required
    def get_sms_config():
        """
        获取短信服务配置

        权限要求：管理员
        返回：短信服务配置信息（包含三个新增的功能开关）
        """
        try:
            # 问题5修复：使用check_permission替代is_admin
            # 权限检查：只有具有manage_users权限的用户才能访问
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 问题12修复：自动补全config.ini配置
            # 读取配置文件
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")

            # 确保所需的配置节存在，如果不存在则创建
            if "Features" not in config:
                config.add_section("Features")
            if "SMS_Service_SMSBao" not in config:
                config.add_section("SMS_Service_SMSBao")

            # 补全缺失的配置项（使用默认值）
            # 主开关：启用短信服务
            if not config.has_option("Features", "enable_sms_service"):
                config.set("Features", "enable_sms_service", "false")

            # 新增：三个功能开关配置项
            # 允许用户修改手机号
            if not config.has_option("Features", "enable_phone_modification"):
                config.set("Features", "enable_phone_modification", "false")
            # 允许手机号登录
            if not config.has_option("Features", "enable_phone_login"):
                config.set("Features", "enable_phone_login", "false")
            # 注册时需要短信验证
            if not config.has_option("Features", "enable_phone_registration_verify"):
                config.set("Features", "enable_phone_registration_verify", "false")

            # 短信宝服务配置项
            if not config.has_option("SMS_Service_SMSBao", "username"):
                config.set("SMS_Service_SMSBao", "username", "")
            if not config.has_option("SMS_Service_SMSBao", "api_key"):
                config.set("SMS_Service_SMSBao", "api_key", "")
            if not config.has_option("SMS_Service_SMSBao", "signature"):
                config.set("SMS_Service_SMSBao", "signature", "")
            if not config.has_option("SMS_Service_SMSBao", "template_register"):
                config.set("SMS_Service_SMSBao", "template_register", "")
            if not config.has_option("SMS_Service_SMSBao", "code_expire_minutes"):
                config.set("SMS_Service_SMSBao", "code_expire_minutes", "5")
            if not config.has_option(
                "SMS_Service_SMSBao", "rate_limit_per_account_day"
            ):
                config.set("SMS_Service_SMSBao", "rate_limit_per_account_day", "10")
            if not config.has_option("SMS_Service_SMSBao", "rate_limit_per_ip_day"):
                config.set("SMS_Service_SMSBao", "rate_limit_per_ip_day", "20")
            if not config.has_option("SMS_Service_SMSBao", "rate_limit_per_phone_day"):
                config.set("SMS_Service_SMSBao", "rate_limit_per_phone_day", "5")

            # 保存补全后的配置（如果有修改的话）
            with open("config.ini", "w", encoding="utf-8") as f:
                config.write(f)

            # 构建返回的配置对象
            sms_config = {
                # 主开关
                "enable_sms_service": config.getboolean(
                    "Features", "enable_sms_service", fallback=False
                ),
                # 新增：三个功能开关
                "enable_phone_modification": config.getboolean(
                    "Features", "enable_phone_modification", fallback=False
                ),
                "enable_phone_login": config.getboolean(
                    "Features", "enable_phone_login", fallback=False
                ),
                "enable_phone_registration_verify": config.getboolean(
                    "Features", "enable_phone_registration_verify", fallback=False
                ),
                # 短信宝服务配置
                "username": config.get("SMS_Service_SMSBao", "username", fallback=""),
                "api_key": config.get("SMS_Service_SMSBao", "api_key", fallback=""),
                "signature": config.get("SMS_Service_SMSBao", "signature", fallback=""),
                "template_register": config.get(
                    "SMS_Service_SMSBao", "template_register", fallback=""
                ),
                "code_expire_minutes": config.getint(
                    "SMS_Service_SMSBao", "code_expire_minutes", fallback=5
                ),
                "rate_limit_per_account_day": config.getint(
                    "SMS_Service_SMSBao", "rate_limit_per_account_day", fallback=10
                ),
                "rate_limit_per_ip_day": config.getint(
                    "SMS_Service_SMSBao", "rate_limit_per_ip_day", fallback=20
                ),
                "rate_limit_per_phone_day": config.getint(
                    "SMS_Service_SMSBao", "rate_limit_per_phone_day", fallback=5
                ),
            }

            return jsonify({"success": True, "config": sms_config})
        except Exception as e:
            # 捕获异常并记录日志
            app.logger.error(f"[短信配置] 获取配置失败：{str(e)}")
            return jsonify({"success": False, "message": "获取配置失败"}), 500

    @app.route("/api/admin/sms/config", methods=["POST"])
    @login_required
    def save_sms_config():
        """
        保存短信服务配置

        权限要求：管理员
        参数：配置对象（enable_sms_service, enable_phone_modification等）
        使用 _write_config_with_comments 函数保存配置，确保注释不会丢失
        """
        try:
            # 问题5修复：使用check_permission替代is_admin
            # 权限检查：只有具有manage_users权限的用户才能保存配置
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 获取前端提交的配置数据
            data = request.get_json() or {}

            # 读取现有配置文件
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")

            # 问题12修复：确保配置节存在
            # 更新 [Features] 节的配置
            if "Features" not in config:
                config.add_section("Features")

            # 更新主开关：启用短信服务
            config.set(
                "Features",
                "enable_sms_service",
                str(data.get("enable_sms_service", False)).lower(),
            )

            # 新增：更新三个功能开关配置项
            # 允许用户修改手机号
            config.set(
                "Features",
                "enable_phone_modification",
                str(data.get("enable_phone_modification", False)).lower(),
            )
            # 允许手机号登录
            config.set(
                "Features",
                "enable_phone_login",
                str(data.get("enable_phone_login", False)).lower(),
            )
            # 注册时需要短信验证
            config.set(
                "Features",
                "enable_phone_registration_verify",
                str(data.get("enable_phone_registration_verify", False)).lower(),
            )

            # 更新 [SMS_Service_SMSBao] 节的配置
            if "SMS_Service_SMSBao" not in config:
                config.add_section("SMS_Service_SMSBao")

            # 更新短信宝服务配置项
            config.set("SMS_Service_SMSBao", "username", data.get("username", ""))
            config.set("SMS_Service_SMSBao", "api_key", data.get("api_key", ""))
            config.set("SMS_Service_SMSBao", "signature", data.get("signature", ""))
            config.set(
                "SMS_Service_SMSBao",
                "template_register",
                data.get("template_register", ""),
            )
            config.set(
                "SMS_Service_SMSBao",
                "code_expire_minutes",
                str(data.get("code_expire_minutes", 5)),
            )
            config.set(
                "SMS_Service_SMSBao",
                "rate_limit_per_account_day",
                str(data.get("rate_limit_per_account_day", 10)),
            )
            config.set(
                "SMS_Service_SMSBao",
                "rate_limit_per_ip_day",
                str(data.get("rate_limit_per_ip_day", 20)),
            )
            config.set(
                "SMS_Service_SMSBao",
                "rate_limit_per_phone_day",
                str(data.get("rate_limit_per_phone_day", 5)),
            )

            # 使用 _write_config_with_comments 函数保存配置文件
            # 这个函数会保留配置文件中的所有注释，而不是简单的 config.write()
            _write_config_with_comments(config, "config.ini")

            # 记录操作日志
            app.logger.info(f"[短信配置] {g.user} 更新了短信服务配置")
            return jsonify({"success": True, "message": "配置已保存"})
        except Exception as e:
            # 捕获异常并记录日志
            app.logger.error(f"[短信配置] 保存配置失败：{str(e)}")
            return jsonify({"success": False, "message": "保存失败"}), 500

    @app.route("/api/admin/sms/check_balance", methods=["GET"])
    @login_required
    def check_sms_balance():
        """
        查询短信宝余额

        权限要求：管理员
        返回：短信余额

        修正：
        1. 增加了120秒的速率限制，限制期间返回缓存数据。
        2. 修正了解析逻辑，以正确处理 "0\n今日条数,剩余条数" 格式的响应。
        """
        try:
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # --- 1. 增加速率限制（120秒） ---
            # cache 和 time 模块在 start_web_server 和文件顶部已导入
            cache_key = "sms_balance_cache"
            current_time = time.time()
            rate_limit_seconds = 120  # 2分钟

            if cache_key in cache:
                last_request_time, cached_data = cache[cache_key]
                if (current_time - last_request_time) < rate_limit_seconds:
                    # 在限制时间内，返回缓存数据
                    remaining_wait = int(
                        rate_limit_seconds - (current_time - last_request_time)
                    )
                    # 复制缓存数据以安全地添加提示消息
                    response_data = cached_data.copy()
                    response_data["message"] = (
                        f"查询过于频繁，请 {remaining_wait} 秒后再试 (返回上次结果)"
                    )

                    logging.debug(f"[短信配置] 查询余额命中速率限制，返回缓存数据。")
                    return jsonify(response_data)

            # --- 2. 执行查询 ---
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")

            username = config.get("SMS_Service_SMSBao", "username", fallback="")
            api_key = config.get("SMS_Service_SMSBao", "api_key", fallback="")

            if not username or not api_key:
                return jsonify({"success": False, "message": "短信宝配置不完整"})

            # 调用短信宝查询余额API
            url = f"https://api.smsbao.com/query?u={username}&p={api_key}"
            logging.debug(f"[短信配置] 查询余额URL: {url}")
            response = requests.get(url, timeout=10)
            response_text = response.text.strip()
            logging.debug(f"[短信配置] 查询余额响应: {response_text}")

            # --- 3. 修正解析逻辑 ---
            lines = response_text.split("\n")

            # 检查第一行是否为 '0' (成功)
            if lines and lines[0] == "0":
                if len(lines) > 1:
                    # 第二行格式为 "今日条数,剩余条数"
                    parts = lines[1].split(",")
                    if len(parts) == 2:
                        try:
                            sent_today = int(parts[0])
                            remaining_balance = int(parts[1])

                            # 准备成功的数据
                            result_data = {
                                "success": True,
                                "balance": remaining_balance,
                                "sent_today": sent_today,
                                "message": "查询成功",
                            }

                            # 存入缓存
                            cache[cache_key] = (current_time, result_data)

                            return jsonify(result_data)
                        except (ValueError, IndexError):
                            # 解析第二行失败
                            return jsonify(
                                {
                                    "success": False,
                                    "message": f"查询成功，但解析余额失败: {lines[1]}",
                                }
                            )
                    else:
                        # 格式不符合 "x,y"
                        return jsonify(
                            {
                                "success": False,
                                "message": f"查询成功，但余额格式不正确: {lines[1]}",
                            }
                        )
                else:
                    # 只有 '0'，没有第二行（异常情况）
                    return jsonify(
                        {"success": False, "message": "查询成功，但未返回余额数据"}
                    )
            else:
                # 失败：第一行不是 '0'，是错误码
                status_code = lines[0] if lines else response_text
                error_codes = {
                    "30": "密码错误",
                    "40": "账号不存在",
                    "41": "余额不足",
                    "43": "IP地址限制",
                    "50": "内容含有敏感词",
                    "51": "手机号码不正确",
                }
                error_msg = error_codes.get(status_code, f"未知错误码: {status_code}")
                return jsonify({"success": False, "message": f"查询失败：{error_msg}"})
        except Exception as e:
            app.logger.error(f"[短信配置] 查询余额失败：{str(e)}")
            return jsonify({"success": False, "message": f"查询失败：{str(e)}"}), 500

    @app.route("/api/admin/sms/history", methods=["GET"])
    @login_required
    def get_sms_history():
        """
        获取短信发送历史记录

        权限要求：管理员
        查询参数：
        - date: 按日期过滤（格式：YYYY-MM-DD）
        - phone: 按手机号过滤
        返回：短信发送历史记录列表
        """
        try:
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 获取过滤参数
            date_filter = request.args.get("date", "").strip()
            phone_filter = request.args.get("phone", "").strip()

            # 读取历史记录文件
            history_file = os.path.join(LOGIN_LOGS_DIR, "sms_history.jsonl")

            if not os.path.exists(history_file):
                return jsonify({"success": True, "records": []})

            records = []
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())

                        # 应用过滤条件
                        if date_filter and not record.get("datetime", "").startswith(
                            date_filter
                        ):
                            continue
                        if phone_filter and phone_filter not in record.get("phone", ""):
                            continue

                        records.append(record)
                    except json.JSONDecodeError:
                        continue

            # 按时间倒序排列（最新的在前）
            records.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

            # 限制返回数量（最多100条）
            records = records[:100]

            # 在函数末尾添加对 g.api_instance._web_session_id 的引用
            _ = getattr(g, "api_instance", None)

            return jsonify({"success": True, "records": records})
        except Exception as e:
            app.logger.error(f"[短信历史] 获取历史失败：{str(e)}")
            return jsonify({"success": False, "message": "获取历史失败"}), 500

    @app.route("/api/admin/sms/verification_codes", methods=["GET"])
    @login_required
    def get_verification_codes():
        """
        获取当前有效的验证码列表

        权限要求：管理员
        返回：当前有效的验证码列表
        """
        try:
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            current_time = time.time()
            codes = []

            # 遍历所有验证码
            for phone, (code, expire_time) in list(sms_verification_codes.items()):
                # 检查是否过期
                if expire_time > current_time:
                    codes.append(
                        {
                            "phone": phone,
                            "code": code,
                            "expires_at": expire_time,
                            "expires_in": int(expire_time - current_time),  # 剩余秒数
                        }
                    )

            # 按过期时间排序（最快过期的在前）
            codes.sort(key=lambda x: x["expires_at"])

            return jsonify({"success": True, "codes": codes})
        except Exception as e:
            app.logger.error(f"[验证码管理] 获取列表失败：{str(e)}")
            return jsonify({"success": False, "message": "获取列表失败"}), 500

    @app.route("/api/admin/sms/invalidate_code", methods=["POST"])
    @login_required
    def invalidate_verification_code():
        """
        使指定手机号的验证码失效

        权限要求：管理员
        参数：
        - phone: 手机号
        返回：操作结果
        """
        try:
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            data = request.get_json() or {}
            phone = data.get("phone", "").strip()

            if not phone:
                return jsonify({"success": False, "message": "手机号不能为空"})

            # 从验证码字典中删除
            if phone in sms_verification_codes:
                del sms_verification_codes[phone]
                app.logger.info(f"[验证码管理] {g.user} 使 {phone} 的验证码失效")
                # 推送SocketIO更新
                _emit_verification_codes_update(g.api_instance._web_session_id)
                return jsonify({"success": True, "message": "验证码已失效"})
            else:
                return jsonify({"success": False, "message": "未找到该手机号的验证码"})
        except Exception as e:
            app.logger.error(f"[验证码管理] 使验证码失效失败：{str(e)}")
            return jsonify({"success": False, "message": "操作失败"}), 500

    @app.route("/api/admin/sms/add_manual_code", methods=["POST"])
    @login_required
    def add_manual_verification_code():
        """
        手动添加验证码（模拟发送，用于测试或紧急情况）

        权限要求：管理员
        参数：
        - phone: 手机号
        - code: 验证码（6位数字）
        返回：操作结果
        """
        try:
            # 权限检查
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            data = request.get_json() or {}
            phone = data.get("phone", "").strip()
            code = data.get("code", "").strip()

            # 验证手机号格式
            if not phone or not re.match(r"^1[3-9]\d{9}$", phone):
                return jsonify({"success": False, "message": "手机号格式不正确"})

            # 验证验证码格式
            if not code or not re.match(r"^\d{6}$", code):
                return jsonify({"success": False, "message": "验证码必须是6位数字"})

            # 获取验证码有效期配置
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            code_expire_minutes = int(
                config.get("SMS_Service_SMSBao", "code_expire_minutes", fallback="5")
            )
            code_expire_seconds = code_expire_minutes * 60

            # 添加到验证码字典
            expire_time = time.time() + code_expire_seconds
            sms_verification_codes[phone] = (code, expire_time)

            app.logger.info(
                f"[验证码管理] {g.user} 手动添加验证码: {phone} (有效期{code_expire_minutes}分钟)"
            )

            try:

                os.makedirs(log_dir, exist_ok=True)

                session_id = (
                    g.api_instance._web_session_id
                    if hasattr(g, "api_instance")
                    else None
                )
                client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

                # 构造一个内容，模仿真实短信
                content = f"管理员 {g.user} 手动添加的验证码: {code}，{code_expire_minutes}分钟内有效。"

                history_entry = {
                    "session_id": session_id,
                    "username": g.user,  # 操作的管理员
                    "phone": phone,  # 目标手机号
                    "scene": "admin_manual_add",  # 场景
                    "timestamp": time.time(),
                    "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content": content,
                    "ip": client_ip,
                }

                history_file = os.path.join(log_dir, "sms_history.jsonl")
                with open(history_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(history_entry, ensure_ascii=False) + "\n")

                app.logger.debug(
                    f"[短信历史] 已记录手动添加验证码: {phone} -> {g.user}"
                )
            except Exception as e:
                app.logger.error(f"[短信历史] 记录手动添加验证码失败: {str(e)}")

            # 推送SocketIO更新
            _emit_verification_codes_update(g.api_instance._web_session_id)

            return jsonify(
                {
                    "success": True,
                    "message": f"验证码已添加，{code_expire_minutes}分钟内有效",
                }
            )
        except Exception as e:
            app.logger.error(f"[验证码管理] 添加验证码失败：{str(e)}")
            return jsonify({"success": False, "message": "添加失败"}), 500

    # ============================================================================
    # SSL/HTTPS 管理 API
    # 提供SSL证书上传、配置更新、信息查询等功能
    # 仅管理员可访问
    # ============================================================================

    @app.route("/api/admin/ssl/info", methods=["GET"])
    @login_required
    def get_ssl_info():
        """
        获取当前SSL配置和证书信息。

        功能说明：
        1. 返回当前SSL配置（是否启用、仅HTTPS模式等）
        2. 如果启用了SSL，返回证书详细信息（有效期、颁发者等）

        权限要求：管理员

        返回示例：
        {
            "success": true,
            "config": {
                "ssl_enabled": true,
                "https_only": false,
                "cert_path": "ssl/fullchain.pem",
                "key_path": "ssl/privkey.key"
            },
            "cert_info": {
                "subject": "CN=example.com",
                "issuer": "CN=Let's Encrypt Authority",
                "not_before": "2024-01-01T00:00:00",
                "not_after": "2024-04-01T00:00:00",
                "is_expired": false
            }
        }
        """
        try:
            # 权限检查：只有管理员才能查看SSL配置
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 加载当前SSL配置
            current_ssl_config = load_ssl_config()

            # 准备返回的配置信息（不包含敏感的完整路径）
            config_info = {
                "ssl_enabled": current_ssl_config.get("ssl_enabled", False),
                "https_only": current_ssl_config.get("https_only", False),
                "cert_path": current_ssl_config.get("ssl_cert_path", ""),
                "key_path": current_ssl_config.get("ssl_key_path", ""),
            }

            # 尝试获取证书详细信息（无论SSL是否启用）
            cert_info = {}

            # 1. 从配置中获取证书路径
            cert_path = current_ssl_config.get("ssl_cert_path", "")

            # 2. 检查路径是否已配置
            if cert_path:
                logging.info(
                    f"检测到证书路径配置: {cert_path}，正在尝试读取证书信息..."
                )
                # 3. 获取证书详细信息
                # get_ssl_certificate_info 会处理文件不存在或解析失败的情况
                cert_info = get_ssl_certificate_info(cert_path)
            else:
                logging.info("证书路径未配置，跳过证书信息读取。")
                # 如果路径为空，也明确返回一个错误信息，便于前端判断
                cert_info = {"error": "证书路径未在 config.ini 中配置"}

            logging.info(f"[SSL管理] {g.user} 查询SSL配置和证书信息")

            return jsonify(
                {"success": True, "config": config_info, "cert_info": cert_info}
            )

        except Exception as e:
            logging.error(f"[SSL管理] 获取SSL信息失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"获取SSL信息失败: {str(e)}"}),
                500,
            )

    @app.route("/api/admin/ssl/upload", methods=["POST"])
    @login_required
    def upload_ssl_certificate():
        """
        上传SSL证书文件和密钥文件。

        功能说明：
        1. 接收证书文件（PEM格式）和密钥文件
        2. 验证文件格式和有效性
        3. 保存到ssl/目录
        4. 返回上传结果

        权限要求：管理员

        请求参数（multipart/form-data）：
        - cert_file: 证书文件（.pem或.crt）
        - key_file: 密钥文件（.key或.pem）

        返回示例：
        {
            "success": true,
            "message": "证书上传成功",
            "cert_path": "ssl/fullchain.pem",
            "key_path": "ssl/privkey.key"
        }
        """
        try:
            # 权限检查：只有管理员才能上传证书
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 检查是否有文件上传
            if "cert_file" not in request.files or "key_file" not in request.files:
                return (
                    jsonify(
                        {"success": False, "message": "请同时上传证书文件和密钥文件"}
                    ),
                    400,
                )

            cert_file = request.files["cert_file"]
            key_file = request.files["key_file"]

            # 检查文件名是否为空
            if cert_file.filename == "" or key_file.filename == "":
                return jsonify({"success": False, "message": "文件名不能为空"}), 400

            # 确定ssl目录路径
            ssl_dir = os.path.join(os.path.dirname(__file__), "ssl")
            # 确保ssl目录存在
            os.makedirs(ssl_dir, exist_ok=True)

            # 生成临时文件名（用于验证）
            import tempfile

            # 创建临时文件用于保存上传的内容并验证
            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=".pem"
            ) as temp_cert:
                cert_file.save(temp_cert.name)
                temp_cert_path = temp_cert.name

            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=".key"
            ) as temp_key:
                key_file.save(temp_key.name)
                temp_key_path = temp_key.name

            try:
                # 验证上传的证书和密钥
                # 检查文件内容格式和证书-密钥匹配性
                is_valid, error_msg, cert_info = validate_ssl_certificate(
                    temp_cert_path, temp_key_path
                )

                if not is_valid:
                    # 如果验证失败，删除临时文件并返回错误
                    os.unlink(temp_cert_path)
                    os.unlink(temp_key_path)
                    return (
                        jsonify(
                            {"success": False, "message": f"证书验证失败: {error_msg}"}
                        ),
                        400,
                    )

                # 验证通过，移动文件到ssl目录
                final_cert_path = os.path.join(ssl_dir, "fullchain.pem")
                final_key_path = os.path.join(ssl_dir, "privkey.key")

                # 如果目标文件已存在，先备份
                if os.path.exists(final_cert_path):
                    backup_cert_path = final_cert_path + ".backup"
                    os.replace(final_cert_path, backup_cert_path)
                    logging.info(f"[SSL管理] 已备份旧证书: {backup_cert_path}")

                if os.path.exists(final_key_path):
                    backup_key_path = final_key_path + ".backup"
                    os.replace(final_key_path, backup_key_path)
                    logging.info(f"[SSL管理] 已备份旧密钥: {backup_key_path}")

                # 移动临时文件到最终位置
                os.replace(temp_cert_path, final_cert_path)
                os.replace(temp_key_path, final_key_path)

                # 设置文件权限（仅所有者可读写，密钥文件更严格）
                os.chmod(final_cert_path, 0o644)  # 证书文件：rw-r--r--
                os.chmod(final_key_path, 0o600)  # 密钥文件：rw-------（仅所有者可读写）

                logging.info(f"[SSL管理] {g.user} 成功上传SSL证书")

                return jsonify(
                    {
                        "success": True,
                        "message": "证书上传成功",
                        "cert_path": "ssl/fullchain.pem",
                        "key_path": "ssl/privkey.key",
                        "cert_info": cert_info,
                    }
                )

            except Exception as e:
                # 如果处理过程中出错，清理临时文件
                if os.path.exists(temp_cert_path):
                    os.unlink(temp_cert_path)
                if os.path.exists(temp_key_path):
                    os.unlink(temp_key_path)
                raise e

        except Exception as e:
            logging.error(f"[SSL管理] 上传证书失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"上传失败: {str(e)}"}), 500

    @app.route("/api/admin/ssl/config", methods=["POST"])
    @login_required
    def update_ssl_config():
        """
        更新SSL配置（不包括证书文件，仅更新配置选项）。

        功能说明：
        更新config.ini中的SSL配置项，如启用状态、仅HTTPS模式等
        注意：更新配置后需要重启服务器才能生效

        权限要求：管理员

        请求参数（JSON）：
        {
            "ssl_enabled": true/false,
            "https_only": true/false,
            "cert_path": "ssl/fullchain.pem",  // 可选
            "key_path": "ssl/privkey.key"      // 可选
        }

        返回示例：
        {
            "success": true,
            "message": "配置已更新，重启服务器后生效"
        }
        """
        try:
            # 权限检查：只有管理员才能修改SSL配置
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 获取请求数据
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "请求数据为空"}), 400

            # 加载当前配置
            current_config = load_ssl_config()

            # 更新配置项（只更新提供的字段）
            if "ssl_enabled" in data:
                current_config["ssl_enabled"] = bool(data["ssl_enabled"])

            if "https_only" in data:
                current_config["https_only"] = bool(data["https_only"])

            if "cert_path" in data and data["cert_path"]:
                current_config["ssl_cert_path"] = str(data["cert_path"])

            if "key_path" in data and data["key_path"]:
                current_config["ssl_key_path"] = str(data["key_path"])

            # 如果要启用SSL，验证证书文件是否存在
            if current_config.get("ssl_enabled", False):
                is_valid, error_msg, _ = validate_ssl_certificate(
                    current_config["ssl_cert_path"], current_config["ssl_key_path"]
                )

                if not is_valid:
                    return (
                        jsonify(
                            {
                                "success": False,
                                "message": f"证书验证失败，无法启用SSL: {error_msg}",
                            }
                        ),
                        400,
                    )

            # 保存配置到文件
            if save_ssl_config(current_config):
                logging.info(f"[SSL管理] {g.user} 更新SSL配置: {current_config}")
                return jsonify(
                    {
                        "success": True,
                        "message": "配置已更新，需要重启服务器才能生效",
                        "config": current_config,
                    }
                )
            else:
                return jsonify({"success": False, "message": "保存配置失败"}), 500

        except Exception as e:
            logging.error(f"[SSL管理] 更新配置失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"更新配置失败: {str(e)}"}),
                500,
            )

    @app.route("/api/admin/ssl/toggle", methods=["POST"])
    @login_required
    def toggle_ssl():
        """
        快速启用/禁用SSL（开关功能）。

        功能说明：
        快速切换SSL启用状态，无需修改其他配置
        注意：启用时会验证证书是否存在，禁用时不验证

        权限要求：管理员

        请求参数（JSON）：
        {
            "enabled": true/false
        }

        返回示例：
        {
            "success": true,
            "message": "SSL已启用，需要重启服务器",
            "ssl_enabled": true
        }
        """
        try:
            # 权限检查：只有管理员才能切换SSL
            if not auth_system.check_permission(g.user, "manage_users"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 获取请求数据
            data = request.get_json()
            if not data or "enabled" not in data:
                return jsonify({"success": False, "message": "缺少enabled参数"}), 400

            enabled = bool(data["enabled"])

            # 加载当前配置
            current_config = load_ssl_config()

            # 如果要启用SSL，验证证书文件
            if enabled:
                is_valid, error_msg, _ = validate_ssl_certificate(
                    current_config["ssl_cert_path"], current_config["ssl_key_path"]
                )

                if not is_valid:
                    return (
                        jsonify(
                            {
                                "success": False,
                                "message": f"无法启用SSL，证书验证失败: {error_msg}",
                            }
                        ),
                        400,
                    )

            # 更新配置
            current_config["ssl_enabled"] = enabled

            # 保存配置
            if save_ssl_config(current_config):
                action = "启用" if enabled else "禁用"
                logging.info(f"[SSL管理] {g.user} {action}了SSL")
                return jsonify(
                    {
                        "success": True,
                        "message": f"SSL已{action}，需要重启服务器才能生效",
                        "ssl_enabled": enabled,
                    }
                )
            else:
                return jsonify({"success": False, "message": "保存配置失败"}), 500

        except Exception as e:
            logging.error(f"[SSL管理] 切换SSL状态失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500

    # ============================================================================
    # 应用主路由
    # ============================================================================

    def get_frontend_config():
        """辅助函数：读取前端需要的功能开关配置"""
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE, encoding="utf-8")

        sms_enabled = (
            config.get("Features", "enable_sms_service", fallback="false").lower()
            == "true"
        )
        reg_verify_enabled = (
            config.get(
                "Features", "enable_phone_registration_verify", fallback="false"
            ).lower()
            == "true"
        )

        phone_modification_enabled = (
            config.get(
                "Features", "enable_phone_modification", fallback="false"
            ).lower()
            == "true"
        )

        return {
            "sms_enabled": sms_enabled,
            "reg_verify_enabled": reg_verify_enabled,
            # --- 新增代码 开始 ---
            "enable_phone_modification": phone_modification_enabled,
            # --- 新增代码 结束 ---
        }

    # ========== 新增路由：Favicon ==========
    @app.route("/favicon.ico")
    def favicon():
        """
        返回网站图标（Favicon）文件。

        功能说明：
        - 当浏览器请求网站图标时，返回位于项目根目录的 favicon.ico 文件
        - 使用 send_file 函数安全地发送文件到客户端
        - 设置正确的 MIME 类型（image/vnd.microsoft.icon）以确保浏览器正确识别

        返回值：
        - 成功：返回 favicon.ico 文件
        - 失败：返回 404 错误（如果文件不存在）
        """
        try:
            # 获取当前脚本所在的目录（项目根目录）
            # __file__ 是当前 Python 文件的路径
            # os.path.dirname() 获取其所在目录
            root_dir = os.path.dirname(__file__)

            # 构建 favicon.ico 的完整路径
            # os.path.join() 会根据操作系统自动处理路径分隔符（Windows用\，Linux用/）
            favicon_path = os.path.join(root_dir, "favicon.ico")

            # 检查文件是否存在
            if not os.path.exists(favicon_path):
                # 如果文件不存在，记录警告日志并返回404错误
                logging.warning(f"Favicon文件不存在: {favicon_path}")
                return jsonify({"success": False, "message": "Favicon文件未找到"}), 404

            # 使用 Flask 的 send_file 函数发送文件
            # mimetype 参数指定文件的 MIME 类型，这样浏览器就知道如何处理这个文件
            # image/vnd.microsoft.icon 是 .ico 文件的标准 MIME 类型
            return send_file(favicon_path, mimetype="image/vnd.microsoft.icon")

        except Exception as e:
            # 捕获所有可能的异常（如文件权限问题、路径错误等）
            # 记录详细的错误日志，包括异常堆栈信息（exc_info=True）
            logging.error(f"返回 favicon.ico 时发生错误: {e}", exc_info=True)
            # 返回500服务器内部错误
            return jsonify({"success": False, "message": "服务器内部错误"}), 500

    # ========== 新增路由：应用退出API ==========
    @app.route("/api/shutdown", methods=["POST"])
    def api_shutdown():
        """
        应用退出API端点。

        功能说明：
        - 响应PC端登录页的退出按钮点击事件
        - 安全地关闭 Flask + SocketIO 服务器
        - 执行必要的清理工作（如关闭数据库连接、保存状态等）

        安全考虑：
        - 此API应该受到权限保护，避免被恶意调用
        - 在生产环境中，建议添加身份验证或IP白名单

        返回值：
        - JSON 响应，表示关闭操作已启动
        """
        try:
            # 记录关闭请求的来源信息（IP地址和User-Agent）
            client_ip = request.remote_addr  # 获取客户端IP地址
            user_agent = request.headers.get("User-Agent", "Unknown")  # 获取浏览器信息

            # 记录关键操作日志：谁在什么时候请求关闭服务器
            logging.warning(
                f"[应用退出] 收到关闭请求 - IP: {client_ip}, User-Agent: {user_agent}"
            )

            # 先返回成功响应给客户端，让客户端知道服务器收到了关闭请求
            # 这样可以避免客户端等待超时
            response = jsonify({"success": True, "message": "服务器正在关闭..."})

            # 定义一个延迟关闭的函数，在后台线程中执行
            # 这样可以先返回响应，再执行关闭操作
            def delayed_shutdown():
                """
                延迟关闭函数：在独立线程中执行关闭操作。

                为什么要延迟？
                - 让 Flask 有时间完成当前请求的响应发送
                - 避免客户端收到连接中断错误
                """
                # 等待1秒，让响应有足够时间发送给客户端
                time.sleep(1)

                # 记录关闭操作开始
                logging.info("[应用退出] 正在执行关闭操作...")

                try:
                    # 方法1：尝试使用 SocketIO 的 stop() 方法优雅关闭
                    # 这会正确关闭所有 WebSocket 连接和后台任务
                    if socketio:
                        logging.info("[应用退出] 调用 socketio.stop() 关闭服务器...")
                        socketio.stop()
                    else:
                        # 方法2：如果 socketio 不可用，直接使用 sys.exit() 退出程序
                        # exit code 0 表示正常退出（非错误）
                        logging.info("[应用退出] 使用 sys.exit(0) 退出程序...")
                        sys.exit(0)

                except Exception as e:
                    # 如果关闭过程中出现异常，记录错误并强制退出
                    logging.error(f"[应用退出] 关闭过程中发生错误: {e}", exc_info=True)
                    # 强制退出，exit code 1 表示异常退出
                    sys.exit(1)

            # 在后台线程中启动延迟关闭函数
            # daemon=True 表示这是一个守护线程，主程序退出时它会自动退出
            shutdown_thread = threading.Thread(target=delayed_shutdown, daemon=True)
            shutdown_thread.start()

            # 立即返回响应给客户端
            return response

        except Exception as e:
            # 捕获所有可能的异常，避免服务器崩溃
            logging.error(f"[应用退出] 处理关闭请求时发生错误: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"关闭失败: {str(e)}"}), 500

    @app.route("/")
    def index():
        """首页：显示登录页面，等待用户认证后分配UUID"""
        # 不再自动分配UUID，直接返回HTML让前端处理认证
        # UUID将在用户完成认证（游客登录或系统账号登录）后由前端或后端API分配
        # 注入前端配置
        app_config = get_frontend_config()
        config_script = f"""
        <script>
            window.APP_CONFIG = {json.dumps(app_config)};
        </script>
        """
        # 注入到 </body> 标签之前
        modified_html = html_content.replace("</body>", f"{config_script}</body>")

        return render_template_string(modified_html)

    @app.route("/uuid=<uuid>")
    def session_view(uuid):
        """会话页面：显示应用界面"""
        # --- 修复 UUID 验证 ---
        # 验证UUID格式 - 标准UUID v4格式
        uuid_pattern = re.compile(
            r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$",
            re.IGNORECASE,
        )
        if not uuid or not uuid_pattern.match(uuid):
            # 日志记录修改为记录实际收到的UUID（截断）和失败原因
            logging.warning(
                f"无效的UUID格式或不匹配标准格式: {uuid[:40] if uuid else 'None'}..."
            )
            return redirect(url_for("index"))  # 验证失败，重定向到首页

        # 确保Api实例存在（从URL或文件恢复会话，不依赖Flask session）
        with web_sessions_lock:
            if uuid not in web_sessions:
                # 尝试从文件加载会话状态
                state = load_session_state(uuid)
                api_instance = Api(args)
                api_instance._session_created_at = time.time()
                api_instance._web_session_id = (
                    uuid  # 关键：保存session_id到实例，用于后台任务自动保存
                )

                if state and state.get("login_success"):
                    # 恢复登录状态
                    api_instance.login_success = True
                    api_instance.user_info = state.get("user_info")
                    api_instance._session_created_at = state.get(
                        "created_at", time.time()
                    )

                    # 使用新的恢复函数恢复完整状态
                    restore_session_to_api_instance(api_instance, state)

                    logging.info(
                        f"从文件恢复已登录会话 : {uuid[:32]}... (用户: {state.get('user_info', {}).get('username', 'Unknown')}, 任务数: {len(api_instance.all_run_data)})"
                    )
                else:
                    logging.info(f"创建新会话 : {uuid[:32]}...")

                web_sessions[uuid] = api_instance
                # save_session_state(uuid, api_instance)
            else:
                # 确保已有会话也有_web_session_id属性
                api_instance = web_sessions[uuid]
                if not hasattr(api_instance, "_web_session_id"):
                    api_instance._web_session_id = uuid
                logging.debug(f"使用现有会话: {uuid[:32]}...")

        # 注入前端配置
        app_config = get_frontend_config()
        config_script = f"""
        <script>
            window.APP_CONFIG = {json.dumps(app_config)};
        </script>
        """
        # 注入到 </body> 标签之前
        modified_html = html_content.replace("</body>", f"{config_script}</body>")

        # 返回HTML内容
        return render_template_string(modified_html)

    @app.route("/JavaScript/<path:function_path>.js", methods=["GET"])
    def serve_javascript(function_path):
        """
        JavaScript 函数动态加载 API 端点

        功能说明：
            根据请求的函数名，从 JavaScript.js 文件中查找并返回对应的函数代码。
            支持浏览器缓存，提升加载速度和性能。

        参数：
            function_path (str): 请求的函数路径，例如 'onlogin' 或 'utils/helper'

        返回：
            - 200: 成功找到函数，返回 JavaScript 代码
            - 404: 未找到指定的函数
            - 500: 服务器内部错误

        缓存策略：
            - 设置 Cache-Control 头，允许浏览器缓存 1 小时
            - 使用 Last-Modified 和 ETag 支持条件请求

        示例：
            GET /JavaScript/onlogin.js
            --> 返回 onlogin 相关的 JavaScript 函数代码
        """
        if function_path == "JavaScript_globals":
            return redirect("/JavaScript_globals.js")
        try:
            # 读取完整的 JavaScript.js 文件内容
            js_file_path = os.path.join(os.path.dirname(__file__), "JavaScript.js")

            # 检查文件是否存在
            if not os.path.exists(js_file_path):
                logging.error(f"JavaScript.js 文件不存在: {js_file_path}")
                return jsonify({"error": "JavaScript file not found"}), 404

            # 读取文件内容（使用 UTF-8 编码确保中文注释正确显示）
            with open(js_file_path, "r", encoding="utf-8") as f:
                full_content = f.read()

            # 提取请求的函数名（移除可能的路径分隔符）
            function_name = function_path.replace("/", "_")

            # 查找函数定义的模式（支持多种函数定义方式）
            # 模式1: function functionName(...) { ... }
            # 模式2: const functionName = function(...) { ... }
            # 模式3: const functionName = (...) => { ... }
            # 模式4: let functionName = function(...) { ... }
            # 模式5: var functionName = function(...) { ... }

            # 构建匹配模式：查找函数声明、函数表达式或箭头函数
            pattern = rf"(?:^|\n)(\s*(?:(?:async\s+)?function\s+{function_name}\s*\([^)]*\)|(?:const|let|var)\s+{function_name}\s*=\s*(?:function\s*\([^)]*\)|(?:async\s+)?function\s*\([^)]*\)|\([^)]*\)\s*=>))\s*{{)"

            match = re.search(pattern, full_content, re.MULTILINE)

            if not match:
                # 如果未找到精确匹配，尝试模糊搜索（查找包含函数名的所有函数）
                logging.warning(
                    f"未找到精确匹配的函数 '{function_name}'，尝试模糊搜索..."
                )

                # 模糊搜索：查找所有包含该名称的函数
                fuzzy_pattern = rf"(?:^|\n)(\s*(?:function\s+\w*{function_name}\w*\s*\([^)]*\)|(?:const|let|var)\s+\w*{function_name}\w*\s*=))"
                fuzzy_matches = re.finditer(
                    fuzzy_pattern, full_content, re.MULTILINE | re.IGNORECASE
                )

                # 收集所有模糊匹配的函数名
                found_functions = []
                for m in fuzzy_matches:
                    func_line = m.group(0).strip()
                    found_functions.append(func_line[:50])  # 只取前50个字符作为提示

                if found_functions:
                    suggestions = "\n".join(found_functions)
                    logging.info(f"找到相似的函数定义:\n{suggestions}")
                    return (
                        jsonify(
                            {
                                "error": f"Function '{function_name}' not found",
                                "suggestions": found_functions[:5],  # 最多返回5个建议
                            }
                        ),
                        404,
                    )
                else:
                    logging.error(f"未找到任何与 '{function_name}' 相关的函数")
                    return (
                        jsonify({"error": f"Function '{function_name}' not found"}),
                        404,
                    )

            # 找到函数起始位置
            func_start = match.start()

            # 查找函数结束位置（匹配大括号）
            # 需要考虑嵌套的大括号，所以要计数
            brace_count = 0
            in_function = False
            func_end = func_start

            for i in range(func_start, len(full_content)):
                char = full_content[i]

                if char == "{":
                    brace_count += 1
                    in_function = True
                elif char == "}":
                    brace_count -= 1

                    # 当大括号计数归零时，说明函数定义结束
                    if in_function and brace_count == 0:
                        func_end = i + 1
                        break

            # 提取函数代码
            function_code = full_content[func_start:func_end]

            # 向前查找函数注释（查找函数定义前的注释块）
            # 注释可能是 // 单行注释或 /* */ 多行注释
            comments_start = func_start

            # 向前搜索，查找连续的注释行
            lines_before = full_content[:func_start].split("\n")
            comment_lines = []

            for line in reversed(lines_before):
                stripped = line.strip()
                # 如果是注释行，添加到列表
                if (
                    stripped.startswith("//")
                    or stripped.startswith("/*")
                    or stripped.startswith("*")
                    or stripped.startswith("*/")
                ):
                    comment_lines.insert(0, line)
                # 如果是空行，继续
                elif stripped == "":
                    comment_lines.insert(0, line)
                # 如果遇到非注释非空行，停止搜索
                else:
                    break

            # 如果找到了注释，将其添加到函数代码前面
            if comment_lines:
                comments = "\n".join(comment_lines)
                function_code = comments + "\n" + function_code

            # 准备响应（添加文件头注释说明这是动态加载的代码）
            response_content = f"""// ==============================================================================
// 动态加载的 JavaScript 函数: {function_name}
// 从 JavaScript.js 文件中提取
// ==============================================================================

{function_code}
"""

            # 创建响应对象，设置正确的 Content-Type
            response = make_response(response_content)
            response.headers["Content-Type"] = "application/javascript; charset=utf-8"

            # 设置缓存策略：允许浏览器缓存 1 小时
            response.headers["Cache-Control"] = "public, max-age=3600"

            # 获取文件的最后修改时间，用于条件请求
            file_mtime = os.path.getmtime(js_file_path)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )
            response.headers["Last-Modified"] = last_modified

            # 生成 ETag（基于文件内容的哈希值）

            etag = hashlib.md5(function_code.encode("utf-8")).hexdigest()
            response.headers["ETag"] = f'"{etag}"'

            # 检查客户端的条件请求头
            if_modified_since = request.headers.get("If-Modified-Since")
            if_none_match = request.headers.get("If-None-Match")

            # 如果客户端已有最新版本，返回 304 Not Modified
            if (if_modified_since == last_modified) or (if_none_match == f'"{etag}"'):
                logging.debug(f"JavaScript 函数 '{function_name}' 使用缓存版本 (304)")
                return "", 304

            logging.info(
                f"成功返回 JavaScript 函数: {function_name} ({len(function_code)} 字符)"
            )
            return response

        except FileNotFoundError as e:
            logging.error(f"JavaScript.js 文件未找到: {e}")
            return jsonify({"error": "JavaScript file not found"}), 404
        except Exception as e:
            logging.error(f"加载 JavaScript 函数时发生错误: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/JavaScript_globals.js", methods=["GET"])
    def serve_javascript_globals():
        """
        返回 JavaScript 全局变量文件（优先加载）

        功能说明：
            返回 JavaScript_globals.js 文件，包含所有全局变量声明
            此文件必须在主 JavaScript.js 之前加载，避免变量未定义错误

        查询参数：
            - minify: 是否压缩代码（默认 true）

        返回：
            - 200: 成功返回全局变量代码
            - 304: 使用缓存版本
            - 404: 文件未找到
            - 500: 服务器内部错误

        使用示例：
            <script src="/JavaScript_globals.js"></script>
            <script src="/JavaScript.js"></script>
        """
        try:
            js_globals_file = os.path.join(
                os.path.dirname(__file__), "JavaScript_globals.js"
            )

            if not os.path.exists(js_globals_file):
                logging.error(f"JavaScript 全局变量文件不存在: {js_globals_file}")
                return jsonify({"error": "JavaScript globals file not found"}), 404

            # 读取文件内容
            with open(js_globals_file, "r", encoding="utf-8") as f:
                original_content = f.read()

            # 检查是否需要压缩
            minify_param = request.args.get("minify", "true").lower()
            should_minify = minify_param in ["true", "1", "yes", ""]

            # if should_minify:
            #     content = minify_javascript(original_content)
            #     content_type_suffix = ' (minified)'
            #     logging.info(f"JavaScript_globals.js 压缩：{len(original_content)} 字节 -> {len(content)} 字节")
            # else:
            #     content = original_content
            #     content_type_suffix = ' (original)'
            if should_minify:
                # 压缩功能已禁用（原始压缩器有Bug），始终返回原始代码
                content = original_content
                content_type_suffix = " (original, compression disabled)"
                logging.info(
                    f"JavaScript_globals.js 压缩功能已禁用，返回原始大小: {len(original_content)} 字节"
                )
            else:
                content = original_content
                content_type_suffix = " (original)"

            # 设置响应头
            file_mtime = os.path.getmtime(js_globals_file)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            etag_base = hashlib.md5(content.encode("utf-8")).hexdigest()
            etag = f'"{etag_base}-{"min" if should_minify else "orig"}"'

            # 检查条件请求
            if_modified_since = request.headers.get("If-Modified-Since")
            if_none_match = request.headers.get("If-None-Match")

            if (if_modified_since == last_modified) or (if_none_match == etag):
                logging.debug(
                    f"JavaScript_globals.js 使用缓存版本 (304){content_type_suffix}"
                )
                return "", 304

            response = make_response(content)
            response.headers["Content-Type"] = "application/javascript; charset=utf-8"
            response.headers["Cache-Control"] = "public, max-age=3600"
            response.headers["Last-Modified"] = last_modified
            response.headers["ETag"] = etag
            response.headers["X-Minified"] = "true" if should_minify else "false"

            logging.info(
                f"成功返回 JavaScript_globals.js{content_type_suffix} ({len(content)} 字符)"
            )
            return response

        except Exception as e:
            logging.error(f"加载 JavaScript_globals.js 时发生错误: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/Cascading_Style_Sheets_Web_animation.css", methods=["GET"])
    def serve_css_animation():
        """
        返回 CSS 动画文件（优先加载）

        功能说明：
            返回 Cascading_Style_Sheets_Web_animation.css 文件，包含所有 CSS 动画样式
            此文件必须在主 CSS 文件之前加载，避免样式未定义错误

        查询参数：
            - minify: 是否压缩代码（默认 true）

        返回：
            - 200: 成功返回全局变量代码
            - 304: 使用缓存版本
            - 404: 文件未找到
            - 500: 服务器内部错误

        """
        try:
            css_animation_file = os.path.join(
                os.path.dirname(__file__), "Cascading_Style_Sheets_Web_animation.css"
            )

            if not os.path.exists(css_animation_file):
                logging.error(f"CSS 动画文件不存在: {css_animation_file}")
                return jsonify({"error": "CSS animation file not found"}), 404

            # 读取文件内容
            with open(css_animation_file, "r", encoding="utf-8") as f:
                original_content = f.read()

            # 检查是否需要压缩
            minify_param = request.args.get("minify", "true").lower()
            should_minify = minify_param in ["true", "1", "yes", ""]

            # if should_minify:
            #     content = minify_javascript(original_content)
            #     content_type_suffix = ' (minified)'
            #     logging.info(f"JavaScript_globals.js 压缩：{len(original_content)} 字节 -> {len(content)} 字节")
            # else:
            #     content = original_content
            #     content_type_suffix = ' (original)'
            if should_minify:
                # 压缩功能已禁用（原始压缩器有Bug），始终返回原始代码
                content = original_content
                content_type_suffix = " (original, compression disabled)"
                logging.info(
                    f"Cascading_Style_Sheets_Web_animation.css 压缩功能已禁用，返回原始大小: {len(original_content)} 字节"
                )
            else:
                content = original_content
                content_type_suffix = " (original)"

            # 设置响应头
            file_mtime = os.path.getmtime(css_animation_file)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            etag_base = hashlib.md5(content.encode("utf-8")).hexdigest()
            etag = f'"{etag_base}-{"min" if should_minify else "orig"}"'

            # 检查条件请求
            if_modified_since = request.headers.get("If-Modified-Since")
            if_none_match = request.headers.get("If-None-Match")

            if (if_modified_since == last_modified) or (if_none_match == etag):
                logging.debug(
                    f"Cascading_Style_Sheets_Web_animation.css 使用缓存版本 (304){content_type_suffix}"
                )
                return "", 304

            response = make_response(content)
            response.headers["Content-Type"] = "text/css; charset=utf-8"
            response.headers["Cache-Control"] = "public, max-age=3600"
            response.headers["Last-Modified"] = last_modified
            response.headers["ETag"] = etag
            response.headers["X-Minified"] = "true" if should_minify else "false"

            logging.info(
                f"成功返回 Cascading_Style_Sheets_Web_animation.css{content_type_suffix} ({len(content)} 字符)"
            )
            return response

        except Exception as e:
            logging.error(
                f"加载 Cascading_Style_Sheets_Web_animation.css 时发生错误: {e}",
                exc_info=True,
            )
            return jsonify({"error": "Internal server error"}), 500

    def get_parsed_stylesheet(css_file_path):
        """
        获取解析后的 CSS 样式表（实时读取，不使用内存缓存）。

        返回 (stylesheet, selectors_list)
        """

        # --- 4. 优化：在解析前先检查文件是否存在 ---
        if not os.path.exists(css_file_path):
            logging.error(f"CSS 文件不存在: {css_file_path}")
            return None, None

        try:
            logging.info(f"正在实时解析 CSS 文件: {css_file_path}")

            # 解析前重置缩进/压缩偏好
            cssutils.ser.prefs.useDefaults()

            # 抑制 cssutils 自己的日志，防止它因错误停止
            cssutils.log.setLevel(logging.CRITICAL)

            # 创建一个不进行验证的解析器
            parser = cssutils.CSSParser(validate=False)

            # 使用该解析器实例来解析文件
            stylesheet = parser.parseFile(css_file_path, encoding="utf-8")

            # 生成选择器列表
            selectors = set()
            for rule in stylesheet:
                if rule.type == cssutils.css.CSSRule.STYLE_RULE:
                    # 这是一个样式规则 (例如 .class, #id)
                    for selector in rule.selectorList:
                        selectors.add(selector.selectorText.strip())

                # --- 2. 移除 @keyframes 兼容性 ---
                # (此处原有的 KEYFRAMES_RULE 和 UNKNOWN_RULE 逻辑已删除)

            sorted_selectors = sorted(list(selectors))

            # --- 1. 移除缓存：不再更新 _css_cache ---

            return stylesheet, sorted_selectors

        except Exception as e:
            logging.error(f"解析 CSS 文件时出错: {e}", exc_info=True)
            # --- 1. 移除缓存：出错时不再需要清理缓存 ---
            return None, None

    @app.route("/css/available-selectors.list", methods=["GET"])
    def get_available_css_selectors():
        """
        返回 Cascading_Style_Sheets.css 文件中所有可用的 CSS 选择器列表。
        """

        # --- 1. 代码复用：定义统一的 CSS 文件路径常量 ---
        # 使用 os.path.dirname(__file__) 来确保路径总是相对于当前脚本
        try:
            CURRENT_DIR = os.path.dirname(__file__)
        except NameError:
            CURRENT_DIR = os.getcwd()  # 备用方案（例如在 REPL 中）

        CSS_FILE_PATH = os.path.join(CURRENT_DIR, "Cascading_Style_Sheets.css")
        try:
            # --- 4. 复用：使用常量 ---
            # --- 1. 移除缓存：每次都调用解析函数 ---

            # 优化：在解析前先检查文件
            if not os.path.exists(CSS_FILE_PATH):
                return jsonify({"错误": "找不到 CSS 文件"}), 500

            stylesheet, selectors = get_parsed_stylesheet(CSS_FILE_PATH)

            if not stylesheet:
                # get_parsed_stylesheet 内部已记录文件不存在或解析失败
                return jsonify({"错误": "解析 CSS 文件失败"}), 500

            # --- 1. 移除缓存：从文件系统实时获取 mtime 用于 HTTP 缓存 ---
            file_mtime = os.path.getmtime(CSS_FILE_PATH)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            # ETag 基于选择器列表的内容
            etag = f'"{hashlib.md5(str(selectors).encode("utf-8")).hexdigest()}"'

            # 检查 HTTP 缓存头
            if (request.headers.get("If-Modified-Since") == last_modified) or (
                request.headers.get("If-None-Match") == etag
            ):
                return "", 304

            response = make_response(jsonify(selectors))
            response.headers["Cache-Control"] = (
                "public, max-age=3600"  # 1 小时浏览器缓存
            )
            response.headers["Last-Modified"] = last_modified
            response.headers["ETag"] = etag

            logging.info(f"成功返回 {len(selectors)} 个 CSS 选择器。")
            return response

        except Exception as e:
            logging.error(f"获取 CSS 选择器列表时发生错误: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500

    # --- 3. 修复路由：使用更健壮的 <path:css_path> 并内部处理 .css 后缀 ---
    @app.route("/css/<path:css_path>", methods=["GET"])
    def serve_css(css_path):
        """
        CSS 样式分段动态加载 API 端点
        """

        # --- 1. 代码复用：定义统一的 CSS 文件路径常量 ---
        # 使用 os.path.dirname(__file__) 来确保路径总是相对于当前脚本
        try:
            CURRENT_DIR = os.path.dirname(__file__)
        except NameError:
            CURRENT_DIR = os.getcwd()  # 备用方案（例如在 REPL 中）

        CSS_FILE_PATH = os.path.join(CURRENT_DIR, "Cascading_Style_Sheets.css")
        try:
            # --- 3. 修复路由：检查并剥离 .css 后缀 ---
            if not css_path or not css_path.endswith(".css"):
                logging.warning(f"无效的 CSS 请求路径: {css_path}")
                return jsonify({"error": "Invalid path. Must end with .css"}), 404

            # 移除末尾的 '.css' 来获取原始选择器字符串
            requested_selector_raw = css_path[:-4]

            # --- 4. 复用：使用常量 ---
            # 优化：在解析前先检查文件
            if not os.path.exists(CSS_FILE_PATH):
                logging.error(f"CSS 文件不存在: {CSS_FILE_PATH}")
                return jsonify({"error": "CSS file not found"}), 500

            # --- 1. 移除缓存：每次都调用解析函数 ---
            stylesheet, _ = get_parsed_stylesheet(CSS_FILE_PATH)

            if not stylesheet:
                return jsonify({"error": "Failed to parse CSS file"}), 500

            # 1. 检查是否需要压缩
            minify_param = request.args.get("minify", "true").lower()
            should_minify = minify_param in ["true", "1", "yes", ""]

            # 2. 设置 cssutils 的压缩偏好
            if should_minify:
                cssutils.ser.prefs.useMinified()
                content_type_suffix = " (minified)"
            else:
                cssutils.ser.prefs.useDefaults()
                content_type_suffix = " (original)"

            # 3. 解码 URL 中的选择器
            try:
                # 步骤 1: 替换组合选择器 (例如 '+~+' -> ' ~ ')
                requested_selector_decoded = requested_selector_raw.replace(
                    "+~+", " ~ "
                )
                requested_selector_decoded = requested_selector_decoded.replace(
                    "+>+", " > "
                )
                # 步骤 2: 替换剩余的 '+' 为空格
                requested_selector = requested_selector_decoded.replace("+", " ")

                if requested_selector_raw != requested_selector:
                    logging.debug(
                        f"CSS 选择器解码: '{requested_selector_raw}' -> '{requested_selector}'"
                    )

            except Exception as decode_err:
                logging.warning(
                    f"CSS 选择器解码失败: {decode_err}，将使用原始请求字符串"
                )
                requested_selector = requested_selector_raw

            if requested_selector == "Web_animation":
                return redirect("/Cascading_Style_Sheets_Web_animation.css")
            found_css_text = []

            # 遍历 stylesheet 对象
            for rule in stylesheet:
                if rule.type == cssutils.css.CSSRule.STYLE_RULE:
                    # 这是一个样式规则
                    for selector in rule.selectorList:
                        if selector.selectorText.strip() == requested_selector:
                            # 找到了！.cssText 会根据上面设置的偏好自动格式化
                            found_css_text.append(rule.cssText)
                            break  # 找到后跳出内循环

                # --- 2. 移除 @keyframes 兼容性 ---
                # (此处原有的 KEYFRAMES_RULE 和 UNKNOWN_RULE 逻辑已删除)

            if not found_css_text:
                logging.warning(
                    f"CSS 规则未找到: {requested_selector} (原始请求: {css_path})"
                )
                return (
                    jsonify({"error": f"CSS rule '{requested_selector}' not found"}),
                    404,
                )

            # 合并所有匹配的规则
            content = "\n".join(found_css_text)

            # --- 1. 移除缓存：从文件系统实时获取 mtime 用于 HTTP 缓存 ---
            file_mtime = os.path.getmtime(CSS_FILE_PATH)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            # ETag 必须基于 *生成的 content*
            etag_base = hashlib.md5(content.encode("utf-8")).hexdigest()
            etag = f'"{etag_base}-{"min" if should_minify else "orig"}"'

            # 检查条件请求
            if_modified_since = request.headers.get("If-Modified-Since")
            if_none_match = request.headers.get("If-None-Match")

            if (if_none_match == etag) or (
                not if_none_match and if_modified_since == last_modified
            ):
                logging.debug(f"CSS 使用缓存版本 (304){content_type_suffix}")
                return "", 304

            response = make_response(content)
            response.headers["Content-Type"] = "text/css; charset=utf-8"
            response.headers["Cache-Control"] = "public, max-age=3600"
            response.headers["Last-Modified"] = last_modified
            response.headers["ETag"] = etag
            response.headers["X-Minified"] = "true" if should_minify else "false"

            logging.info(
                f"成功返回 CSS{content_type_suffix} ({len(content)} 字符) for: {requested_selector}"
            )
            return response

        except Exception as e:
            logging.error(f"加载 CSS 时发生错误: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/html/<path:fragment_name>.json", methods=["GET"])
    def serve_html_fragment(fragment_name):
        """
        HTML 片段动态加载 API 端点（支持自动压缩，从统一文件读取）
        """
        try:
            # 统一的 HTML 片段文件
            fragments_file = os.path.join(
                os.path.dirname(__file__), "html_fragments.html"
            )

            # 检查文件是否存在
            if not os.path.exists(fragments_file):
                logging.error(f"HTML 片段文件不存在: {fragments_file}")
                return jsonify({"error": "HTML fragments file not found"}), 500

            # 读取整个片段文件
            with open(fragments_file, "r", encoding="utf-8") as f:
                fragments_content = f.read()

            # 从文件中提取指定的片段
            # 格式：<!-- 段落开始： fragment-name --> ... <!-- 段落结束： fragment-name -->

            pattern = rf"<!-- 段落开始： {re.escape(fragment_name)} -->\s*(.*?)\s*<!-- 段落结束： {re.escape(fragment_name)} -->"
            match = re.search(pattern, fragments_content, re.DOTALL)

            if not match:
                logging.error(f"HTML 片段未找到: {fragment_name}")
                return (
                    jsonify({"error": f"HTML fragment '{fragment_name}' not found"}),
                    404,
                )

            # 提取片段内容
            original_content = match.group(1).strip()

            # 检查是否需要压缩（默认为 true）
            minify_param = request.args.get("minify", "true").lower()
            should_minify = minify_param in ["true", "1", "yes", ""]

            # # 根据参数决定是否压缩
            # if should_minify:
            #     # 压缩 HTML
            #     content = minify_html(original_content)
            #     content_type_suffix = ' (minified)'
            #     logging.info(f"HTML 片段 {fragment_name} 压缩：{len(original_content)} 字节 -> {len(content)} 字节 ({(1-len(content)/len(original_content))*100:.1f}% 压缩率)")
            # else:
            #     # 返回原始 HTML
            #     content = original_content
            #     content_type_suffix = ' (original)'
            #     logging.info(f"HTML 片段 {fragment_name} 返回原始版本：{len(content)} 字节")

            # 根据参数决定是否压缩
            if should_minify:
                # 压缩 HTML
                # （已禁用，因为自定义压缩器有Bug）
                content = original_content
                content_type_suffix = " (original, compression disabled)"
                logging.info(
                    f"HTML 片段 {fragment_name} 压缩功能已禁用，返回原始大小: {len(original_content)} 字节"
                )
            else:
                # 返回原始 HTML
                content = original_content
                content_type_suffix = " (original)"
                logging.info(
                    f"HTML 片段 {fragment_name} 返回原始版本：{len(content)} 字节"
                )

            # 设置 Last-Modified（基于统一文件的修改时间）
            file_mtime = os.path.getmtime(fragments_file)
            last_modified = datetime.datetime.fromtimestamp(file_mtime).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            # 设置 ETag（基于内容哈希 + 压缩标志）

            etag_base = hashlib.md5(content.encode("utf-8")).hexdigest()
            etag = f'"{etag_base}-{"min" if should_minify else "orig"}"'

            # 检查条件请求
            if_modified_since = request.headers.get("If-Modified-Since")
            if_none_match = request.headers.get("If-None-Match")

            if (if_modified_since == last_modified) or (if_none_match == etag):
                logging.debug(
                    f"HTML 片段 {fragment_name} 使用缓存版本 (304){content_type_suffix}"
                )
                return "", 304

            # 创建响应
            response = make_response(content)
            response.headers["Content-Type"] = "text/html; charset=utf-8"
            response.headers["Cache-Control"] = "public, max-age=3600"
            response.headers["Last-Modified"] = last_modified
            response.headers["ETag"] = etag

            # 添加自定义头，标识是否已压缩
            response.headers["X-Minified"] = "true" if should_minify else "false"

            logging.info(
                f"成功返回 HTML 片段 {fragment_name}{content_type_suffix} ({len(content)} 字符)"
            )
            return response

        except Exception as e:
            logging.error(f"加载 HTML 片段时发生错误: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/<path:method>", methods=["GET", "POST"])
    def api_call(method):
        """API调用端点：将前端调用转发到Python后端"""
        # 从请求头获取session_id（前端会在每次调用时添加）
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 401

        # ===== Token验证 (仅非游客会话) =====
        with web_sessions_lock:
            if session_id in web_sessions:
                api_instance = web_sessions[session_id]

                # 如果是已认证的非游客用户，验证token
                if (
                    hasattr(api_instance, "is_authenticated")
                    and api_instance.is_authenticated
                ):
                    if hasattr(api_instance, "is_guest") and not api_instance.is_guest:
                        username = getattr(api_instance, "auth_username", None)

                        if username:
                            # 从cookie获取token
                            token = request.cookies.get("auth_token")

                            if not token:
                                return (
                                    jsonify(
                                        {
                                            "success": False,
                                            "message": "未找到认证令牌，请重新登录",
                                            "need_login": True,
                                        }
                                    ),
                                    401,
                                )

                            # 验证token
                            is_valid, reason = token_manager.verify_token(
                                username, session_id, token
                            )

                            if not is_valid:
                                if reason == "token_expired":
                                    return (
                                        jsonify(
                                            {
                                                "success": False,
                                                "message": "令牌已过期，请重新登录",
                                                "need_login": True,
                                            }
                                        ),
                                        401,
                                    )
                                elif reason == "token_mismatch":
                                    return (
                                        jsonify(
                                            {
                                                "success": False,
                                                "message": "令牌验证失败，可能账号在其他设备登录",
                                                "need_login": True,
                                                "logged_out_elsewhere": True,
                                            }
                                        ),
                                        401,
                                    )
                                else:
                                    return (
                                        jsonify(
                                            {
                                                "success": False,
                                                "message": "令牌验证失败，请重新登录",
                                                "need_login": True,
                                            }
                                        ),
                                        401,
                                    )

                            # Token有效，刷新过期时间
                            token_manager.refresh_token(username, session_id)

        # 更新会话活动时间
        update_session_activity(session_id)

        with web_sessions_lock:
            if session_id not in web_sessions:
                # 尝试恢复会话
                state = load_session_state(session_id)
                if state and state.get("login_success"):
                    api_instance = Api(args)
                    api_instance._session_created_at = state.get(
                        "created_at", time.time()
                    )

                    # 【关键修复】恢复会话ID，确保后续任务可以推送消息
                    api_instance._web_session_id = session_id

                    api_instance.login_success = True
                    api_instance.user_info = state.get("user_info")
                    restore_session_to_api_instance(api_instance, state)
                    web_sessions[session_id] = api_instance
                    logging.info(f"API调用时自动恢复会话: {session_id[:32]}...")
                else:
                    return (
                        jsonify({"success": False, "message": "会话已过期或无效"}),
                        401,
                    )
            api_instance = web_sessions[session_id]

        # 获取请求参数
        if request.method == "POST":
            params = request.get_json() or {}
        else:
            params = dict(request.args)

        # 调用对应的API方法
        try:
            # ============================================================
            # 权限检查：细粒度权限控制
            # 为不同的API方法配置所需的权限
            # ============================================================
            # 说明：
            # - 未列出的方法（如login、logout、get_initial_data等）无需权限检查
            # - 内部方法和回调方法也不需要权限检查
            # - 权限名称遵循"动词_名词"格式（如view_tasks, execute_multi_account）
            # ============================================================
            permission_required_methods = {
                # ===== 通知相关权限 =====
                "mark_notification_read": "mark_notifications_read",  # 标记单个通知已读
                "mark_all_read": "mark_notifications_read",  # 标记所有通知已读
                "get_notifications": "view_notifications",  # 获取通知列表
                "get_cached_notifications": "view_notifications",  # 获取缓存的通知
                # ===== 签到相关权限 =====
                "trigger_attendance": "use_attendance",  # 触发签到操作
                # ===== 多账号管理相关权限 =====
                # 多账号模式切换
                "enter_multi_account_mode": "execute_multi_account",  # 进入多账号模式
                "exit_multi_account_mode": "execute_multi_account",  # 退出多账号模式
                # 多账号的账户管理
                "multi_add_account": "execute_multi_account",  # 添加多账号
                "multi_remove_account": "execute_multi_account",  # 删除单个多账号
                "multi_remove_selected_accounts": "execute_multi_account",  # 删除选中的多个账号
                "multi_remove_all_accounts": "execute_multi_account",  # 删除所有多账号
                # 多账号的配置管理
                "multi_get_all_config_users": "execute_multi_account",  # 获取配置文件中的所有用户
                "multi_load_accounts_from_config": "execute_multi_account",  # 从配置文件加载账号
                "multi_import_accounts": "execute_multi_account",  # 导入多账号数据
                "multi_export_accounts_summary": "execute_multi_account",  # 导出多账号摘要
                "multi_download_import_template": "execute_multi_account",  # 下载导入模板
                # 多账号的状态查询
                "multi_refresh_all_statuses": "execute_multi_account",  # 刷新所有账号状态
                "multi_refresh_single_status": "execute_multi_account",  # 刷新单个账号状态
                "multi_get_all_accounts_status": "execute_multi_account",  # 获取所有账号状态
                # 多账号的参数管理
                "multi_get_account_params": "execute_multi_account",  # 获取账号参数
                "multi_update_account_param": "execute_multi_account",  # 更新账号参数
                # 多账号的任务执行
                "multi_start_single_account": "execute_multi_account",  # 启动单个账号任务
                "multi_start_all_accounts": "execute_multi_account",  # 启动所有账号任务
                "multi_stop_single_account": "execute_multi_account",  # 停止单个账号任务
                "multi_stop_all_accounts": "execute_multi_account",  # 停止所有账号任务
                # ===== 任务管理相关权限 =====
                # 任务查看
                "load_tasks": "view_tasks",  # 加载任务列表
                "get_task_details": "view_tasks",  # 获取任务详情
                "get_task_history": "view_tasks",  # 获取任务历史记录
                "get_historical_track": "view_tasks",  # 获取历史轨迹数据
                "get_run_status": "view_tasks",  # 获取运行状态
                # 任务创建和删除
                "create_task": "create_tasks",  # 创建新任务
                "delete_task": "delete_tasks",  # 删除任务
                # 任务执行控制
                "start_single_run": "start_tasks",  # 启动单个任务
                "start_all_runs": "start_tasks",  # 启动所有任务
                "stop_run": "stop_tasks",  # 停止当前运行的任务
                "stop_current_run": "stop_tasks",  # 停止当前运行（别名）
                # ===== 数据操作权限 =====
                "import_offline_file": "import_offline",  # 导入离线数据文件
                "import_task_data": "import_offline",  # 导入任务数据
                "export_offline_file": "export_data",  # 导出离线数据文件
                "export_task_data": "export_data",  # 导出任务数据
                # ===== 路径操作权限 =====
                "record_path": "record_path",  # 记录路径
                "set_draft_path": "record_path",  # 设置草稿路径
                "clear_path": "record_path",  # 清除路径
                "process_path": "record_path",  # 处理路径数据
                "clear_current_task_draft": "record_path",  # 清除当前任务草稿
                # 路径自动生成
                "auto_generate_path": "auto_generate_path",  # 自动生成路径
                "auto_generate_path_with_api": "auto_generate_path",  # 使用API自动生成路径
                # ===== 参数修改权限 =====
                "update_param": "modify_params",  # 更新参数
                "generate_new_ua": "modify_params",  # 生成新的User-Agent
                "save_amap_key": "modify_params",  # 保存高德地图API密钥
                # # ===== 参数查看权限 =====
                # 'get_params': 'view_params',  # 获取当前参数配置（用于前端读取配置）
                # ===== 地图查看权限 =====
                "get_map_data": "view_map",  # 获取地图数据
                # ===== 用户信息权限 =====
                "get_user_info": "view_user_details",  # 获取用户信息
                "on_user_selected": "view_user_details",  # 选择用户时查看详情
                "update_user_settings": "modify_user_settings",  # 更新用户设置
                # ===== 会话管理权限 =====
                "get_user_sessions": "manage_own_sessions",  # 查看自己的会话列表
                # ===== 日志权限 =====
                "get_logs": "view_logs",  # 查看日志
                "clear_logs": "clear_logs",  # 清除日志
            }

            if method in permission_required_methods:
                required_permission = permission_required_methods[method]
                if hasattr(api_instance, "auth_username"):
                    if not auth_system.check_permission(
                        api_instance.auth_username, required_permission
                    ):
                        return (
                            jsonify(
                                {
                                    "success": False,
                                    "message": f"权限不足：需要 {required_permission} 权限",
                                }
                            ),
                            403,
                        )
                else:
                    return jsonify({"success": False, "message": "请先登录认证"}), 401

            # ============================================================
            # 特殊处理：记录get_initial_data调用时的会话活跃时间
            # 说明：
            # - get_initial_data是前端初始化时调用的核心方法
            # - 每次调用都表示用户在活跃使用应用
            # - 通过更新session_activity时间戳，配合monitor_session_inactivity
            #   实现基于实际用户活跃度的会话管理
            # - 这个记录会覆盖前面的update_session_activity(session_id)调用
            # ============================================================
            if method == "get_initial_data":
                # 记录当前时间为会话最后活跃时间
                # (已提取到 update_session_activity 函数)
                update_session_activity(session_id)
                logging.debug(
                    f"会话 {session_id} 调用 get_initial_data，更新活跃时间戳"
                )

            if hasattr(api_instance, method):
                func = getattr(api_instance, method)

                # 调试：记录params类型和内容
                # logging.debug(f"API call: method={method}, params type={type(params)}, params={str(params)[:200]}")
                logging.debug(
                    f"API调用: 方法={method}, 参数类型={type(params)}, 参数内容={str(params)[:200]}"
                )

                if params:
                    # 保持原有逻辑不变，用于处理其他所有API调用
                    # (例如 login(user, pass) 会收到 params=[user, pass]，
                    #  执行 func(*params) 变为 login(self, user, pass)，这是正确的)

                    # （新）set_draft_path 将落入此分支：
                    # params = [[{...}, ...]]
                    # func(*params) -> set_draft_path(self, [{...}, ...])
                    result = (
                        func(**params) if isinstance(params, dict) else func(*params)
                    )
                else:
                    result = func()

                # 权限过滤：on_user_selected需要检查auto_fill_password权限
                if method == "on_user_selected" and result and isinstance(result, dict):
                    # 检查用户是否有auto_fill_password权限
                    has_auto_fill = False
                    if hasattr(api_instance, "auth_username"):
                        has_auto_fill = auth_system.check_permission(
                            api_instance.auth_username, "auto_fill_password"
                        )

                    # 如果没有权限，清空密码字段
                    if not has_auto_fill:
                        result["password"] = ""

                # 关键改进：对于会改变会话状态的API调用，保存会话状态
                # 扩展自动保存的方法列表，包括所有可能改变状态的操作
                auto_save_methods = [
                    "login",
                    "logout",
                    "load_tasks",
                    "select_task",
                    "start_single_run",
                    "start_all_runs",
                    "stop_current_run",
                    "import_offline_file",
                    "export_offline_file",
                    "record_path",
                    "auto_generate_path",
                    "process_path",
                    "clear_path",
                    "update_param",
                    "generate_new_ua",
                    "enter_multi_account_mode",
                    "exit_multi_account_mode",
                    "enter_single_account_mode",  # 模式切换
                    "multi_add_account",
                    "multi_remove_account",  # 多账号操作
                ]
                if method in auto_save_methods:
                    save_session_state(session_id, api_instance)
                    logging.debug(f"API '{method}' 调用后自动保存会话状态")

                # 返回结果时刷新cookie（如果是非游客）
                response = jsonify(result if result is not None else {"success": True})

                # 刷新cookie过期时间（仅非游客）
                if (
                    hasattr(api_instance, "is_authenticated")
                    and api_instance.is_authenticated
                ):
                    if hasattr(api_instance, "is_guest") and not api_instance.is_guest:
                        token = request.cookies.get("auth_token")
                        if token:
                            response.set_cookie(
                                "auth_token",
                                value=token,
                                max_age=3600,
                                httponly=True,
                                secure=False,
                                samesite="Lax",
                            )

                return response
            else:
                return (
                    jsonify({"success": False, "message": f"未知的API方法: {method}"}),
                    404,
                )
        except Exception as e:
            logging.error(f"API调用失败 {method}: {e}", exc_info=True)
            # 不暴露详细错误信息给前端，只记录到日志
            return jsonify({"success": False, "message": "服务器内部错误"}), 500

    @app.route("/execute_js", methods=["POST"])
    def execute_js():
        """在服务器端Chrome中执行JavaScript代码"""
        # 从请求头获取session_id
        session_id = request.headers.get("X-Session-ID", "")

        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 401
        data = request.get_json() or {}
        script = data.get("script", "")
        args_list = data.get("args", [])

        if not script:
            return jsonify({"success": False, "message": "缺少script参数"}), 400

        try:
            result = chrome_pool.execute_js(session_id, script, *args_list)
            return jsonify({"success": True, "result": result})
        except Exception as e:
            logging.error(f"执行JS失败: {e}")
            return jsonify({"success": False, "message": "JS执行失败"}), 500

    @app.route("/api/background_task/start", methods=["POST"])
    def start_background_task():
        """启动后台任务执行"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "会话无效或未登录"}), 401

        data = request.get_json() or {}
        task_indices = data.get("task_indices", [])
        auto_generate = data.get("auto_generate", False)

        if not task_indices:
            return jsonify({"success": False, "message": "未指定任务"}), 400

        api_instance = web_sessions[session_id]
        result = background_task_manager.start_background_task(
            session_id, api_instance, task_indices, auto_generate
        )
        return jsonify(result)

    @app.route("/api/background_task/status", methods=["GET"])
    def get_background_task_status():
        """获取后台任务状态"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 401

        task_status = background_task_manager.get_task_status(session_id)
        if task_status:
            return jsonify({"success": True, "task_status": task_status})
        else:
            return jsonify({"success": False, "message": "未找到后台任务"})

    @app.route("/api/background_task/stop", methods=["POST"])
    def stop_background_task():
        """停止后台任务"""
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "会话无效或未登录"}), 401

        # 停止任务不仅要更新 TaskManager 的状态，
        # 还必须设置 Api 实例上的 stop_run_flag (threading.Event)，
        # 否则 _run_submission_thread 线程不会停止。
        try:
            with web_sessions_lock:
                if session_id in web_sessions:
                    api_instance = web_sessions[session_id]
                    if hasattr(api_instance, "stop_run_flag"):
                        api_instance.stop_run_flag.set()
                        logging.info(
                            f"已为会话 {session_id[:8]}... 设置 api_instance.stop_run_flag 停止标志"
                        )
                    else:
                        logging.warning(
                            f"会话 {session_id[:8]}... 的 Api 实例缺少 stop_run_flag 属性"
                        )
                else:
                    logging.warning(
                        f"无法在 web_sessions 中找到会话 {session_id[:8]}... 来设置停止标志"
                    )
        except Exception as e:
            logging.error(f"设置 stop_run_flag 时出错: {e}", exc_info=True)
            # 即使这里出错，也继续尝试停止 TaskManager

        result = background_task_manager.stop_task(session_id)
        return jsonify(result)

    # ========== 留言板API ========== #

    @app.route("/api/messages/list", methods=["GET"])
    def get_messages():
        """获取留言列表"""
        # ============================================================
        # IP封禁检查：留言板功能专项封禁
        # 检查客户端IP是否被封禁（scope='messages_only'或'all'）
        # ============================================================
        client_ip = request.remote_addr
        if check_ip_ban(client_ip, scope="messages_only"):
            logging.warning(
                f"[IP封禁] 留言功能封禁拦截：IP {client_ip} 尝试访问 /api/messages/list"
            )
            return (
                jsonify({"success": False, "message": "您的IP已被限制访问留言功能"}),
                403,
            )

        # 验证会话
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "view_messages"):
            return jsonify({"success": False, "message": "无权查看留言"}), 403

        # 读取原始留言文件
        messages_file = "messages.json"
        messages = []

        if os.path.exists(messages_file):
            try:
                with open(messages_file, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logging.error(f"[留言板] 读取留言失败: {e}")
                messages = []

        # --- 实时数据扩充 ---
        enriched_messages = []
        for msg in messages:
            # 复制原始数据
            enriched_msg = msg.copy()

            msg_auth_username = msg.get("auth_username")
            msg_ip = msg.get("ip")
            msg_is_guest = msg.get("is_guest", True)

            # 1. 实时获取IP归属地
            enriched_msg["ip_city"] = get_ip_location(msg_ip)

            # 2. 实时获取昵称和头像
            if not msg_is_guest and msg_auth_username:
                # 注册用户：从 auth_system 获取
                user_details = auth_system.get_user_details(msg_auth_username)
                if user_details:
                    enriched_msg["nickname"] = user_details.get(
                        "nickname", msg_auth_username
                    )
                    enriched_msg["avatar_url"] = user_details.get(
                        "avatar_url", "default_avatar.png"
                    )
                else:
                    # 如果用户文件被删了
                    enriched_msg["nickname"] = f"{msg_auth_username} (已注销)"
                    enriched_msg["avatar_url"] = "default_avatar.png"
            else:
                # 游客：优先使用保存的昵称，其次是邮箱，最后是"游客"
                enriched_msg["nickname"] = (
                    msg.get("nickname") or msg.get("email") or "游客"
                )
                enriched_msg["avatar_url"] = "default_avatar.png"

            enriched_messages.append(enriched_msg)
        # --- 扩充结束 ---

        # 按时间倒序排序（最新的在前）
        enriched_messages.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

        return jsonify({"success": True, "messages": enriched_messages})

    # ============================================================
    # 任务15：IP归属地获取辅助函数
    # 用于获取IP地址的地理位置信息
    # ============================================================
    global get_ip_location

    def get_ip_location(ip_address):
        """
        获取IP地址的地理位置信息 (带1天缓存)

        参数:
            ip_address (str): IP地址字符串（支持IPv4和IPv6）

        返回:
            str: 地理位置信息字符串，格式为去重后的"info1 info2 info3 isp"
                 获取失败返回"未知"

        实现说明:
            - 优先从内存和文件缓存 (logs/ip_location_cache.json) 中读取
            - 缓存有效期为1天 (CACHE_DURATION_SECONDS)
            - 缓存未命中或过期时，调用第三方API（https://api.vore.top/api/IPdata）查询
            - 查询成功后更新内存缓存和文件缓存
            - 异常情况返回'未知'，确保不影响主业务流程
        """
        if not ip_address:
            return "未知"

        current_time = time.time()

        # 1. 检查内存缓存
        with ip_cache_lock:
            cached_entry = ip_location_cache.get(ip_address)

        if cached_entry:
            timestamp = cached_entry.get("timestamp", 0)
            location = cached_entry.get("location")

            # 检查缓存是否在有效期内
            if (current_time - timestamp < CACHE_DURATION_SECONDS) and location:
                logging.debug(f"[IP缓存] 命中: ip={ip_address}, 位置={location}")
                return location
            else:
                logging.debug(f"[IP缓存] 过期: ip={ip_address}")

        # 2. 缓存未命中或已过期，调用API
        try:
            # 从 config.ini 读取 API 密钥
            config_file = os.path.join(os.path.dirname(__file__), "config.ini")
            api_key = ""
            if os.path.exists(config_file):
                try:
                    cfg = configparser.ConfigParser()
                    cfg.read(config_file, encoding="utf-8")
                    api_key = cfg.get("API", "ip_api_key", fallback="")
                except Exception as e:
                    logging.debug(f"[IP定位] 读取配置文件失败: {e}")

            if api_key and api_key != "your_api_key_here" and api_key.strip() != "":
                api_url = (
                    f"https://api.vore.top/api/IPdata?key={api_key}&ip={ip_address}"
                )
            else:
                api_url = f"https://api.vore.top/api/IPdata?ip={ip_address}"

            # 发送GET请求，设置5秒超时
            response = requests.get(api_url, timeout=5)
            data = response.json()

            code = data.get("code")
            msg = data.get("msg", "")

            if code != 200:
                logging.warning(
                    f"[IP定位] API返回错误码: code={code}, msg={msg}, ip={ip_address}"
                )
                return "未知"

            ipdata = data.get("ipdata", {})

            info1 = ipdata.get("info1", "").strip()
            info2 = ipdata.get("info2", "").strip()
            info3 = ipdata.get("info3", "").strip()
            isp = ipdata.get("isp", "").strip()

            location_parts = [info1, info2, info3, isp]

            seen = {}
            unique_parts = []

            for part in location_parts:
                if part and part not in seen:
                    seen[part] = True
                    unique_parts.append(part)

            if unique_parts:
                location_str = " ".join(unique_parts)
                logging.debug(
                    f"[IP定位] 成功获取: ip={ip_address}, 位置={location_str}"
                )

                # 3. 存入缓存并保存
                with ip_cache_lock:
                    ip_location_cache[ip_address] = {
                        "location": location_str,
                        "timestamp": current_time,
                    }
                # 立即保存到文件
                _save_ip_cache()

                return location_str
            else:
                logging.warning(f"[IP定位] API返回空数据: ip={ip_address}")
                return "未知"

        except requests.exceptions.Timeout:
            logging.warning(f"[IP定位] 请求超时: ip={ip_address}")
            return "未知"
        except requests.exceptions.RequestException as e:
            logging.warning(f"[IP定位] 网络请求失败: ip={ip_address}, 错误={str(e)}")
            return "未知"
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            # 添加 JSONDecodeError
            logging.warning(f"[IP定位] 数据解析失败: ip={ip_address}, 错误={str(e)}")
            return "未知"
        except Exception as e:
            logging.error(
                f"[IP定位] 未知错误: ip={ip_address}, 错误={str(e)}", exc_info=True
            )
            return "未知"

    @app.route("/api/messages/post", methods=["POST"])
    def post_message():
        """发表留言"""
        # ============================================================
        # IP封禁检查：留言板功能专项封禁
        # 检查客户端IP是否被封禁（scope='messages_only'或'all'）
        # ============================================================
        # 修复：优先从 X-Forwarded-For 获取真实IP，解决代理后IP显示为127.0.0.1的问题
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For 可能包含多个IP (client, proxy1, proxy2)，取第一个
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.remote_addr

        if check_ip_ban(client_ip, scope="messages_only"):
            logging.warning(f"[IP封禁] 留言功能封禁拦截：IP {client_ip} 尝试发表留言")
        # 验证会话
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查权限
        if not auth_system.check_permission(auth_username, "post_messages"):
            return jsonify({"success": False, "message": "无权发表留言"}), 403

        data = request.json
        content = data.get("content", "").strip()
        email = data.get("email", "").strip()
        nickname = data.get("nickname", "").strip()

        # 验证内容
        if not content:
            return jsonify({"success": False, "message": "留言内容不能为空"})

        if len(content) > 1000:
            return jsonify({"success": False, "message": "留言内容不能超过1000字"})

        # 游客必须填写邮箱和昵称
        is_guest = auth_username == "guest" or not auth_username
        if is_guest:
            if not email:
                return jsonify({"success": False, "message": "游客必须填写邮箱"})
            if not nickname:
                return jsonify({"success": False, "message": "游客必须设置昵称"})
            # 简单的邮箱格式验证

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, email):
                return jsonify({"success": False, "message": "邮箱格式不正确"})

        # ============================================================
        # 任务15：获取用户信息（昵称、头像）和IP归属地
        # 为留言添加更丰富的用户信息和位置信息
        # ============================================================

        # 获取客户端IP地址 (再次确认，确保使用处理过代理的真实IP)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.remote_addr

        # 获取IP归属地（城市）
        ip_city = get_ip_location(client_ip)

        # 获取用户的昵称和头像（对于已登录用户）
        user_nickname = nickname  # 默认使用提交的昵称
        avatar_url = "default_avatar.png"  # 默认头像

        if not is_guest and auth_username:
            # 已登录用户：从用户文件中读取昵称和头像
            try:
                user_hash = hashlib.sha256(auth_username.encode()).hexdigest()
                user_file = os.path.join(SYSTEM_ACCOUNTS_DIR, f"{user_hash}.json")

                if os.path.exists(user_file):
                    with open(user_file, "r", encoding="utf-8") as f:
                        user_data = json.load(f)
                        # 读取用户设置的昵称，如果没有则使用用户名
                        user_nickname = user_data.get("nickname", auth_username)
                        # 读取用户的头像URL
                        avatar_url = user_data.get("avatar_url") or "default_avatar.png"
            except Exception as e:
                # 读取用户信息失败，使用默认值
                logging.warning(f"[留言板] 读取用户信息失败: {str(e)}")
                user_nickname = auth_username

        # 构建留言对象（增强版，包含更多信息）
        message = {
            "id": str(uuid.uuid4()),  # 留言唯一ID
            "content": content,  # 留言内容
            "auth_username": (
                auth_username if not is_guest else None
            ),  # 用户名（已登录用户）
            "nickname": nickname if is_guest else None,  # 昵称（游客）
            "email": email if is_guest else None,  # 邮箱（游客）
            "is_guest": is_guest,  # 是否游客
            "timestamp": time.time(),  # 发表时间戳
            "ip": client_ip,  # IP地址（用于管理，使用处理后的真实IP）
        }

        # 读取现有留言
        messages_file = "messages.json"
        messages = []

        if os.path.exists(messages_file):
            try:
                with open(messages_file, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logging.error(f"[留言板] 读取留言失败: {e}")
                messages = []

        # 添加新留言
        messages.append(message)

        # 保存留言
        try:
            with open(messages_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            logging.info(
                f"[留言板] 新留言 --> 用户: {auth_username}, 昵称: {nickname}, 内容长度: {len(content)}字"
            )
            return jsonify(
                {
                    "success": True,
                    "message": "留言发表成功",
                    "message_id": message["id"],
                }
            )
        except OSError as e:
            logging.error(f"[留言板] 保存留言失败: {e}")
            return jsonify({"success": False, "message": "保存留言失败"}), 500

    @app.route("/api/messages/delete", methods=["POST"])
    def delete_message():
        """删除留言"""
        # 验证会话
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未登录"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        data = request.json
        message_id = data.get("message_id", "").strip()

        if not message_id:
            return jsonify({"success": False, "message": "留言ID不能为空"})

        # 读取留言
        messages_file = "messages.json"
        messages = []

        if os.path.exists(messages_file):
            try:
                with open(messages_file, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logging.error(f"[留言板] 读取留言失败: {e}")
                return jsonify({"success": False, "message": "读取留言失败"}), 500

        # 查找要删除的留言
        message_to_delete = None
        for msg in messages:
            if msg.get("id") == message_id:
                message_to_delete = msg
                break

        if not message_to_delete:
            return jsonify({"success": False, "message": "留言不存在"})

        # 检查权限
        can_delete_any = auth_system.check_permission(
            auth_username, "delete_any_messages"
        )
        can_delete_own = auth_system.check_permission(
            auth_username, "delete_own_messages"
        )
        is_own_message = message_to_delete.get(
            "auth_username"
        ) == auth_username and not message_to_delete.get("is_guest")

        if can_delete_any:
            # 管理员可以删除任何留言
            pass
        elif can_delete_own and is_own_message:
            # 普通用户可以删除自己的留言
            pass
        else:
            return jsonify({"success": False, "message": "无权删除此留言"}), 403

        # 删除留言
        messages = [msg for msg in messages if msg.get("id") != message_id]

        # 保存留言
        try:
            with open(messages_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            logging.info(
                f"[留言板] 删除留言 --> 操作用户: {auth_username}, 留言ID: {message_id}"
            )
            return jsonify({"success": True, "message": "留言已删除"})
        except OSError as e:
            logging.error(f"[留言板] 保存留言失败: {e}")
            return jsonify({"success": False, "message": "保存留言失败"}), 500

    # ============================================================
    # 任务22：高德地图Key验证API
    # 用于验证用户输入的高德地图API Key是否有效
    # ============================================================
    @app.route("/api/validate_amap_key", methods=["POST"])
    def validate_amap_key():
        """
        验证高德地图API Key的有效性

        请求体:
            {
                "key": "高德地图API Key字符串"
            }

        返回:
            {
                "success": True/False,
                "message": "验证结果消息"
            }

        实现说明:
            - 调用高德地图的地理编码API进行验证
            - 使用固定坐标（天安门）作为测试参数
            - 根据返回的status字段判断Key是否有效
        """
        try:
            # 从请求体中获取要验证的API Key
            data = request.get_json() or {}
            amap_key = data.get("key", "").strip()

            # 验证Key不能为空
            if not amap_key:
                return jsonify({"success": False, "message": "API Key不能为空"})

            # 调用高德地图逆地理编码API进行验证
            # 使用天安门的坐标（116.397428,39.90923）作为测试参数
            import requests

            test_url = f"https://restapi.amap.com/v3/geocode/regeo?location=116.397428,39.90923&key={amap_key}"

            # 设置5秒超时，防止长时间等待
            response = requests.get(test_url, timeout=5)
            result = response.json()

            # 检查高德API返回的status字段
            # status='1' 表示成功，Key有效
            # status='0' 表示失败，Key无效或其他错误
            if result.get("status") == "1":
                return jsonify(
                    {"success": True, "message": "API Key验证成功，该Key有效"}
                )
            else:
                # 获取错误信息
                error_info = result.get("info", "未知错误")
                return jsonify(
                    {"success": False, "message": f"API Key无效: {error_info}"}
                )

        except requests.exceptions.Timeout:
            # 请求超时
            return jsonify({"success": False, "message": "验证超时，请检查网络连接"})
        except requests.exceptions.RequestException as e:
            # 网络错误
            return jsonify({"success": False, "message": f"网络请求失败: {str(e)}"})
        except Exception as e:
            # 其他异常
            logging.error(f"[高德Key验证] 验证失败: {str(e)}")
            return jsonify({"success": False, "message": f"验证失败: {str(e)}"})

    # ============================================================
    # 定时提醒功能API
    # 用于管理定时提醒，在特定时间段弹出提示
    # ============================================================

    @app.route("/api/reminders/list", methods=["GET"])
    def get_reminders_list():
        """
        获取所有提醒列表

        功能说明:
            - 读取reminders.json文件中的所有提醒数据
            - 返回提醒列表供前端显示
            - 仅管理员有权查看和管理提醒

        返回格式:
            {
                "success": True/False,
                "reminders": [提醒对象列表],
                "message": "错误消息（仅失败时）"
            }

        提醒对象格式:
            {
                "id": "唯一标识符",
                "title": "提醒标题",
                "message": "提醒内容",
                "start_time": "开始时间 HH:MM",
                "end_time": "结束时间 HH:MM",
                "enabled": true/false,
                "created_at": 创建时间戳,
                "updated_at": 更新时间戳
            }
        """
        # 从请求头获取session_id，进行权限验证
        session_id = request.headers.get("X-Session-ID", "")

        # 验证session_id是否存在且有效
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问，请先登录"}), 401

        # 获取当前用户的认证信息
        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查用户权限：只有管理员可以管理提醒
        # 使用auth_system检查用户是否有管理员权限
        if not auth_system.check_permission(auth_username, "view_logs"):
            # 这里使用view_logs权限作为管理员判断依据
            # 您也可以添加专门的'manage_reminders'权限
            return (
                jsonify(
                    {"success": False, "message": "权限不足，仅管理员可以管理提醒"}
                ),
                403,
            )

        try:
            # 定义提醒数据文件路径
            reminders_file = "reminders.json"

            # 初始化提醒列表
            reminders = []

            # 检查文件是否存在
            if os.path.exists(reminders_file):
                # 读取JSON文件
                with open(reminders_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 从JSON中提取reminders数组
                    reminders = data.get("reminders", [])

            # 按创建时间倒序排序（最新的在前）
            reminders.sort(key=lambda x: x.get("created_at", 0), reverse=True)

            # 记录日志
            logging.info(
                f"[定时提醒] 用户 {auth_username} 获取提醒列表，共 {len(reminders)} 条"
            )

            # 返回成功响应
            return jsonify({"success": True, "reminders": reminders})

        except json.JSONDecodeError as e:
            # JSON解析错误
            logging.error(f"[定时提醒] JSON解析失败: {e}")
            return jsonify({"success": False, "message": "提醒数据文件格式错误"}), 500

        except Exception as e:
            # 其他异常
            logging.error(f"[定时提醒] 获取提醒列表失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"获取提醒列表失败: {str(e)}"}),
                500,
            )

    @app.route("/api/reminders/add", methods=["POST"])
    def add_reminder():
        """
        添加新提醒

        请求体:
            {
                "title": "提醒标题",
                "message": "提醒内容",
                "start_time": "19:00",
                "end_time": "20:00",
                "enabled": true
            }

        返回:
            {
                "success": True/False,
                "message": "操作结果消息",
                "reminder_id": "新创建的提醒ID（成功时）"
            }

        验证规则:
            - 标题和内容不能为空
            - 时间格式必须为 HH:MM（24小时制）
            - 标题长度不超过50字符
            - 内容长度不超过500字符
        """
        # 权限验证
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        # 检查管理员权限
        if not auth_system.check_permission(auth_username, "view_logs"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        try:
            # 获取请求数据
            data = request.get_json() or {}
            title = data.get("title", "").strip()
            message = data.get("message", "").strip()
            start_time = data.get("start_time", "").strip()
            end_time = data.get("end_time", "").strip()
            enabled = data.get("enabled", True)

            # ===== 数据验证 =====

            # 验证标题
            if not title:
                return jsonify({"success": False, "message": "提醒标题不能为空"})
            if len(title) > 50:
                return jsonify(
                    {"success": False, "message": "提醒标题不能超过50个字符"}
                )

            # 验证内容
            if not message:
                return jsonify({"success": False, "message": "提醒内容不能为空"})
            if len(message) > 500:
                return jsonify(
                    {"success": False, "message": "提醒内容不能超过500个字符"}
                )

            # 验证时间格式（HH:MM）
            time_pattern = re.compile(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
            if not time_pattern.match(start_time):
                return jsonify(
                    {
                        "success": False,
                        "message": "开始时间格式错误，应为 HH:MM（如 19:00）",
                    }
                )
            if not time_pattern.match(end_time):
                return jsonify(
                    {
                        "success": False,
                        "message": "结束时间格式错误，应为 HH:MM（如 20:00）",
                    }
                )

            # 验证enabled字段类型
            if not isinstance(enabled, bool):
                enabled = bool(enabled)

            # ===== 创建提醒对象 =====

            # 生成唯一ID
            reminder_id = str(uuid.uuid4())
            current_timestamp = time.time()

            # 构建提醒对象
            new_reminder = {
                "id": reminder_id,
                "title": title,
                "message": message,
                "start_time": start_time,
                "end_time": end_time,
                "enabled": enabled,
                "created_at": current_timestamp,
                "updated_at": current_timestamp,
            }

            # ===== 保存到文件 =====

            reminders_file = "reminders.json"
            reminders = []

            # 读取现有提醒
            if os.path.exists(reminders_file):
                try:
                    with open(reminders_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        reminders = data.get("reminders", [])
                except (json.JSONDecodeError, OSError):
                    # 文件损坏，使用空列表
                    reminders = []

            # 添加新提醒到列表
            reminders.append(new_reminder)

            # 写入文件
            with open(reminders_file, "w", encoding="utf-8") as f:
                json.dump({"reminders": reminders}, f, indent=2, ensure_ascii=False)

            # 记录日志
            logging.info(
                f"[定时提醒] 用户 {auth_username} 添加提醒: {title} ({start_time}-{end_time})"
            )

            # 返回成功响应
            return jsonify(
                {"success": True, "message": "提醒添加成功", "reminder_id": reminder_id}
            )

        except Exception as e:
            logging.error(f"[定时提醒] 添加提醒失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"添加提醒失败: {str(e)}"}),
                500,
            )

    @app.route("/api/reminders/update", methods=["POST"])
    def update_reminder():
        """
        更新现有提醒

        请求体:
            {
                "id": "提醒ID",
                "title": "新标题",
                "message": "新内容",
                "start_time": "19:00",
                "end_time": "20:00",
                "enabled": true
            }

        返回:
            {
                "success": True/False,
                "message": "操作结果消息"
            }

        说明:
            - 必须提供提醒ID
            - 其他字段可选，未提供的字段保持原值
            - 更新updated_at时间戳
        """
        # 权限验证
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_system.check_permission(auth_username, "view_logs"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        try:
            # 获取请求数据
            data = request.get_json() or {}
            reminder_id = data.get("id", "").strip()

            # 验证ID
            if not reminder_id:
                return jsonify({"success": False, "message": "提醒ID不能为空"})

            # 读取现有提醒
            reminders_file = "reminders.json"
            if not os.path.exists(reminders_file):
                return jsonify({"success": False, "message": "提醒文件不存在"}), 404

            with open(reminders_file, "r", encoding="utf-8") as f:
                reminders_data = json.load(f)
                reminders = reminders_data.get("reminders", [])

            # 查找要更新的提醒
            reminder_found = False
            for reminder in reminders:
                if reminder.get("id") == reminder_id:
                    reminder_found = True

                    # 更新字段（如果提供了新值）
                    if "title" in data:
                        title = data["title"].strip()
                        if not title:
                            return jsonify(
                                {"success": False, "message": "标题不能为空"}
                            )
                        if len(title) > 50:
                            return jsonify(
                                {"success": False, "message": "标题不能超过50个字符"}
                            )
                        reminder["title"] = title

                    if "message" in data:
                        message = data["message"].strip()
                        if not message:
                            return jsonify(
                                {"success": False, "message": "内容不能为空"}
                            )
                        if len(message) > 500:
                            return jsonify(
                                {"success": False, "message": "内容不能超过500个字符"}
                            )
                        reminder["message"] = message

                    if "start_time" in data:
                        start_time = data["start_time"].strip()
                        time_pattern = re.compile(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
                        if not time_pattern.match(start_time):
                            return jsonify(
                                {"success": False, "message": "开始时间格式错误"}
                            )
                        reminder["start_time"] = start_time

                    if "end_time" in data:
                        end_time = data["end_time"].strip()
                        time_pattern = re.compile(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
                        if not time_pattern.match(end_time):
                            return jsonify(
                                {"success": False, "message": "结束时间格式错误"}
                            )
                        reminder["end_time"] = end_time

                    if "enabled" in data:
                        reminder["enabled"] = bool(data["enabled"])

                    # 更新时间戳
                    reminder["updated_at"] = time.time()

                    break

            if not reminder_found:
                return jsonify({"success": False, "message": "提醒不存在"}), 404

            # 保存更新后的数据
            with open(reminders_file, "w", encoding="utf-8") as f:
                json.dump({"reminders": reminders}, f, indent=2, ensure_ascii=False)

            logging.info(f"[定时提醒] 用户 {auth_username} 更新提醒: {reminder_id}")

            return jsonify({"success": True, "message": "提醒更新成功"})

        except Exception as e:
            logging.error(f"[定时提醒] 更新提醒失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"更新提醒失败: {str(e)}"}),
                500,
            )

    @app.route("/api/reminders/delete", methods=["POST"])
    def delete_reminder():
        """
        删除提醒

        请求体:
            {
                "id": "提醒ID"
            }

        返回:
            {
                "success": True/False,
                "message": "操作结果消息"
            }
        """
        # 权限验证
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        api_instance = web_sessions[session_id]
        auth_username = getattr(api_instance, "auth_username", "")

        if not auth_system.check_permission(auth_username, "view_logs"):
            return jsonify({"success": False, "message": "权限不足"}), 403

        try:
            # 获取请求数据
            data = request.get_json() or {}
            reminder_id = data.get("id", "").strip()

            # 验证ID
            if not reminder_id:
                return jsonify({"success": False, "message": "提醒ID不能为空"})

            # 读取现有提醒
            reminders_file = "reminders.json"
            if not os.path.exists(reminders_file):
                return jsonify({"success": False, "message": "提醒文件不存在"}), 404

            with open(reminders_file, "r", encoding="utf-8") as f:
                reminders_data = json.load(f)
                reminders = reminders_data.get("reminders", [])

            # 查找并删除提醒
            original_count = len(reminders)
            reminders = [r for r in reminders if r.get("id") != reminder_id]

            if len(reminders) == original_count:
                # 没有删除任何提醒，说明ID不存在
                return jsonify({"success": False, "message": "提醒不存在"}), 404

            # 保存更新后的数据
            with open(reminders_file, "w", encoding="utf-8") as f:
                json.dump({"reminders": reminders}, f, indent=2, ensure_ascii=False)

            logging.info(f"[定时提醒] 用户 {auth_username} 删除提醒: {reminder_id}")

            return jsonify({"success": True, "message": "提醒删除成功"})

        except Exception as e:
            logging.error(f"[定时提醒] 删除提醒失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"删除提醒失败: {str(e)}"}),
                500,
            )

    @app.route("/api/reminders/check", methods=["GET"])
    def check_reminders():
        """
        检查当前时间是否有需要显示的提醒

        功能说明:
            - 获取当前时间（HH:MM格式）
            - 遍历所有启用的提醒
            - 判断当前时间是否在提醒的时间范围内
            - 支持跨天时间段判断（如 20:00 到次日 08:00）

        返回:
            {
                "success": True,
                "reminders": [当前需要显示的提醒列表]
            }

        时间判断逻辑:
            - 正常时间段（start_time < end_time）：
              当前时间 >= start_time 且 当前时间 < end_time
            - 跨天时间段（start_time > end_time）：
              当前时间 >= start_time 或 当前时间 < end_time
        """
        try:
            # 获取当前时间（HH:MM格式）
            from datetime import datetime

            current_time_str = datetime.now().strftime("%H:%M")

            # 读取所有提醒
            reminders_file = "reminders.json"
            if not os.path.exists(reminders_file):
                # 文件不存在，返回空列表
                return jsonify({"success": True, "reminders": []})

            with open(reminders_file, "r", encoding="utf-8") as f:
                reminders_data = json.load(f)
                all_reminders = reminders_data.get("reminders", [])

            # 筛选需要显示的提醒
            active_reminders = []

            for reminder in all_reminders:
                # 只处理启用的提醒
                if not reminder.get("enabled", False):
                    continue

                start_time = reminder.get("start_time", "")
                end_time = reminder.get("end_time", "")

                # 验证时间格式
                if not start_time or not end_time:
                    continue

                # 判断当前时间是否在提醒时间范围内
                if _is_time_in_range(current_time_str, start_time, end_time):
                    # 添加到活动提醒列表
                    active_reminders.append(
                        {
                            "id": reminder.get("id"),
                            "title": reminder.get("title"),
                            "message": reminder.get("message"),
                        }
                    )

            # 返回结果
            return jsonify({"success": True, "reminders": active_reminders})

        except Exception as e:
            logging.error(f"[定时提醒] 检查提醒失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": f"检查提醒失败: {str(e)}"}),
                500,
            )

    def _is_time_in_range(current_time, start_time, end_time):
        """
        辅助函数：判断当前时间是否在指定的时间范围内

        参数:
            current_time (str): 当前时间，格式为 HH:MM
            start_time (str): 开始时间，格式为 HH:MM
            end_time (str): 结束时间，格式为 HH:MM

        返回:
            bool: True表示在范围内，False表示不在范围内

        逻辑说明:
            - 情况1：正常时间段（start_time < end_time）
              例如：09:00 到 17:00
              判断：current_time >= start_time 且 current_time < end_time

            - 情况2：跨天时间段（start_time > end_time）
              例如：20:00 到次日 08:00
              判断：current_time >= start_time 或 current_time < end_time

        示例:
            - _is_time_in_range("19:30", "19:00", "20:00") -> True
            - _is_time_in_range("20:30", "20:00", "08:00") -> True （跨天）
            - _is_time_in_range("07:30", "20:00", "08:00") -> True （跨天）
            - _is_time_in_range("09:00", "20:00", "08:00") -> False
        """
        try:
            # 将时间字符串转换为分钟数（从00:00开始计算）
            # 例如："19:30" -> 19 * 60 + 30 = 1170分钟
            def time_to_minutes(time_str):
                """将HH:MM格式的时间转换为从00:00开始的分钟数"""
                hours, minutes = map(int, time_str.split(":"))
                return hours * 60 + minutes

            # 转换所有时间为分钟数
            current_minutes = time_to_minutes(current_time)
            start_minutes = time_to_minutes(start_time)
            end_minutes = time_to_minutes(end_time)

            # 情况1：正常时间段（不跨天）
            if start_minutes < end_minutes:
                # 例如：09:00 到 17:00
                # 判断当前时间是否在 [start, end) 区间内
                return start_minutes <= current_minutes < end_minutes

            # 情况2：跨天时间段
            elif start_minutes > end_minutes:
                # 例如：20:00 到次日 08:00
                # 判断当前时间是否 >= 20:00 或者 < 08:00
                return current_minutes >= start_minutes or current_minutes < end_minutes

            # 情况3：start_time == end_time（边界情况，视为无效）
            else:
                return False

        except Exception as e:
            # 时间解析失败，记录错误并返回False
            logging.warning(f"[定时提醒] 时间范围判断失败: {e}")
            return False

    # ============================================================
    # 验证码功能API
    # 用于获取和验证图形验证码，增强系统安全性
    # ============================================================

    @app.route("/api/captcha/get", methods=["GET"])
    def get_captcha():
        """
        获取验证码接口 【本地验证码生成器】

        功能说明:
            - 使用本地MicroPixelCaptcha生成器生成验证码（替代不稳定的第三方API）
            - 生成唯一的验证码ID，将ID和答案存储在JSON文件中
            - 返回验证码的HTML内容、验证码ID和尺寸给前端显示

        返回格式:
            {
                "success": True/False,
                "html": "验证码HTML内容（用于在前端显示图片）",
                "captcha_id": "唯一的验证码ID",
                "width": 验证码宽度（像素），
                "height": 验证码高度（像素），
                "message": "错误消息（仅失败时返回）"
            }

        安全说明:
            - 验证码答案存储在服务器端JSON文件中，不会返回给前端
            - 使用UUID生成唯一的验证码ID，防止冲突
            - 验证码文件存储在logs/captchas目录下
            - 验证码有效期10分钟，过期自动清理
        """
        # 从请求头获取session_id
        session_id = request.headers.get("X-Session-ID", "")

        # 验证session_id是否存在
        if not session_id:
            return jsonify({"success": False, "message": "缺少会话ID"}), 401

        try:
            # 【本地验证码生成器】读取配置参数
            config_file = os.path.join(os.path.dirname(__file__), "config.ini")
            length = 4  # 默认4位验证码
            scale_factor = 2  # 默认细分倍数为2
            noise_level = 0.08  # 默认噪点比例0.08

            if os.path.exists(config_file):
                try:
                    cfg = configparser.ConfigParser()
                    cfg.read(config_file, encoding="utf-8")
                    # 从[Captcha]节读取参数
                    length = int(cfg.get("Captcha", "length", fallback="4"))
                    scale_factor = int(cfg.get("Captcha", "scale_factor", fallback="2"))
                    noise_level = float(
                        cfg.get("Captcha", "noise_level", fallback="0.08")
                    )
                    logging.debug(
                        f"[本地验证码] 从config.ini读取参数: length={length}, scale_factor={scale_factor}, noise_level={noise_level}"
                    )
                except Exception as e:
                    logging.warning(f"[本地验证码] 读取配置文件失败，使用默认值: {e}")

            # 【本地验证码生成器】使用 MicroPixelCaptcha (已在文件顶部处理导入或Fallback)
            # from get_captchas import MicroPixelCaptcha # 不需要再次导入，使用全局定义
            generator = MicroPixelCaptcha()

            # 生成验证码（返回验证码答案、HTML、宽度和高度）
            captcha_code, captcha_html, captcha_width, captcha_height = (
                generator.generate(
                    length=length, scale_factor=scale_factor, noise_level=noise_level
                )
            )

            logging.debug(
                f"[本地验证码] 已生成验证码，长度={length}，答案={captcha_code}，尺寸={captcha_width}x{captcha_height}"
            )

            # 验证数据完整性
            if not captcha_html or not captcha_code:
                logging.error(
                    f"[本地验证码] 生成数据不完整: html={bool(captcha_html)}, code={bool(captcha_code)}"
                )
                return jsonify({"success": False, "message": "验证码生成失败"}), 500

            # 生成唯一的验证码ID
            import uuid

            captcha_id = str(uuid.uuid4())

            # 确保captchas目录存在 - 使用全局 LOGIN_LOGS_DIR
            captchas_dir = os.path.join(LOGIN_LOGS_DIR, "captchas")
            os.makedirs(captchas_dir, exist_ok=True)

            # 准备验证码数据
            # 【CDN缓存修复】添加html字段，用于新的iframe API读取
            captcha_data = {
                "id": captcha_id,
                "code": captcha_code.upper(),  # 统一转换为大写
                "html": captcha_html,  # 【CDN缓存修复】存储HTML内容，供 /api/captcha/html/<captcha_id> 使用
                "session_id": session_id,
                "timestamp": time.time(),
                "expires_at": time.time() + 600,  # 10分钟后过期
            }

            # 将验证码数据存储到JSON文件
            captcha_file = os.path.join(captchas_dir, f"{captcha_id}.json")
            with open(captcha_file, "w", encoding="utf-8") as f:
                json.dump(captcha_data, f, indent=2, ensure_ascii=False)

                # 记录验证码请求历史（用于排查错误）
            # 修正：函数定义接收参数，以避免在线程中访问 request 上下文
            def log_captcha_history(
                p_captcha_id, p_code, p_html, p_session_id, p_client_ip, p_user_agent
            ):
                try:
                    # 使用全局配置的 LOGIN_LOGS_DIR，确保路径一致性
                    history_dir = os.path.join(LOGIN_LOGS_DIR, "captcha_history")
                    os.makedirs(history_dir, exist_ok=True)

                    # 获取客户端IP和User-Agent (已通过参数传入)

                    # 准备历史记录数据
                    history_data = {
                        "captcha_id": p_captcha_id,  # 修正：使用参数
                        "code": p_code.upper(),  # 修正：使用参数
                        "html": p_html,  # 保存HTML以便查看验证码图片 # 修正：使用参数
                        "session_id": p_session_id,  # 修正：使用参数
                        "client_ip": p_client_ip,  # 修正：使用参数
                        "user_agent": p_user_agent,  # 修正：使用参数
                        "timestamp": time.time(),
                        "timestamp_readable": datetime.datetime.fromtimestamp(
                            time.time()
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                        "expires_at": time.time() + 600,  # 10分钟后过期
                        "status": "created",  # created, verified_success, verified_failed, expired
                        "verified_at": None,
                        "verified_input": None,
                    }

                    # 使用时间戳作为历史记录文件名的一部分，便于查询
                    date_str = datetime.datetime.now().strftime("%Y%m%d")
                    history_file = os.path.join(
                        history_dir, f"captcha_history_{date_str}.jsonl"
                    )

                    # 追加到历史记录文件（使用JSONL格式，每行一个JSON对象）
                    with open(history_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(history_data, ensure_ascii=False) + "\n")

                    logging.debug(
                        f"[验证码历史] 已记录验证码请求: ID={p_captcha_id[:8]}..."
                    )
                except Exception as e:
                    logging.error(f"[验证码历史] 记录历史失败: {e}", exc_info=True)

            # 在后台线程中记录历史
            import threading

            # 修正：在启动线程前，从 request 上下文中提取所需数据
            client_ip_data = (
                request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
            )
            user_agent_data = request.headers.get("User-Agent", "unknown")

            # 修正：将提取的数据作为 args 传递给线程
            threading.Thread(
                target=log_captcha_history,
                args=(
                    captcha_id,
                    captcha_code,
                    captcha_html,
                    session_id,
                    client_ip_data,
                    user_agent_data,
                ),
                daemon=True,
            ).start()

            # 清理过期的验证码文件（后台任务）
            def cleanup_expired_captchas():
                try:
                    current_time = time.time()
                    for filename in os.listdir(captchas_dir):
                        if filename.endswith(".json"):
                            file_path = os.path.join(captchas_dir, filename)
                            try:
                                with open(file_path, "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                if data.get("expires_at", 0) < current_time:
                                    os.remove(file_path)
                                    logging.debug(
                                        f"[验证码清理] 删除过期验证码: {filename}"
                                    )
                            except Exception as e:
                                logging.warning(
                                    f"[验证码清理] 处理文件 {filename} 时出错: {e}"
                                )
                except Exception as e:
                    logging.error(f"[验证码清理] 清理过期验证码失败: {e}")

            # 在后台线程中清理过期验证码
            import threading

            threading.Thread(target=cleanup_expired_captchas, daemon=True).start()

            # 记录日志（不记录验证码答案）
            logging.info(
                f"[本地验证码] 已生成验证码 ID: {captcha_id[:8]}... 会话: {session_id[:8]}... 长度: {length} 尺寸: {captcha_width}x{captcha_height}px"
            )

            # 返回验证码HTML、ID和尺寸给前端
            return jsonify(
                {
                    "success": True,
                    "html": captcha_html,
                    "captcha_id": captcha_id,
                    "width": captcha_width,
                    "height": captcha_height,
                }
            )

        except ImportError as e:
            # 【本地验证码生成器】无法导入get_captchas模块
            logging.error(f"[本地验证码] 导入MicroPixelCaptcha失败: {str(e)}")
            return jsonify({"success": False, "message": "验证码生成器加载失败"}), 500

        except (ValueError, KeyError, TypeError) as e:
            # 【本地验证码生成器】数据处理错误
            logging.error(f"[本地验证码] 数据处理失败: {str(e)}")
            return jsonify({"success": False, "message": "验证码数据处理错误"}), 500

        except Exception as e:
            # 【本地验证码生成器】其他未知错误
            logging.error(f"[本地验证码] 未知错误: {str(e)}", exc_info=True)
            return jsonify({"success": False, "message": "生成验证码时发生错误"}), 500

    @app.route("/api/captcha/html/<captcha_id>", methods=["GET"])
    def get_captcha_html_page(captcha_id):
        """
        获取验证码HTML页面（用于iframe嵌入）
        """

        def get_full_html_for_error(message):
            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
        <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>跑步助手图形化验证码</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <p style="color: red; text-align: center; padding: 20px;">{message}</p>
</body>
</html>"""
            return full_html

        if not captcha_id:
            logging.warning("[验证码HTML页面] 请求缺少验证码ID")
            return get_full_html_for_error("验证码ID无效"), 400

        target_width = request.args.get("width", type=int, default=None)

        if target_width is not None:
            if target_width <= 0:
                logging.warning(
                    f"[移动端验证码缩放] 无效的width参数: {target_width} (必须 > 0)，使用原始HTML"
                )
                target_width = None
            elif target_width < 100:
                logging.warning(
                    f"[移动端验证码缩放] width参数过小: {target_width} (建议 >= 100)，使用原始HTML"
                )
                target_width = None

        captchas_dir = os.path.join("logs", "captchas")
        captcha_file = os.path.join(captchas_dir, f"{captcha_id}.json")

        if not os.path.exists(captcha_file):
            logging.warning(f"[验证码HTML页面] 验证码文件不存在: {captcha_id[:8]}...")
            return get_full_html_for_error("验证码不存在或已过期"), 404

        try:

            with open(captcha_file, "r", encoding="utf-8") as f:
                captcha_data = json.load(f)

            current_time = time.time()
            expires_at = captcha_data.get("expires_at", 0)
            if expires_at < current_time:
                logging.info(
                    f"[验证码HTML页面] 验证码已过期: {captcha_id[:8]}... (过期时间: {expires_at}, 当前时间: {current_time})"
                )
                return get_full_html_for_error("验证码已过期，请刷新"), 410

            captcha_html_content = captcha_data.get("html", "")

            if not captcha_html_content:
                logging.error(
                    f"[验证码HTML页面] 验证码HTML内容为空: {captcha_id[:8]}..."
                )
                return get_full_html_for_error("验证码内容不可用"), 404

            if target_width is not None:
                captcha_html_content = resize_captcha_html(
                    captcha_html_content, target_width
                )

            # ========================================
            # 步骤7: 构建完整的HTML5页面
            # - 添加完整的HTML文档结构（<!DOCTYPE html>, <html>, <head>, <body>）
            # - 添加meta标签设置字符编码和viewport（移动端适配）
            # - 【关键】添加多层防缓存meta标签：
            #   * Cache-Control: no-cache, no-store, must-revalidate
            #   * Pragma: no-cache (兼容HTTP/1.0)
            #   * Expires: 0 (立即过期)
            # - 添加CSS样式，确保验证码图片在iframe中居中显示且响应式
            # - 插入验证码HTML内容（通常是<img>标签）
            # ========================================
            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 【CDN缓存修复】禁用缓存的meta标签，确保验证码每次都是最新的 -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>跑步助手图形化验证码</title>
    <style>
        /* 【CDN缓存修复】响应式样式，确保验证码在iframe中正确显示 */
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80px;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        /* 确保验证码图片响应式显示，不超出iframe边界 */
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            image-rendering: crisp-edges; /* 优化图片渲染，避免模糊 */
        }}
    </style>
</head>
<body>
    <!-- 【CDN缓存修复】验证码HTML内容，通常是包含base64图片的<img>标签 -->
    {captcha_html_content}
</body>
</html>"""

            # ========================================
            # 步骤8: 设置HTTP响应头，强制禁用缓存
            # - Content-Type: text/html; charset=utf-8（指定HTML内容和字符编码）
            # - Cache-Control: no-cache, no-store, must-revalidate（HTTP/1.1禁用缓存）
            #   * no-cache: 必须向服务器验证后才能使用缓存
            #   * no-store: 完全禁止缓存
            #   * must-revalidate: 过期后必须重新验证
            # - Pragma: no-cache（HTTP/1.0兼容性，禁用缓存）
            # - Expires: 0（设置过期时间为0，立即过期）
            # ========================================
            response = make_response(full_html)
            response.headers["Content-Type"] = "text/html; charset=utf-8"
            # 【CDN缓存修复】多层防缓存响应头，确保CDN和浏览器都不缓存
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

            # 记录成功日志（仅记录captcha_id的前8位，避免日志过长）
            logging.debug(f"[验证码HTML页面] 成功返回验证码HTML: {captcha_id}")

            return response

        except json.JSONDecodeError as e:
            # JSON解析错误（文件损坏或格式错误）
            logging.error(f"[验证码HTML页面] JSON解析失败: {captcha_id} - {e}")
            return (
                '<html><body><p style="color: red; text-align: center; padding: 20px;">验证码数据损坏</p></body></html>',
                500,
            )

        except IOError as e:
            # 文件读取错误（权限问题、磁盘错误等）
            logging.error(f"[验证码HTML页面] 文件读取失败: {captcha_id} - {e}")
            return (
                '<html><body><p style="color: red; text-align: center; padding: 20px;">读取验证码失败</p></body></html>',
                500,
            )

        except Exception as e:
            # 其他未预料的错误
            logging.error(
                f"[验证码HTML页面] 未知错误: {captcha_id} - {e}", exc_info=True
            )
            return (
                '<html><body><p style="color: red; text-align: center; padding: 20px;">读取验证码时发生错误</p></body></html>',
                500,
            )

    def verify_captcha(captcha_id, user_input):
        """
        验证验证码辅助函数

        参数:
            captcha_id (str): 验证码ID
            user_input (str): 用户输入的验证码

        返回:
            tuple: (是否验证成功: bool, 错误消息: str)
                   成功返回 (True, "")
                   失败返回 (False, "具体错误原因")

        验证逻辑:
            1. 根据验证码ID从JSON文件中读取验证码数据
            2. 检查验证码是否过期
            3. 不区分大小写比对用户输入与存储的验证码答案
            4. 验证后立即删除验证码文件（一次性使用）

        安全特性:
            - 验证码使用后立即失效（防止重放攻击）
            - 不区分大小写，提升用户体验
            - 验证失败也会删除验证码，需要重新获取
            - 支持验证码过期机制
        """
        # 检查验证码ID是否为空
        if not captcha_id or not captcha_id.strip():
            return False, "验证码ID不能为空"

        # 检查用户输入是否为空
        if not user_input or not user_input.strip():
            return False, "验证码不能为空"

        # 构建验证码文件路径
        captchas_dir = os.path.join("logs", "captchas")
        captcha_file = os.path.join(captchas_dir, f"{captcha_id}.json")

        # 检查验证码文件是否存在
        if not os.path.exists(captcha_file):
            return False, "验证码不存在或已失效"

        try:
            # 读取验证码数据
            with open(captcha_file, "r", encoding="utf-8") as f:
                captcha_data = json.load(f)

            # 检查验证码是否过期
            current_time = time.time()
            if captcha_data.get("expires_at", 0) < current_time:
                # 删除过期的验证码文件
                try:
                    os.remove(captcha_file)
                except Exception as e:
                    logging.warning(f"[验证码] 删除过期验证码文件失败: {e}")
                return False, "验证码已过期"

            # 获取存储的验证码答案
            stored_code = captcha_data.get("code", "")

            # 不区分大小写比对（统一转换为大写）
            user_input_upper = user_input.strip().upper()

            # 比对验证码
            is_correct = user_input_upper == stored_code

            # 记录验证结果到历史
            def update_captcha_history():
                try:
                    history_dir = os.path.join("logs", "captcha_history")
                    date_str = datetime.datetime.now().strftime("%Y%m%d")
                    history_file = os.path.join(
                        history_dir, f"captcha_history_{date_str}.jsonl"
                    )

                    if os.path.exists(history_file):
                        # 读取所有历史记录
                        lines = []
                        with open(history_file, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                        # 更新对应的记录
                        updated = False
                        for i, line in enumerate(lines):
                            try:
                                record = json.loads(line.strip())
                                if record.get("captcha_id") == captcha_id:
                                    record["status"] = (
                                        "verified_success"
                                        if is_correct
                                        else "verified_failed"
                                    )
                                    record["verified_at"] = time.time()
                                    record["verified_at_readable"] = (
                                        datetime.datetime.fromtimestamp(
                                            time.time()
                                        ).strftime("%Y-%m-%d %H:%M:%S")
                                    )
                                    record["verified_input"] = user_input_upper
                                    lines[i] = (
                                        json.dumps(record, ensure_ascii=False) + "\n"
                                    )
                                    updated = True
                                    break
                            except:
                                pass

                        if updated:
                            # 写回文件
                            with open(history_file, "w", encoding="utf-8") as f:
                                f.writelines(lines)

                            logging.debug(
                                f"[验证码历史] 已更新验证结果: ID={captcha_id[:8]}..., 结果={'成功' if is_correct else '失败'}"
                            )
                except Exception as e:
                    logging.error(f"[验证码历史] 更新验证结果失败: {e}", exc_info=True)

            # 在后台线程中更新历史
            import threading

            threading.Thread(target=update_captcha_history, daemon=True).start()

            # 删除验证码文件（无论验证成功或失败，都删除）
            # 这确保验证码只能使用一次
            try:
                os.remove(captcha_file)
                logging.debug(f"[验证码] 已删除验证码文件: {captcha_id}")
            except Exception as e:
                logging.warning(f"[验证码] 删除验证码文件失败: {e}")

            # 返回验证结果
            if is_correct:
                logging.info(f"[验证码] 验证成功: ID={captcha_id[:8]}...")
                return True, ""
            else:
                logging.warning(f"[验证码] 验证失败: ID={captcha_id[:8]}...")
                return False, "验证码错误"

        except json.JSONDecodeError as e:
            logging.error(f"[验证码] JSON解析失败: {e}")
            # 删除损坏的验证码文件
            try:
                os.remove(captcha_file)
            except:
                pass
            return False, "验证码数据损坏"

        except Exception as e:
            logging.error(f"[验证码] 验证过程出错: {e}", exc_info=True)
            return False, "验证码验证失败"

    @app.route("/api/captcha/history", methods=["GET"])
    def get_captcha_history():
        """
        获取验证码请求历史记录（管理员功能）

        权限要求：管理员
        查询参数：
        - date: 日期（格式：YYYYMMDD），默认为今天
        - limit: 返回记录数量限制，默认100
        - status: 状态过滤（created, verified_success, verified_failed, expired）

        返回格式：
            {
                "success": True/False,
                "data": [验证码历史记录列表],
                "total": 总记录数,
                "message": "错误消息"
            }
        """
        # 权限检查：只有管理员可以查看验证码历史
        session_id = request.headers.get("X-Session-ID", "")
        if not session_id or session_id not in web_sessions:
            return jsonify({"success": False, "message": "未授权访问"}), 401

        # 修正：web_sessions 存储的是 Api 实例，不是字典
        api_instance = web_sessions.get(session_id)
        if not api_instance:
            return jsonify({"success": False, "message": "会话无效"}), 401

        username = getattr(api_instance, "auth_username", None)

        if not username:
            return jsonify({"success": False, "message": "未登录"}), 401

        # 检查是否为管理员
        # 修正：AuthSystem 的方法是 check_permission
        if not auth_system.check_permission(username, "view_captcha_history"):
            return jsonify({"success": False, "message": "没有权限查看验证码历史"}), 403

        try:
            # 获取查询参数
            date_str = request.args.get(
                "date", datetime.datetime.now().strftime("%Y%m%d")
            )
            limit = int(request.args.get("limit", 100))
            status_filter = request.args.get("status", "")

            # # 【修正】移除日期字符串中的连字符，以匹配文件名格式 (YYYY-MM-DD -> YYYYMMDD)
            clean_date_str = date_str.replace("-", "")

            # 读取历史记录 - 使用全局 LOGIN_LOGS_DIR
            history_dir = os.path.join(LOGIN_LOGS_DIR, "captcha_history")
            # 使用处理后的日期字符串构建文件名
            history_file = os.path.join(
                history_dir, f"captcha_history_{clean_date_str}.jsonl"
            )

            logging.debug(f"[验证码历史] 正在读取文件: {history_file}")

            if not os.path.exists(history_file):
                logging.info(f"[验证码历史] 文件不存在: {history_file}")
                return jsonify(
                    {
                        "success": True,
                        "data": [],
                        "total": 0,
                        "message": "该日期没有验证码历史记录",
                    }
                )

            # 读取并解析历史记录 - 优化：只保留需要的记录
            records = []
            current_time = time.time()
            expiry_threshold = 30 * 60  # 30分钟（1800秒）

            line_count = 0
            parse_error_count = 0
            total_matched = 0  # 符合过滤条件的总数

            # 状态映射：前端状态 -> 后端状态
            # pending -> created
            # success -> verified_success
            # failed -> verified_failed
            # all -> (忽略过滤)
            target_status = status_filter
            if status_filter == "pending":
                target_status = "created"
            elif status_filter == "success":
                target_status = "verified_success"
            elif status_filter == "failed":
                target_status = "verified_failed"

            # 优化：使用迭代器逐行处理，避免一次性加载所有记录到内存
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    line_count += 1
                    line = line.strip()
                    if not line:
                        continue  # 跳过空行

                    try:
                        record = json.loads(line)

                        # 自动标记过期的验证码
                        # 如果状态是 'created' 且已经超过30分钟，自动标记为 'expired'
                        if record.get("status") == "created":
                            timestamp = record.get("timestamp", 0)
                            if current_time - timestamp > expiry_threshold:
                                record["status"] = "expired"
                                record["expired_at"] = timestamp + expiry_threshold
                                record["expired_at_readable"] = (
                                    datetime.datetime.fromtimestamp(
                                        timestamp + expiry_threshold
                                    ).strftime("%Y-%m-%d %H:%M:%S")
                                )

                        # 状态过滤 (修正：处理 'all' 和状态映射)
                        if status_filter and status_filter != "all":
                            if record.get("status") != target_status:
                                continue

                        total_matched += 1

                        # 移除敏感信息
                        record.pop("session_id", None)
                        records.append(record)
                    except Exception as e:
                        logging.warning(f"[验证码历史] 解析记录失败: {e}")
                        continue

            # 按时间戳倒序排列（最新的在前）
            # 优化：如果记录数超过limit * 2，使用heapq.nlargest进行高效选择
            if len(records) > limit * 2:
                records = heapq.nlargest(
                    limit * 2, records, key=lambda x: x.get("timestamp", 0)
                )
            else:
                records.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

            # 修正：使用 total_matched 作为总数
            total = total_matched

            # 限制返回数量（最多100条）
            records = records[:limit]

            logging.info(
                f"[验证码历史] 管理员 {username} 查询验证码历史: 日期={date_str}, 返回={len(records)}条 (总计={total}条)"
            )

            # 后台任务：永久标记过期的验证码（异步更新历史文件）
            def update_expired_captchas_in_history():
                try:
                    if not os.path.exists(history_file):
                        return

                    # 读取所有记录
                    lines = []
                    updated_count = 0
                    current_time = time.time()
                    expiry_threshold = 30 * 60  # 30分钟

                    with open(history_file, "r", encoding="utf-8") as f:
                        for line in f:
                            try:
                                record = json.loads(line.strip())
                                # 如果状态是 'created' 且已经超过30分钟，永久标记为 'expired'
                                if record.get("status") == "created":
                                    timestamp = record.get("timestamp", 0)
                                    if current_time - timestamp > expiry_threshold:
                                        record["status"] = "expired"
                                        record["expired_at"] = (
                                            timestamp + expiry_threshold
                                        )
                                        record["expired_at_readable"] = (
                                            datetime.datetime.fromtimestamp(
                                                timestamp + expiry_threshold
                                            ).strftime("%Y-%m-%d %H:%M:%S")
                                        )
                                        updated_count += 1
                                lines.append(
                                    json.dumps(record, ensure_ascii=False) + "\n"
                                )
                            except:
                                lines.append(line)  # 保留原始行

                    # 如果有更新，写回文件
                    if updated_count > 0:
                        with open(history_file, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        logging.info(
                            f"[验证码历史] 已永久标记 {updated_count} 个过期验证码: {date_str}"
                        )
                except Exception as e:
                    logging.error(f"[验证码历史] 更新过期验证码状态失败: {e}")

            # 在后台线程中更新历史文件
            import threading

            threading.Thread(
                target=update_expired_captchas_in_history, daemon=True
            ).start()

            return jsonify(
                {
                    "success": True,
                    "data": records,
                    "total": total,  # 此时 'total' 变量已定义
                    "date": date_str,
                }
            )

        except Exception as e:
            logging.error(f"[验证码历史] 获取历史记录失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": "获取验证码历史失败"}), 500

    # ============================================================
    # 修正：验证码详情API
    # 用于根据ID获取单个验证码的详细信息
    # ============================================================
    @app.route("/api/captcha/detail/<captcha_id>", methods=["GET"])
    @login_required
    def get_captcha_detail(captcha_id):
        """
        获取单个验证码的详细信息

        权限要求：管理员 (view_captcha_history)
        """
        try:
            # 1. 权限检查
            if not auth_system.check_permission(g.user, "view_captcha_history"):
                return jsonify({"success": False, "message": "权限不足"}), 403

            # 2. 验证 captcha_id (防止路径遍历)
            if not captcha_id or ".." in captcha_id or "/" in captcha_id:
                return jsonify({"success": False, "message": "无效的验证码ID"}), 400

            # 3. 遍历所有历史文件查找该ID
            # 使用全局 LOGIN_LOGS_DIR
            history_dir = os.path.join(LOGIN_LOGS_DIR, "captcha_history")
            if not os.path.exists(history_dir):
                return (
                    jsonify({"success": False, "message": "验证码历史目录不存在"}),
                    404,
                )

            found_record = None
            current_time = time.time()
            expiry_threshold = 30 * 60  # 30分钟

            # 遍历目录中的所有 .jsonl 文件
            for filename in os.listdir(history_dir):
                if filename.endswith(".jsonl"):
                    history_file = os.path.join(history_dir, filename)
                    try:
                        with open(history_file, "r", encoding="utf-8") as f:
                            for line in f:
                                try:
                                    record = json.loads(line.strip())
                                    if record.get("captcha_id") == captcha_id:
                                        # 找到了！
                                        found_record = record

                                        # 自动标记过期的验证码
                                        if record.get("status") == "created":
                                            timestamp = record.get("timestamp", 0)
                                            if (
                                                current_time - timestamp
                                                > expiry_threshold
                                            ):
                                                found_record["status"] = "expired"
                                                found_record["expired_at"] = (
                                                    timestamp + expiry_threshold
                                                )
                                                found_record["expired_at_readable"] = (
                                                    datetime.datetime.fromtimestamp(
                                                        timestamp + expiry_threshold
                                                    ).strftime("%Y-%m-%d %H:%M:%S")
                                                )

                                        # 移除敏感信息 (如果需要)
                                        found_record.pop("session_id", None)

                                        # 返回成功响应
                                        return jsonify(
                                            {"success": True, "data": found_record}
                                        )
                                except json.JSONDecodeError:
                                    continue  # 跳过损坏的行
                    except (IOError, OSError) as e:
                        logging.warning(
                            f"[验证码详情] 读取历史文件 {filename} 失败: {e}"
                        )
                        continue  # 继续查找下一个文件

            # 4. 如果遍历完所有文件都未找到
            if not found_record:
                return (
                    jsonify({"success": False, "message": "未找到该验证码的详细信息"}),
                    404,
                )

        except Exception as e:
            logging.error(f"[验证码详情] 获取详情失败: {e}", exc_info=True)
            return (
                jsonify({"success": False, "message": "获取验证码详情时发生错误"}),
                500,
            )

    # ========================================
    # 【本地验证码】新增API端点
    # ========================================

    @app.route("/api/captcha/save_settings", methods=["POST"])
    @login_required
    def save_captcha_settings():
        """
        【本地验证码】保存验证码生成器设置到config.ini

        权限要求：管理员 (modify_config)

        功能说明:
            - 将验证码生成参数（length, scale_factor, noise_level）保存到config.ini的[Captcha]节
            - 参数会经过严格的范围验证，防止无效或危险的配置
            - 保存后立即生效，下次生成验证码时使用新参数

        请求格式 (JSON):
            {
                "length": 4,           # 验证码字符数（3-6）
                "scale_factor": 2,     # 像素细分倍数（2-4）
                "noise_level": 0.08    # 噪点比例（0.0-0.3）
            }

        返回格式:
            {
                "success": True/False,
                "message": "设置保存成功" / "错误信息"
            }

        安全说明:
            - 只有管理员才能修改验证码设置
            - 所有参数都会进行范围检查，防止异常值
            - 使用_write_config_with_comments保存，保留注释
        """
        try:
            # ========================================
            # 1. 权限检查：只有管理员可以修改验证码设置
            # ========================================
            if not auth_system.check_permission(g.user, "modify_config"):
                logging.warning(
                    f"【本地验证码】用户 {g.user} 尝试保存验证码设置但权限不足"
                )
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "权限不足：只有管理员可以修改验证码设置",
                        }
                    ),
                    403,
                )

            # ========================================
            # 2. 解析请求数据
            # ========================================
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "请求数据为空"}), 400

            # ========================================
            # 3. 提取并验证参数
            # ========================================
            # 提取参数，如果不存在则使用默认值
            try:
                length = int(data.get("length", 4))
                scale_factor = int(data.get("scale_factor", 2))
                noise_level = float(data.get("noise_level", 0.08))
            except (ValueError, TypeError) as e:
                logging.error(f"【本地验证码】参数类型转换失败: {e}")
                return (
                    jsonify({"success": False, "message": f"参数类型错误: {str(e)}"}),
                    400,
                )

            # 参数范围检查（防止异常值导致验证码生成失败或性能问题）
            if not (3 <= length <= 6):
                return (
                    jsonify({"success": False, "message": "验证码长度必须在3-6之间"}),
                    400,
                )

            if not (2 <= scale_factor <= 4):
                return (
                    jsonify({"success": False, "message": "细分倍数必须在2-4之间"}),
                    400,
                )

            if not (0 <= noise_level <= 0.3):
                return (
                    jsonify({"success": False, "message": "噪点比例必须在0.0-0.3之间"}),
                    400,
                )

            logging.info(
                f"【本地验证码】用户 {g.user} 请求保存验证码设置: length={length}, scale_factor={scale_factor}, noise_level={noise_level}"
            )

            # ========================================
            # 4. 读取现有配置文件
            # ========================================
            config_file = "config.ini"
            config = configparser.ConfigParser()

            # 如果配置文件存在，先读取现有配置
            if os.path.exists(config_file):
                config.read(config_file, encoding="utf-8")

            # ========================================
            # 5. 确保[Captcha]节存在
            # ========================================
            # 如果[Captcha]节不存在（旧版本配置文件），则创建它
            if not config.has_section("Captcha"):
                config.add_section("Captcha")
                logging.debug("【本地验证码】[Captcha]节不存在，已创建")

            # ========================================
            # 6. 更新配置值
            # ========================================
            config.set("Captcha", "length", str(length))
            config.set("Captcha", "scale_factor", str(scale_factor))
            config.set("Captcha", "noise_level", str(noise_level))

            _write_config_with_comments(config, config_file)

            logging.info(f"【本地验证码】验证码设置已成功保存到 {config_file}")

            # ========================================
            # 8. 返回成功响应
            # ========================================
            return jsonify({"success": True, "message": "验证码设置保存成功"})

        except Exception as e:
            # 捕获所有未预期的异常，防止服务器崩溃
            logging.error(f"【本地验证码】保存验证码设置失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"保存失败: {str(e)}"}), 500

    @app.route("/api/captcha/test_generate", methods=["POST"])
    @login_required
    def test_generate_captcha():
        """
        【本地验证码】测试生成验证码（用于预览效果）
        """
        try:
            # ========================================
            # 1. 权限检查：只有管理员可以测试生成验证码
            # ========================================
            if not auth_system.check_permission(g.user, "modify_config"):
                logging.warning(
                    f"【本地验证码】用户 {g.user} 尝试测试生成验证码但权限不足"
                )
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "权限不足：只有管理员可以测试验证码",
                        }
                    ),
                    403,
                )

            # ========================================
            # 2. 导入本地验证码生成器
            # ========================================
            # 使用全局定义的 MicroPixelCaptcha (支持 Fallback)
            # from get_captchas import MicroPixelCaptcha # 不需要再次导入
            pass

            # ========================================
            # 3. 解析请求数据
            # ========================================
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "请求数据为空"}), 400

            # ========================================
            # 4. 提取并验证参数
            # ========================================
            # 提取参数，如果不存在则使用默认值
            try:
                length = int(data.get("length", 4))
                scale_factor = int(data.get("scale_factor", 2))
                noise_level = float(data.get("noise_level", 0.08))
            except (ValueError, TypeError) as e:
                logging.error(f"【本地验证码】测试生成时参数类型转换失败: {e}")
                return (
                    jsonify({"success": False, "message": f"参数类型错误: {str(e)}"}),
                    400,
                )

            # 参数范围检查（防止异常值导致生成失败）
            if not (3 <= length <= 6):
                return (
                    jsonify({"success": False, "message": "验证码长度必须在3-6之间"}),
                    400,
                )

            if not (2 <= scale_factor <= 4):
                return (
                    jsonify({"success": False, "message": "细分倍数必须在2-4之间"}),
                    400,
                )

            if not (0 <= noise_level <= 0.3):
                return (
                    jsonify({"success": False, "message": "噪点比例必须在0.0-0.3之间"}),
                    400,
                )

            logging.info(
                f"【本地验证码】用户 {g.user} 测试生成验证码: length={length}, scale_factor={scale_factor}, noise_level={noise_level}"
            )

            # ========================================
            # 5. 生成验证码
            # ========================================
            # 创建验证码生成器实例
            generator = MicroPixelCaptcha()

            # 调用generate方法生成验证码
            # 返回: (验证码答案, 验证码HTML, 宽度, 高度)
            code, html, width, height = generator.generate(
                length=length, scale_factor=scale_factor, noise_level=noise_level
            )

            logging.debug(
                f"【本地验证码】测试验证码生成成功: code={code}, html_length={len(html)}, size={width}x{height}"
            )

            # ========================================
            # 5.1 保存到文件及历史记录 (新增逻辑)
            # ========================================
            import uuid

            captcha_id = str(uuid.uuid4())

            # 1. 保存验证码数据文件 (供iframe读取)
            captchas_dir = os.path.join(LOGIN_LOGS_DIR, "captchas")
            os.makedirs(captchas_dir, exist_ok=True)

            captcha_data = {
                "id": captcha_id,
                "code": code.upper(),
                "html": html,
                "session_id": request.headers.get("X-Session-ID", "test_session"),
                "timestamp": time.time(),
                "expires_at": time.time() + 600,  # 10分钟后过期
            }

            captcha_file = os.path.join(captchas_dir, f"{captcha_id}.json")
            with open(captcha_file, "w", encoding="utf-8") as f:
                json.dump(captcha_data, f, indent=2, ensure_ascii=False)

            # 2. 记录到历史记录文件 (供管理员查看)
            try:
                history_dir = os.path.join(LOGIN_LOGS_DIR, "captcha_history")
                os.makedirs(history_dir, exist_ok=True)

                date_str = datetime.datetime.now().strftime("%Y%m%d")
                history_file = os.path.join(
                    history_dir, f"captcha_history_{date_str}.jsonl"
                )

                history_entry = {
                    "captcha_id": captcha_id,
                    "code": code.upper(),
                    "html": html,
                    "session_id": request.headers.get("X-Session-ID", "unknown"),
                    "client_ip": request.headers.get(
                        "X-Forwarded-For", request.remote_addr
                    ),
                    "user_agent": request.headers.get("User-Agent", "unknown"),
                    "timestamp": time.time(),
                    "timestamp_readable": datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "expires_at": time.time() + 600,
                    "status": "test_generated",  # 特殊状态：测试生成
                    "verified_at": None,
                    "verified_input": None,
                }

                with open(history_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(history_entry, ensure_ascii=False) + "\n")

                logging.info(f"【本地验证码】测试记录已保存: ID={captcha_id}")
            except Exception as e:
                logging.error(f"【本地验证码】保存测试历史失败: {e}")

            # ========================================
            # 6. 返回成功响应
            # ========================================
            # 注意：code仅用于测试预览，实际使用时不应返回
            return jsonify(
                {
                    "success": True,
                    "code": code,  # 验证码答案（仅用于测试预览）
                    "html": html,  # 验证码HTML（保留用于兼容）
                    "captcha_id": captcha_id,  # 返回ID供iframe使用
                    "width": width,  # 验证码宽度（像素）
                    "height": height,  # 验证码高度（像素）
                    "message": "验证码生成成功",
                }
            )

        except ImportError as e:
            # 如果get_captchas.py文件不存在或MicroPixelCaptcha类不存在
            logging.error(
                f"【本地验证码】导入MicroPixelCaptcha失败: {e}", exc_info=True
            )
            return (
                jsonify({"success": False, "message": f"验证码生成器不可用: {str(e)}"}),
                500,
            )

        except Exception as e:
            # 捕获所有未预期的异常，防止服务器崩溃
            logging.error(f"【本地验证码】测试生成验证码失败: {e}", exc_info=True)
            return jsonify({"success": False, "message": f"生成失败: {str(e)}"}), 500

    @app.route("/health")
    def health():
        """
        健康检查端点（已增强）

        功能说明：
        - 提供服务器的健康状态和运行统计信息
        - 用于监控系统、负载均衡器或运维人员检查服务是否正常

        返回的信息包括：
        1. status: 服务器状态（ok表示正常）
        2. uptime_seconds: 服务器运行秒数（原始数值）
        3. uptime_formatted: 服务器运行时间（人类可读格式，如"2天3小时15分钟"）
        4. active_memory_sessions: 活跃的内存会话数
        5. active_background_tasks: 活跃的后台任务数
        6. current_thread_chrome_contexts: 当前线程的Chrome上下文数
        7. response_time_ms: 请求响应延迟（毫秒）
        """

        # ========== 记录请求开始时间（用于计算响应延迟） ==========
        request_start_time = time.time()

        # ========== 计算服务器运行时间 ==========
        # 获取当前时间戳
        current_time = time.time()

        # 计算运行时长（秒）
        # 如果 server_start_time 未定义（理论上不应该发生），则默认为0
        uptime_seconds = (
            current_time - server_start_time if "server_start_time" in globals() else 0
        )

        # 将运行时长转换为人类可读格式
        # 例如："2天3小时15分钟30秒"
        def format_uptime(seconds):
            """
            将秒数转换为人类可读的时间格式。

            参数:
                seconds: 总秒数

            返回:
                格式化的字符串，如 "2天3小时15分钟30秒"
            """
            # 计算天数：1天 = 86400秒
            days = int(seconds // 86400)
            seconds %= 86400  # 取余数，剩余不足一天的秒数

            # 计算小时数：1小时 = 3600秒
            hours = int(seconds // 3600)
            seconds %= 3600  # 取余数，剩余不足一小时的秒数

            # 计算分钟数：1分钟 = 60秒
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)  # 剩余秒数

            # 构建格式化字符串
            # 只显示非零的时间单位，避免冗余（如 "0天0小时5分钟"）
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0:
                parts.append(f"{hours}小时")
            if minutes > 0:
                parts.append(f"{minutes}分钟")
            if seconds > 0 or len(parts) == 0:  # 如果所有单位都是0，至少显示"0秒"
                parts.append(f"{seconds}秒")

            return "".join(parts)

        uptime_formatted = format_uptime(uptime_seconds)

        # ========== 获取活跃会话数 ==========
        # 从全局变量 web_sessions 获取当前活跃的会话数
        # 注意：原代码中减1可能是为了排除某个特殊会话（如管理员会话）
        # 这里保持一致，减1
        active_sessions = len(web_sessions) - 1 if web_sessions else 0
        # 确保不出现负数
        active_sessions = max(0, active_sessions)

        # ========== 获取后台任务数 ==========
        # 从后台任务管理器获取当前活跃的任务数
        active_tasks = 0
        if background_task_manager:
            # 使用线程锁保护，确保线程安全
            with background_task_manager.lock:
                # background_task_manager.tasks 是一个字典，存储所有任务
                active_tasks = len(background_task_manager.tasks)

        # ========== 获取Chrome上下文数（线程安全） ==========
        # Chrome上下文数表示当前有多少个浏览器实例在运行
        # 注意：这只显示当前工作线程的上下文数量，而不是全局总数
        contexts_count = 0
        if chrome_pool and hasattr(chrome_pool, "thread_local"):
            # 使用 getattr 安全访问，如果 'contexts' 尚未在当前线程创建，则返回空字典 {}
            contexts_count = len(getattr(chrome_pool.thread_local, "contexts", {}))

        # ========== 计算响应延迟 ==========
        # 记录请求处理完成的时间
        request_end_time = time.time()
        # 计算响应延迟（毫秒）
        response_time_ms = round((request_end_time - request_start_time) * 1000, 2)

        # ========== 返回健康检查信息 ==========
        return jsonify(
            {
                "status": "ok",  # 服务器状态：正常
                "uptime_seconds": int(uptime_seconds),  # 运行秒数（整数）
                "uptime_formatted": uptime_formatted,  # 运行时间（格式化）
                "active_memory_sessions": active_sessions,  # 活跃会话数
                "active_background_tasks": active_tasks,  # 活跃后台任务数
                "current_thread_chrome_contexts": contexts_count,  # 当前线程Chrome上下文数
                "response_time_ms": response_time_ms,  # 响应延迟（毫秒）
            }
        )

    @socketio.on("connect")
    def handle_connect():
        # 前端 JS 连接时会触发
        # 从请求头或 cookie 中获取 session_id (这取决于前端如何发送)
        # 假设前端通过 cookie 或查询参数传递 session_id
        session_id = request.args.get("session_id") or request.cookies.get(
            "session_id_cookie"
        )  # 示例，需要前端配合
        if not session_id:
            # 或者从 Flask session 获取，如果使用了 Flask-Session
            session_id = session.get("session_id")

        # 更可靠的方式: 让前端在连接后立即发送一个带有 session_id 的 'join' 事件
        logging.info(f"WebSocket 客户端连接: {request.sid}")
        # 注意：此时还不知道是哪个 session_id，等待前端发送 'join' 事件

    @socketio.on("join")
    def handle_join(data):
        # 【修复】增强健壮性：处理 data 可能为字符串的情况
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                logging.warning(
                    f"WebSocket 'join' 事件数据解析失败: {e}, 原始数据: {data}"
                )
                return

        # 确保 data 是字典类型
        if not isinstance(data, dict):
            logging.warning(f"WebSocket 'join' 接收到无效数据类型: {type(data)}")
            return

        session_id = data.get("session_id")
        if session_id:
            # 将当前 WebSocket 连接加入以 session_id 命名的房间
            join_room(session_id)
            logging.info(f"WebSocket 客户端 {request.sid} 成功加入 {session_id}")
            # 可以选择性地在这里发送一条欢迎消息
            emit("log_message", {"msg": "WebSocket 连接成功！"}, room=session_id)
        else:
            logging.warning(
                f"WebSocket 客户端 {request.sid} 加入房间失败：缺少 session_id。"
            )

    @socketio.on("disconnect")
    def handle_disconnect():
        logging.info(f"WebSocket 客户端断开连接: {request.sid}")

    # 辅助函数，用于向指定会话推送验证码列表更新
    def _emit_verification_codes_update(session_id):
        """辅助函数：向指定会话推送验证码列表更新事件"""
        if not session_id or not socketio:
            logging.debug(
                f"[SocketIO] 跳过 'verification_codes_updated' 推送（缺少 session_id 或 socketio）"
            )
            return
        try:
            socketio.emit("verification_codes_updated", {}, room=session_id)
            logging.debug(
                f"[SocketIO] 已向会话 {session_id[:8]}... 推送 'verification_codes_updated' 事件"
            )
        except Exception as e:
            logging.error(f"[SocketIO] 推送 'verification_codes_updated' 失败: {e}")

    # 定期清理过期会话

    def cleanup_sessions():
        """定期清理超过24小时无活动的会话，并强制执行内存会话数量限制"""
        while True:
            time.sleep(3600)  # 每小时检查一次
            try:
                current_time = time.time()
                expired_sessions = []

                with web_sessions_lock:
                    # 识别过期会话（24小时无活动）
                    for session_id in list(web_sessions.keys()):
                        with session_activity_lock:
                            last_activity = session_activity.get(session_id, 0)
                            if current_time - last_activity > 86400:  # 24小时 = 86400秒
                                expired_sessions.append(session_id)

                    # 内存优化：如果会话数减去已过期会话后仍超过限制，清理最旧的会话
                    remaining_sessions = len(web_sessions) - len(expired_sessions)
                    if remaining_sessions > MAX_MEMORY_SESSIONS:
                        # 按最后活动时间排序，清理最旧的会话
                        with session_activity_lock:
                            # 只考虑未过期的会话
                            active_sessions = [
                                sid
                                for sid in web_sessions.keys()
                                if sid not in expired_sessions
                            ]
                            sorted_sessions = sorted(
                                active_sessions,
                                key=lambda sid: session_activity.get(sid, 0),
                            )
                            # 清理超出限制的会话（保留最新的MAX_MEMORY_SESSIONS个）
                            sessions_to_remove = (
                                remaining_sessions - MAX_MEMORY_SESSIONS
                            )
                            for session_id in sorted_sessions[:sessions_to_remove]:
                                expired_sessions.append(session_id)
                        logging.warning(
                            f"[会话清理] 内存会话数超过限制({MAX_MEMORY_SESSIONS})，额外清理了 {sessions_to_remove} 个最旧会话"
                        )

                    # 清理过期会话
                    for session_id in expired_sessions:
                        try:
                            # 清理Chrome上下文
                            if chrome_pool:
                                chrome_pool.cleanup_context(session_id)

                            # 从内存中移除会话
                            if session_id in web_sessions:
                                del web_sessions[session_id]

                            with session_activity_lock:
                                if session_id in session_activity:
                                    del session_activity[session_id]

                            # Note: session_file_locks cleanup is handled separately
                            # as it uses session hash as key, not session_id directly

                            logging.info(f"[会话清理] 已清理会话: {session_id[:8]}...")
                        except Exception as e:
                            logging.error(
                                f"[会话清理] 清理会话 {session_id[:8]}... 时出错: {e}"
                            )

                if expired_sessions:
                    logging.info(
                        f"[会话清理] 本次清理了 {len(expired_sessions)} 个会话"
                    )
                    # 强制垃圾回收以释放内存
                    gc.collect()
                else:
                    # 即使没有过期会话，也记录当前会话数量
                    with web_sessions_lock:
                        logging.debug(
                            f"[会话清理] 当前内存会话数: {len(web_sessions)}/{MAX_MEMORY_SESSIONS}"
                        )
            except Exception as e:
                logging.error(f"[会话清理] 清理过程出错: {e}", exc_info=True)

    cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
    cleanup_thread.start()

    # 加载持久化会话
    logging.info("正在加载持久化会话...")
    load_all_sessions(args)

    # 启动会话监控线程
    logging.info("正在启动会话监控...")
    start_session_monitor()

    # 扫描 .ini 文件，为已配置的账号启动服务
    # 这必须在加载会话之后，但在启动Web服务器（阻塞）之前
    try:
        start_background_auto_attendance(args)
    except Exception as e:
        logging.error(f"启动后台自动签到服务失败: {e}", exc_info=True)

    cleaned_sessions_count = 0
    with web_sessions_lock:
        for session_id, api_instance in web_sessions.items():
            try:
                # 强制设置所有停止标志为 True (停止状态)
                if hasattr(api_instance, "stop_run_flag") and isinstance(
                    api_instance.stop_run_flag, threading.Event
                ):
                    api_instance.stop_run_flag.set()
                if hasattr(api_instance, "multi_run_stop_flag") and isinstance(
                    api_instance.multi_run_stop_flag, threading.Event
                ):
                    api_instance.multi_run_stop_flag.set()
                if hasattr(api_instance, "stop_auto_refresh") and isinstance(
                    api_instance.stop_auto_refresh, threading.Event
                ):
                    api_instance.stop_auto_refresh.set()
                if hasattr(api_instance, "stop_multi_auto_refresh") and isinstance(
                    api_instance.stop_multi_auto_refresh, threading.Event
                ):
                    api_instance.stop_multi_auto_refresh.set()

                # 如果是多账号模式，也停止所有子账号的事件
                if getattr(api_instance, "is_multi_account_mode", False) and hasattr(
                    api_instance, "accounts"
                ):
                    for acc in api_instance.accounts.values():
                        if hasattr(acc, "stop_event") and isinstance(
                            acc.stop_event, threading.Event
                        ):
                            acc.stop_event.set()
                        # 清理可能存在的 worker_thread 引用（线程已不存在）
                        acc.worker_thread = None
                        # 重置状态文本为待命（如果不是错误状态）
                        if not api_instance._should_preserve_status(
                            acc.status_text, "待命"
                        ):
                            acc.status_text = "待命"

                # 清理 Api 实例可能残留的 worker thread 引用
                if hasattr(api_instance, "auto_refresh_thread"):
                    api_instance.auto_refresh_thread = None
                if hasattr(api_instance, "multi_auto_refresh_thread"):
                    api_instance.multi_auto_refresh_thread = None

                # 重置单账号进度
                api_instance.current_run_idx = -1
                api_instance._first_center_done = False

                cleaned_sessions_count += 1
            except Exception as e:
                logging.error(f"重置会话 {session_id[:8]}... 状态时出错: {e}")

    logging.info(f"已重置 {cleaned_sessions_count} 个会话的运行状态标志。")

    logging.info("正在检查并修正持久化的后台任务状态...")
    interrupted_task_files = 0
    if background_task_manager and os.path.exists(
        background_task_manager.task_storage_dir
    ):
        try:
            for filename in os.listdir(background_task_manager.task_storage_dir):
                # 只处理该管理器的JSON状态文件
                if filename.endswith(".json"):
                    filepath = os.path.join(
                        background_task_manager.task_storage_dir, filename
                    )
                    try:
                        # 读取-修改-写回，需要独占访问（使用文件锁或确保单线程启动）
                        # 这里假设启动阶段是单线程的，直接读写
                        task_state = None
                        with open(filepath, "r", encoding="utf-8") as f:
                            task_state = json.load(f)

                        # 如果状态是 'running'，则修改为 'stopped' 并添加原因
                        if task_state and task_state.get("status") == "running":
                            # 或者 'interrupted' 更准确
                            task_state["status"] = "stopped"
                            task_state["error"] = "程序意外重启导致任务中断。"
                            task_state["last_update"] = time.time()  # 更新时间戳

                            # 写回文件
                            with open(filepath, "w", encoding="utf-8") as f:
                                json.dump(task_state, f, indent=2, ensure_ascii=False)
                            interrupted_task_files += 1
                            logging.debug(
                                f"已将持久化的后台任务 {filename} 状态修正为 stopped。"
                            )

                    except (IOError, json.JSONDecodeError) as e:
                        logging.warning(
                            f"处理后台任务状态文件 {filename} 时出错: {e}，跳过此文件。"
                        )
                    except Exception as e:  # 捕获其他可能的错误
                        logging.error(
                            f"更新后台任务状态文件 {filename} 时发生意外错误: {e}",
                            exc_info=True,
                        )

            if interrupted_task_files > 0:
                logging.info(
                    f"已修正 {interrupted_task_files} 个持久化的 'running' 后台任务状态为 stopped。"
                )
            else:
                logging.info("未发现需要修正状态的持久化后台任务文件。")
        except Exception as e:
            logging.error(f"检查持久化后台任务状态时发生错误: {e}", exc_info=True)
    else:
        logging.info("后台任务管理器未初始化或存储目录不存在，跳过持久化状态检查。")

    # # 清理后台任务管理器的内存状态（但不删除持久化文件）
    if background_task_manager:
        with background_task_manager.lock:
            initial_task_count = len(background_task_manager.tasks)
            background_task_manager.tasks.clear()
            logging.info(
                f"已清空后台任务管理器的内存状态（清理了 {initial_task_count} 个任务记录）。"
            )

    # ============================================================================
    # SSL/HTTPS 配置加载和验证
    # 在启动服务器之前，加载SSL配置并验证证书（如果启用了SSL）
    # ============================================================================

    # 加载SSL配置
    # 从config.ini文件读取SSL相关设置
    ssl_config = load_ssl_config()

    # 定义SSL上下文变量，用于存储SSL配置
    # 如果不启用SSL，此值为None
    ssl_context = None
    cert_path = None
    key_path = None

    # 如果启用了SSL，进行证书验证和SSL上下文创建
    if ssl_config["ssl_enabled"]:
        logging.info("检测到SSL已启用，正在验证证书文件...")

        # 验证证书文件和密钥文件
        # validate_ssl_certificate函数会检查文件是否存在、可读、格式正确等
        is_valid, error_msg, cert_info = validate_ssl_certificate(
            ssl_config["ssl_cert_path"], ssl_config["ssl_key_path"]
        )

        if not is_valid:
            # 如果证书验证失败，记录错误并退出程序
            # 这是为了防止使用无效证书导致安全问题
            print(f"\n{'='*60}")
            print(f"错误: SSL证书验证失败")
            print(f"")
            print(f"原因: {error_msg}")
            print(f"")
            print(f"请检查以下内容：")
            print(f"  1. 证书文件路径是否正确")
            print(f"  2. 证书文件是否存在且可读")
            print(f"  3. 证书文件格式是否为PEM格式")
            print(f"  4. 证书和密钥是否匹配")
            print(f"")
            print(f"配置文件位置: config.ini")
            print(f"证书路径: {ssl_config['ssl_cert_path']}")
            print(f"密钥路径: {ssl_config['ssl_key_path']}")
            print(f"{'='*60}\n")
            logging.error(f"SSL证书验证失败，程序退出: {error_msg}")
            sys.exit(1)

        # 证书验证通过，创建SSL上下文
        try:
            import ssl as ssl_module

            # 创建SSL上下文，使用TLS协议
            # PROTOCOL_TLS_SERVER会自动选择最安全的TLS版本
            ssl_context = ssl_module.SSLContext(ssl_module.PROTOCOL_TLS_SERVER)

            # 加载证书链和私钥
            # 如果路径是相对路径，需要转换为绝对路径
            cert_path = ssl_config["ssl_cert_path"]
            key_path = ssl_config["ssl_key_path"]

            if not os.path.isabs(cert_path):
                cert_path = os.path.join(os.path.dirname(__file__), cert_path)
            if not os.path.isabs(key_path):
                key_path = os.path.join(os.path.dirname(__file__), key_path)

            # 加载证书和密钥到SSL上下文
            ssl_context.load_cert_chain(cert_path, key_path)

            # 设置SSL选项，禁用不安全的协议版本
            # OP_NO_SSLv2 和 OP_NO_SSLv3 禁用旧版SSL协议
            # OP_NO_TLSv1 和 OP_NO_TLSv1_1 禁用旧版TLS协议（可选）
            ssl_context.options |= ssl_module.OP_NO_SSLv2
            ssl_context.options |= ssl_module.OP_NO_SSLv3
            # ssl_context.options |= ssl_module.OP_NO_TLSv1
            # ssl_context.options |= ssl_module.OP_NO_TLSv1_1

            logging.info(f"SSL上下文创建成功，使用证书: {cert_path}")
            print(f"✓ SSL/HTTPS 已启用")
            print(f"  证书文件: {cert_path}")
            print(f"  密钥文件: {key_path}")
            if ssl_config["https_only"]:
                print(f"  ⚠ 仅HTTPS模式: 已启用（HTTP请求将被重定向）")

        except Exception as e:
            # 如果创建SSL上下文失败，记录错误并退出
            print(f"\n{'='*60}")
            print(f"错误: 创建SSL上下文失败")
            print(f"")
            print(f"详细信息: {e}")
            print(f"")
            print(f"可能的原因：")
            print(f"  1. 证书和密钥不匹配")
            print(f"  2. 证书或密钥文件损坏")
            print(f"  3. Python SSL模块配置问题")
            print(f"{'='*60}\n")
            logging.error(f"创建SSL上下文失败: {e}", exc_info=True)
            sys.exit(1)
    else:
        # SSL未启用，使用HTTP模式
        logging.info("SSL未启用，服务器将以HTTP模式运行")

    # ============================================================================
    # 添加请求钩子：处理X-Forwarded-*头和HTTPS重定向
    # 这些钩子在每个请求处理之前执行
    # ============================================================================

    @app.before_request
    def handle_forwarded_proto():
        """
        处理反向代理（如Nginx）转发的请求头。

        功能说明：
        1. 检查X-Forwarded-Proto头，识别原始请求是HTTP还是HTTPS
        2. 检查X-Forwarded-For头，获取真实客户端IP
        3. 如果启用了https_only模式且检测到HTTP请求，重定向到HTTPS

        这个函数在每个请求处理之前自动执行。
        """
        # 1. 处理X-Forwarded-Proto头
        # 当使用Nginx等反向代理时，实际的请求协议（HTTP/HTTPS）会通过此头传递
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "")

        # 2. 处理X-Forwarded-For头
        # 获取真实的客户端IP地址（当使用代理时）
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            # X-Forwarded-For可能包含多个IP（逗号分隔），取第一个
            real_ip = forwarded_for.split(",")[0].strip()
            # 将真实IP存储到request对象，供其他路由使用
            request.environ["REMOTE_ADDR"] = real_ip

        # 3. HTTPS重定向逻辑（仅在启用https_only模式时）
        if ssl_config.get("https_only", False) and ssl_config.get("ssl_enabled", False):
            # 检查请求是否通过HTTP协议
            # [修正] 解决无限重定向问题：
            # 如果没有反向代理头(forwarded_proto为空)，说明是直连。
            # 在本程序的架构中，底层的 DualProtocolSocket 已经拦截了非SSL的直连请求。
            # 因此，能到达这里的直连请求必然是HTTPS。即便 request.is_secure 为 False (WSGI环境误判)，我们也强制认定为安全。
            if not forwarded_proto:
                is_https = True
            else:
                # 如果有代理头，则信赖代理头或 Flask 的判断
                is_https = request.is_secure or forwarded_proto.lower() == "https"

            if not is_https:
                # 如果是HTTP请求，构造HTTPS URL并重定向
                # 排除某些特殊路径（如健康检查）不进行重定向
                # [修正] 必须排除 /socket.io，否则握手时的 POST 请求会被重定向导致 xhr post error
                excluded_paths = ["/health", "/api/health", "/socket.io"]
                
                # 检查当前路径是否以排除列表中的任何一项开头 (兼容 /socket.io/...)
                should_redirect = True
                for path in excluded_paths:
                    if request.path.startswith(path):
                        should_redirect = False
                        break

                if should_redirect:
                    # 构造HTTPS URL
                    url = request.url.replace("http://", "https://", 1)
                    logging.info(f"HTTP请求被重定向到HTTPS: {request.url} -> {url}")
                    # 返回301永久重定向
                    from flask import redirect

                    return redirect(url, code=301)

                    return redirect(url, code=301)

    @app.after_request
    def add_security_headers(response):
        """
        为所有响应添加安全相关的HTTP头。
        """
        # 1. 添加HSTS头（仅在启用SSL时）
        # HSTS告诉浏览器在指定时间内，该域名只能通过HTTPS访问
        if ssl_config.get("ssl_enabled", False):
            # max-age=31536000: 一年内强制使用HTTPS
            # includeSubDomains: 该策略也适用于所有子域名
            # preload: 允许加入HSTS预加载列表
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # 2. 防止MIME类型嗅探
        # 这可以防止浏览器错误地将非可执行MIME类型作为可执行内容
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 3. 防止点击劫持（Clickjacking）
        # SAMEORIGIN表示页面只能被同源页面嵌入frame/iframe
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # 4. 启用XSS防护
        # 1; mode=block表示检测到XSS攻击时阻止页面加载
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 5. Referrer策略
        # strict-origin-when-cross-origin: 同源请求发送完整referer，跨域只发送origin
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 6. 内容安全策略（可选，较为严格）
        # 这里注释掉，因为可能会影响现有功能，可以根据需要启用
        # response.headers['Content-Security-Policy'] = "default-src 'self'"

        return response

    # ============================================================================
    # 启动服务器
    # 根据SSL配置选择HTTP或HTTPS模式
    # ============================================================================

    # 确定服务器协议和访问地址
    protocol = "https" if ssl_config.get("ssl_enabled", False) else "http"
    server_url = f"{protocol}://{args.host}:{args.port}"

    # 打印启动信息
    print(f"\n{'='*60}")
    print(f"  跑步助手 Web 版本已启动")
    print(f"  访问地址: {server_url}")
    if ssl_config.get("ssl_enabled", False):
        print(f"  SSL/HTTPS: 已启用 ✓")
        if ssl_config.get("https_only", False):
            print(f"  仅HTTPS模式: 已启用 ⚠")
    else:
        print(f"  SSL/HTTPS: 未启用（使用HTTP）")
    # print(f"  首次访问将自动分配2048位UUID并重定向")
    print(f"  会话持久化已启用（服务器重启后保留登录状态）")
    print(f"  JS计算在服务器端Chrome中执行，提升安全性")
    print(f"  会话监控已启用（5分钟不活跃自动清理）")
    print(f"{'='*60}\n")

    try:
        # 修正：HTTPS/SSL 启动方式
        # 当 async_mode='eventlet' 时，Flask-SocketIO 不支持 ssl_context 参数
        # 需要使用 certfile 和 keyfile 参数代替

        if ssl_context:
            # HTTPS 模式
            logging.info(
                f"正在启动带有 WebSocket 和 SSL(HTTPS) 支持的 Web 服务器于 {server_url}"
            )

            try:

                logging.info(f"Eventlet 将使用 SSLContext 启动服务器...")
                logging.info(f"  证书文件: {cert_path}")
                logging.info(f"  密钥文件: {key_path}")

                # ============================================================
                # 【SSL 智能兼容层】
                # 定义一个双协议 Socket 包装类，用于在同一端口处理 HTTPS 和 HTTP 跳转
                # ============================================================
                class DualProtocolSocket(object):
                    def __init__(self, raw_socket, ssl_ctx, https_only=False):
                        self.sock = raw_socket
                        self.ssl_ctx = ssl_ctx
                        self.https_only = https_only  # [新增] 存储是否强制HTTPS的配置

                    # 【修正】使用 __getattr__ 自动代理所有未定义的方法到底层 socket
                    def __getattr__(self, name):
                        return getattr(self.sock, name)

                    def accept(self):
                        while True:
                            try:
                                # 1. 接受原始连接
                                client, addr = self.sock.accept()
                                
                                # 2. 嗅探第一个字节（不从缓冲区移除）
                                try:
                                    # 设置短超时防止恶意连接挂起
                                    client.settimeout(1.0)
                                    first_byte = client.recv(1, socket.MSG_PEEK)
                                    client.settimeout(None) # 恢复阻塞模式或默认超时
                                    
                                    if len(first_byte) == 0:
                                        client.close()
                                        continue
                                        
                                    # 3. 判断协议类型
                                    # 0x16 (十进制22) 是 TLS Handshake 的第一个字节
                                    if first_byte[0] == 22:
                                        # === HTTPS 连接 ===
                                        # 包装为 SSL Socket 并返回给 WSGI Server
                                        secure_client = self.ssl_ctx.wrap_socket(client, server_side=True)
                                        return secure_client, addr
                                    else:
                                        # === HTTP 连接 (或其他) ===
                                        
                                        # 如果配置了仅允许 HTTPS，则发送 JS 跳转
                                        if self.https_only:
                                            logging.info(f"检测到 HTTP 请求 (来自 {addr[0]})，发送 HTTPS 跳转指令...")
                                            
                                            # [关键修复] 消耗掉接收缓冲区中的 HTTP 请求数据
                                            # 如果不读取，直接关闭 Socket，内核会发送 TCP RST 包，
                                            # 导致浏览器报错 "ERR_CONNECTION_RESET"
                                            try:
                                                client.settimeout(0.1)
                                                # 读取最多 4KB 数据（通常足够包含请求头）
                                                client.recv(4096)
                                            except Exception:
                                                pass

                                            response = (
                                                "HTTP/1.1 200 OK\r\n"
                                                "Content-Type: text/html\r\n"
                                                "Connection: close\r\n\r\n"
                                                "<html><head><title>Redirecting...</title></head>"
                                                "<body><script>window.location.protocol = 'https:';</script>"
                                                "Please wait, redirecting to HTTPS...</body></html>"
                                            )
                                            try:
                                                client.sendall(response.encode('utf-8'))
                                            except Exception:
                                                pass
                                            finally:
                                                client.close()
                                            # 继续循环等待下一个连接，不返回给 WSGI
                                            continue
                                        else:
                                            # [新增] 如果允许 HTTP，直接返回原始 Socket
                                            # 这样可以在同一端口同时支持 HTTP 和 HTTPS
                                            return client, addr
                                        
                                except (socket.error, ssl.SSLError) as e:
                                    # 握手或读取错误，关闭连接并忽略
                                    try: client.close() 
                                    except: pass
                                    continue
                                    
                            except Exception as e:
                                logging.error(f"DualProtocolSocket accept error: {e}")
                                continue
                # 【修正】1. 手动创建 TCP 监听 Socket
                server_socket = eventlet.listen((args.host, args.port))

                # 【修正】2. 使用自定义的双协议包装器
                # 传入配置中的 https_only 选项
                dual_socket = DualProtocolSocket(
                    server_socket, 
                    ssl_context, 
                    https_only=ssl_config.get("https_only", False)
                )

                # 【修正】3. 启动服务器
                try:
                    # 将 dual_socket 传给 server
                    eventlet.wsgi.server(dual_socket, app, log_output=False)
                except KeyboardInterrupt:
                    raise
                except Exception as runtime_e:
                    logging.error(f"HTTPS 服务器运行时错误: {runtime_e}", exc_info=True)
                    # 尝试安全关闭 Socket
                    try:
                        server_socket.close()
                    except:
                        pass
                    # 抛出异常以便上层处理或退出
                    raise

            except ImportError:
                logging.error(
                    "Eventlet 模块未找到，无法启动HTTPS服务器。请运行 'pip install eventlet'"
                )
                raise
            except KeyboardInterrupt:
                # 捕获 HTTPS 模式下的 Ctrl+C
                raise
            except Exception as ssl_e:
                # 这里只捕获启动时的致命错误（如端口绑定失败、证书错误等）
                logging.error(
                    f"使用 Eventlet 启动 SSL 服务器失败: {ssl_e}", exc_info=True
                )
                print(f"\n[错误] 无法使用 eventlet 启动 HTTPS 服务器: {ssl_e}")
                print("请检查证书文件路径和权限是否正确。")
                raise

        else:
            # HTTP 模式
            logging.info(f"正在启动带有 WebSocket 支持的 Web 服务器于 {server_url}")

            # HTTP 模式也添加 Ctrl+C 支持
            try:
                socketio.run(app, host=args.host, port=args.port, debug=False)
            except KeyboardInterrupt:
                raise

    except KeyboardInterrupt:
        # 最外层的 Ctrl+C 捕获，确保优雅退出
        print(f"\n{'='*60}")
        print(f"  用户终止了程序 (Ctrl+C)")
        print(f"  正在清理资源并退出...")
        print(f"{'='*60}\n")
        logging.info("用户通过 Ctrl+C 停止了服务器")
        # 可以在这里调用清理函数，例如 _cleanup_playwright()
        sys.exit(0)

    except OSError as e:
        if (
            "WinError 10013" in str(e)
            or "permission" in str(e).lower()
            or "访问权限" in str(e)
        ):
            print(f"\n{'='*60}")
            print(f"错误: 端口 {args.port} 被占用或无访问权限")
            print(f"")
            print(f"可能的原因：")
            print(f"  1. 端口已被其他程序使用")
            print(f"  2. Windows系统保留了该端口")
            print(f"  3. 需要管理员权限")
            print(f"")
            print(f"解决方法：")
            print(f"  方法1: 使用其他端口")
            print(f"    python main.py --port 8080")
            print(f"    python main.py --port 3000")
            print(f"")
            print(f"  方法2: 以管理员身份运行")
            print(f"    右键点击 PowerShell → 以管理员身份运行")
            print(f"")
            print(f"  方法3 (Windows): 检查并关闭占用端口的程序")
            print(f"    netstat -ano | findstr :{args.port}")
            print(f"    taskkill /PID <进程ID> /F")
            print(f"{'='*60}\n")
            logging.error(f"端口绑定失败: {e}")
        else:
            print(f"\n错误: 启动服务器失败 - {e}\n")
            logging.error(f"服务器启动失败: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: 服务器运行时发生异常 - {e}\n")
        logging.error(f"服务器异常: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # # 清理Chrome资源
        # if chrome_pool:
        #     logging.info("正在清理Chrome浏览器资源...")
        #     chrome_pool.cleanup()
        pass


def main():
    """主函数，启动Web服务器模式（已弃用桌面模式）"""

    # ========== 第1步：导入内置模块 ==========
    # 必须最先执行，因为后续所有操作都依赖这些模块
    # try:
    #     import_builtin_modules()
    # except Exception as e:
    #     print(f"[致命错误] 导入内置模块失败: {e}")
    #     import traceback
    #     traceback.print_exc()
    #     import sys
    #     sys.exit(1)

    # ========== 第2步：初始化日志系统 ==========
    # 在程序最开始就初始化日志，确保后续所有操作都能被记录
    try:
        setup_logging()
    except Exception as e:
        # 如果日志系统初始化失败，至少要在控制台输出错误
        print(f"[错误] 日志系统初始化失败: {e}")
        traceback.print_exc()
        # 不退出，继续尝试运行
        # 启动时加载IP缓存
        _load_ip_cache()

    # ========== 第3步：导入所有依赖库 ==========
    # 导入标准库 (socket, math, etc.)
    import_standard_libraries()

    # 导入核心第三方库 (Pillow, bcrypt, Flask-SocketIO)
    import_core_third_party()

    # 导入主要应用依赖库 (Flask, requests, playwright 等)
    check_and_import_dependencies()

    # ========== 第4步：初始化系统 ==========
    # 创建目录、配置文件、默认管理员账号等
    auto_init_system()

    # 创建 AuthSystem, TokenManager, 并加载 html_content
    initialize_global_variables()

    # ========== 第5步：解析命令行参数 ==========
    parser = argparse.ArgumentParser(description="跑步助手 - Web服务器模式")
    parser.add_argument(
        "--port", type=int, default=5000, help="Web服务器端口（默认5000）"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Web服务器地址（默认127.0.0.1）"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="使用无头Chrome模式（默认启用）",
    )
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="debug",
        help="设置日志级别（默认 debug）",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试日志（兼容旧参数，等同于 --log-level debug）",
    )
    args = parser.parse_args()

    # ========== 第6步：配置日志级别 ==========
    selected_level_name = "debug" if args.debug else args.log_level
    log_level = getattr(logging, selected_level_name.upper(), logging.DEBUG)

    log_format = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"

    # 创建UTF-8编码的StreamHandler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(level=log_level, format=log_format, handlers=[handler])

    logging.info("=" * 60)
    logging.info("跑步助手 Web 模式启动中...")
    level_name_map = {
        logging.DEBUG: "调试",
        logging.INFO: "信息",
        logging.WARNING: "警告",
        logging.ERROR: "错误",
        logging.CRITICAL: "严重",
    }
    logging.info(
        f"日志级别: {level_name_map.get(log_level, selected_level_name.upper())} ({selected_level_name.upper()})"
    )
    logging.info(f"服务器地址: {args.host}:{args.port}")
    logging.info("=" * 60)

    # ========== 第7步：检查Playwright是否可用 ==========
    if not playwright_available:
        print("\n" + "=" * 60)
        print("错误: 需要安装 Playwright 以在服务器端运行Chrome")
        print("请运行以下命令:")
        print("  pip install playwright")
        print("  python -m playwright install chromium")
        print("=" * 60 + "\n")
        sys.exit(1)

    # ========== 第8步：检查并选择可用端口 ==========
    initial_port = args.port
    DEFAULT_PORT = 5000  # 从 argparse 定义中获取的默认端口

    # 检查用户是否 *明确* 指定了 *非默认* 端口
    if initial_port != DEFAULT_PORT:
        # --- 用户明确指定了端口 (例如 --port 80) ---
        logging.info(f"用户已明确指定端口 {initial_port}。")
        logging.warning(f"将 *直接尝试* 绑定到端口 {initial_port}。")
        logging.warning(
            f"注意：如果此端口已被占用，或需要更高权限 (例如在 Linux/macOS 上绑定端口 80)，程序将会启动失败。"
        )
        # 我们跳过了 check_port_available 和自动重分配逻辑
        # args.port 保持用户指定的值 (例如 80)

    else:
        # --- 用户使用的是默认端口 (5000)，我们执行自动检查和重分配 ---
        logging.info(f"用户正在使用默认端口 {DEFAULT_PORT}。正在检查端口可用性...")
        if not check_port_available(args.host, args.port):
            logging.warning(
                f"默认端口 {args.port} 不可用或已被占用，尝试自动查找可用端口..."
            )
            found_port = None
            # 尝试常用备选端口
            alternative_ports = [8080, 8000, 3000, 5001, 8888, 9000, 5005, 5050]
            for port in alternative_ports:
                logging.info(f"尝试端口 {port}...")
                if check_port_available(args.host, port):
                    found_port = port
                    logging.info(f"找到可用端口: {found_port}")
                    break

            # 如果常用端口都不可用，尝试随机端口
            if not found_port:
                logging.info(
                    "常用备选端口均不可用，尝试在 10000-65535 范围内查找随机可用端口..."
                )
                max_random_tries = 20  # 限制尝试次数
                for i in range(max_random_tries):
                    random_port = random.randint(10000, 65535)
                    if check_port_available(args.host, random_port):
                        found_port = random_port
                        logging.info(f"找到可用随机端口: {found_port}")
                        break
                    time.sleep(0.01)

            # 如果最终仍未找到可用端口
            if not found_port:
                logging.error(
                    f"自动查找端口失败。默认端口 {initial_port} 及所有尝试的备选/随机端口均不可用。"
                )
                print(f"\n{'='*60}")
                print(f"错误: 无法自动找到可用的网络端口。")
                print(
                    f"请检查端口 {initial_port} 或其他常用端口是否被占用，或手动指定一个可用端口:"
                )
                print(f"  python main.py --port <可用端口号>")
                print(f"{'='*60}\n")
                sys.exit(1)
            else:
                args.port = found_port  # 更新 args 中的端口号为找到的可用端口
        else:
            logging.info(f"默认端口 {DEFAULT_PORT} 可用。")

    # ========== 第9步：启动Web服务器 ==========
    logging.info("启动Web服务器模式（使用服务器端Chrome渲染）...")
    start_web_server(args)


if __name__ == "__main__":
    main()
