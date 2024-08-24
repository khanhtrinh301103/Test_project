import requests

def get_weather_data(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": ["relative_humidity_2m", "precipitation", "showers", "cloudcover"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "sunshine_duration", "precipitation_sum", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "sunrise", "sunset"],
        "timezone": "Asia/Bangkok",
        "past_days": 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'current_weather' not in data or not isinstance(data['current_weather'], dict):
        raise KeyError("API response does not contain valid 'current_weather' data")
    if 'daily' not in data:
        raise KeyError("API response does not contain 'daily' data")
    if 'hourly' not in data:
        raise KeyError("API response does not contain 'hourly' data")

    return data
