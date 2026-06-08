@echo off
title Video Subtitle Generator - Environment Check

echo =====================================
echo VIDEO SUBTITLE GENERATOR
echo ENVIRONMENT CHECK
echo =====================================
echo.

echo [1/7] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found.
    pause
    exit /b
)

echo.
echo [2/7] Checking Pip...
pip --version
if errorlevel 1 (
    echo ERROR: Pip not found.
    pause
    exit /b
)

echo.
echo [3/7] Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: FFmpeg not found in PATH.
) else (
    echo FFmpeg Found.
)

echo.
echo [4/7] Checking Backend Dependencies...

python -c "import fastapi"
if errorlevel 1 echo Missing: fastapi

python -c "import uvicorn"
if errorlevel 1 echo Missing: uvicorn

python -c "import whisper"
if errorlevel 1 echo Missing: openai-whisper

python -c "import ffmpeg"
if errorlevel 1 echo Missing: ffmpeg-python

python -c "import multipart"
if errorlevel 1 echo Missing: python-multipart

echo.
echo [5/7] Checking Frontend Dependencies...

python -c "import flet"
if errorlevel 1 echo Missing: flet

python -c "import requests"
if errorlevel 1 echo Missing: requests

echo.
echo [6/7] Checking Port 8000...

netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo Port 8000 Available.
) else (
    echo WARNING: Port 8000 Already In Use.
)

echo.
echo [7/7] System Summary

echo.
echo Environment Check Completed.
echo.
echo If no errors are shown:
echo Project is ready to run.
echo.
pause