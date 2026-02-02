import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load data (if not already loaded) ---
# You can skip these lines if df and forecast_df are already defined in memory
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
forecast_df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv", index_col=0, parse_dates=True)

# --- Step 2: Prepare historical data ---
df["Date"] = pd.to_datetime(df["Date"])
historical = df.groupby(["Date", "Plant"])["Energy_Gcal_tcs"].mean().unstack()
historical = historical.sort_index()
historical.index.freq = "YS"

# --- Step 3: Combine historical and forecast ---
combined_df = pd.concat([historical, forecast_df], axis=0)

# --- Step 4: Plot ---
plt.figure(figsize=(14, 6))
for plant in forecast_df.columns:
    if plant in combined_df.columns:
        plt.plot(combined_df.index, combined_df[plant], label=plant, marker='o')

# Highlight forecast region
plt.axvspan(forecast_df.index[0], forecast_df.index[-1], color='orange', alpha=0.1, label="Forecast Period")

plt.title("Historical + Forecasted Energy Consumption per Plant")
plt.xlabel("Year")
plt.ylabel("Energy Consumption (Gcal/tcs)")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\historical_all.png")
plt.show()