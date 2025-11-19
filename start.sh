#!/bin/bash

# --- 配置 ---
VENV_NAME="zs_campus_run_helper_venv"
PYTHON_CMD="python3" # 如果你的默认 python 是 3.x，可以改成 "python"
# --- 结束配置 ---

# 获取脚本文件所在的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查 python 命令是否存在
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "错误: $PYTHON_CMD 未找到。"
    echo "请安装 Python 3 并确保它在您的 PATH 中。"
    exit 1
fi

# 检查依赖文件是否存在
if [ ! -f "${SCRIPT_DIR}/requirements.txt" ]; then
    echo "错误: 未找到 requirements.txt 文件。"
    echo "请确保依赖文件与此脚本位于同一目录。"
    exit 1
fi

# 检查是否为手动模式
if [ "$1" == "manual" ]; then
    echo "--- 手动模式 ---"
    echo "请按以下步骤手动操作："
    echo "1. (如果需要) 创建虚拟环境: $PYTHON_CMD -m venv $VENV_NAME"
    echo "2. 激活虚拟环境: source $VENV_NAME/bin/activate"
    echo "3. 安装依赖: pip install -r ${SCRIPT_DIR}/requirements.txt"
    echo "4. 运行程序: $PYTHON_CMD ${SCRIPT_DIR}/main.py"
    echo "5. (完成后) 退出虚拟环境: deactivate"
    exit 0
fi

# --- 自动模式 ---

# 1. 检查虚拟环境是否存在
if [ ! -f "$VENV_NAME/bin/activate" ]; then
    echo "未找到虚拟环境 '$VENV_NAME'。正在创建..."
    $PYTHON_CMD -m venv $VENV_NAME
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败。请尝试使用 'manual' 模式运行。"
        exit 1
    fi
else
    echo "找到虚拟环境 '$VENV_NAME'。"
fi

# 2. 激活虚拟环境
echo "正在激活虚拟环境..."
source $VENV_NAME/bin/activate
if [ $? -ne 0 ]; then
    echo "激活虚拟环境失败。请尝试使用 'manual' 模式运行。"
    exit 1
fi

# 3. 安装/更新依赖
echo "正在从 requirements.txt 安装/更新依赖..."
pip install -r "${SCRIPT_DIR}/requirements.txt"
if [ $? -ne 0 ]; then
    echo "安装依赖失败。请检查 requirements.txt 文件和网络连接。"
    echo "请尝试使用 'manual' 模式运行。"
    exit 1
fi

# 4. 启动 main.py
echo "依赖安装完毕。正在启动 main.py ..."
echo "-----------------------------------------"
# *** 这是修改过的行 ***
cd "$SCRIPT_DIR"
$PYTHON_CMD "${SCRIPT_DIR}/main.py" "$@"
# 脚本执行完毕后，虚拟环境会自动停用（因为脚本 shell 退出了）
echo "-----------------------------------------"
echo "程序已退出。"