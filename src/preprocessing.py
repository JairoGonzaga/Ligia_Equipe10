# Responsável por:
# - Carregar o dataset
# - Fazer tratamentos iniciais (baseados na EDA)
# - Separar features numéricas e categóricas
# - Construir um pré-processador reutilizável (ColumnTransformer)
# - Fazer split treino/teste de forma estratificada
# - Retornar tudo pronto para a etapa de modelagem

# Obs.: NÃO treina modelo aqui. 

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# 1) Carregamento dos dados

def load_data(path: str) -> pd.DataFrame:

    #Lê o dataset a partir de um caminho (CSV) e retorna um DataFrame.

    df = pd.read_csv(path)
    return df


# 2) Tratamentos iniciais baseados nos insights

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    # Aplica correções simples no dataframe bruto, com base na EDA.

    # Principais decisões (EDA):
    # - RestingBP == 0: valor fisiologicamente improvável -> tratar como inválido
    # - Cholesterol == 0: valor improvável -> tratar como inválido

    # Estratégia adotada:
    # - Substituir zeros por NaN e depois imputar (mediana) no pipeline numérico.
    # Isso evita "vazamento" (o imputador é ajustado apenas no treino).
   

    df = df.copy()

    # Substitui valores inválidos (0) por NaN para serem imputados no pipeline
    if "RestingBP" in df.columns:
        df.loc[df["RestingBP"] == 0, "RestingBP"] = pd.NA

    if "Cholesterol" in df.columns:
        df.loc[df["Cholesterol"] == 0, "Cholesterol"] = pd.NA

    return df


# 3) Definição de grupos de features (EDA)

def get_feature_groups():

    # Retorna duas listas:
    # - features numéricas
    # - features categóricas

    # Importante:
    # - A variável alvo (HeartDisease) NÃO entra aqui.

    numerical_features = [
        "Age",
        "RestingBP",
        "Cholesterol",
        "MaxHR",
        "Oldpeak"
    ]

    categorical_features = [
        "Sex",
        "ChestPainType",
        "FastingBS",
        "RestingECG",
        "ExerciseAngina",
        "ST_Slope"
    ]

    return numerical_features, categorical_features


# 4) Construção do pré-processador

def build_preprocessor():
  
    # Cria o ColumnTransformer com pipelines separados para dados numéricos e categóricos.
   
    num_features, cat_features = get_feature_groups()

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    # Combina os pipelines por tipo de coluna
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, num_features),
            ("cat", categorical_pipeline, cat_features)
        ]
    )

    return preprocessor


# 5) Split treino/teste (estratificado)

def split_data(df: pd.DataFrame, target: str = "HeartDisease"):
    
    # Realiza a separação treino/teste de forma estratificada.
    
    X = df.drop(columns=[target])
    y = df[target]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


# 6) Função final: prepara tudo para modelagem

def prepare_data(path: str):
    # Pipeline completo de preparação dos dados:
    # - Carrega dataset
    # - Aplica preprocessamento inicial
    # - Realiza split treino/teste
    # - Retorna dados prontos para modelagem
    
    df = load_data(path)
    df = preprocess_dataframe(df)

    X_train, X_test, y_train, y_test = split_data(df)

    preprocessor = build_preprocessor()

    return X_train, X_test, y_train, y_test, preprocessor