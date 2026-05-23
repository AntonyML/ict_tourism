@echo off
setlocal enabledelayedexpansion

echo.
echo ==== ICT_TOURISM - Run script ====
echo.

REM Posicionarse en el directorio del .bat
cd /d "%~dp0"

set PYTHON_VENV=.venv\Scripts\python.exe

REM -----------------------------------------------------------------------
REM 1. Si el venv ya existe, usarlo directamente sin buscar Python en PATH
REM -----------------------------------------------------------------------
if exist "%PYTHON_VENV%" (
    echo [OK] Entorno virtual encontrado. Usando .venv\Scripts\python.exe
    goto install_deps
)

REM -----------------------------------------------------------------------
REM 2. El venv no existe: buscar Python para crearlo
REM -----------------------------------------------------------------------
echo Entorno virtual no encontrado. Buscando Python para crearlo...
echo.

set PYTHON_PATH=
set PYTHON_FOUND=0

python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_PATH=python
    set PYTHON_FOUND=1
    echo [OK] Python encontrado en PATH del sistema
    goto create_venv
)

for %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_PATH=%%D\python.exe"
        set PYTHON_FOUND=1
        echo [OK] Python encontrado en: !PYTHON_PATH!
        goto create_venv
    )
)

for %%D in ("C:\Program Files\Python3*" "C:\Program Files (x86)\Python3*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_PATH=%%D\python.exe"
        set PYTHON_FOUND=1
        echo [OK] Python encontrado en: !PYTHON_PATH!
        goto create_venv
    )
)

echo [ERROR] Python no encontrado y el entorno virtual tampoco existe.
echo         Instale Python desde https://www.python.org
echo         Marque "Add Python to PATH" durante la instalacion.
echo.
pause
exit /b 1

:create_venv
echo.
echo Creando entorno virtual .venv ...
"!PYTHON_PATH!" -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado.
echo.

REM -----------------------------------------------------------------------
REM 3. Instalar dependencias
REM -----------------------------------------------------------------------
:install_deps
echo Verificando dependencias...
"%PYTHON_VENV%" -m pip install --upgrade pip --quiet
if not exist requirements.txt (
    echo [ERROR] No se encontro requirements.txt en %CD%
    pause
    exit /b 1
)
"%PYTHON_VENV%" -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Fallo la instalacion de dependencias.
    echo.
    pause
    exit /b 1
)
echo [OK] Dependencias listas.
echo.

REM -----------------------------------------------------------------------
REM 4. Liberar puerto 8501 si hay instancia previa
REM -----------------------------------------------------------------------
for /f "tokens=5" %%P in ('netstat -ano 2^>nul ^| findstr ":8501 " ^| findstr "LISTENING"') do (
    taskkill /PID %%P /F >nul 2>&1
)

REM -----------------------------------------------------------------------
REM 5. Lanzar Streamlit
REM -----------------------------------------------------------------------
echo Iniciando aplicacion en http://localhost:8501
echo Presiona Ctrl+C para detener el servidor.
echo.

"%PYTHON_VENV%" -m streamlit run app.py --server.port 8501

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Streamlit termino con codigo %ERRORLEVEL%.
    echo.
)

pause
endlocal
