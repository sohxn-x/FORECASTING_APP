# energy_efficiency_plot.py
# Plot a single chart of energy efficiency (Efficiency Index) for all plants.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path("outputs_efficiency")
BASELINE_YEAR = None  # e.g., 2019; None = each plant's first year used as baseline

OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Load & basic checks
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
required = {"Date", "Plant", "Energy_Gcal_tcs"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}. Found: {list(df.columns)}")

# --- Annualize and compute Efficiency Index (baseline / SEC)
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
yearly = (df.groupby(["Plant","Year"], as_index=False)["Energy_Gcal_tcs"]
            .mean()
            .sort_values(["Plant","Year"]))

def add_efficiency(g):
    g = g.sort_values("Year").copy()
    if BASELINE_YEAR is not None and BASELINE_YEAR in g["Year"].values:
        baseline = float(g.loc[g["Year"] == BASELINE_YEAR, "Energy_Gcal_tcs"].iloc[0])
    else:
        baseline = float(g["Energy_Gcal_tcs"].iloc[0])
    g["Efficiency_Index"] = baseline / g["Energy_Gcal_tcs"].clip(lower=1e-12).astype(float)
    return g

enriched = yearly.groupby("Plant", group_keys=False).apply(add_efficiency)

# --- Single plot: Efficiency Index vs Year (all plants)
plt.figure(figsize=(9, 5))
for plant, g in enriched.groupby("Plant"):
    g = g.sort_values("Year")
    plt.plot(g["Year"], g["Efficiency_Index"], marker="o", label=plant)

plt.title("Energy Efficiency Pattern — Efficiency Index (baseline / Gcal per tcs)")
plt.xlabel("Year")
plt.ylabel("Efficiency Index (higher is better)")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2, fontsize=8)
plt.tight_layout()

out_path = OUT_DIR / "energy_efficiency_plot.png"
plt.savefig(out_path, dpi=160)
plt.show()  # remove this line if running headless
print(f"[OK] Saved plot to: {out_path.resolve()}")
