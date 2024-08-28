from datetime import datetime
from components.RainProbability import predict_precipitation_probability

def format_current_weather(current_weather, daily_data, hourly_data):
    # Giả sử bạn chỉ muốn lấy xác suất mưa cho ngày hôm nay
    precipitation_probability_today = predict_precipitation_probability(daily_data, predict_next_14_days=False)
    
    # Nếu kết quả trả về là một danh sách, bạn có thể lấy giá trị đầu tiên
    if isinstance(precipitation_probability_today, list):
        precipitation_probability_today = precipitation_probability_today[0]
    
    # Extract and format sunrise and sunset times
    sunrise_raw = daily_data.get('sunrise', [''])[0]
    sunset_raw = daily_data.get('sunset', [''])[0]
    
    # Format the times to display only hours and minutes
    sunrise_time = datetime.fromisoformat(sunrise_raw).strftime('%H:%M') if sunrise_raw else ''
    sunset_time = datetime.fromisoformat(sunset_raw).strftime('%H:%M') if sunset_raw else ''

    # Get today's date in the desired format
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Lấy dữ liệu từ hourly_data
    humidity = hourly_data.get('relative_humidity_2m', [''])[0]
    shower = hourly_data.get('showers', [''])[0]
    precipitation = hourly_data.get('precipitation', [''])[0]
    cloud_cover = hourly_data.get('cloudcover', [''])[0]

    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': sunrise_time,
        'sunset': sunset_time,
        'precipitation_probability': round(precipitation_probability_today, 2),  # Chỉ làm tròn giá trị của ngày hôm nay
        'today_date': today_date,
        'humidity': humidity,
        'showers': shower,
        'precipitation': precipitation,
        'cloud_cover': cloud_cover
    }
