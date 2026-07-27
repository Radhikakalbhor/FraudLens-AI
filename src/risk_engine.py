def get_risk_level(fraud_probability):
    risk_score = fraud_probability * 100

    if risk_score < 30:
        return "LOW"

    elif risk_score < 60:
        return "MEDIUM"

    elif risk_score < 80:
        return "HIGH"

    else:
        return "CRITICAL"


def get_recommended_action(risk_level):

    if risk_level == "LOW":
        return "Allow transaction with normal monitoring."

    elif risk_level == "MEDIUM":
        return "Monitor transaction and consider additional verification."

    elif risk_level == "HIGH":
        return "Flag transaction for manual fraud review."

    else:
        return "Immediately flag transaction and require fraud investigation."


if __name__ == "__main__":
    test_probability = 0.92

    risk_level = get_risk_level(test_probability)
    action = get_recommended_action(risk_level)

    print("Risk Score:", f"{test_probability * 100:.2f}%")
    print("Risk Level:", risk_level)
    print("Recommended Action:", action)