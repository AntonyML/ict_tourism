@echo off
setlocal enabledelayedexpansion

echo.
echo ==== ICT_TOURISM - Run script ==== 
echo.

REM Buscar Python en ubicaciones comunes
set PYTHON_PATH=
set PYTHON_FOUND=0

REM 1. Verificar en PATH del sistema
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_PATH=python
    set PYTHON_FOUND=1
    echo [OK] Python encontrado en PATH del sistema
    goto python_found
)

REM 2. Buscar en Program Files
for %%D in (C:\Program Files\Python* C:\Program Files (x86)\Python*) do (
    if exist "%%D\python.exe" (
        set PYTHON_PATH=%%D\python.exe
        set PYTHON_FOUND=1
        echo [OK] Python encontrado en: !PYTHON_PATH!
        goto python_found
    )
)

REM 3. Buscar en AppData
for %%D in (%APPDATA%\..\Local\Programs\Python\*) do (
    if exist "%%D\python.exe" (
        set PYTHON_PATH=%%D\python.exe
        set PYTHON_FOUND=1
        echo [OK] Python encontrado en: !PYTHON_PATH!
        goto python_found
    )
)

REM Python no encontrado
if %PYTHON_FOUND% equ 0 (
    echo.
    echo [ERROR] Python no encontrado en el sistema.
    echo.
    echo Opciones:
    echo 1. Descargar Python desde: https://www.python.org/downloads/
    echo 2. IMPORTANTE: Marcar "Add Python to PATH" durante la instalacion
    echo 3. Reiniciar esta ventana despues de instalar Python
    echo.
    pause
    exit /b 1
)

:python_found
echo.

REM Crear entorno virtual si no existe
if not exist ".venv\Scripts\activate.bat" (
    echo Creando entorno virtual en .venv...
    !PYTHON_PATH! -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
)

REM Usar Python del venv
set PYTHON_VENV=.venv\Scripts\python.exe

echo Instalando/actualizando dependencias...
%PYTHON_VENV% -m pip install --upgrade pip >nul 2>&1
if exist requirements.txt (
    %PYTHON_VENV% -m pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Fallo al instalar dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
) else (
    echo [ADVERTENCIA] No se encontro requirements.txt
)

echo.
echo Liberando puerto 8501 si existe instancia anterior de Streamlit...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8501" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo [OK] Iniciando aplicacion en http://localhost:8501
echo Presiona Ctrl+C para detener el servidor
echo.

%PYTHON_VENV% -m streamlit run app.py --server.port 8501

endlocal
