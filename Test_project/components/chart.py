import dash_core_components as dcc
import plotly.graph_objs as go
import datetime
from dash.dependencies import Input, Output

def create_temperature_chart(app, weather_data):
    @app.callback(
        Output('temperature-graph', 'figure'),
        [Input('temperature-graph', 'hoverData')]
    )
    def update_graph(hoverData):
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

    return dcc.Graph(id='temperature-graph', config={'displayModeBar': False}, style={'background': 'transparent'})
