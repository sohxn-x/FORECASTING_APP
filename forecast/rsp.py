import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load historical + forecast data ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Process historical data for RSP ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Prepare RSP forecast (extend with 2023 actual point) ---
plant = "RSP"
last_actual_year = historical.index[-1]
last_actual_value = historical[plant].iloc[-1]

rsp_extended = pd.concat([
    pd.Series([last_actual_value], index=[last_actual_year]),
    forecast_df[plant]
])

# --- Step 4: Plot ---
plt.figure(figsize=(8, 4))
plt.plot(historical.index, historical[plant], label="Historical", linewidth=2)
plt.plot(rsp_extended.index, rsp_extended.values, label="Forecast", linestyle='--', marker='o', color='orange')
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=last_actual_year, color='gray', linestyle=':', label="Forecast Start")

plt.title(f"{plant}: Energy Consumption (Historical + Forecast)")
plt.xlabel("Year")
plt.ylabel("Gcal/tcs")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Optional: save plot
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\rsp_forecast.png")
plt.show()

# --- Step 5: Show forecast values ---
print(f"\n📊 Forecast (2025–2030) for {plant}:\n")
print(forecast_df[plant])

# --- Step 6: Summary ---
print("""
🏭 Rourkela Steel Plant (RSP)

Overview:
RSP, established in 1959 in Odisha, was India’s first integrated public sector steel plant. It currently produces around 4.2 million tonnes of crude steel annually and specializes in flat products for automotive, appliance, and defense sectors.

🌱 Sustainability Achievements:
- Achieved ISO 50001:2018 Energy Management Certification.
- In 2022, won the National Energy Conservation Award.
- In 2024, became the first SAIL unit to pilot biochar injection in blast furnace #1—cutting fossil PCI coal use.
- Installed Zero Liquid Discharge (ZLD) systems in its hot-strip mill.
- Over 5.2 million trees planted around the campus.
- Developed a 4 MLD sewage treatment facility for industrial reuse.

📈 Areas for Further Improvement:
- Scale up biochar injection and test green hydrogen as an alternative in blast furnace trials.
- Expand solar and hydro generation beyond 1 MW rooftop and planned 15 MW micro-hydro.
- Use AI/ML for predictive maintenance of furnaces and energy optimization.
""")
