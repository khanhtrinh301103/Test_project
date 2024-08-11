from flask import Flask, render_template
from components.api import get_weather_data
from components.chart import create_temperature_chart
import dash
import dash_html_components as html

server = Flask(__name__)

@server.route('/')
def landing():
    return render_template('landing.html')

@server.route('/index')
def index():
    weather_data = get_weather_data()
    current_weather = weather_data['current_weather']
    weather = {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': current_weather.get('sunrise', ''),
        'sunset': current_weather.get('sunset', ''),
        'precipitation_probability': current_weather.get('precipitation_probability', '')
    }
    daily_weather = weather_data['daily']
    return render_template('index.html', weather=weather, daily_weather=daily_weather)

# Tạo Dash app
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

# Layout của Dash app
weather_data = get_weather_data()['daily']  # Lấy dữ liệu trước để sử dụng trong biểu đồ
app.layout = html.Div([
    create_temperature_chart(app, weather_data)
])

if __name__ == '__main__':
    server.run(debug=True)
