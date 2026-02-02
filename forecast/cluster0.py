import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# --- Step 1: Load Dataset ---
df = pd.read_csv(r"C:\Users\Sohan\Desktop\sohan\Dataset\Unique_Timeseries_Dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

# --- Step 2: Prepare Time Series for Cluster 0 (RSP + ISP) ---
cluster_0_plants = ["RSP", "ISP"]
cluster_0_series = df[df["Plant"].isin(cluster_0_plants)] \
    .groupby("Date")["Energy_Gcal_tcs"].mean().sort_index()
cluster_0_series.index.freq = 'YS'

# --- Step 3: Fit ARIMA Model ---
arima_model = ARIMA(cluster_0_series, order=(1, 1, 1))
arima_result = arima_model.fit()
arima_fitted = arima_result.fittedvalues
residuals = cluster_0_series[1:] - arima_fitted

# --- Step 4: LSTM on Residuals ---
residuals_array = residuals.values.reshape(-1, 1)
if residuals_array.max() - residuals_array.min() < 1e-6:
    residuals_array += np.random.normal(0, 1e-3, size=residuals_array.shape)

scaler = MinMaxScaler()
residuals_scaled = scaler.fit_transform(residuals_array)

def create_sequences(data, seq_len=5):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

X, y = create_sequences(residuals_scaled, seq_len=5)
X = X.reshape((X.shape[0], X.shape[1], 1))

# LSTM Model
model = Sequential([
    Input(shape=(X.shape[1], 1)),
    LSTM(64, activation='relu'),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=250, verbose=0)

# --- Step 5: Forecast Hybrid ARIMA + LSTM ---
future_steps = 6
arima_forecast = arima_result.forecast(steps=future_steps).values

last_seq = residuals_scaled[-5:]
lstm_preds = []
for _ in range(future_steps):
    pred = model.predict(last_seq.reshape(1, 5, 1), verbose=0)
    lstm_preds.append(pred[0, 0])
    last_seq = np.vstack([last_seq[1:], pred])

lstm_forecast = np.nan_to_num(np.array(lstm_preds).reshape(-1, 1))
lstm_residuals = scaler.inverse_transform(lstm_forecast).flatten()
hybrid_forecast = arima_forecast + lstm_residuals

# --- Step 6: Plot Results ---
forecast_dates = pd.date_range(start=cluster_0_series.index[-1] + pd.DateOffset(years=1), periods=6, freq='YS')
forecast_series = pd.Series(hybrid_forecast, index=forecast_dates)

last_real_point = cluster_0_series.iloc[-1]
extended_forecast_series = pd.concat([
    pd.Series([last_real_point], index=[cluster_0_series.index[-1]]),
    forecast_series
])

plt.figure(figsize=(14, 5))
plt.plot(cluster_0_series, label="Historical", linewidth=2)
plt.plot(extended_forecast_series.index, extended_forecast_series.values,
         label="Hybrid Forecast (2025–2030)", linestyle='--', marker='o', color='orange', linewidth=2)
plt.axvspan(forecast_series.index[0], forecast_series.index[-1], color='orange', alpha=0.1, label="Forecast Period")
plt.axvline(x=cluster_0_series.index[-1], color='gray', linestyle=':', label='Forecast Start')
plt.title("Cluster 0 (RSP + ISP) - Hybrid Forecast with ARIMA and LSTM Influence")
plt.xlabel("Year")
plt.ylabel("Energy Consumption (Gcal/tcs)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\Sohan\Desktop\sohan\energy_app\static\cluster0_forecast.png")
plt.show()
# --- Step 7: Output Forecast to Console ---
print("\nForecast (2025–2030):")
print(forecast_series)

# Optional: Save forecast to CSV
forecast_series.to_csv(r"C:\Users\Sohan\Desktop\sohan\cluster0_forecast.csv")
