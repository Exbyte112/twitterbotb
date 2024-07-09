@echo off
title Exbyte Signup Bot
color 0A

:: Clear the screen
cls

:: Set the name for the virtual environment
set VENV_DIR=venv

:: Check if the virtual environment exists
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate the virtual environment and install required packages
call %VENV_DIR%\Scripts\activate && (
    echo Installing required packages from requirements.txt...
    pip install -r requirements.txt
    
    :: Clear the screen after installation
    cls
    
    :: Run the Python script
    python accountgen.py
)

:: Pause the terminal window before closing (optional)
pause
