import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Conv1D, MaxPooling1D, Flatten, Dropout
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.regularizers import l2

def predict_precipitation_probability(data):
    # Kiểm tra dữ liệu daily có đầy đủ
    if not data.get('time') or not data.get('temperature_2m_max'):
        raise ValueError("Missing necessary fields in daily data")

    dates = pd.to_datetime(data['time'])
    df = pd.DataFrame({
        'date': dates,
        'temperature_2m_max': data['temperature_2m_max'],
        'temperature_2m_min': data['temperature_2m_min'],
        'sunshine_duration': data['sunshine_duration'],
        'precipitation_sum': data['precipitation_sum'],
        'precipitation_probability_max': data['precipitation_probability_max'],
        'wind_speed_10m_max': data['wind_speed_10m_max'],
        'wind_gusts_10m_max': data['wind_gusts_10m_max'],
        'wind_direction_10m_dominant': data['wind_direction_10m_dominant']
    })
    df.set_index('date', inplace=True)
    df.fillna(0, inplace=True)

    # Chọn đặc trưng và mục tiêu
    features = df.columns.difference(['precipitation_sum'])
    target = 'precipitation_sum'

    feature_scaler = MinMaxScaler()
    scaled_features = feature_scaler.fit_transform(df[features])
    target_scaler = MinMaxScaler()
    scaled_target = target_scaler.fit_transform(df[[target]])

    # Chuẩn bị dữ liệu huấn luyện
    look_back = 14
    X, y = [], []
    for i in range(look_back, len(scaled_features)):
        X.append(scaled_features[i-look_back:i])
        y.append(scaled_target[i])

    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], len(features)))

    # Xây dựng mô hình học máy
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(look_back, len(features))))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.4))  # Tăng tỷ lệ Dropout
    model.add(Bidirectional(LSTM(64, return_sequences=True, kernel_regularizer=l2(0.01))))  # Thêm Regularization
    model.add(Dropout(0.4))  # Tăng tỷ lệ Dropout
    model.add(Bidirectional(LSTM(64, kernel_regularizer=l2(0.01))))  # Thêm Regularization
    model.add(Dropout(0.4))  # Tăng tỷ lệ Dropout
    model.add(Dense(50, activation='relu', kernel_regularizer=l2(0.01)))  # Thêm Regularization
    model.add(Dropout(0.4))  # Tăng tỷ lệ Dropout
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')

    # Huấn luyện mô hình
    model.fit(X, y, epochs=200, batch_size=16, validation_split=0.2, verbose=0, shuffle=False)

    # Dự đoán xác suất mưa cho ngày hôm nay
    last_14_days = scaled_features[-look_back:]
    X_pred = last_14_days.reshape((1, look_back, len(features)))
    y_pred = model.predict(X_pred)
    predicted_precipitation = target_scaler.inverse_transform(y_pred)

    # Tính toán xác suất mưa
    precipitation_probability = np.minimum(predicted_precipitation[0][0] * 10, 100)
    return precipitation_probability
