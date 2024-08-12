from datetime import datetime
from components.probability_prediction import predict_precipitation_probability

def format_current_weather(current_weather, daily_data):
    precipitation_probability = predict_precipitation_probability(daily_data)
    
    # Extract and format sunrise and sunset times
    sunrise_raw = daily_data.get('sunrise', [''])[0]
    sunset_raw = daily_data.get('sunset', [''])[0]
    
    # Format the times to display only hours and minutes
    sunrise_time = datetime.fromisoformat(sunrise_raw).strftime('%H:%M') if sunrise_raw else ''
    sunset_time = datetime.fromisoformat(sunset_raw).strftime('%H:%M') if sunset_raw else ''

    # Get today's date in the desired format
    today_date = datetime.now().strftime('%Y-%m-%d')

    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': sunrise_time,
        'sunset': sunset_time,
        'precipitation_probability': round(precipitation_probability, 2),  # Làm tròn đến 2 chữ số thập phân
        'today_date': today_date  # Add today's date
    }
