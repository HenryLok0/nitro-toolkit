@echo off
echo Discord Nitro Generator + Checker 整合工具
echo ========================================
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤: 未找到 Python。請先安裝 Python。
    pause
    exit /b 1
)

REM 安裝必要的 Python 套件
echo 安裝必要的套件...
pip install requests colorama >nul 2>&1

echo 啟動整合工具...
echo.

REM 運行整合工具
python integrated_tool.py

echo.
echo 程序結束！
pause
