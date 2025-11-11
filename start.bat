@echo off
SETLOCAL

REM 修正：强制脚本在自己的目录下运行，解决在 PowerShell 中调用时的路径问题
cd /d "%~dp0"

REM --- 配置 ---
SET VENV_NAME=zs_campus_run_helper_venv
SET PYTHON_CMD=python
REM --- 结束配置 ---

REM 检查 python 命令是否存在
%PYTHON_CMD% --version >NUL 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo 错误: %PYTHON_CMD% 未找到。
    echo 请安装 Python 3 并确保它在您的 PATH 环境变量中。
    GOTO :fail
)

REM 检查依赖文件是否存在
IF NOT EXIST "requirements.txt" (
    echo 错误: 未找到 requirements.txt 文件。
    echo 请确保依赖文件与此脚本位于同一目录。
    GOTO :fail
)

REM 检查是否为手动模式
IF /I "%1" == "manual" GOTO :manual_mode

REM --- 自动模式 ---

REM 1. 检查虚拟环境是否存在
IF NOT EXIST "%VENV_NAME%\" (
    echo 未找到虚拟环境 '%VENV_NAME%'。正在创建...
    %PYTHON_CMD% -m venv %VENV_NAME%
    IF %ERRORLEVEL% NEQ 0 GOTO :venv_fail
) ELSE (
    echo 找到虚拟环境 '%VENV_NAME%'。
)

REM 2. 激活虚拟环境
echo 正在激活虚拟环境...
CALL "%VENV_NAME%\Scripts\activate.bat"
IF %ERRORLEVEL% NEQ 0 GOTO :activate_fail

REM 3. 安装/更新依赖
echo 正在从 requirements.txt 安装/更新依赖...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 GOTO :deps_fail

REM 4. 启动 main.py
echo 依赖安装完毕。正在启动 main.py ...
echo -----------------------------------------
%PYTHON_CMD% main.py
echo -----------------------------------------
echo 程序已退出。

GOTO :end

:manual_mode
echo --- 手动模式 ---
echo 请按以下步骤手动操作：
echo 1. (如果需要) 创建虚拟环境: %PYTHON_CMD% -m venv %VENV_NAME%
echo 2. 激活虚拟环境: .\%VENV_NAME%\Scripts\activate.bat
echo 3. 安装依赖: pip install -r requirements.txt
echo 4. 运行程序: %PYTHON_CMD% main.py
echo 5. (完成后) 退出虚拟环境: deactivate
GOTO :end

:venv_fail
echo 创建虚拟环境失败。请尝试使用 'manual' 模式运行。
GOTO :fail

:activate_fail
echo 激活虚拟环境失败。请尝试使用 'manual' 模式运行。
GOTO :fail

:deps_fail
echo 安装依赖失败。请检查 requirements.txt 文件和网络连接。
echo 请尝试使用 'manual' 模式运行。
GOTO :fail

:fail
echo.
echo 脚本执行失败。
ENDLOCAL
exit /b 1

:end
ENDLOCAL
exit /b 0