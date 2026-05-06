@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src

python "%ROOT_DIR%\src\kaburadar\launcher.py"

endlocal
