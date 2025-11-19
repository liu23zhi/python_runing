#!/bin/bash

# --- 配置部分 ---

# 1. screen 会话的英文名称
SESSION_NAME="zis_runner_helper"


# 获取脚本文件所在的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 2. 临时的 screen 配置文件路径 (用于添加顶部提示栏)
SCREEN_RC_FILE="${SCRIPT_DIR}/${SESSION_NAME}.screenrc"
# 3. 你想在后台运行的实际命令 
COMMAND_TO_RUN="${SCRIPT_DIR}/start.sh --port 443 --host 0.0.0.0"

# --- 脚本正文 ---

# 检查 'screen' 是否安装
if ! command -v screen &> /dev/null; then
    echo "错误: 'screen' 未安装。"
    echo "请先安装 'screen' (例如: sudo apt install screen 或 yum install screen)"
    exit 1
fi

# 显示主菜单
show_menu() {
    clear
    echo "================================================="
    echo " 电子科技大学中山学院校园跑步助手 (Screen 管理器)"
    echo " (ZIS Runner Helper - Session Manager)"
    echo "================================================="
    echo "  会话名称: $SESSION_NAME"
    echo "  运行命令: $COMMAND_TO_RUN"
    echo "-------------------------------------------------"
    echo "  1. 启动 / 连接会话 (Start / Attach Session)"
    echo "  2. 关闭会话 (Stop Session)"
    echo "  0. 退出脚本 (Exit)"
    echo "-------------------------------------------------"
    echo -n "请输入选项 [0-2]: "
}

# 功能 1: 启动或连接会话
start_session() {
    # 检查会话是否已在运行
    if screen -ls | grep -q "\.$SESSION_NAME\s"; then
        echo "会话 '$SESSION_NAME' 已在运行。正在连接..."
        sleep 1
        # 直接连接，它会自动使用已有的配置
        exec screen -r "$SESSION_NAME"
    else
        echo "未找到会话。正在启动新的会话 '$SESSION_NAME'..."

        # --- 新增功能：创建顶部提示栏的配置文件 ---
        echo "正在创建顶部提示栏配置文件: $SCREEN_RC_FILE"
        
        # 1. 告诉 screen 把状态栏放在最顶行 (first line) 并始终显示
        echo "hardstatus alwaysfirstline" > "$SCREEN_RC_FILE"
        
        # 2. 设置状态栏的显示内容
        # %{= Yk} -> 黄色(Y)背景，黑色(k)文字
        # %{= Kk} -> 重置为默认颜色
        # 您可以按需修改 "分离会话" 后的中文
        echo "hardstatus string \"%{= Yk} 提示: 按 Ctrl+A 然后按 D (分离会话)，返回到主终端 %{= Kk}\"" >> "$SCREEN_RC_FILE"
        # --- 配置文件创建完毕 ---

        # 使用 -c 加载我们的自定义配置文件来启动 screen
        # 防止会话立即消失，以便用户能连接进去看到底发生了什么。
        screen -c "$SCREEN_RC_FILE" -dmS "$SESSION_NAME" bash -c "$COMMAND_TO_RUN; exec bash"
        
        # 检查是否启动成功
        sleep 0.5
        if screen -ls | grep -q "\.$SESSION_NAME\s"; then
            echo "会话已在后台启动。现在连接..."
            sleep 1
            # 连接到新创建的会话
            exec screen -r "$SESSION_NAME"
        else
            echo "错误：无法启动会话 '$SESSION_NAME'。"
            echo "请检查 '$COMMAND_TO_RUN' 命令是否正确。"
            sleep 3
        fi
    fi
}

# 功能 2: 关闭会话
stop_session() {
    if screen -ls | grep -q "\.$SESSION_NAME\s"; then
        echo "正在发送关闭命令到会话 '$SESSION_NAME'..."
        screen -S "$SESSION_NAME" -X quit
        
        sleep 1
        if screen -ls | grep -q "\.$SESSION_NAME\s"; then
            echo "错误：会话未能正常关闭。请手动检查: screen -ls"
        else
            echo "会话 '$SESSION_NAME' 已成功关闭。"
            
            # --- 新增功能：清理临时的配置文件 ---
            if [ -f "$SCREEN_RC_FILE" ]; then
                rm "$SCREEN_RC_FILE"
                echo "已自动清理临时配置文件: $SCREEN_RC_FILE"
            fi
            # --- 清理完毕 ---
        fi
    else
        echo "会话 '$SESSION_NAME' 未在运行。"
    fi
    echo ""
    echo "按 Enter 键返回菜单..."
    read -r
}

# 主循环
main() {
    while true; do
        show_menu
        read -r choice
        case $choice in
            1)
                start_session
                echo "会话已结束或启动失败。正在返回菜单..."
                sleep 2
                ;;
            2)
                stop_session
                ;;
            0)
                echo "正在退出。"
                break
                ;;
            *)
                echo "无效选项 '$choice'，请重试。"
                sleep 2
                ;;
        esac
    done
}

# 运行主函数
main