import requests

def get_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ['rain_sum', 'temperature_2m_max'],
        "timezone": "Asia/Bangkok",
        "past_days": 60
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract 'time', 'rain_sum', and 'temperature_2m_max' from the data
    time_data = data.get('daily', {}).get('time', [])
    rain_sum_data = data.get('daily', {}).get('rain_sum', [])
    temperature_max_data = data.get('daily', {}).get('temperature_2m_max', [])
    
    return time_data, rain_sum_data, temperature_max_data
