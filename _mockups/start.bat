@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

rem Намира Python: първо "python", после "py" (Windows launcher)
set PY=
python --version >nul 2>nul && set PY=python
if not defined PY (py --version >nul 2>nul && set PY=py)
if not defined PY (
    echo Python не е намерен. Инсталирай го от python.org и отбележи "Add Python to PATH".
    pause
    exit /b 1
)

echo Пускам макетите...
start "" http://127.0.0.1:8041/_mockups/g-prozhektor/index.html

echo.
echo   Визия Прожектор (нова):
echo     Начало:  http://127.0.0.1:8041/_mockups/g-prozhektor/index.html
echo     Книга:   http://127.0.0.1:8041/_mockups/g-prozhektor/kniga.html
echo     Български: добави ?lang=bg в края на адреса
echo.
echo   По-ранни варианти:
echo     А: http://127.0.0.1:8041/_mockups/a-titri.html
echo     Б: http://127.0.0.1:8041/_mockups/b-dosie.html
echo     В: http://127.0.0.1:8041/_mockups/c-shifar.html
echo.
echo Затварянето на този прозорец спира сървъра.
echo.
%PY% serve.py 8041
pause
