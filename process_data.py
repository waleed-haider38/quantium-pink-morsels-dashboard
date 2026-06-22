import glob
import pandas as pd

# 1. Direct sirf data folder ke andar saari CSV files ko target karo
csv_files = glob.glob("data/*.csv")

print("CSV files found:")
for file in csv_files:
    print(file)

if not csv_files:
    raise ValueError("No CSV files found in the 'data' directory. Check your path!")

all_dataframes = []

for file in csv_files:
    print(f"\nProcessing {file}...")
    df = pd.read_csv(file)

    # Normalize column names to lowercase to avoid any mismatch
    df.columns = df.columns.str.strip().str.lower()

    # Strict check: Exact match for 'pink morsel' to prevent partial string matches
    df = df[df["product"].astype(str).str.lower().str.strip() == "pink morsel"].copy()

    if df.empty:
        print(f"Skipping {file}: No 'pink morsel' records found.")
        continue

    # Clean price values (remove '$' sign) and cast to float
    df["price"] = df["price"].astype(str).replace(r"[\$,]", "", regex=True).astype(float)

    # Business Logic: Calculate total sales revenue (quantity * price)
    df["sales"] = df["quantity"].astype(float) * df["price"]

    # Select only the required enterprise columns
    df = df[["sales", "date", "region"]]
    all_dataframes.append(df)

if not all_dataframes:
    raise ValueError("CSV files were processed, but zero 'pink morsel' rows were extracted.")

# 2. Combine all datasets vertically and export to clean CSV
output = pd.concat(all_dataframes, ignore_index=True)
output.to_csv("formatted_output.csv", index=False)

print("\nPipeline executed successfully!")
print("Created: formatted_output.csv")
print(output.head())
print(f"Total rows extracted: {len(output)}")