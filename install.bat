@echo off

:: Verifica che Python sia installato
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python non è installato. Per favore installalo prima di continuare.
    pause
    exit /b 1
)

:: Verifica la versione di Python (almeno 3.12)
for /f "tokens=2 delims= " %%i in ('python --version') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%i in ("%PYTHON_VERSION%") do (
    set MAJOR=%%i
    set MINOR=%%j
)
IF %MAJOR% LSS 3 (
    echo Python deve essere almeno alla versione 3.12. Versione rilevata: %PYTHON_VERSION%.
    pause
    exit /b 1
)
IF %MAJOR%==3 IF %MINOR% LSS 12 (
    echo Python deve essere almeno alla versione 3.12. Versione rilevata: %PYTHON_VERSION%.
    pause
    exit /b 1
)

:: Verifica che pip sia installato
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip non è installato. Installazione di pip in corso...
    python -m ensurepip --upgrade
)

:: Verifica se numpy è installato e alla versione corretta
echo Verifica della versione di numpy...
python -c "import numpy; assert numpy.__version__ == '1.26.4', 'Versione errata: ' + numpy.__version__" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo numpy non è installato o non è alla versione corretta. Installazione/aggiornamento in corso...
    pip install numpy==1.26.4
) ELSE (
    echo numpy è già installato alla versione corretta.
)

:: Verifica che PyInstaller sia installato
pyinstaller --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller non è installato. Installazione in corso...
    pip install pyinstaller
)

:: Pulizia dei vecchi file di build
rmdir /s /q build
rmdir /s /q dist

:: Creazione del file eseguibile con PyInstaller
echo Creazione dell'eseguibile con PyInstaller...
pyinstaller --onefile --noconsole --add-data "Meta1;Meta1" --add-data "Meta2;Meta2" main.py

echo Operazione completata.
pause
