@echo off
setlocal

echo.
echo ==== ICT_TOURISM - Run script ==== 

REM Check for Python
python --version >nul 2>&1
if ERRORLEVEL 1 (
    echo Python no encontrado en la ruta. Instale Python 3.10+ y reintente.
    pause
    exit /b 1
)

REM Create virtual environment if missing
if not exist ".venv\Scripts\activate.bat" (
    echo Creando entorno virtual en .venv...
    python -m venv .venv
)

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Upgrade pip and install requirements if file exists
if exist requirements.txt (
    echo Instalando dependencias desde requirements.txt...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo No se encontró requirements.txt, omitiendo instalacion de dependencias.
)

echo Arrancando Streamlit (presiona CTRL+C para detener)...
streamlit run app.py

endlocal
