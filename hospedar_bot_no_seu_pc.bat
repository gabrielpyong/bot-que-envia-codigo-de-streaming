@echo off
title Bot de Codigos de Verificacao

REM Define o diretório do script (ajuste conforme necessário)
set "BOT_DIR=%~dp0"
cd /d "%BOT_DIR%"

REM Tenta encontrar o Python no sistema
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python nao encontrado. Certifique-se de que o Python esta instalado e adicionado ao PATH.
    pause
    exit /b 1
)

REM Executa o bot
python botqueenviacodigo.py
if %ERRORLEVEL% neq 0 (
    echo Ocorreu um erro ao executar o bot. Verifique o script ou as dependencias.
    pause
    exit /b 1
)

pause