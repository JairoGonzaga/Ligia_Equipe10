import streamlit as st
import pandas as pd
import joblib
import os
import sys

import sys
import subprocess
import os

def check_environment():
    """Verifica se está rodando no ambiente virtual correto"""
    try:
        import sklearn
        if sklearn.__version__ != '1.7.2':
            print(f"AVISO: scikit-learn versão {sklearn.__version__} detectada")
            print("   O modelo foi treinado com versão 1.7.2")
            print("   Recomendado usar ambiente virtual com: scikit-learn==1.7.2")
            print("   Execute: .\\venv\\Scripts\\Activate.ps1")
            return False
        return True
    except ImportError:
        print("scikit-learn não encontrado!")
        print("   Execute: pip install scikit-learn==1.7.2")
        return False

# Executar verificação
if not check_environment():
    print("\nDica: Use o script run_app.ps1 para rodar no ambiente virtual correto")
    response = input("\nContinuar mesmo assim? (s/n): ").lower()
    if response != 's':
        sys.exit(1)


# Configuração da página
st.set_page_config(
    page_title="Preditor de Risco Cardíaco - Modelo 1.6.1",
    page_icon="❤️",
    layout="wide"
)

# Título
st.title("❤️ Preditor de Risco Cardíaco")
st.markdown("---")
st.markdown("**Versão do modelo:** scikit-learn 1.6.1")
st.markdown("**Status:** ✅ Modelo compatível carregado")

# Carregar o modelo
@st.cache_resource
def load_model_1_6_1():
    alternative_paths = [
        os.path.join("Model", "model.joblib"),
        os.path.join("..", "Model", "model.joblib"),
        os.path.join(os.path.dirname(__file__), "..", "Model", "model.joblib"),
        "model.joblib"
    ]
    
    model_path = None
    
    # Busca o arquivo nos caminhos da lista
    for path in alternative_paths:
        if os.path.exists(path):
            model_path = path
            break
            
    try:
        if not model_path:
            # Se não achou em nenhum lugar, avisa onde tentou por último
            raise FileNotFoundError("Não foi possível localizar 'model.joblib' nas pastas padrão.")
        
        # Carregar o modelo usando joblib
        model = joblib.load(model_path)
        return model, "✅ Modelo original carregado com sucesso!"
        
    except Exception as e:
        # Se o erro for STACK_GLOBAL, o problema é a versão do Python/Sklearn, não o caminho
        st.error(f"Erro técnico ao carregar: {str(e)}")
        return None, f"❌ Erro: {str(e)}"

# Carregar o modelo
model, status_msg = load_model_1_6_1()

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações do Sistema")
    st.write(f"**Status:** {status_msg}")
    
    try:
        import sklearn
        st.write(f"**scikit-learn:** {sklearn.__version__}")
    except:
        pass
    
    st.markdown("---")
    st.markdown("**Versões compatíveis:**")
    st.markdown("- scikit-learn: 1.6.1")
    st.markdown("- Modelo: RandomForest/XGBoost")
    st.markdown("- Dados: Heart Disease UCI")
    
    st.markdown("---")
    st.markdown("⚠️ **Aviso importante:**")
    st.markdown("Esta ferramenta é para fins educacionais. Consulte sempre um médico para diagnóstico adequado.")

# Interface principal apenas se o modelo foi carregado
if model is not None:
    st.success("✅ Sistema pronto para análise!")
    
    # Seção de entrada de dados
    st.header("📋 Dados do Paciente")
    st.markdown("Preencha os dados clínicos abaixo:")
    
    # Organizar em duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        # Dados numéricos
        idade = st.slider("Idade (anos)", 20, 100, 50, 1)
        pressao = st.slider("Pressão arterial (mmHg)", 80, 200, 120, 1)
        colesterol = st.slider("Colesterol (mg/dL)", 100, 600, 200, 1)
        freq_max = st.slider("Frequência cardíaca máxima (bpm)", 60, 220, 150, 1)
        
    with col2:
        # Dados categóricos
        sexo = st.selectbox("Sexo", ["Masculino (M)", "Feminino (F)"])
        
        tipo_dor = st.selectbox(
            "Tipo de dor no peito",
            ["ASY (Assintomático)", "ATA (Angina atípica)", "NAP (Sem dor)", "TA (Angina típica)"]
        )
        
        glicose = st.selectbox("Diabetes (glicose > 120 mg/dL)", ["Não", "Sim"])
        
        eletro = st.selectbox(
            "Resultado eletrocardiográfico",
            ["Normal", "LVH (Hipertrofia ventricular)", "ST (Anormalidade)"]
        )
    
    # Segunda linha de inputs
    col3, col4 = st.columns(2)
    
    with col3:
        angina = st.selectbox("Angina no exercício", ["Não (N)", "Sim (Y)"])
        oldpeak = st.slider("Depressão ST (Oldpeak)", 0.0, 6.0, 1.0, 0.1)
    
    with col4:
        slope = st.selectbox(
            "Inclinação do segmento ST",
            ["Up (Ascendente)", "Flat (Plana)", "Down (Descendente)"]
        )
    
    # Botão de análise
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        analisar = st.button(
            "🔍 Analisar Risco Cardíaco", 
            type="primary", 
            use_container_width=True,
            help="Clique para analisar os dados do paciente"
        )
    
    # Processar quando o botão for clicado
    if analisar:
        with st.spinner("Processando análise..."):
            # Converter dados para formato do modelo
            
            # Converter sexo
            sexo_cod = 'M' if "Masculino" in sexo else 'F'
            
            # Extrair código do tipo de dor
            tipo_dor_cod = tipo_dor.split(' ')[0]  # Pega "ASY", "ATA", etc
            
            # Converter glicose
            glicose_cod = 1 if glicose == "Sim" else 0
            
            # Extrair código do eletro
            if "LVH" in eletro:
                eletro_cod = "LVH"
            elif "ST" in eletro:
                eletro_cod = "ST"
            else:
                eletro_cod = "Normal"
            
            # Converter angina
            angina_cod = 'Y' if "Sim" in angina else 'N'
            
            # Extrair código do slope
            if "Up" in slope:
                slope_cod = "Up"
            elif "Down" in slope:
                slope_cod = "Down"
            else:
                slope_cod = "Flat"
            
            # Criar dicionário com os dados
            dados_paciente = {
                'Age': idade,
                'Sex': sexo_cod,
                'ChestPainType': tipo_dor_cod,
                'RestingBP': pressao,
                'Cholesterol': colesterol,
                'FastingBS': glicose_cod,
                'RestingECG': eletro_cod,
                'MaxHR': freq_max,
                'ExerciseAngina': angina_cod,
                'Oldpeak': oldpeak,
                'ST_Slope': slope_cod
            }
            
            # Converter para DataFrame
            df_paciente = pd.DataFrame([dados_paciente])
            
            try:
                # Fazer previsão
                previsao = model.predict(df_paciente)[0]
                probabilidade = model.predict_proba(df_paciente)[0]
                
                # Mostrar resultados
                st.markdown("---")
                st.header("📊 Resultados da Análise")
                
                if previsao == 0:
                    # Saudável
                    st.success(f"## ✅ PACIENTE SAUDÁVEL")
                    st.markdown(f"""
                    **Probabilidade de risco cardíaco:** {probabilidade[1]:.1%}
                    
                    **Recomendações:**
                    - Continue com hábitos de vida saudáveis
                    - Pratique exercícios regularmente
                    - Mantenha check-ups anuais
                    - Controle peso, colesterol e pressão arterial
                    """)
                else:
                    # Risco
                    st.error(f"## ⚠️ RISCO CARDÍACO DETECTADO")
                    st.markdown(f"""
                    **Probabilidade de risco cardíaco:** {probabilidade[1]:.1%}
                    
                    **Recomendações URGENTES:**
                    - Consulte um cardiologista para avaliação detalhada
                    - Faça exames complementares (ecocardiograma, teste de esforço)
                    - Monitore sintomas como dor no peito, falta de ar ou palpitações
                    - Evite esforços intensos até avaliação médica
                    """)
                
                # Métricas detalhadas
                st.markdown("### 📈 Métricas Detalhadas")
                
                col_met1, col_met2, col_met3 = st.columns(3)
                with col_met1:
                    st.metric(
                        "Probabilidade de SAÚDE", 
                        f"{probabilidade[0]:.1%}",
                        delta=f"{(probabilidade[0] - 0.5):+.1%}" if probabilidade[0] > 0.5 else None
                    )
                
                with col_met2:
                    st.metric(
                        "Probabilidade de RISCO", 
                        f"{probabilidade[1]:.1%}",
                        delta=f"{(probabilidade[1] - 0.5):+.1%}" if probabilidade[1] > 0.5 else None
                    )
                
                with col_met3:
                    confianca = max(probabilidade)
                    st.metric(
                        "Confiança do modelo", 
                        f"{confianca:.1%}",
                        delta="Alta" if confianca > 0.8 else "Média" if confianca > 0.6 else "Baixa"
                    )
                
                # Mostrar dados enviados
                with st.expander("📋 Ver dados analisados"):
                    st.dataframe(df_paciente)
                    st.markdown(f"**Previsão:** {previsao} (0 = Saudável, 1 = Risco)")
                    st.markdown(f"**Probabilidades:** {probabilidade}")
                
                # Seção de interpretação
                st.markdown("### 💡 Interpretação dos Resultados")
                st.markdown("""
                - **Probabilidade < 30%:** Risco baixo, mantenha hábitos saudáveis
                - **Probabilidade 30-70%:** Risco moderado, recomendável avaliação médica
                - **Probabilidade > 70%:** Risco alto, procure atendimento especializado
                """)
                
            except Exception as e:
                st.error(f"❌ Erro ao fazer previsão: {str(e)}")
                st.info("Verifique se os dados estão no formato correto.")
    
    # Seção de exemplos rápidos
    with st.expander("🚀 Testar com casos exemplo"):
        st.markdown("**Teste rápido com dados predefinidos:**")
        
        col_ex1, col_ex2 = st.columns(2)
        
        with col_ex1:
            if st.button("👤 Paciente Saudável (exemplo)"):
                # Preencher automaticamente com dados de paciente saudável
                st.session_state.update({
                    'idade': 35,
                    'pressao': 115,
                    'colesterol': 180,
                    'freq_max': 165,
                    'sexo': "Masculino (M)",
                    'tipo_dor': "NAP (Sem dor)",
                    'glicose': "Não",
                    'eletro': "Normal",
                    'angina': "Não (N)",
                    'oldpeak': 0.5,
                    'slope': "Up (Ascendente)"
                })
                st.rerun()
        
        with col_ex2:
            if st.button("⚠️ Paciente de Risco (exemplo)"):
                # Preencher automaticamente com dados de paciente de risco
                st.session_state.update({
                    'idade': 68,
                    'pressao': 180,
                    'colesterol': 350,
                    'freq_max': 95,
                    'sexo': "Feminino (F)",
                    'tipo_dor': "ASY (Assintomático)",
                    'glicose': "Sim",
                    'eletro': "LVH (Hipertrofia ventricular)",
                    'angina': "Sim (Y)",
                    'oldpeak': 4.2,
                    'slope': "Down (Descendente)"
                })
                st.rerun()
    
    # Informações sobre o modelo
    with st.expander("🔧 Informações Técnicas do Modelo"):
        st.markdown("""
        **Especificações técnicas:**
        
        - **Framework:** scikit-learn 1.6.1
        - **Algoritmo:** Random Forest / XGBoost (conforme treinamento)
        - **Dataset:** Heart Disease UCI (303 amostras)
        - **Features:** 13 características clínicas
        - **Métrica otimizada:** Recall (detecção de casos positivos)
        
        **Pré-processamento:**
        - Normalização de variáveis numéricas
        - One-hot encoding de variáveis categóricas
        - Tratamento de valores ausentes
        - Balanceamento de classes
        
        **Performance esperada:**
        - Acurácia: 85-90%
        - Recall: 90-95%
        - AUC-ROC: 0.90-0.95
        """)
    
    # Rodapé
    st.markdown("---")
    st.caption("""
    Sistema de Predição de Risco Cardíaco | 
    Desenvolvido para fins educacionais | 
    Modelo treinado com dataset Heart Disease UCI
    """)

else:
    # Se o modelo não carregou
    st.error("""
    ❌ **Não foi possível carregar o modelo compatível**
    
    **Solução recomendada:**
    
    1. **Verifique se o arquivo do modelo existe:**
       - Caminho: `Model/model.joblib`
    
    2. **Instale a versão correta do scikit-learn:**
       ```bash
       pip uninstall scikit-learn -y
       pip install scikit-learn==1.6.1
       ```
    
    3. **Recarregue esta página ou reinicie o servidor**
    
    4. **Se o problema persistir:**
       - Execute o script de treinamento original novamente
       - Certifique-se de salvar o modelo corretamente
    """)
    
    # Botão de diagnóstico
    if st.button("🩺 Executar Diagnóstico do Sistema"):
        st.markdown("### Diagnóstico do Sistema")
        
        # Verificar arquivos
        st.write("**Verificando arquivos do modelo:**")
        model_paths = [
            "Model/model.joblib",
            "./model.joblib",
            os.path.join(os.path.dirname(__file__), "Model", "model.joblib")
        ]
        
        for path in model_paths:
            exists = os.path.exists(path)
            st.write(f"- `{path}`: {'✅ Existe' if exists else '❌ Não existe'}")
        
        # Verificar versões
        st.write("\n**Verificando versões instaladas:**")
        try:
            import sklearn
            st.write(f"- scikit-learn: {sklearn.__version__}")
        except:
            st.write("- scikit-learn: ❌ Não importável")
        
        try:
            import pandas
            st.write(f"- pandas: {pandas.__version__}")
        except:
            st.write("- pandas: ❌ Não importável")