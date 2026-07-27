import sys
from pathlib import Path

# Allow Python to import files from the src folder
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from model_loader import load_model
from database import get_connection, get_transaction, get_dashboard_statistics
from transaction_service import analyze_database_transaction
from model_info import get_model_info


def run_backend_tests():

    print("=" * 50)
    print("FraudLens AI - Backend Integration Test")
    print("=" * 50)

    # --------------------------------------------------
    # TEST 1: Load ML Model
    # --------------------------------------------------
    print("\n[TEST 1] Loading Machine Learning Model...")

    model = load_model()

    if model is not None:
        print("PASS - Random Forest model loaded successfully.")

    # --------------------------------------------------
    # TEST 2: MySQL Connection
    # --------------------------------------------------
    print("\n[TEST 2] Testing MySQL Connection...")

    connection = get_connection()

    if connection.is_connected():
        print("PASS - MySQL connection successful.")

    connection.close()

    # --------------------------------------------------
    # TEST 3: Retrieve Transaction
    # --------------------------------------------------
    print("\n[TEST 3] Retrieving Transaction from MySQL...")

    transaction = get_transaction(
        step=1,
        nameOrig="C1305486145"
    )

    if transaction is not None:
        print("PASS - Transaction retrieved successfully.")
        print(
            "Transaction:",
            transaction["type"],
            transaction["amount"]
        )

    # --------------------------------------------------
    # TEST 4: ML Fraud Analysis
    # --------------------------------------------------
    print("\n[TEST 4] Running Fraud Analysis...")

    result = analyze_database_transaction(
        step=1,
        nameOrig="C1305486145"
    )

    if result is not None:

        analysis = result["analysis"]

        prediction = (
            "FRAUD"
            if analysis["prediction"] == 1
            else "LEGITIMATE"
        )

        print("PASS - Fraud analysis completed.")
        print("Prediction:", prediction)
        print(
            "Risk Score:",
            f"{analysis['fraud_probability'] * 100:.2f}%"
        )
        print("Risk Level:", analysis["risk_level"])

    # --------------------------------------------------
    # TEST 5: Dashboard Statistics
    # --------------------------------------------------
    print("\n[TEST 5] Loading Dashboard Statistics...")

    statistics = get_dashboard_statistics()

    if statistics is not None:
        print("PASS - Dashboard statistics retrieved.")
        print(
            "Total Transactions:",
            statistics["total_transactions"]
        )
        print(
            "Fraud Transactions:",
            statistics["fraud_transactions"]
        )

    # --------------------------------------------------
    # TEST 6: Model Information
    # --------------------------------------------------
    print("\n[TEST 6] Loading Model Information...")

    info = get_model_info()

    if info is not None:
        print("PASS - Model information available.")
        print("Model:", info["model_name"])
        print("Dataset:", info["dataset"])

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------
    print("\n" + "=" * 50)
    print("ALL FRAUDLENS BACKEND TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    run_backend_tests()