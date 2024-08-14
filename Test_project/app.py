from flask import Flask, render_template
from components.api import get_weather_data
from components.weather_display import format_current_weather
from components.PredictedPrecipitation import process_data, train_models, predict_precipitation
from components.PredictedPrecipitationChart import create_dash_app

server = Flask(__name__)

# Khởi tạo Dash app ngay sau khi khởi tạo Flask
weather_data = get_weather_data()

# Check if daily data exists and is not empty
if not weather_data.get('daily'):
    raise ValueError("No daily data available")

# Xử lý dữ liệu và mô hình trước khi tạo Dash app
current_weather = weather_data['current_weather']
hourly_data = weather_data.get('hourly', {})
formatted_weather = format_current_weather(current_weather, weather_data['daily'], hourly_data)

daily_df, features = process_data(weather_data['daily'], hourly_data)
gb_model, lstm_model = train_models(daily_df, features)
pred_df = predict_precipitation(daily_df, gb_model, lstm_model, features)

# Tạo Dash app trước khi Flask xử lý yêu cầu đầu tiên
dash_app = create_dash_app(server, pred_df)

@server.route('/')
def landing():
    return render_template('landing.html')

@server.route('/index')
def index():
    return render_template('index.html', weather=formatted_weather)

if __name__ == '__main__':
    server.run(debug=True)
