@echo off
set "file=%~nx1"
set "name=%~n1"
set "ext=%~x1"
pyinstaller.exe --log-level ERROR %file% -F
move /Y dist\%name%.exe %name%.exe
RD /S /Q dist
RD /S /Q build
RD /S /Q __pycache__
del /Q %name%.spec