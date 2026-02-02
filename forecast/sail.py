import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("static", exist_ok=True)

# --- Step 1: Load historical and forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical average across all plants ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

sail_history = historical.mean(axis=1)

# --- Step 3: Extend SAIL forecast with 2023 actual point ---
plant = "All Plants Avg"
last_year = sail_history.index[-1]
last_value = sail_history.iloc[-1]

sail_extended = pd.concat([
    pd.Series([last_value], index=[last_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(sail_history.index, sail_history.values, label="Historical Avg", linewidth=2)
plt.plot(sail_extended.index, sail_extended.values,
         label="Forecast Avg", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_year, color='gray', linestyle=':', label="Forecast Start")

plt.title("SAIL (All Plants Avg): Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: save the figure
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\sail_forecast.png")
plt.show()

# --- Step 5: Forecast values ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

# --- Step 6: Group Sustainability Summary ---
print("""
🏢 Steel Authority of India Limited (SAIL) – Sustainability Summary

SAIL, one of India’s largest steelmakers, manages integrated steel plants across the country. It is actively pursuing decarbonization, energy efficiency, and circular economy practices.

🌱 Group Sustainability Highlights:
- Over 98% solid waste utilization across all plants.
- Installed 60+ MW of renewable energy and planning large-scale solar integration.
- Rolling out electric vehicles, smart meters, and AI-based quality control across sites.
- Active member of the Global Steel Climate Council (GSCC) and aligned with India's 2070 net-zero target.

📈 Group-Wide Suggestions:
- Invest in green hydrogen trials in collaboration with NTPC and IndianOil.
- Accelerate digital transformation to unify energy and environment data across plants.
- Set plant-wise carbon intensity benchmarks and publish annual public disclosures.
""")
