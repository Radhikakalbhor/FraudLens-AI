from database import (
    get_dashboard_statistics,
    get_recent_transactions,
    get_high_value_transactions,
    get_fraud_by_type,
    get_fraud_trend,
    get_amount_analytics
)

from transaction_service import (
    analyze_transaction,
    analyze_database_transaction
)

from model_info import get_model_info


# --------------------------------------------------
# Dashboard overview
# --------------------------------------------------
def get_dashboard_data():
    """
    Collect the main analytics required by the
    FraudLens dashboard.
    """

    return {
        "statistics": get_dashboard_statistics(),
        "fraud_by_type": get_fraud_by_type(),
        "fraud_trend": get_fraud_trend(),
        "amount_analytics": get_amount_analytics()
    }


# --------------------------------------------------
# Recent transaction feed
# --------------------------------------------------
def get_transaction_feed(limit=10):
    return get_recent_transactions(limit=limit)


# --------------------------------------------------
# High-value transaction feed
# --------------------------------------------------
def get_high_value_feed(min_amount=1000000, limit=10):
    return get_high_value_transactions(
        min_amount=min_amount,
        limit=limit
    )


# --------------------------------------------------
# Analyze manually entered transaction
# --------------------------------------------------
def analyze_new_transaction(transaction_data):
    return analyze_transaction(transaction_data)


# --------------------------------------------------
# Analyze transaction stored in MySQL
# --------------------------------------------------
def analyze_existing_transaction(step, nameOrig):
    return analyze_database_transaction(
        step=step,
        nameOrig=nameOrig
    )


# --------------------------------------------------
# ML model information
# --------------------------------------------------
def get_ml_model_info():
    return get_model_info()


# --------------------------------------------------
# Test unified FraudLens backend
# --------------------------------------------------
if __name__ == "__main__":

    print("FraudLens Unified Backend Test")
    print("------------------------------")

    # Test dashboard statistics
    dashboard = get_dashboard_data()

    statistics = dashboard["statistics"]

    print("\nDashboard Statistics")
    print("Total Transactions:", statistics["total_transactions"])
    print("Fraud Transactions:", statistics["fraud_transactions"])
    print("Fraud Rate:", statistics["fraud_rate_percent"], "%")

    # Test transaction feed
    transactions = get_transaction_feed(limit=3)

    print("\nRecent Transactions")

    for transaction in transactions:
        print(transaction)

    # Test model information
    model_info = get_ml_model_info()

    print("\nML Model")
    print("Model:", model_info["model_name"])
    print("Dataset:", model_info["dataset"])

    print("\nFraudLens backend is working successfully!")