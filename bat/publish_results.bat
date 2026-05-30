@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src;%PYTHONPATH%

python "%ROOT_DIR%\scripts\publish_results.py" %* || goto :fail
echo.
echo GitHub へ自動反映する場合: bat\analyze_and_publish.bat または --push オプション
endlocal & exit /b 0

:fail
echo Failed: publish_results.bat
endlocal & exit /b 1
