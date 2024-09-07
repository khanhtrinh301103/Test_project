from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from components.api import get_weather_data
from components.weather_display import format_current_weather
from components.PredictedPrecipitation import process_data, train_models, predict_precipitation
from components.PredictedPrecipitationChart import create_dash_app
from components.RainProbability import predict_precipitation_probability
from components.RainProbabilityChart import create_rain_probability_chart
from components.RainSum import get_daily_rain_sum
from components.RainSumChart import create_rain_sum_chart
from components.locations import get_location_coordinates
from components.TemperatureMap import create_temperature_map  # Import từ file TemperatureMap.py
import json

server = Flask(__name__)
server.secret_key = 'supersecretkey'

# Tạo Dash App cho các biểu đồ
dash_app = create_dash_app(server)
rain_probability_chart = create_rain_probability_chart(server)
rain_sum_chart = create_rain_sum_chart(server)

@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_location = request.form.get('location')
        if selected_location:
            session['location'] = selected_location
        return redirect(url_for('index'))

    current_location = session.get('location', 'Ho Chi Minh')
    
    coords = get_location_coordinates(current_location)
    
    weather_data = get_weather_data(coords['latitude'], coords['longitude'])
    
    if not weather_data.get('daily'):
        raise ValueError("No daily data available")
    
    current_weather = weather_data['current_weather']
    hourly_data = weather_data.get('hourly', {})
    formatted_weather = format_current_weather(current_weather, weather_data['daily'], hourly_data)

    daily_df, features = process_data(weather_data['daily'], hourly_data)
    gb_model, lstm_model = train_models(daily_df, features)
    pred_df = predict_precipitation(daily_df, gb_model, lstm_model, features)

    # Lấy dữ liệu daily rain sum
    rain_sum_df = get_daily_rain_sum(weather_data['daily'])
    session['rain_sum_data'] = rain_sum_df.to_json()

    # Dự đoán xác suất mưa cho 14 ngày tới từ hôm nay
    precipitation_probabilities = predict_precipitation_probability(weather_data['daily'], predict_next_14_days=True)
    session['precipitation_probabilities_14d'] = precipitation_probabilities

    session['pred_data'] = pred_df.to_json()
    pred_json = pred_df.to_json()

    # Tạo bản đồ nhiệt độ
    temperature_map_json = create_temperature_map(weather_data, current_location, coords['latitude'], coords['longitude'])

    formatted_weather['location'] = current_location

    return render_template('index.html', weather=formatted_weather, pred_data=pred_json, temp_map=temperature_map_json)

# Route cho bản đồ nhiệt độ
@server.route('/temperature_map/')
def temperature_map():
    current_location = session.get('location', 'Ho Chi Minh')
    coords = get_location_coordinates(current_location)
    weather_data = get_weather_data(coords['latitude'], coords['longitude'])

    # Gọi hàm tạo bản đồ nhiệt độ từ file TemperatureMap.py
    temperature_map_html = create_temperature_map(weather_data, current_location, coords['latitude'], coords['longitude'])

    return temperature_map_html

if __name__ == '__main__':
    server.run(debug=True)
