@echo off
REM Thunderwolf Citadel — local http server (textures + ES modules work here)
cd /d "%~dp0"
echo.
echo  Thunderwolf Citadel
echo  --------------------
echo  Serving: %cd%
echo  Open:    http://localhost:8765/
echo  Play:    http://localhost:8765/index.html
echo.
echo  Press Ctrl+C to stop.
echo.
where py >nul 2>nul && (
  start "" "http://localhost:8765/index.html"
  py -m http.server 8765
  goto :eof
)
where python >nul 2>nul && (
  start "" "http://localhost:8765/index.html"
  python -m http.server 8765
  goto :eof
)
echo ERROR: Python not found. Install Python or open index.html after fixing file:// limits.
pause
