import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load historical + forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical data ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Extend ISP forecast with 2023 actual point ---
plant = "ISP"
last_year = historical.index[-1]
last_value = historical[plant].iloc[-1]

isp_extended_forecast = pd.concat([
    pd.Series([last_value], index=[last_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(historical.index, historical[plant], label="Historical", linewidth=2)
plt.plot(isp_extended_forecast.index, isp_extended_forecast.values,
         label="Forecast", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_year, color='gray', linestyle=':', label="Forecast Start")

plt.title("ISP: Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: Save the figure
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\isp_forecast.png")
plt.show()

# --- Step 5: Print Forecast and Summary ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

print("""
🏭 IISCO Steel Plant (ISP)

Overview:
IISCO Steel Plant, located in Burnpur (West Bengal), is one of India's oldest steel plants—revamped extensively in the last decade. It now houses state-of-the-art facilities, including India’s largest blast furnace (Kalyani) with an 8,000 TPD capacity.

🌱 Sustainability Achievements:
- Modernization in 2015 drastically improved energy efficiency and reduced emissions.
- Established dry gas cleaning systems and bag filters to control particulate emissions.
- Reuses 100% of solid waste generated from blast furnace and steelmaking slag.
- Integrated advanced control systems to minimize coke consumption.

📈 Areas for Further Improvement:
- Add solar rooftops and explore waste-heat recovery in sinter and rolling units.
- Integrate AI for combustion tuning in blast furnaces.
- Pilot small-scale hydrogen-based iron reduction to prepare for green transition.
""")
