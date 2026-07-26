CREATE DATABASE IF NOT EXISTS fraudlens_db;
USE fraudlens_db;

CREATE TABLE IF NOT EXISTS transactions (
    step INT,
    type VARCHAR(20),
    amount DOUBLE,
    nameOrig VARCHAR(20),
    oldbalanceOrg DOUBLE,
    newbalanceOrig DOUBLE,
    nameDest VARCHAR(20),
    oldbalanceDest DOUBLE,
    newbalanceDest DOUBLE,
    isFraud INT,
    isFlaggedFraud INT
);

CREATE OR REPLACE VIEW fraud_transactions AS
SELECT *
FROM transactions
WHERE isFraud = 1;