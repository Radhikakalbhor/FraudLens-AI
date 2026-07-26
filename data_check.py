import pandas as pd

file_path = "data/raw/PS_20174392719_1491204439457_log.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFirst 5 transactions:")
print(df.head())
print("\n--- DATASET INFORMATION ---")
df.info()

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- TRANSACTION TYPES ---")
print(df["type"].value_counts())

print("\n--- FRAUD DISTRIBUTION ---")
print(df["isFraud"].value_counts())
print("\n--- FRAUD RATE ---")
fraud_rate = (df["isFraud"].sum() / len(df)) * 100
print(f"Fraud Rate: {fraud_rate:.4f}%")

print("\n--- FRAUD BY TRANSACTION TYPE ---")
fraud_by_type = df[df["isFraud"] == 1]["type"].value_counts()
print(fraud_by_type)

print("\n--- FLAGGED FRAUD ---")
print(df["isFlaggedFraud"].value_counts())