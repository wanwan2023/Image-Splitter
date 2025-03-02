@echo off
echo 正在清理旧的构建文件...
rmdir /s /q build
rmdir /s /q dist

echo 开始打包...
pyinstaller build_config.spec --noconfirm

echo 打包完成！
pause 