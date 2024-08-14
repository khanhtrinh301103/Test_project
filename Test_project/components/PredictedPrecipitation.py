import numpy as np
import pandas as pd
import datetime  # Thêm dòng này
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def process_data(daily_data, hourly_data):
    # Convert hourly_data from dict to DataFrame
    hourly_df = pd.DataFrame(hourly_data)
    
    # Ensure 'time' column is in datetime format
    hourly_df['time'] = pd.to_datetime(hourly_df['time'])
    
    # Resample hourly data to daily data, aggregating by the median
    hourly_df.set_index('time', inplace=True)
    daily_cloudcover = hourly_df['cloudcover'].resample('D').median().reset_index()
    daily_relative_humidity = hourly_df['relative_humidity_2m'].resample('D').median().reset_index()
    daily_showers = hourly_df['showers'].resample('D').median().reset_index()

    # Convert daily_data from dict to DataFrame
    daily_df = pd.DataFrame(daily_data)
    daily_df['time'] = pd.to_datetime(daily_df['time'])

    # Merge the aggregated data with the daily_df
    daily_df = pd.merge(daily_df, daily_cloudcover, on='time')
    daily_df = pd.merge(daily_df, daily_relative_humidity, on='time')
    daily_df = pd.merge(daily_df, daily_showers, on='time')

    # Feature selection and trend features
    features = ['temperature_2m_max', 'temperature_2m_min', 'sunshine_duration', 
                'precipitation_probability_max', 'wind_speed_10m_max', 
                'cloudcover', 'relative_humidity_2m', 'showers']

    daily_df['precipitation_sum_7d_mean'] = daily_df['precipitation_sum'].rolling(window=7).mean()
    daily_df['precipitation_sum_14d_mean'] = daily_df['precipitation_sum'].rolling(window=14).mean()
    daily_df['precipitation_sum_7d_std'] = daily_df['precipitation_sum'].rolling(window=7).std()
    daily_df['precipitation_sum_14d_std'] = daily_df['precipitation_sum'].rolling(window=14).std()
    daily_df['precipitation_sum_cumsum'] = daily_df['precipitation_sum'].cumsum()

    features += ['precipitation_sum_7d_mean', 'precipitation_sum_14d_mean', 
                 'precipitation_sum_7d_std', 'precipitation_sum_14d_std', 
                 'precipitation_sum_cumsum']

    # Drop rows with NaN values
    daily_df.dropna(inplace=True)
    return daily_df, features

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Output a single value for regression
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

def train_models(daily_df, features):
    # Prepare the target variable
    target = 'precipitation_sum'
    y = daily_df[target].values  # Assign target variable

    # Prepare data for LSTM (trend features)
    trend_features = ['precipitation_sum_7d_mean', 'precipitation_sum_14d_mean', 
                      'precipitation_sum_7d_std', 'precipitation_sum_14d_std', 
                      'precipitation_sum_cumsum']
    X_trend = daily_df[trend_features].values
    X_trend = X_trend.reshape((X_trend.shape[0], 1, X_trend.shape[1]))

    # Train LSTM model
    lstm_model = create_lstm_model((X_trend.shape[1], X_trend.shape[2]))
    lstm_model.fit(X_trend, y, epochs=50, batch_size=32, verbose=2, shuffle=False)

    # Generate trend features for Gradient Boosting
    trend_features_lstm = lstm_model.predict(X_trend)
    X_combined = np.hstack((daily_df[features].values, trend_features_lstm))

    # Train Gradient Boosting model
    X_train_full, X_test, y_train_full, y_test = train_test_split(X_combined, y, test_size=0.2, shuffle=False)
    gb_model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        min_samples_split=5,
        min_samples_leaf=3,
        subsample=0.8,
        random_state=42
    )
    gb_model.fit(X_train_full, y_train_full)
    
    return gb_model, lstm_model

def predict_precipitation(daily_df, gb_model, lstm_model, features):
    future_dates = pd.date_range(datetime.datetime.now() + pd.Timedelta(days=1), periods=14)
    trend_features = ['precipitation_sum_7d_mean', 'precipitation_sum_14d_mean', 
                      'precipitation_sum_7d_std', 'precipitation_sum_14d_std', 
                      'precipitation_sum_cumsum']
    future_trend_features_lstm = lstm_model.predict(daily_df[trend_features].tail(14).values.reshape((14, 1, len(trend_features))))
    future_features_combined = np.hstack((daily_df[features].tail(14).values, future_trend_features_lstm))
    predictions = gb_model.predict(future_features_combined)
    predictions = np.maximum(predictions, 0)

    pred_df = pd.DataFrame({'date': future_dates, 'predicted_precipitation_sum': predictions.flatten()})
    return pred_df
