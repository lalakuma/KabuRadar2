@echo off
setlocal

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
set PYTHONPATH=%ROOT_DIR%\src;%PYTHONPATH%

python "%ROOT_DIR%\src\kaburadar\tasks\update_prices.py" --menu 1 || goto :fail
python "%ROOT_DIR%\src\kaburadar\tasks\screening_trade.py" LO || goto :fail

echo Completed: LO screening/trade flow
endlocal & exit /b 0

:fail
echo Failed: 2-2.KabuStation_kessai_GetYahooF.bat
endlocal & exit /b 1
