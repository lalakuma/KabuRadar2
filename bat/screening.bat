@echo off
setlocal

set SCRIPT_DIR=%~dp0

call "%SCRIPT_DIR%2-1.kabu_screening_trade_GetYahooF.bat" || goto :fail
call "%SCRIPT_DIR%2-2.KabuStation_kessai_GetYahooF.bat" || goto :fail

echo Completed: screening.bat
endlocal & exit /b 0

:fail
echo Failed: screening.bat
endlocal & exit /b 1
