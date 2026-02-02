from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from werkzeug.utils import secure_filename
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Setup paths
project_root = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(project_root, "static", "uploads")
MODELS_FOLDER = os.path.join(project_root, "models")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODELS_FOLDER, exist_ok=True)

# Configuration
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_data_quality(series, plant_name):
    """Comprehensive data quality validation."""
    if series.empty:
        raise ValueError(f"No data found for selected plant: {plant_name}")

    if len(series) < 10:
        raise ValueError(
            f"Insufficient data for {plant_name}. "
            f"Need at least 10 data points, got {len(series)}"
        )

    # Check for missing values
    if series.isnull().sum() > len(series) * 0.1:  # More than 10% missing
        raise ValueError(f"Too many missing values in {plant_name} data")

    # Fill missing values with interpolation
    series = series.interpolate(method='linear')

    # Check for outliers (values beyond 3 standard deviations)
    mean_val = series.mean()
    std_val = series.std()
    outliers = series[(series < mean_val - 3 * std_val) |
                      (series > mean_val + 3 * std_val)]

    if len(outliers) > len(series) * 0.05:  # More than 5% outliers
        print(f"Warning: High number of outliers detected in {plant_name} data")

    return series


def determine_optimal_params(series_length):
    """Determine optimal LSTM parameters based on data size."""
    if series_length < 20:
        seq_len = max(3, series_length // 4)
        lstm_units = 32
        epochs = 120
    elif series_length < 50:
        seq_len = max(5, min(series_length // 3, 8))
        lstm_units = 64
        epochs = 180
    else:
        seq_len = max(5, min(series_length // 4, 12))
        lstm_units = 128
        epochs = 220

    return seq_len, lstm_units, epochs


def create_sequences(data, seq_len):
    """
    Create (X, y) sequences from a 1D array.

    data: 1D numpy array
    seq_len: length of lookback window
    """
    if len(data) <= seq_len:
        raise ValueError(
            f"Data length ({len(data)}) must be greater than sequence length ({seq_len})"
        )

    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i + seq_len])
        y.append(data[i + seq_len])
    return np.array(X), np.array(y)


def train_lstm_time_series(X_train, y_train, X_val, y_val, lstm_units, epochs):
    """Train LSTM on residual series with time-ordered validation."""
    model = Sequential([
        Input(shape=(X_train.shape[1], 1)),
        LSTM(lstm_units, activation='tanh', return_sequences=True),
        Dropout(0.2),
        LSTM(lstm_units // 2, activation='tanh'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(
        optimizer='adam',
        loss='huber',  # More robust to outliers than MSE
        metrics=['mae']
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=20,
        restore_best_weights=True,
        verbose=0
    )

    lr_scheduler = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=10,
        min_lr=1e-6,
        verbose=0
    )

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=min(32, len(X_train)),
        callbacks=[early_stopping, lr_scheduler],
        verbose=0
    )

    metrics = {
        "epochs_trained": len(history.history["loss"])
    }
    return model, metrics


@app.route("/", methods=["POST"])
def home():
    """Forecast endpoint with hybrid ARIMA + LSTM model."""
    if 'csv_file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    uploaded_file = request.files['csv_file']
    plant_name = request.form.get("plant")

    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if not plant_name:
        return jsonify({"error": "Please select a plant."}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({"error": "Only CSV files are allowed."}), 400

    try:
        # Secure file handling
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Check file size
        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": "File too large. Maximum size is 16MB."}), 400

        uploaded_file.save(file_path)

        # Load and validate data
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])

        required_columns = ["Plant", "Date", "Energy_Gcal_tcs"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"CSV missing required columns: {missing_columns}")

        # Process data based on plant selection
        if plant_name == "All Plants Avg":
            series = df.groupby("Date")["Energy_Gcal_tcs"].mean().sort_index()
        else:
            plant_data = df[df["Plant"] == plant_name]
            if plant_data.empty:
                available_plants = df["Plant"].unique().tolist()
                raise ValueError(
                    f"Plant '{plant_name}' not found. Available plants: {available_plants}"
                )
            series = plant_data.groupby("Date")["Energy_Gcal_tcs"].mean().sort_index()

        # Data quality validation
        series = validate_data_quality(series, plant_name)

        # Force yearly frequency (assuming annual data)
        series.index = pd.to_datetime(series.index)
        series.index = series.index.to_period("Y").to_timestamp()  # normalize to year start
        series = series.sort_index()

        # Determine LSTM hyperparameters
        seq_len, lstm_units, epochs = determine_optimal_params(len(series))

        # ==============================
        # 1) ARIMA baseline (full series)
        # ==============================
        # Simple ARIMA(1,1,1). You can tune this later if needed.
        arima_model = ARIMA(series, order=(1, 1, 1))
        arima_result = arima_model.fit()

        # In-sample ARIMA fitted values
        arima_fitted = arima_result.fittedvalues  # aligned to series index (with some NaNs at start)

        # Align residual series where ARIMA has valid fitted values
        common_index = arima_fitted.index.intersection(series.index)
        arima_fitted = arima_fitted.loc[common_index]
        series_aligned = series.loc[common_index]

        residual_series = series_aligned - arima_fitted
        residual_series = residual_series.dropna()
        arima_fitted = arima_fitted.loc[residual_series.index]
        series_aligned = series_aligned.loc[residual_series.index]

        # ==============================
        # 2) LSTM on ARIMA residuals
        # ==============================
        values_residual = residual_series.values.reshape(-1, 1)
        n = len(values_residual)

        if n <= seq_len + 5:
            raise ValueError(
                "Insufficient data after ARIMA residual computation to build sequences robustly. "
                "Please provide more historical data."
            )

        train_size = int(n * 0.8)
        if train_size <= seq_len + 1:
            raise ValueError(
                "Too little data left for a proper 80/20 time split. "
                "Try aggregating to a longer horizon."
            )

        # Scale residuals using only train segment
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(values_residual[:train_size])
        scaled_all = scaler.transform(values_residual).flatten()

        # Create sequences on full residual series
        X_all, y_all = create_sequences(scaled_all, seq_len)
        target_indices = np.arange(seq_len, n)  # indices in residual_series

        train_mask = target_indices < train_size
        val_mask = ~train_mask

        if train_mask.sum() < 5 or val_mask.sum() < 3:
            raise ValueError(
                "Not enough samples for a robust train/validation split. "
                "Need more historical data."
            )

        X_train = X_all[train_mask]
        y_train = y_all[train_mask]
        X_val = X_all[val_mask]
        y_val = y_all[val_mask]

        # Reshape for LSTM [samples, timesteps, features]
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

        # Train LSTM
        model, metrics_resid = train_lstm_time_series(
            X_train, y_train, X_val, y_val, lstm_units, epochs
        )

        # ==============================
        # 3) Metrics on hybrid ARIMA + LSTM (actual scale)
        # ==============================
        # LSTM predictions for residuals
        train_pred_scaled = model.predict(X_train, verbose=0)
        val_pred_scaled = model.predict(X_val, verbose=0)

        train_pred_resid = scaler.inverse_transform(train_pred_scaled).flatten()
        val_pred_resid = scaler.inverse_transform(val_pred_scaled).flatten()

        # Map target positions to timestamps
        residual_idx = residual_series.index.to_list()
        train_target_pos = target_indices[train_mask]
        val_target_pos = target_indices[val_mask]

        train_timestamps = [residual_idx[i] for i in train_target_pos]
        val_timestamps = [residual_idx[i] for i in val_target_pos]

        # Actual series values at those timestamps
        train_true_actual = series.loc[train_timestamps].values
        val_true_actual = series.loc[val_timestamps].values

        # ARIMA component at those timestamps
        arima_train = arima_fitted.loc[train_timestamps].values
        arima_val = arima_fitted.loc[val_timestamps].values

        # Hybrid preds = ARIMA + LSTM(residual)
        train_pred_actual = arima_train + train_pred_resid
        val_pred_actual = arima_val + val_pred_resid

        train_mae = mean_absolute_error(train_true_actual, train_pred_actual)
        val_mae = mean_absolute_error(val_true_actual, val_pred_actual)
        train_rmse = np.sqrt(mean_squared_error(train_true_actual, train_pred_actual))
        val_rmse = np.sqrt(mean_squared_error(val_true_actual, val_pred_actual))

        metrics = {
            'train_mae': float(train_mae),
            'val_mae': float(val_mae),
            'train_rmse': float(train_rmse),
            'val_rmse': float(val_rmse),
            'epochs_trained': metrics_resid['epochs_trained']
        }

        # ==============================
        # 4) Forecasting: ARIMA + LSTM residual
        # ==============================
        steps_ahead = 5  # next 5 years

        # ARIMA future forecast
        arima_future = arima_result.forecast(steps=steps_ahead)  # pandas Series

        # LSTM residual future forecast (recursive)
        last_seq = scaled_all[-seq_len:].reshape(1, seq_len, 1)
        residual_forecasts_scaled = []

        for _ in range(steps_ahead):
            pred = model.predict(last_seq, verbose=0)
            residual_forecasts_scaled.append(pred[0, 0])
            # roll sequence and append prediction
            last_seq = np.roll(last_seq, -1, axis=1)
            last_seq[0, -1, 0] = pred[0, 0]

        residual_forecasts = scaler.inverse_transform(
            np.array(residual_forecasts_scaled).reshape(-1, 1)
        ).flatten()

        hybrid_forecast = arima_future.values + residual_forecasts

        # Create forecast dates (annual)
        last_year = series.index[-1].year
        forecast_years = [last_year + i for i in range(1, steps_ahead + 1)]
        forecast_dates = pd.to_datetime([f"{y}-01-01" for y in forecast_years])

        forecast_series = pd.Series(hybrid_forecast, index=forecast_dates)

        # Smooth connection (include last actual point)
        last_actual = series.iloc[-1]
        connected_forecast = pd.concat([
            pd.Series([last_actual], index=[series.index[-1]]),
            forecast_series
        ])

        # Confidence interval based on validation RMSE on actual scale
        sigma = val_rmse
        upper_bound = hybrid_forecast + 1.96 * sigma
        lower_bound = hybrid_forecast - 1.96 * sigma

        # ==============================
        # 5) Plotting
        # ==============================
        plot_filename = (
            f"forecast_{plant_name.lower().replace(' ', '_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        plot_rel_path = f"uploads/{plot_filename}"
        full_path = os.path.join(project_root, "static", plot_rel_path)

        plt.figure(figsize=(12, 8))

        # Main plot
        plt.subplot(2, 1, 1)
        plt.plot(series.index, series.values,
                 label="Historical Data", linewidth=2.5)
        plt.plot(connected_forecast.index, connected_forecast.values,
                 label="Hybrid ARIMA + LSTM Forecast", linestyle='--',
                 marker='o', linewidth=2)

        plt.fill_between(
            forecast_dates,
            lower_bound,
            upper_bound,
            alpha=0.2,
            label='Approx. 95% Prediction Interval'
        )

        plt.axvspan(forecast_dates[0], forecast_dates[-1], alpha=0.06)
        plt.axvline(x=series.index[-1], linestyle=':',
                    label="Forecast Start", alpha=0.7)

        plt.title(
            f"{plant_name} - Energy Consumption Forecast (Hybrid ARIMA + LSTM)",
            fontsize=14,
            fontweight='bold'
        )
        plt.xlabel("Year")
        plt.ylabel("Energy Consumption (Gcal/tcs)")
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Metrics subplot (NO R²)
        plt.subplot(2, 1, 2)
        metric_names = ['Train MAE', 'Val MAE', 'Train RMSE', 'Val RMSE']
        metric_values = [
            metrics['train_mae'],
            metrics['val_mae'],
            metrics['train_rmse'],
            metrics['val_rmse']
        ]

        bars = plt.bar(range(len(metric_names)), metric_values)
        plt.title(
            "Model Performance Metrics (Hybrid ARIMA + LSTM, Actual Scale)",
            fontsize=12,
            fontweight='bold'
        )
        plt.xticks(range(len(metric_names)), metric_names, rotation=45)
        plt.ylabel("Metric Value")

        for bar, value in zip(bars, metric_values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(metric_values) * 0.01,
                f'{value:.3f}',
                ha='center',
                va='bottom',
                fontsize=8
            )

        plt.tight_layout()
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()

        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

        # Prepare response
        image_url = f"http://127.0.0.1:5000/static/uploads/{plot_filename}"

        forecast_summary = {
            int(year): f"{value:.2f} Gcal/tcs"
            for year, value in zip(forecast_dates.year, hybrid_forecast)
        }

        return jsonify({
            "message": (
                f"✅ Hybrid ARIMA + LSTM forecast generated for {plant_name} "
                f"with time-ordered validation"
            ),
            "image": image_url,
            "plant": plant_name,
            "model_metrics": {
                "train_mae": f"{metrics['train_mae']:.3f}",
                "val_mae": f"{metrics['val_mae']:.3f}",
                "train_rmse": f"{metrics['train_rmse']:.33f}" if False else f"{metrics['train_rmse']:.3f}",
                "val_rmse": f"{metrics['val_rmse']:.3f}",
                "epochs_trained": metrics['epochs_trained'],
                "data_quality": (
                    "✅ Passed validation checks (ARIMA residual modeling, "
                    "time-ordered split, no leakage in LSTM scaling)"
                )
            },
            "forecast_summary": forecast_summary,
            "forecast_years": list(forecast_dates.year.astype(int)),
            "forecast_values": [f"{val:.2f}" for val in hybrid_forecast]
        })

    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": f"Forecast generation failed: {str(e)}"}), 500


@app.route("/api/forecasts")
def get_static_forecasts():
    """Return list of all static forecast images for React predictions page."""
    base_url = "http://127.0.0.1:5000/static/uploads"
    forecasts = [
        {"title": "Cluster 0 (RSP + ISP)", "src": f"{base_url}/cluster0_forecast.png"},
        {"title": "Cluster 1 (BSP + DSP + BSL + SAIL)", "src": f"{base_url}/cluster1_forecast.png"},
        {"title": "All Plants Forecast", "src": f"{base_url}/all_forecast_plot.png"},
        {"title": "Cluster Comparison", "src": f"{base_url}/comparison_plot.png"},
        {"title": "RSP Forecast", "src": f"{base_url}/rsp_forecast.png"},
        {"title": "ISP Forecast", "src": f"{base_url}/isp_forecast.png"},
        {"title": "BSP Forecast", "src": f"{base_url}/bsp_forecast.png"},
        {"title": "DSP Forecast", "src": f"{base_url}/dsp_forecast.png"},
        {"title": "BSL Forecast", "src": f"{base_url}/bsl_forecast.png"},
        {"title": "SAIL Avg Forecast", "src": f"{base_url}/sail_forecast.png"}
    ]
    return jsonify(forecasts)


@app.route('/static/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve static forecast images securely."""
    static_folder = os.path.join(project_root, "static", "uploads")
    return send_from_directory(static_folder, filename)


if __name__ == "__main__":
    print("🚀 Starting Hybrid ARIMA + LSTM Forecasting Server...")
    print("📊 Features: ARIMA baseline, residual LSTM, time-series validation, realistic metrics")
    app.run(debug=True, host='127.0.0.1', port=5000)
