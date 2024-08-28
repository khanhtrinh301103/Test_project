from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from components.api import get_weather_data
from components.weather_display import format_current_weather
from components.PredictedPrecipitation import process_data, train_models, predict_precipitation
from components.PredictedPrecipitationChart import create_dash_app
from components.RainProbability import predict_precipitation_probability  # Đảm bảo import hàm này
from components.RainProbabilityChart import create_rain_probability_chart
from components.locations import get_location_coordinates
import json

server = Flask(__name__)
server.secret_key = 'supersecretkey'  # Cần thiết để sử dụng session

# Khởi tạo Dash app một lần duy nhất với server
dash_app = create_dash_app(server)
rain_probability_chart = create_rain_probability_chart(server)  # Thêm Dash app cho biểu đồ Rain Probability

@server.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        selected_location = request.form.get('location')
        if selected_location:
            session['location'] = selected_location  # Lưu vị trí vào session
        return redirect(url_for('index'))
    return render_template('landing.html')

@server.route('/index')
def index():
    # Lấy vị trí từ session
    current_location = session.get('location', 'Ho Chi Minh')  # Mặc định là Ho Chi Minh nếu không có vị trí
    
    # Lấy tọa độ của vị trí hiện tại
    coords = get_location_coordinates(current_location)
    
    # Cập nhật dữ liệu thời tiết và các mô hình với tọa độ mới
    weather_data = get_weather_data(coords['latitude'], coords['longitude'])
    
    # Check if daily data exists and is not empty
    if not weather_data.get('daily'):
        raise ValueError("No daily data available")
    
    current_weather = weather_data['current_weather']
    hourly_data = weather_data.get('hourly', {})
    formatted_weather = format_current_weather(current_weather, weather_data['daily'], hourly_data)

    daily_df, features = process_data(weather_data['daily'], hourly_data)
    gb_model, lstm_model = train_models(daily_df, features)
    pred_df = predict_precipitation(daily_df, gb_model, lstm_model, features)

    # Dự đoán xác suất mưa cho 14 ngày tới từ hôm nay
    precipitation_probabilities = predict_precipitation_probability(weather_data['daily'], predict_next_14_days=True)
    session['precipitation_probabilities_14d'] = precipitation_probabilities  # Lưu trữ dữ liệu dự đoán 14 ngày vào session

    # Lưu trữ dự đoán vào session Flask
    session['pred_data'] = pred_df.to_json()
    pred_json = pred_df.to_json()

    # Thêm vị trí vào weather
    formatted_weather['location'] = current_location

    return render_template('index.html', weather=formatted_weather, pred_data=pred_json)

if __name__ == '__main__':
    server.run(debug=True)
