@echo off
chcp 65001 >nul
cd /d "%~dp0"
cls
echo.
echo    მათბოტი — მათემატიკა VII
echo    ─────────────────────────────
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo    [!] Python ვერ მოიძებნა.
    echo    ჩამოტვირთე: https://www.python.org/downloads/
    echo    დაინსტალირებისას მონიშნე "Add Python to PATH"
    echo.
    pause
    exit /b
)

python -c "import streamlit, anthropic, sklearn" >nul 2>nul
if errorlevel 1 (
    echo    პირველი გაშვება — ვამზადებ საჭირო პროგრამებს.
    echo    ეს 1-2 წუთს გასტანს, დაელოდე...
    echo.
    python -m pip install -q -r requirements.txt
    echo    მზადაა.
    echo.
)

if exist .env (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do set %%a=%%b
)

if "%ANTHROPIC_API_KEY%"=="" (
    echo    საჭიროა Anthropic-ის API გასაღები.
    echo    აიღე აქედან: https://console.anthropic.com
    echo.
    set /p key="   ჩასვი გასაღები და დააჭირე Enter: "
    echo ANTHROPIC_API_KEY=%key%> .env
    set ANTHROPIC_API_KEY=%key%
    echo.
    echo    შენახულია — მეორედ აღარ მოგიწევს.
    echo.
)

echo    ვუშვებ... ბრაუზერი თავისით გაიხსნება.
echo    (გასაჩერებლად დააჭირე Ctrl+C)
echo.

python -m streamlit run app.py
pause
