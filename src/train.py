# Responsável por:
# - Carregar dados pré-processados
# - Treinar o modelo final escolhido
# - Organizar o pipeline (preprocessador + modelo)
# - Salvar o modelo treinado em formato .pkl
# - Deixar o código simples e reprodutível

import joblib
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline

# Importa a função de preparação dos dados
from preprocessing import prepare_data


def train_and_save_model(data_path: str, save_path: str = "../Model/model.pkl"):

    # 1) Carregamento dos dados já divididos e com pré-processador
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(data_path)

    # 2) Define o modelo final escolhido (XGBoost)
    model = XGBClassifier(
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5
    )

    # 3) Monta pipeline completo (pré-processamento + modelo)
    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model)
    ])

    # 4) Treinamento do pipeline
    pipeline.fit(X_train, y_train)

    # 5) Salva o pipeline final em arquivo .pkl
    joblib.dump(pipeline, save_path)

    print(f"Modelo salvo em: {save_path}")


if __name__ == "__main__":

    # Caminho do dataset bruto
    data_path = "../Data/heart.csv"

    # Executa o treinamento e salva o modelo
    train_and_save_model(data_path)
