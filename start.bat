@echo off
echo ========================================
echo  SISTEMA DE PREDIÇÃO DE RISCO CARDÍACO
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.11 em: https://www.python.org/downloads/release/python-3119/
    echo.
    pause
    exit /b 1
)

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python detectado: %PYTHON_VERSION%

REM Verificar se é Python 3.11 (recomendado)
echo %PYTHON_VERSION% | findstr /r "^3\.11" >nul
if errorlevel 1 (
    echo AVISO: Recomendado usar Python 3.11 para compatibilidade
    echo Você tem: %PYTHON_VERSION%
    echo.
    echo Deseja continuar mesmo assim? (S/N)
    choice /c SN /n
    if errorlevel 2 (
        echo Instalação cancelada.
        pause
        exit /b 1
    )
)

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    echo Ambiente virtual criado!
) else (
    echo Ambiente virtual já existe.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
pip install --upgrade pip

REM Instalar pacotes do requirements.txt
if exist "requirements.txt" (
    echo Instalando pacotes do requirements.txt...
    pip install -r requirements.txt
) else (
    echo AVISO: requirements.txt não encontrado!
    echo Instalando versões padrão...
    pip install streamlit==1.28.0 pandas==2.2.2 scikit-learn==1.6.1 joblib==1.5.3 numpy==2.0.2
)

REM Verificar instalação
echo.
echo ========================================
echo VERIFICANDO INSTALAÇÃO...
echo ========================================
python -c "
try:
    import numpy, pandas, sklearn, joblib, streamlit
    print('✅ numpy:', numpy.__version__)
    print('✅ pandas:', pandas.__version__)
    print('✅ scikit-learn:', sklearn.__version__)
    print('✅ joblib:', joblib.__version__)
    print('✅ streamlit:', streamlit.__version__)
    print('\n✅ Todas as bibliotecas instaladas com sucesso!')
except Exception as e:
    print('❌ Erro:', e)
"

echo.
echo ========================================
echo INICIANDO APLICATIVO...
echo ========================================
echo Acesse: http://localhost:8501
echo Pressione Ctrl+C para parar
echo ========================================
echo.

REM Executar o aplicativo
python -m streamlit run app.py

REM Manter janela aberta após erro
if errorlevel 1 (
    echo.
    echo O aplicativo foi encerrado com erro.
    pause
)