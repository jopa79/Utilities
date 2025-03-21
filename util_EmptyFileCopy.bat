@echo off
echo Datei-Namen Exporter wird gestartet...

:: Prüfen ob Python installiert ist
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python konnte nicht gefunden werden!
    echo Bitte installieren Sie Python von https://www.python.org/downloads/
    echo.
    echo Drücken Sie eine beliebige Taste zum Beenden...
    pause >nul
    exit /b 1
)

:: Pfad zum Python-Skript - befindet sich im gleichen Verzeichnis wie die BAT-Datei
set SCRIPT_PATH=%~dp0util_EmptyFileCopy.py

:: Prüfen ob die Skriptdatei existiert
if not exist "%SCRIPT_PATH%" (
    echo FEHLER: Die Datei %SCRIPT_PATH% wurde nicht gefunden!
    echo Bitte stellen Sie sicher, dass sich die Python-Datei im gleichen Verzeichnis befindet.
    echo.
    echo Drücken Sie eine beliebige Taste zum Beenden...
    pause >nul
    exit /b 1
)

:: Python-Skript starten
echo Skript wird ausgeführt: %SCRIPT_PATH%
python "%SCRIPT_PATH%"

:: Falls ein Fehler auftritt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Es ist ein Fehler aufgetreten.
    echo Drücken Sie eine beliebige Taste zum Beenden...
    pause >nul
)

exit /b
