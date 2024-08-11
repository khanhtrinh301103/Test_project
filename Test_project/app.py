from flask import Flask, render_template
from components.api import get_weather_data
from components.chart import create_temperature_chart
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
    
    # Kiểm tra dữ liệu daily có tồn tại và không rỗng
    if not weather_data.get('daily'):
        return "No daily data available", 500

    current_weather = format_current_weather(weather_data['current_weather'], weather_data['daily'])
    return render_template('index.html', weather=current_weather, daily_weather=weather_data['daily'])

# Tạo Dash app
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

# Layout của Dash app
weather_data = get_weather_data()['daily']  # Lấy dữ liệu daily từ API
app.layout = html.Div([
    create_temperature_chart(app, weather_data)
])

if __name__ == '__main__':
    server.run(debug=True)
