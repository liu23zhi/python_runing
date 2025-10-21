@echo off
cd /d "%~dp0"


@REM 2. 检查第一个参数 (%1) 是否为 "debug" 或 "console"
@REM    /i 表示不区分大小写
if /i "%1"=="debug" (
    goto :build_debug
)
if /i "%1"=="console" (
    goto :build_debug
)

@REM 3. 默认构建 (Release) - 不带控制台
@REM    使用 --windowed (或 -w) 来确保不显示控制台
echo Building WITHOUT CONSOLE (Release Mode)...
pyinstaller --noconfirm --onefile --windowed --add-data "index.html;." --upx-dir=./upx "高德js在线地图+高德在线规划+多账号模式+3D地图-2.py"
goto :end

:build_debug
@REM 4. 调试构建 (Debug) - 带控制台
@REM    使用 --console (或 -c) 来显示控制台
echo Building WITH CONSOLE (Debug Mode)...
pyinstaller --noconfirm --onefile --console --add-data "index.html;." --upx-dir=./upx "高德js在线地图+高德在线规划+多账号模式+3D地图-2.py"
goto :end

:end
echo.
echo 打包完成！请在 dist 文件夹中查找生成的 exe 文件。
pause