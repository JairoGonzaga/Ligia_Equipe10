Write-Host "CONFIGURANDO AMBIENTE VIRTUAL SIMPLIFICADO" -ForegroundColor Green
Write-Host "=" * 50

# Criar ambiente virtual
python -m venv venv --clear

# Ativar
.\venv\Scripts\Activate.ps1

# Atualizar pip
python -m pip install --upgrade pip

# Instalar versões compatíveis com Python 3.13
pip install scikit-learn==1.6.1
pip install streamlit==1.40.0
pip install pandas==2.2.3
pip install joblib==1.3.2
pip install numpy==1.26.4

Write-Host ""
Write-Host "AMBIENTE CONFIGURADO!" -ForegroundColor Green
Write-Host "Para ativar: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "Para rodar: python -m streamlit run app.py" -ForegroundColor Yellow