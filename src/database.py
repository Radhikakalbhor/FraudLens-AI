import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    return connection


if __name__ == "__main__":
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT type, COUNT(*) AS fraud_count
    FROM transactions
    WHERE isFraud = 1
    GROUP BY type;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    print("Fraud Transactions by Type:")

    for row in results:
        print(row)

    cursor.close()
    connection.close()
   