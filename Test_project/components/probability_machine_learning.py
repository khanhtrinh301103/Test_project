import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Conv1D, MaxPooling1D, Dropout
from sklearn.preprocessing import MinMaxScaler

def train_and_predict(weather_df):
    # Chọn các đặc trưng và mục tiêu
    features = weather_df.columns.difference(['precipitation_sum'])
    target = 'precipitation_sum'

    # Chuẩn hóa dữ liệu
    feature_scaler = MinMaxScaler()
    scaled_features = feature_scaler.fit_transform(weather_df[features])
    target_scaler = MinMaxScaler()
    scaled_target = target_scaler.fit_transform(weather_df[[target]])

    # Chuẩn bị dữ liệu huấn luyện
    look_back = 14
    X, y = [], []
    for i in range(look_back, len(scaled_features)):
        X.append(scaled_features[i-look_back:i])
        y.append(scaled_target[i])

    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], len(features)))

    # Xây dựng mô hình
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(look_back, len(features))))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(64, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.3))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')

    # Huấn luyện mô hình
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
    model.fit(X, y, epochs=200, batch_size=16, validation_split=0.2, verbose=2, shuffle=False, callbacks=[early_stopping])

    # Dự đoán xác suất mưa cho 14 ngày tới
    predictions = predict_rain_probability(model, weather_df, feature_scaler, target_scaler, features, look_back)
    return predictions

def predict_rain_probability(model, df, feature_scaler, target_scaler, features, look_back):
    scaled_features = feature_scaler.transform(df[features])
    last_14_days = scaled_features[-look_back:]
    
    predictions = []
    for _ in range(14):
        X_pred = last_14_days.reshape((1, look_back, len(features)))
        y_pred = model.predict(X_pred)
        predictions.append(y_pred[0][0])
        
        next_feature = np.append(last_14_days[1:], np.zeros((1, len(features))), axis=0)
        next_feature[-1, 0] = y_pred[0]
        last_14_days = next_feature

    predictions_rescaled = target_scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=14)
    predictions_df = pd.DataFrame({
        'date': future_dates,
        'predicted_precipitation': predictions_rescaled.flatten()
    })
    predictions_df.set_index('date', inplace=True)

    predictions_df['precipitation_probability'] = np.minimum(predictions_df['predicted_precipitation'] * 10, 100)
    predictions_df['will_rain'] = predictions_df['precipitation_probability'] > 50

    return predictions_df
