import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load historical + forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical data for DSP ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Extend DSP forecast with 2023 actual value ---
plant = "DSP"
last_year = historical.index[-1]
last_value = historical[plant].iloc[-1]

dsp_extended = pd.concat([
    pd.Series([last_value], index=[last_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(historical.index, historical[plant], label="Historical", linewidth=2)
plt.plot(dsp_extended.index, dsp_extended.values,
         label="Forecast", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_year, color='gray', linestyle=':', label="Forecast Start")

plt.title("DSP: Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: save the plot
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\dsp_forecast.png")
plt.show()

# --- Step 5: Forecast values ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

# --- Step 6: Summary ---
print("""
🏭 Durgapur Steel Plant (DSP)

Overview:
DSP, commissioned in the 1960s and located in West Bengal, is a critical facility producing medium structural steel, railway wheels and axles, and semis. It supports Indian Railways, defense, and infrastructure projects.

🌱 Sustainability Achievements:
- Installed low-NOx burners and high-efficiency recuperative furnaces.
- Modernized mills to reduce electrical and thermal energy intensity.
- Dust suppression systems implemented across material handling areas.
- Adopted LED lighting across plant facilities.

📈 Areas for Further Improvement:
- Implement predictive maintenance using machine learning on compressors, turbines.
- Introduce ZLD for wastewater treatment and expand rainwater harvesting.
- Pilot hybrid power systems combining solar and natural gas microturbines.
""")
