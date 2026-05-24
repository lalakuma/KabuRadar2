@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src;%PYTHONPATH%

python "%ROOT_DIR%\scripts\publish_results.py" || goto :fail
echo.
echo Next: commit docs\data.json and push to update the site.
endlocal & exit /b 0

:fail
echo Failed: publish_results.bat
endlocal & exit /b 1
