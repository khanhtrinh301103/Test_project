from flask import Flask, render_template
from components.api import get_weather_data
from components.weather_display import format_current_weather
import dash
import dash_html_components as html

server = Flask(__name__)

@server.route('/')
def landing():
    return render_template('landing.html')

@server.route('/index')
def index():
    weather_data = get_weather_data()
    
    # Check if daily data exists and is not empty
    if not weather_data.get('daily'):
        return "No daily data available", 500

    current_weather = weather_data['current_weather']
    hourly_data = weather_data.get('hourly', {})  # Lấy dữ liệu hourly nếu có

    # Truyền thêm hourly_data vào hàm format_current_weather
    formatted_weather = format_current_weather(current_weather, weather_data['daily'], hourly_data)
    
    return render_template('index.html', weather=formatted_weather)

if __name__ == '__main__':
    server.run(debug=True)
