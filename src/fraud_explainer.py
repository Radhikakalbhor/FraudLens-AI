def explain_transaction(
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
):
    reasons = []

    # Calculate balance inconsistencies
    orig_balance_error = newbalanceOrig - (oldbalanceOrg - amount)
    dest_balance_error = newbalanceDest - (oldbalanceDest + amount)

    # Check transaction type
    if transaction_type in ["TRANSFER", "CASH_OUT"]:
        reasons.append(
            f"{transaction_type} transactions showed higher fraud risk in historical data."
        )

    # Check transaction amount
    if amount >= 200000:
        reasons.append(
            "The transaction amount is relatively large."
        )

    # Check sender balance behaviour
    if abs(orig_balance_error) > 1000:
        reasons.append(
            "The sender's balance movement is inconsistent with the transaction amount."
        )

    # Check destination balance behaviour
    if transaction_type in ["TRANSFER", "CASH_OUT"] and abs(dest_balance_error) > 1000:
        reasons.append(
            "The destination account balance movement is inconsistent with the transaction amount."
        )

    # Check if sender account was emptied
    if oldbalanceOrg > 0 and newbalanceOrig == 0:
        reasons.append(
            "The transaction reduced the sender's balance to zero."
        )

    if not reasons:
        reasons.append(
            "No major rule-based risk indicators were identified."
        )

    return reasons


if __name__ == "__main__":
    reasons = explain_transaction(
        transaction_type="TRANSFER",
        amount=181.00,
        oldbalanceOrg=181.00,
        newbalanceOrig=0.00,
        oldbalanceDest=0.00,
        newbalanceDest=0.00
    )

    print("FraudLens Risk Indicators")
    print("-------------------------")

    for reason in reasons:
        print("-", reason)