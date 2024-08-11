from components.probability_prediction import predict_precipitation_probability

def format_current_weather(current_weather, daily_data):
    if not daily_data:  # Kiểm tra daily_data có tồn tại
        raise ValueError("No daily data available to predict precipitation probability")

    precipitation_probability = predict_precipitation_probability(daily_data)
    
    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': current_weather.get('sunrise', ''),
        'sunset': current_weather.get('sunset', ''),
        'precipitation_probability': precipitation_probability
    }
