@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src;%PYTHONPATH%

python "%ROOT_DIR%\src\kaburadar\tasks\analyze_all.py" --publish || goto :fail
echo Completed: analyze + GitHub Pages update
endlocal & exit /b 0

:fail
echo Failed: analyze_and_publish.bat
endlocal & exit /b 1
