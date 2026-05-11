@echo off
chcp 65001 >nul
echo ========================================
echo   图像处理工具箱 - 打包为 EXE
echo ========================================
echo.

pip install pyqt5 opencv-python numpy pyinstaller
echo.
echo 开始打包...
pyinstaller --onefile --windowed --add-data "resources;resources" --name "ImageTool" main.py

echo.
if exist "dist\ImageTool.exe" (
    echo ========================================
    echo   打包成功！
    echo   EXE 文件位置: dist\ImageTool.exe
    echo ========================================
) else (
    echo ========================================
    echo   打包失败，请检查错误信息。
    echo ========================================
)
pause
