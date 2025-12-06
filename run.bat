@echo off
REM Run geoclip_pipeline with the correct virtual environment
cd /d "%~dp0"
call geoclip-env\Scripts\activate.bat
python geoclip_pipeline.py
pause
