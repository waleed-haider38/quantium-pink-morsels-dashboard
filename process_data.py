import glob
import pandas as pd

# Find every CSV file in the repo, excluding virtual environment folders
csv_files = [
    file for file in glob.glob("**/*.csv", recursive=True)
    if "venv" not in file.lower() and ".venv" not in file.lower()
]

print("CSV files found:")
for file in csv_files:
    print(file)

if not csv_files:
    raise ValueError("No CSV files found anywhere in this repo.")

all_dataframes = []

for file in csv_files:
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    print(f"\nReading {file}")
    print("Columns:", list(df.columns))

    if "product" not in df.columns:
        print(f"Skipping {file}: no product column")
        continue

    print("Sample products:", df["product"].dropna().unique()[:20])

    # Keep rows where product contains "pink"
    df = df[df["product"].astype(str).str.lower().str.strip().str.contains("pink")].copy()

    if df.empty:
        print(f"No pink products found in {file}")
        continue

    # Clean price values like "$2.50"
    df["price"] = df["price"].astype(str).replace(r"[\$,]", "", regex=True).astype(float)

    # Calculate sales
    df["Sales"] = df["quantity"].astype(float) * df["price"]

    # Build required output
    df["Date"] = df["date"]
    df["Region"] = df["region"]

    df = df[["Sales", "Date", "Region"]]
    all_dataframes.append(df)

if not all_dataframes:
    raise ValueError("CSV files were found, but no pink product rows were found.")

output = pd.concat(all_dataframes, ignore_index=True)
output.to_csv("formatted_output.csv", index=False)

print("\nCreated formatted_output.csv")
print(output.head())
print(f"Total rows: {len(output)}")