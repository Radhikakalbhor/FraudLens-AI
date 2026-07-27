import pandas as pd
from model_loader import load_model
from risk_engine import get_risk_level, get_recommended_action
from fraud_explainer import explain_transaction


model = load_model()


def prepare_transaction(
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest,
    step
):
    # Convert PaySim step into day and hour
    day = ((step - 1) // 24) + 1
    hour = (step - 1) % 24

    # Calculate the same engineered features used during training
    orig_balance_error = newbalanceOrig - (oldbalanceOrg - amount)
    dest_balance_error = newbalanceDest - (oldbalanceDest + amount)

    transaction = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "day": day,
        "hour": hour,
        "orig_balance_error": orig_balance_error,
        "dest_balance_error": dest_balance_error
    }])

    return transaction


def predict_transaction(
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest,
    step
):
    transaction = prepare_transaction(
        transaction_type,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        step
    )

    # Predict 0 = legitimate, 1 = fraud
    prediction = model.predict(transaction)[0]

    # Get probability of fraud
    fraud_probability = model.predict_proba(transaction)[0][1]
    risk_level = get_risk_level(fraud_probability)
    recommended_action = get_recommended_action(risk_level)
    risk_indicators = explain_transaction(
        transaction_type,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest
    )

    return {
        "prediction": int(prediction),
        "fraud_probability": float(fraud_probability),
        "risk_level": risk_level,
        "risk_indicators": risk_indicators,
        "recommended_action": recommended_action
    }

if __name__ == "__main__":
    result = predict_transaction(
    transaction_type="PAYMENT",
    amount=9839.64,
    oldbalanceOrg=170136.00,
    newbalanceOrig=160296.36,
    oldbalanceDest=0.00,
    newbalanceDest=0.00,
    step=1
)

    print("FraudLens Prediction")
    print("--------------------")
    print("Prediction:", "FRAUD" if result["prediction"] == 1 else "LEGITIMATE")
    print(f"Fraud Probability: {result['fraud_probability'] * 100:.2f}%")
    print("Risk Level:", result["risk_level"])

    print("\nRisk Indicators:")
    for reason in result["risk_indicators"]:
        print("-", reason)

    print("\nRecommended Action:")
    print(result["recommended_action"])