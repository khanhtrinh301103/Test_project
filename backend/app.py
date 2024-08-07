from flask import Flask, render_template, jsonify
import requests

server = Flask(__name__)

# Hàm lấy dữ liệu từ API
def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "current_weather": "true",
        "timezone": "Asia/Bangkok"
    }
    response = requests.get(url, params=params)
    data = response.json()
    current_weather = data.get('current_weather', {})
    
    # Chỉ trả về các thông tin cần thiết
    weather_info = {
        "temperature": current_weather.get("temperature"),
        "windspeed": current_weather.get("windspeed"),
        "is_day": current_weather.get("is_day"),
        "sunrise": current_weather.get("sunrise", ""),
        "sunset": current_weather.get("sunset", ""),
        "precipitation_probability": current_weather.get("precipitation_probability", 0),
        "weathercode": current_weather.get("weathercode", "")
    }
    return weather_info

@server.route('/')
def landing():
    return render_template('landing.html')

@server.route('/index')
def index():
    weather_data = get_weather_data()
    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    server.run(debug=True)
