from flask import Flask, render_template, request, redirect, url_for
from dash import dcc, html
import dash
import plotly.graph_objs as go
from api import get_weather_data

# Tạo ứng dụng Flask
server = Flask(__name__)

# Tạo ứng dụng Dash và gán nó vào Flask
app = dash.Dash(__name__, server=server, url_base_pathname='/dash1/')

# Định nghĩa layout cho ứng dụng Dash
app.layout = html.Div(children=[
    html.H1(children='Rainfall and Maximum Temperature Data'),
    dcc.Graph(id='rainfall-temperature-chart')
])

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/update', methods=['POST'])
def update():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Xử lý dữ liệu với latitude và longitude đã chọn
    time_data, rain_sum_data, temperature_max_data = get_weather_data(latitude, longitude)

    # Cập nhật biểu đồ trong Dash
    app.layout = html.Div(children=[
        html.H1(children='Rainfall and Maximum Temperature Data'),
        dcc.Graph(
            id='rainfall-temperature-chart',
            figure={
                'data': [
                    go.Bar(
                        x=time_data,
                        y=rain_sum_data,
                        name='Rainfall (mm)',
                        marker=dict(color='blue')
                    ),
                    go.Scatter(
                        x=time_data,
                        y=temperature_max_data,
                        name='Max Temperature (°C)',
                        mode='lines+markers',
                        marker=dict(color='orange'),
                        yaxis='y2'
                    )
                ],
                'layout': go.Layout(
                    title='Rainfall and Maximum Temperature Over Time',
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Rainfall (mm)'},
                    yaxis2={
                        'title': 'Max Temperature (°C)',
                        'overlaying': 'y',
                        'side': 'right'
                    },
                    barmode='group',
                    dragmode='pan'
                )
            }
        )
    ])

    return redirect(url_for('index'))

# Chạy ứng dụng Flask
if __name__ == '__main__':
    server.run(debug=True)










