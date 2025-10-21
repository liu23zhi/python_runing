#!/usr/bin/env python3
"""
使用示例脚本

演示如何启动和使用Web模式
"""

import sys
import argparse

def print_header():
    print("=" * 70)
    print("跑步助手 - Web模式使用示例")
    print("=" * 70)
    print()

def example_basic():
    """示例1: 基本Web模式启动"""
    print("示例1: 基本Web模式启动")
    print("-" * 70)
    print("命令:")
    print("    python main.py --mode web")
    print()
    print("说明:")
    print("    - 使用默认端口5000")
    print("    - 监听 127.0.0.1 (仅本地访问)")
    print("    - 使用pywebview作为JS引擎")
    print()
    print("访问地址:")
    print("    http://127.0.0.1:5000")
    print()

def example_custom_port():
    """示例2: 自定义端口"""
    print("示例2: 自定义端口和地址")
    print("-" * 70)
    print("命令:")
    print("    python main.py --mode web --web-host 0.0.0.0 --web-port 8080")
    print()
    print("说明:")
    print("    - 使用端口8080")
    print("    - 监听所有网络接口 (允许远程访问)")
    print("    - 适合在服务器上部署")
    print()
    print("访问地址:")
    print("    http://你的服务器IP:8080")
    print()

def example_chrome():
    """示例3: 使用Chrome引擎"""
    print("示例3: 使用Chrome作为JS引擎")
    print("-" * 70)
    print("命令:")
    print("    python main.py --mode web --use-chrome")
    print()
    print("说明:")
    print("    - 使用Chrome浏览器执行JS")
    print("    - 需要安装selenium和chromedriver")
    print("    - 更稳定，推荐用于生产环境")
    print()
    print("前置条件:")
    print("    pip install selenium")
    print("    # 并安装ChromeDriver到PATH")
    print()

def example_uuid_usage():
    """示例4: UUID会话使用说明"""
    print("示例4: UUID会话工作原理")
    print("-" * 70)
    print("1. 首次访问: http://localhost:5000/")
    print("   → 自动重定向到: http://localhost:5000/uuid=abc123...")
    print()
    print("2. 系统为您分配一个32位UUID")
    print("   例如: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
    print()
    print("3. 保存这个URL，下次访问时会恢复您的会话")
    print()
    print("4. 每个UUID对应一个独立的会话，互不干扰")
    print()
    print("5. 多用户可以同时使用，每人有自己的UUID")
    print()

def example_production():
    """示例5: 生产环境部署"""
    print("示例5: 生产环境部署建议")
    print("-" * 70)
    print("1. 使用Gunicorn或uWSGI作为WSGI服务器:")
    print("   gunicorn -w 4 -b 0.0.0.0:5000 'web_mode:create_app(api, event)'")
    print()
    print("2. 配置Nginx反向代理:")
    print("   upstream app {")
    print("       server 127.0.0.1:5000;")
    print("   }")
    print("   server {")
    print("       listen 80;")
    print("       location / {")
    print("           proxy_pass http://app;")
    print("       }")
    print("   }")
    print()
    print("3. 启用HTTPS (使用Let's Encrypt)")
    print()
    print("4. 配置防火墙规则")
    print()
    print("5. 使用systemd管理服务")
    print()

def main():
    parser = argparse.ArgumentParser(description="Web模式使用示例")
    parser.add_argument(
        '--example',
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="显示特定示例 (1-5)"
    )
    args = parser.parse_args()
    
    print_header()
    
    if args.example:
        examples = {
            1: example_basic,
            2: example_custom_port,
            3: example_chrome,
            4: example_uuid_usage,
            5: example_production
        }
        examples[args.example]()
    else:
        # 显示所有示例
        example_basic()
        print()
        example_custom_port()
        print()
        example_chrome()
        print()
        example_uuid_usage()
        print()
        example_production()
    
    print("=" * 70)
    print("提示: 运行 'python examples.py --example N' 查看特定示例")
    print("=" * 70)

if __name__ == "__main__":
    main()
