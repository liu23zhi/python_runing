#!/usr/bin/env python3
"""测试 HTML 压缩功能"""

import os

# 读取一个 HTML 片段进行测试
fragment_file = 'html_fragments/admin-panel-modal.html'
with open(fragment_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

print("="*80)
print("HTML 压缩功能测试")
print("="*80)
print(f"\n测试文件: {fragment_file}")
print(f"原始大小: {len(html_content):,} 字节 ({len(html_content)/1024:.1f} KB)")

# 简化的 HTML 压缩函数（用于测试）
def minify_html_simple(html):
    import re
    
    # 移除 HTML 注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 移除多余的空白
    html = re.sub(r'\s+', ' ', html)
    
    # 移除标签之间的空格
    html = re.sub(r'>\s+<', '><', html)
    
    return html.strip()

minified = minify_html_simple(html_content)

print(f"压缩后大小: {len(minified):,} 字节 ({len(minified)/1024:.1f} KB)")

compression_ratio = (1 - len(minified) / len(html_content)) * 100
print(f"压缩率: {compression_ratio:.1f}%")
print(f"节省: {len(html_content) - len(minified):,} 字节 ({(len(html_content) - len(minified))/1024:.1f} KB)")

# 测试所有片段
print("\n" + "="*80)
print("所有 HTML 片段压缩效果:")
print("="*80)

fragments_dir = 'html_fragments'
total_original = 0
total_minified = 0

for filename in sorted(os.listdir(fragments_dir)):
    if filename.endswith('.html'):
        filepath = os.path.join(fragments_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        minified = minify_html_simple(content)
        ratio = (1 - len(minified) / len(content)) * 100
        
        total_original += len(content)
        total_minified += len(minified)
        
        print(f"{filename:35s} {len(content):6,} -> {len(minified):6,} 字节 ({ratio:5.1f}%)")

print("-"*80)
print(f"{'总计':35s} {total_original:6,} -> {total_minified:6,} 字节 ({(1-total_minified/total_original)*100:5.1f}%)")
print(f"\n节省: {total_original - total_minified:,} 字节 ({(total_original - total_minified)/1024:.1f} KB)")

