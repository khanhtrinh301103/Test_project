from components.probability_prediction import predict_precipitation_probability

def format_current_weather(current_weather, daily_data):
    precipitation_probability = predict_precipitation_probability(daily_data)
    
    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': current_weather.get('sunrise', ''),
        'sunset': current_weather.get('sunset', ''),
        'precipitation_probability': round(precipitation_probability, 2)  # Làm tròn đến 2 chữ số thập phân
    }
