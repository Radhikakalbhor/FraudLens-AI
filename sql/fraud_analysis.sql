USE fraudlens_db;

-- 1. Fraud Distribution
SELECT isFraud, COUNT(*) AS transaction_count
FROM transactions
GROUP BY isFraud;

-- 2. Fraud by Transaction Type
SELECT type, COUNT(*) AS fraud_count
FROM transactions
WHERE isFraud = 1
GROUP BY type
ORDER BY fraud_count DESC;

-- 3. Fraud Rate by Transaction Type
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND((SUM(isFraud) / COUNT(*)) * 100, 4) AS fraud_rate_percent
FROM transactions
GROUP BY type
ORDER BY fraud_rate_percent DESC;

-- 4. Fraudulent Transaction Amounts
SELECT
    type,
    COUNT(*) AS fraud_count,
    ROUND(AVG(amount), 2) AS avg_fraud_amount,
    ROUND(MIN(amount), 2) AS min_fraud_amount,
    ROUND(MAX(amount), 2) AS max_fraud_amount
FROM transactions
WHERE isFraud = 1
GROUP BY type;

-- 5. Existing Fraud Flag Effectiveness
SELECT
    COUNT(*) AS actual_frauds,
    SUM(isFlaggedFraud) AS flagged_frauds,
    ROUND((SUM(isFlaggedFraud) / COUNT(*)) * 100, 4) AS flag_rate_percent
FROM transactions
WHERE isFraud = 1;

-- 6. Top 10 Highest-Value Frauds
SELECT
    step, type, amount, nameOrig, nameDest, isFlaggedFraud
FROM transactions
WHERE isFraud = 1
ORDER BY amount DESC
LIMIT 10;

-- 7. Fraud by Time Step
SELECT
    step,
    COUNT(*) AS fraud_count
FROM transactions
WHERE isFraud = 1
GROUP BY step
ORDER BY fraud_count DESC
LIMIT 10;

-- 8. Fraud vs Legitimate Transaction Amounts
SELECT
    isFraud,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS avg_amount,
    ROUND(MIN(amount), 2) AS min_amount,
    ROUND(MAX(amount), 2) AS max_amount
FROM transactions
GROUP BY isFraud;

-- 9. Sender Balance Analysis
SELECT
    isFraud,
    ROUND(AVG(oldbalanceOrg), 2) AS avg_old_balance,
    ROUND(AVG(newbalanceOrig), 2) AS avg_new_balance
FROM transactions
GROUP BY isFraud;

-- 10. Balance Error Analysis
SELECT
    isFraud,
    ROUND(AVG(ABS(oldbalanceOrg - amount - newbalanceOrig)), 2)
        AS avg_origin_balance_error,
    ROUND(AVG(ABS(oldbalanceDest + amount - newbalanceDest)), 2)
        AS avg_destination_balance_error
FROM transactions
GROUP BY isFraud;