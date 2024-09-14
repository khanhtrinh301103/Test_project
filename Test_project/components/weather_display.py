from datetime import datetime
from components.RainProbability import predict_precipitation_probability

def format_current_weather(current_weather, daily_data, hourly_data):
    # Lấy xác suất mưa cho 14 ngày tới từ hàm predict_precipitation_probability
    precipitation_probabilities = predict_precipitation_probability(daily_data, predict_next_14_days=True)
    
    # Nếu kết quả trả về là một danh sách, bạn có thể lấy giá trị đầu tiên cho ngày hôm nay
    precipitation_probability_today = precipitation_probabilities[0] if precipitation_probabilities else 0
    
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
    cloud_cover = hourly_data.get('cloudcover', [''])[0]  # Đảm bảo tên khóa trùng khớp với dữ liệu API

    # Lấy dữ liệu rain_sum từ daily_data
    rain_sum_today = daily_data.get('rain_sum', [''])[0]

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
        'cloud_cover': cloud_cover,
        'rain_sum': rain_sum_today  # Thêm rain_sum vào kết quả trả về
    }
