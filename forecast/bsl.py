import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load historical + forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical data for BSL ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Extend forecast to include last actual (2023) value ---
plant = "BSL"
last_year = historical.index[-1]
last_value = historical[plant].iloc[-1]

bsl_extended = pd.concat([
    pd.Series([last_value], index=[last_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(historical.index, historical[plant], label="Historical", linewidth=2)
plt.plot(bsl_extended.index, bsl_extended.values,
         label="Forecast", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_year, color='gray', linestyle=':', label="Forecast Start")

plt.title("BSL: Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: save the plot
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\bsl_forecast.png")

plt.show()

# --- Step 5: Forecast values ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

# --- Step 6: Summary ---
print("""
🏭 Bokaro Steel Plant (BSL)

Overview:
Located in Jharkhand, BSL is a major integrated steel plant under SAIL and a leading producer of cold-rolled and galvanized products, serving automobile and consumer goods industries.

🌱 Sustainability Achievements:
- Partnered with BPSCL (joint venture with DVC) for efficient steam/power generation.
- Installed slag-to-tile Green Paver Plant in 2025, converting 100% solid waste into 2,000 eco-tiles daily.
- Significantly reduced coke rate and specific energy consumption via process gas recovery.
- Practicing internal water recycling and improved wastewater handling.

📈 Areas for Further Improvement:
- Expand slag-based tile production for external sales and urban use.
- Shift part of production to electric arc furnace using scrap steel to lower emissions.
- Apply digital twin simulations and smart meters for energy/water tracking.
""")
