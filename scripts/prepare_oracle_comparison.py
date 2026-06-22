import pandas as pd
from pathlib import Path

INPUT_FILE = Path("results/oracle_performance.csv")
OUTPUT_FILE = Path("results/oracle_performance_for_comparison.csv")

df = pd.read_csv(INPUT_FILE)

df.insert(0, "database", "Oracle NoSQL")

df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved comparison CSV to: {OUTPUT_FILE}")