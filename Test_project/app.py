from flask import Flask, render_template
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime

server = Flask(__name__)

# Hàm lấy dữ liệu từ API
def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Bangkok",
        "past_days": 5
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

@server.route('/')
def landing():
    return render_template('landing.html')

@server.route('/index')
def index():
    weather_data = get_weather_data()
    current_weather = weather_data['current_weather']
    print(current_weather)  # Kiểm tra dữ liệu API
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
app.layout = html.Div([
    dcc.Graph(id='temperature-graph', config={'displayModeBar': False}, style={'background': 'transparent'})
])

# Callback để cập nhật biểu đồ
@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('temperature-graph', 'hoverData')]
)
def update_graph(hoverData):
    weather_data = get_weather_data()['daily']
    dates = [datetime.datetime.strptime(day, '%Y-%m-%d') for day in weather_data['time']]
    max_temps = weather_data['temperature_2m_max']
    min_temps = weather_data['temperature_2m_min']

    figure = {
        'data': [
            go.Scatter(
                x=dates,
                y=max_temps,
                mode='lines+markers',
                name='Max Temp',
                line={'color': 'orange'}
            ),
            go.Scatter(
                x=dates,
                y=min_temps,
                mode='lines+markers',
                name='Min Temp',
                line={'color': 'blue'}
            )
        ],
        'layout': go.Layout(
            title='Temperature in the Past 5 Days',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Temperature (°C)'},
            hovermode='closest',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
    }
    return figure

if __name__ == '__main__':
    server.run(debug=True)
