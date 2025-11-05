#!/usr/bin/env python3
"""
简单测试脚本：验证 JavaScript API 功能
"""
import os
import hashlib
from datetime import datetime

# 测试 JavaScript.js 文件读取
js_file_path = 'JavaScript.js'

print("="*70)
print("测试 JavaScript API 功能")
print("="*70)

# 测试1: 检查文件是否存在
print("\n[测试1] 检查 JavaScript.js 文件...")
if os.path.exists(js_file_path):
    print(f"✓ 文件存在: {js_file_path}")
    file_size = os.path.getsize(js_file_path)
    print(f"  文件大小: {file_size:,} 字节 ({file_size/1024:.1f} KB)")
else:
    print(f"✗ 文件不存在: {js_file_path}")
    exit(1)

# 测试2: 读取文件内容
print("\n[测试2] 读取文件内容...")
try:
    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✓ 成功读取 {len(content):,} 字符")
    print(f"  前100个字符: {content[:100]}...")
except Exception as e:
    print(f"✗ 读取失败: {e}")
    exit(1)

# 测试3: 生成 ETag
print("\n[测试3] 生成 ETag...")
try:
    etag = hashlib.md5(content.encode('utf-8')).hexdigest()
    print(f"✓ ETag: {etag}")
except Exception as e:
    print(f"✗ 生成失败: {e}")
    exit(1)

# 测试4: 生成 Last-Modified
print("\n[测试4] 生成 Last-Modified 头...")
try:
    file_mtime = os.path.getmtime(js_file_path)
    last_modified = datetime.fromtimestamp(file_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')
    print(f"✓ Last-Modified: {last_modified}")
except Exception as e:
    print(f"✗ 生成失败: {e}")
    exit(1)

# 测试5: 查找特定函数
print("\n[测试5] 查找特定函数（示例：handleCdnError）...")
import re
function_name = 'handleCdnError'
pattern = rf'(?:^|\n)(\s*(?:function\s+{function_name}\s*\([^)]*\)|(?:const|let|var)\s+{function_name}\s*=\s*(?:function\s*\([^)]*\)|(?:async\s+)?function\s*\([^)]*\)|\([^)]*\)\s*=>))\s*{{)'
match = re.search(pattern, content, re.MULTILINE)

if match:
    print(f"✓ 找到函数: {function_name}")
    print(f"  位置: 第 {content[:match.start()].count(chr(10))+1} 行")
    print(f"  定义: {match.group(0)[:80]}...")
else:
    print(f"✗ 未找到函数: {function_name}")

print("\n" + "="*70)
print("所有测试完成！")
print("="*70)
