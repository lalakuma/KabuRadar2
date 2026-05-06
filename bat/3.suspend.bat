@echo off
setlocal

echo This refactored script does not force system suspend by default.
echo To keep workspace-safe behavior, it only prints this message.
echo If you really need suspend, edit this file and enable power commands.

endlocal & exit /b 0
