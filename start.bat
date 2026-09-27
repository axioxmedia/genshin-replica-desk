@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"

if exist "app.py" if defined PY (
  if not exist ".venv\Scripts\python.exe" (
    %PY% -m venv .venv
  )
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  ".venv\Scripts\python.exe" app.py
  exit /b %ERRORLEVEL%
)

if exist "dist\GenshinReplicaDesk.exe" (
  start "" "%cd%\dist\GenshinReplicaDesk.exe"
  exit /b 0
)

echo [ERROR] Python was not found, and no built exe is present.
pause
exit /b 1
