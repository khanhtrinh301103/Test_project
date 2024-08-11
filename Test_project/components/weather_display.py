def format_current_weather(current_weather):
    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': current_weather.get('sunrise', ''),
        'sunset': current_weather.get('sunset', ''),
        'precipitation_probability': current_weather.get('precipitation_probability', '')
    }
