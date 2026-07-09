@echo off
cd /d "%~dp0"

echo Building site...
python scripts\build.py

start "Karel Voden Admin" python admin_server.py
timeout /t 1 /nobreak >nul

start "" http://localhost:8040/
start "" http://localhost:8050/admin

echo.
echo Site:  http://localhost:8040/
echo Admin: http://localhost:8050/admin
echo.
echo Closing this window stops the site server. The admin panel runs in its own window.
python -m http.server 8040 --directory dist
