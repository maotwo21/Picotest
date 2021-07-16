@echo off
pyinstaller -F Learn.py
rd /s /q build
rd /s /q __pycache__
cd dist
move Learn.exe %~dp0
cd %~dp0
rd /s /q dist
del /q Learn.spec
pause