import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_FILE = Path("results/oracle_performance.csv")
OUT_FILE = Path("results/oracle_performance_chart.png")

df = pd.read_csv(CSV_FILE)

plt.figure(figsize=(10, 6))
plt.bar(df["query"], df["avg_ms"])

plt.xlabel("Query scenario")
plt.ylabel("Average execution time (ms)")
plt.title("Oracle NoSQL Query Performance")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT_FILE, dpi=300)

print(f"Chart saved to: {OUT_FILE}")