import requests

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
