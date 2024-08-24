import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests

# Function to get weather data
def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "daily": ['rain_sum', 'temperature_2m_max'],  # Fetch rain_sum and temperature_2m_max
        "timezone": "Asia/Bangkok",
        "past_days": 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract 'time', 'rain_sum', and 'temperature_2m_max' data
    time_data = data.get('daily', {}).get('time', [])
    rain_sum_data = data.get('daily', {}).get('rain_sum', [])
    temperature_max_data = data.get('daily', {}).get('temperature_2m_max', [])
    
    return time_data, rain_sum_data, temperature_max_data

# Get data
time_data, rain_sum_data, temperature_max_data = get_weather_data()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div(children=[
    html.H1(children='Rainfall and Maximum Temperature Data'),
    
    dcc.Graph(
        id='rainfall-temperature-chart',
        figure={
            'data': [
                # Bar chart for rainfall
                go.Bar(
                    x=time_data,  # x-axis: time data
                    y=rain_sum_data,  # y-axis: rain sum data
                    name='Rainfall (mm)',
                    marker=dict(color='blue')
                ),
                # Line chart for temperature
                go.Scatter(
                    x=time_data,  # x-axis: time data
                    y=temperature_max_data,  # y-axis: temperature data
                    name='Max Temperature (°C)',
                    mode='lines+markers',  # Line and markers for temperature
                    marker=dict(color='orange'),
                    yaxis='y2'  # Use the second y-axis for temperature
                )
            ],
            'layout': go.Layout(
                title='Rainfall and Maximum Temperature Over Time',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Rainfall (mm)'},  # Left y-axis for rainfall
                yaxis2={
                    'title': 'Max Temperature (°C)',  # Right y-axis for temperature
                    'overlaying': 'y',
                    'side': 'right'
                },
                barmode='group'  # Keep the bars grouped side by side
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
