#!/usr/bin/env python3
"""
测试 JavaScript 压缩功能
"""

def minify_javascript(code):
    """简化版的压缩函数用于测试"""
    if not code:
        return code
    
    result = []
    in_string = False
    string_delimiter = None
    in_regex = False
    in_single_comment = False
    in_multi_comment = False
    
    i = 0
    length = len(code)
    
    while i < length:
        char = code[i]
        next_char = code[i + 1] if i + 1 < length else ''
        prev_char = result[-1] if result else ''
        
        # 处理多行注释
        if in_multi_comment:
            if char == '*' and next_char == '/':
                in_multi_comment = False
                i += 2
                continue
            i += 1
            continue
        
        # 处理单行注释
        if in_single_comment:
            if char == '\n':
                in_single_comment = False
                if result and result[-1] not in [';', '{', '}', '\n']:
                    result.append('\n')
            i += 1
            continue
        
        # 检测多行注释开始
        if not in_string and not in_regex and char == '/' and next_char == '*':
            in_multi_comment = True
            i += 2
            continue
        
        # 检测单行注释开始
        if not in_string and not in_regex and char == '/' and next_char == '/':
            in_single_comment = True
            i += 2
            continue
        
        # 处理字符串
        if char in ['"', "'", '`'] and not in_regex:
            if not in_string:
                in_string = True
                string_delimiter = char
                result.append(char)
            elif char == string_delimiter and (not result or result[-1] != '\\'):
                in_string = False
                string_delimiter = None
                result.append(char)
            else:
                result.append(char)
            i += 1
            continue
        
        if in_string:
            result.append(char)
            i += 1
            continue
        
        # 简化的空白压缩
        if char in [' ', '\t', '\n', '\r']:
            if result and result[-1] not in [' ', '\n']:
                result.append(' ')
            i += 1
            continue
        
        result.append(char)
        i += 1
    
    return ''.join(result)

# 测试用例
test_code = """
// 这是单行注释
function hello(name) {
    /* 这是
       多行注释 */
    console.log("Hello, " + name);
    var msg = 'Test message';
    return true;
}

// 另一个函数
const add = (a, b) => {
    return a + b;
};
"""

print("原始代码：")
print(test_code)
print(f"\n原始大小：{len(test_code)} 字节")

minified = minify_javascript(test_code)
print("\n压缩后代码：")
print(minified)
print(f"\n压缩后大小：{len(minified)} 字节")
print(f"压缩率：{(1 - len(minified)/len(test_code))*100:.1f}%")

