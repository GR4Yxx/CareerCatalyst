@echo off
echo Installing required dependencies...
pip install aiohttp==3.8.5

echo.
echo Running resume upload test...
echo.
python -m app.scripts.test_resume_upload

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Test completed successfully!
) else (
    echo.
    echo Test failed with error code %ERRORLEVEL%
)

echo.
echo Press any key to exit...
pause > nul 