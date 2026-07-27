from database import get_transaction
from predictor import predict_transaction


def analyze_transaction(transaction_data):
    """
    Analyze transaction data using the FraudLens ML engine.
    """

    result = predict_transaction(
        transaction_type=transaction_data["type"],
        amount=transaction_data["amount"],
        oldbalanceOrg=transaction_data["oldbalanceOrg"],
        newbalanceOrig=transaction_data["newbalanceOrig"],
        oldbalanceDest=transaction_data["oldbalanceDest"],
        newbalanceDest=transaction_data["newbalanceDest"],
        step=transaction_data["step"]
    )

    return {
        "transaction": transaction_data,
        "analysis": result
    }


def analyze_database_transaction(step, nameOrig):
    """
    Retrieve a transaction from MySQL and analyze it.
    """

    transaction = get_transaction(step, nameOrig)

    if transaction is None:
        return None

    return analyze_transaction(transaction)


if __name__ == "__main__":

    result = analyze_database_transaction(
    step=276,
    nameOrig="C1715283297"
)

    if result is None:
        print("Transaction not found.")

    else:
        transaction = result["transaction"]
        analysis = result["analysis"]

        print("FraudLens Database Transaction Analysis")
        print("---------------------------------------")

        print("\nTransaction:")
        print("Sender:", transaction["nameOrig"])
        print("Receiver:", transaction["nameDest"])
        print("Type:", transaction["type"])
        print("Amount:", transaction["amount"])

        print("\nFraudLens Analysis:")
        print(
            "Prediction:",
            "FRAUD" if analysis["prediction"] == 1 else "LEGITIMATE"
        )
        print(
            f"Fraud Probability: "
            f"{analysis['fraud_probability'] * 100:.2f}%"
        )
        print("Risk Level:", analysis["risk_level"])

        print("\nRisk Indicators:")
        for reason in analysis["risk_indicators"]:
            print("-", reason)

        print("\nRecommended Action:")
        print(analysis["recommended_action"])

        print("\nActual Historical Label:")
        print(
            "FRAUD"
            if transaction["isFraud"] == 1
            else "LEGITIMATE"
        )