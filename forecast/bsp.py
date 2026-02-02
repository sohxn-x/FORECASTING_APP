import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load historical and forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical data for BSP ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Extend forecast with 2023 actual value ---
plant = "BSP"
last_year = historical.index[-1]
last_value = historical[plant].iloc[-1]

bsp_extended = pd.concat([
    pd.Series([last_value], index=[last_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(historical.index, historical[plant], label="Historical", linewidth=2)
plt.plot(bsp_extended.index, bsp_extended.values,
         label="Forecast", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_year, color='gray', linestyle=':', label="Forecast Start")

plt.title("BSP: Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: save the figure
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\bsp_forecast.png")

plt.show()

# --- Step 5: Forecast values ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

# --- Step 6: Sustainability Summary ---
print("""
🏭 Bhilai Steel Plant (BSP)

Overview:
Commissioned in 1955 and located in Chhattisgarh, BSP is India’s largest rail manufacturer and a key producer of structural steel. It’s a flagship SAIL unit with a massive integrated facility.

🌱 Sustainability Achievements:
- Achieved zero solid waste utilization by producing green paver tiles and eco bricks from steel slag.
- Operates a captive power plant via NSPCL (500+ MW capacity).
- Deployed 2 MW rooftop solar and is setting up 15–35 MW floating solar on reservoir water.
- Uses ZLD technologies and advanced wastewater recycling.
- Successfully implemented PCB waste disposal systems.

📈 Areas for Further Improvement:
- Expand floating solar to cover at least 50% of internal energy needs.
- Implement carbon capture for coke ovens and BF off-gases.
- Deploy AI-based predictive systems for air and water quality compliance.
""")
