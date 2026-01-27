# Verificar se o ambiente existe
if (-not (Test-Path "venv")) {
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    & "$PSScriptRoot\setup_venv.ps1"
}

# Ativar ambiente
.\venv\Scripts\Activate.ps1

# Executar app
python -m streamlit run app.py