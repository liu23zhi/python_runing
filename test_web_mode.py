#!/usr/bin/env python3
"""
测试脚本：验证Web模式的基本功能
"""

import sys
import time
import subprocess
import requests
from threading import Thread

def test_web_mode_startup():
    """测试Web模式能否正常启动"""
    print("测试1: Web模式启动测试")
    print("=" * 50)
    
    # 启动Web服务器（子进程）
    print("正在启动Web服务器...")
    process = subprocess.Popen(
        [sys.executable, "main.py", "--mode", "web", "--web-port", "5001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动
    print("等待服务器初始化...")
    time.sleep(5)
    
    try:
        # 测试健康检查端点
        print("测试健康检查端点...")
        response = requests.get("http://127.0.0.1:5001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 健康检查通过: {data}")
        else:
            print(f"✗ 健康检查失败: {response.status_code}")
            return False
        
        # 测试根路径重定向
        print("\n测试UUID重定向...")
        response = requests.get("http://127.0.0.1:5001/", allow_redirects=False, timeout=5)
        if response.status_code in [301, 302, 303, 307, 308]:
            redirect_url = response.headers.get('Location', '')
            print(f"✓ 重定向成功: {redirect_url}")
            
            # 验证重定向URL包含uuid参数
            if 'uuid=' in redirect_url:
                print("✓ UUID格式正确")
            else:
                print("✗ UUID格式错误")
                return False
        else:
            print(f"✗ 重定向失败: {response.status_code}")
            return False
        
        # 测试会话端点
        print("\n测试会话端点...")
        # 使用session来保持cookie
        session = requests.Session()
        response = session.get("http://127.0.0.1:5001/", timeout=5)
        if response.status_code == 200:
            print(f"✓ 会话页面加载成功")
            
            # 检查HTML内容是否包含SESSION_UUID
            if 'SESSION_UUID' in response.text:
                print("✓ UUID已注入到页面")
            else:
                print("✗ UUID未注入到页面")
        else:
            print(f"✗ 会话页面加载失败: {response.status_code}")
            return False
        
        print("\n✓ 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        return False
    finally:
        # 清理：终止子进程
        print("\n正在关闭服务器...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("服务器已关闭")

def test_uuid_persistence():
    """测试UUID持久性"""
    print("\n\n测试2: UUID持久性测试")
    print("=" * 50)
    
    # 启动服务器
    print("正在启动Web服务器...")
    process = subprocess.Popen(
        [sys.executable, "main.py", "--mode", "web", "--web-port", "5002"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(5)
    
    try:
        session = requests.Session()
        
        # 第一次访问，获取UUID
        print("第一次访问...")
        response = session.get("http://127.0.0.1:5002/", timeout=5)
        first_url = response.url
        print(f"分配的UUID URL: {first_url}")
        
        # 提取UUID
        if 'uuid=' in first_url:
            uuid_part = first_url.split('uuid=')[1]
            print(f"UUID: {uuid_part}")
        else:
            print("✗ 未找到UUID")
            return False
        
        # 第二次访问根路径，应该重定向到相同的UUID
        print("\n第二次访问根路径...")
        response = session.get("http://127.0.0.1:5002/", timeout=5)
        second_url = response.url
        print(f"重定向到: {second_url}")
        
        if first_url == second_url:
            print("✓ UUID持久性测试通过")
            return True
        else:
            print("✗ UUID不一致")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False
    finally:
        print("\n正在关闭服务器...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("服务器已关闭")

def test_multiple_sessions():
    """测试多个独立会话"""
    print("\n\n测试3: 多会话隔离测试")
    print("=" * 50)
    
    # 启动服务器
    print("正在启动Web服务器...")
    process = subprocess.Popen(
        [sys.executable, "main.py", "--mode", "web", "--web-port", "5003"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(5)
    
    try:
        # 创建两个独立的会话
        session1 = requests.Session()
        session2 = requests.Session()
        
        print("创建会话1...")
        response1 = session1.get("http://127.0.0.1:5003/", timeout=5)
        url1 = response1.url
        print(f"会话1 UUID URL: {url1}")
        
        print("\n创建会话2...")
        response2 = session2.get("http://127.0.0.1:5003/", timeout=5)
        url2 = response2.url
        print(f"会话2 UUID URL: {url2}")
        
        # 验证两个会话有不同的UUID
        if url1 != url2 and 'uuid=' in url1 and 'uuid=' in url2:
            print("\n✓ 多会话隔离测试通过")
            return True
        else:
            print("\n✗ 会话未正确隔离")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False
    finally:
        print("\n正在关闭服务器...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("服务器已关闭")

def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Web模式功能测试套件")
    print("=" * 60 + "\n")
    
    results = []
    
    # 运行测试
    results.append(("Web模式启动", test_web_mode_startup()))
    results.append(("UUID持久性", test_uuid_persistence()))
    results.append(("多会话隔离", test_multiple_sessions()))
    
    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
