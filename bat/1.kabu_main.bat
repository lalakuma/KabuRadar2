@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src;%PYTHONPATH%

python "%ROOT_DIR%\src\kaburadar\launcher.py"
set EXIT_CODE=%ERRORLEVEL%

endlocal & exit /b %EXIT_CODE%
