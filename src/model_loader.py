import joblib
from pathlib import Path


def load_model():
    # Find the main FraudLens-AI project folder
    project_root = Path(__file__).resolve().parent.parent

    # Path to our trained Random Forest model
    model_path = project_root / "models" / "fraudlens_random_forest.pkl"

    # Load the trained model
    model = joblib.load(model_path)

    return model


if __name__ == "__main__":
    model = load_model()
    print("FraudLens model loaded successfully!")