import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

def create_dash_app(server, pred_df):
    app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')
    
    app.layout = html.Div([
        dcc.Graph(
            id='precipitation-graph',
            figure={
                'data': [
                    go.Scatter(
                        x=pred_df['date'],
                        y=pred_df['predicted_precipitation_sum'],
                        mode='lines+markers',
                        name='Predicted Precipitation',
                        line=dict(color='yellow')
                    )
                ],
                'layout': go.Layout(
                    xaxis={
                        'title': 'Date',
                        'color': 'white',  # Màu của các thông số trục X
                        'tickfont': dict(color='white')  # Màu của các nhãn ngày
                    },
                    yaxis={
                        'title': 'Predicted Precipitation Sum (mm)',
                        'color': 'white',  # Màu của các thông số trục Y
                        'tickfont': dict(color='white')  # Màu của các nhãn giá trị
                    },
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',  # Nền biểu đồ trong suốt
                    paper_bgcolor='rgba(0,0,0,0)',  # Nền tổng thể trong suốt
                    font=dict(color='white')  # Màu của các nhãn khác
                )
            }
        )
    ])
    
    return app
