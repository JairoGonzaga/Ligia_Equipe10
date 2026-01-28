# 🏥 Lígia: Predição de Risco Cardiovascular - Equipe 10

Este projeto foi desenvolvido como parte do desafio **Lígia**, focado na criação de uma solução inteligente de Machine Learning para auxiliar profissionais de saúde na identificação precoce de riscos cardiovasculares. A solução utiliza algoritmos de classificação para analisar dados clínicos e comportamentais, fornecendo uma probabilidade de risco para cada paciente.

O projeto inclui um dashboard interativo desenvolvido em **Streamlit**, que permite realizar predições em tempo real de forma simples e intuitiva.

---

## 📂 Estrutura do Repositório

O projeto está organizado da seguinte forma para facilitar a manutenção e o deploy:

* **`app.py`**: Arquivo principal que carrega a interface web do Streamlit e realiza a integração com o modelo.
* **`Model/`**: Contém o modelo treinado serializado (`model.joblib`), pronto para inferência.
* **`src/`**: Pasta com o código-fonte de suporte, incluindo o script `preprocessing.py` para tratamento de dados.
* **`Notebooks/`**: Registros do processo de Análise Exploratória de Dados (EDA), limpeza e treinamento dos modelos experimentais.
* **`requirements.txt`**: Arquivo de configuração com todas as bibliotecas e versões necessárias para o projeto.

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar o ambiente em sua máquina:

### 1. Clonar o Repositório
```bash
git clone https://github.com/JairoGonzaga/Ligia_Equipe10.git
cd Ligia_Equipe10
```
# Instalar Dependências
Recomendamos o uso de um ambiente virtual:

Bash
```
python -m venv .venv
```
## No Windows:
```
.\.venv\Scripts\activate
```
## No Linux/Mac:
```
source .venv/bin/activate
```
## Instalando Requisitos
```
pip install -r requirements.txt
```
## Rodar o Dashboard
```
cd src
streamlit run inference.py
```
# Requisitos:
```
streamlit==1.53.1
pandas==2.3.3
scikit-learn==1.7.2
joblib==1.5.3
numpy==2.4.1
xgboost==3.1.3
matplotlib==3.10.8
seaborn==0.13.2
python == 3.12
```
🧠 Detalhes do Modelo
O modelo utiliza o algoritmo XGBoost, treinado para identificar padrões em variáveis como idade, colesterol, pressão arterial e nível de atividade física.

Nota: O modelo atual foi otimizado para a versão do scikit-learn 1.7.2. Caso ocorra um aviso de InconsistentVersionWarning, verifique as notas de versão no arquivo requirements.txt.

👥 Equipe 10
 - Jairo Gonzaga - jcgn
 - Victoria Pessoa - vpbm
 - Felipe de Labio
 - Jose Guilherme - jgtn
 - Ivan Bezerra - iceb
 - Maria beatriz
 - Thiago Jose - tjbmo
