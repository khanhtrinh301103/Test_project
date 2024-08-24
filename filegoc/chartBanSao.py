import dash
from dash import dcc, html
import plotly.graph_objs as go

def daily_temperature_chart(time_data, rain_sum_data, temperature_max_data):
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
                    barmode='group',  # Keep the bars grouped side by side
                    dragmode='pan'  # Set pan as the default mode
                )
            }
        )
    ])
    
    return app
