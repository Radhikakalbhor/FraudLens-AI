import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# Connect to MySQL
# --------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


# --------------------------------------------------
# Fetch one specific transaction
# --------------------------------------------------
def get_transaction(step, nameOrig):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        step,
        type,
        amount,
        nameOrig,
        oldbalanceOrg,
        newbalanceOrig,
        nameDest,
        oldbalanceDest,
        newbalanceDest,
        isFraud,
        isFlaggedFraud
    FROM transactions
    WHERE step = %s
      AND nameOrig = %s
    LIMIT 1;
    """

    cursor.execute(query, (step, nameOrig))
    transaction = cursor.fetchone()

    cursor.close()
    connection.close()

    return transaction


# --------------------------------------------------
# Fetch recent transactions
# --------------------------------------------------
def get_recent_transactions(limit=10):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        step,
        type,
        amount,
        nameOrig,
        nameDest,
        isFraud,
        isFlaggedFraud
    FROM transactions
    ORDER BY step DESC
    LIMIT %s;
    """

    cursor.execute(query, (limit,))
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions


# --------------------------------------------------
# Fetch high-value transactions
# --------------------------------------------------
def get_high_value_transactions(min_amount=1000000, limit=10):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        step,
        type,
        amount,
        nameOrig,
        nameDest,
        isFraud,
        isFlaggedFraud
    FROM transactions
    WHERE amount >= %s
    ORDER BY amount DESC
    LIMIT %s;
    """

    cursor.execute(query, (min_amount, limit))
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions


# --------------------------------------------------
# Dashboard KPI statistics
# --------------------------------------------------
def get_dashboard_statistics():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        COUNT(*) AS total_transactions,
        SUM(isFraud) AS fraud_transactions,
        ROUND(
            (SUM(isFraud) / COUNT(*)) * 100,
            4
        ) AS fraud_rate_percent,
        ROUND(SUM(amount), 2) AS total_transaction_amount,
        ROUND(AVG(amount), 2) AS average_transaction_amount
    FROM transactions;
    """

    cursor.execute(query)
    statistics = cursor.fetchone()

    cursor.close()
    connection.close()

    return statistics


# --------------------------------------------------
# Fraud statistics by transaction type
# --------------------------------------------------
def get_fraud_by_type():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        type,
        COUNT(*) AS total_transactions,
        SUM(isFraud) AS fraud_transactions,
        ROUND(
            (SUM(isFraud) / COUNT(*)) * 100,
            4
        ) AS fraud_rate_percent
    FROM transactions
    GROUP BY type
    ORDER BY fraud_transactions DESC;
    """

    cursor.execute(query)
    statistics = cursor.fetchall()

    cursor.close()
    connection.close()

    return statistics


# --------------------------------------------------
# Fraud trend across time
# --------------------------------------------------
def get_fraud_trend():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        step,
        COUNT(*) AS total_transactions,
        SUM(isFraud) AS fraud_transactions
    FROM transactions
    GROUP BY step
    ORDER BY step;
    """

    cursor.execute(query)
    trend = cursor.fetchall()

    cursor.close()
    connection.close()

    return trend


# --------------------------------------------------
# Fraud vs legitimate amount analytics
# --------------------------------------------------
def get_amount_analytics():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        isFraud,
        COUNT(*) AS transaction_count,
        ROUND(SUM(amount), 2) AS total_amount,
        ROUND(AVG(amount), 2) AS average_amount,
        ROUND(MIN(amount), 2) AS minimum_amount,
        ROUND(MAX(amount), 2) AS maximum_amount
    FROM transactions
    GROUP BY isFraud
    ORDER BY isFraud;
    """

    cursor.execute(query)
    analytics = cursor.fetchall()

    cursor.close()
    connection.close()

    return analytics


# --------------------------------------------------
# Test amount analytics
# --------------------------------------------------
if __name__ == "__main__":

    analytics = get_amount_analytics()

    print("FraudLens Amount Analytics")
    print("--------------------------")

    for row in analytics:

        category = (
            "FRAUD"
            if row["isFraud"] == 1
            else "LEGITIMATE"
        )

        print(f"\n{category}")
        print("Transaction Count:", row["transaction_count"])
        print("Total Amount:", row["total_amount"])
        print("Average Amount:", row["average_amount"])
        print("Minimum Amount:", row["minimum_amount"])
        print("Maximum Amount:", row["maximum_amount"])