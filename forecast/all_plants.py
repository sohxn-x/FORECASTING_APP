import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# --- Step 1: Load Dataset ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

# --- Step 2: Forecast for Each Plant ---
plant_names = df["Plant"].unique()
forecast_dict = {}
years = pd.date_range("2025-01-01", periods=6, freq="YS")

def create_sequences(data, seq_len=5):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

for plant in plant_names:
    plant_series = df[df["Plant"] == plant].groupby("Date")["Energy_Gcal_tcs"].mean().sort_index()
    plant_series.index = pd.to_datetime(plant_series.index)
    plant_series.index.freq = 'YS'

    # ARIMA
    arima_model = ARIMA(plant_series, order=(1, 1, 1))
    arima_result = arima_model.fit()
    arima_fitted = arima_result.fittedvalues
    residuals = plant_series[1:] - arima_fitted

    residuals_array = residuals.values.reshape(-1, 1)
    if residuals_array.max() - residuals_array.min() < 1e-6:
        print(f"⚠️ Residuals for {plant} nearly flat. Adding noise.")
        residuals_array += np.random.normal(0, 1e-3, size=residuals_array.shape)

    scaler = MinMaxScaler()
    residuals_scaled = scaler.fit_transform(residuals_array)
    X, y = create_sequences(residuals_scaled)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # LSTM
    model = Sequential([
        Input(shape=(X.shape[1], 1)),
        LSTM(64, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=250, verbose=0)

    arima_forecast = arima_result.forecast(steps=6).values

    # LSTM residual forecast
    last_seq = residuals_scaled[-5:]
    lstm_preds = []
    for _ in range(6):
        pred = model.predict(last_seq.reshape(1, 5, 1), verbose=0)
        lstm_preds.append(pred[0, 0])
        last_seq = np.vstack([last_seq[1:], pred])

    lstm_forecast = np.array(lstm_preds).reshape(-1, 1)
    lstm_forecast = np.nan_to_num(lstm_forecast)
    lstm_residuals = scaler.inverse_transform(lstm_forecast).flatten()

    if np.isnan(arima_forecast).any():
        print(f"⚠️ ARIMA NaNs in {plant}. Replacing with 0.")
        arima_forecast = np.nan_to_num(arima_forecast)

    hybrid_forecast = arima_forecast + lstm_residuals
    forecast_dict[plant] = pd.Series(hybrid_forecast, index=years)

# --- Step 3: Forecast for All-Plants Average ---
national_avg = df.groupby("Date")["Energy_Gcal_tcs"].mean().sort_index()
national_avg.index = pd.to_datetime(national_avg.index)
national_avg.index.freq = 'YS'

arima_model = ARIMA(national_avg, order=(1, 1, 1))
arima_result = arima_model.fit()
arima_fitted = arima_result.fittedvalues
residuals = national_avg[1:] - arima_fitted
residuals_array = residuals.values.reshape(-1, 1)

if residuals_array.max() - residuals_array.min() < 1e-6:
    residuals_array += np.random.normal(0, 1e-3, size=residuals_array.shape)

scaler = MinMaxScaler()
residuals_scaled = scaler.fit_transform(residuals_array)
X, y = create_sequences(residuals_scaled)
X = X.reshape((X.shape[0], X.shape[1], 1))

model = Sequential([
    Input(shape=(X.shape[1], 1)),
    LSTM(64, activation='relu'),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=250, verbose=0)

arima_forecast = arima_result.forecast(steps=6).values
last_seq = residuals_scaled[-5:]
lstm_preds = []
for _ in range(6):
    pred = model.predict(last_seq.reshape(1, 5, 1), verbose=0)
    lstm_preds.append(pred[0, 0])
    last_seq = np.vstack([last_seq[1:], pred])

lstm_forecast = np.array(lstm_preds).reshape(-1, 1)
lstm_forecast = np.nan_to_num(lstm_forecast)
lstm_residuals = scaler.inverse_transform(lstm_forecast).flatten()
national_forecast = arima_forecast + lstm_residuals

forecast_dict["All Plants Avg"] = pd.Series(national_forecast, index=years)

# --- Step 4: Plot All Forecasts ---
plt.figure(figsize=(14, 6))
for plant, forecast in forecast_dict.items():
    plt.plot(forecast.index, forecast.values, label=plant, marker='o', linewidth=2)

plt.title("Hybrid Forecasts (2025–2030) for All Plants")
plt.xlabel("Year")
plt.ylabel("Energy Consumption (Gcal/tcs)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save plot
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\all_forecast_plot.png")
plt.show()

# --- Step 5: Export Forecasts ---
forecast_df = pd.DataFrame(forecast_dict)
forecast_df.index.name = "Year"
forecast_df.to_csv(r"C:\Users\Sohan\Desktop\sohan\all_plant_forecasts.csv")
print(forecast_df)

# --- Step 6: Summary ---
print("""

1. 🏭 Rourkela Steel Plant (RSP):
Located in Odisha, RSP is a pioneer in green steelmaking, with ISO 50001 certification, Zero Liquid Discharge in hot-strip mill, biochar injection in blast furnace #1, and over 5.2 million trees planted. It leads SAIL in sustainable operations. Future gains can come from full-scale hydrogen trials and expanding renewable energy.

2. 🏭 IISCO Steel Plant (ISP):
Based in Burnpur, West Bengal, ISP is one of India’s oldest steel units, modernized with India's largest blast furnace. It boasts 100% slag reuse, dry gas cleaning, and real-time energy management. It can improve further by integrating solar rooftops and piloting green hydrogen injection.

3. 🏭 Bhilai Steel Plant (BSP):
India’s largest rail producer, BSP is known for zero solid waste generation, floating solar (~15–35 MW planned), and slag-to-paver conversion. It also manages power via captive generation (NSPCL). Further improvements include carbon capture for coke ovens and expanding predictive AI-based emission control.

4. 🏭 Durgapur Steel Plant (DSP):
Located in West Bengal, DSP produces rails, axles, and semis. It has upgraded furnaces, implemented LED lighting, and improved dust suppression. DSP can enhance its performance with smart energy dashboards, rainwater harvesting, and hybrid power systems.

5. 🏭 Bokaro Steel Plant (BSL):
BSL in Jharkhand is a flat product leader. It excels in process gas recovery, installed a 2,000-tile/day slag-to-tile plant (2025), and practices closed-loop water recycling. Future directions include introducing electric arc furnaces and AI-driven energy optimization.

6. 🏢 SAIL (Overall):
Across all plants, SAIL has achieved over 98% solid waste utilization, initiated multiple solar projects, and committed to India's 2070 Net Zero goal. Group-wide priorities now include scaling green hydrogen, digitalizing sustainability metrics, and unifying carbon reduction strategies.

🔚 Conclusion:
Each SAIL plant has contributed uniquely to India's sustainable steel journey. Continued focus on AI, circular economy, and renewable energy can elevate SAIL to global benchmarks in green manufacturing.
""")
