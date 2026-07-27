MODEL_INFO = {
    "model_name": "Random Forest Classifier",
    "dataset": "PaySim",
    "training_strategy": "Time-based validation",
    "number_of_trees": 100,
    "max_depth": 15,

    "random_split_metrics": {
        "precision": 0.9957,
        "recall": 0.9976,
        "f1_score": 0.9967
    },

    "temporal_validation_metrics": {
        "precision": 1.0000,
        "recall": 1.0000,
        "f1_score": 1.0000
    },

    "limitations": [
        "The model was trained and evaluated using the simulated PaySim dataset.",
        "Engineered balance-error features strongly influence model performance.",
        "Evaluation results should not be interpreted as real-world banking performance."
    ]
}


def get_model_info():
    return MODEL_INFO


if __name__ == "__main__":
    info = get_model_info()

    print("FraudLens Model Information")
    print("---------------------------")
    print("Model:", info["model_name"])
    print("Dataset:", info["dataset"])
    print("Training Strategy:", info["training_strategy"])

    print("\nRandom Split Evaluation:")
    print(
        f"Precision: "
        f"{info['random_split_metrics']['precision'] * 100:.2f}%"
    )
    print(
        f"Recall: "
        f"{info['random_split_metrics']['recall'] * 100:.2f}%"
    )
    print(
        f"F1 Score: "
        f"{info['random_split_metrics']['f1_score'] * 100:.2f}%"
    )

    print("\nTemporal Validation:")
    print(
        f"Precision: "
        f"{info['temporal_validation_metrics']['precision'] * 100:.2f}%"
    )
    print(
        f"Recall: "
        f"{info['temporal_validation_metrics']['recall'] * 100:.2f}%"
    )
    print(
        f"F1 Score: "
        f"{info['temporal_validation_metrics']['f1_score'] * 100:.2f}%"
    )

    print("\nImportant Limitations:")
    for limitation in info["limitations"]:
        print("-", limitation)