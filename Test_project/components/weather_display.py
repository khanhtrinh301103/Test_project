from datetime import datetime
from components.RainProbability import predict_precipitation_probability

def format_current_weather(current_weather, daily_data, hourly_data):
    try:
        # Lấy xác suất mưa cho ngày hôm nay từ mô hình RainProbability
        precipitation_probability_today = predict_precipitation_probability(daily_data, predict_next_14_days=False)
        
        # Nếu kết quả trả về là một danh sách, lấy giá trị đầu tiên
        if isinstance(precipitation_probability_today, list) and precipitation_probability_today:
            precipitation_probability_today = precipitation_probability_today[0]
        else:
            precipitation_probability_today = 0.0  # Gán giá trị mặc định nếu không có dữ liệu hợp lệ
    except Exception as e:
        print(f"Error in precipitation prediction: {e}")
        precipitation_probability_today = 0.0

    try:
        # Lấy và định dạng thời gian bình minh và hoàng hôn
        sunrise_raw = daily_data.get('sunrise', [''])[0]
        sunset_raw = daily_data.get('sunset', [''])[0]
        
        # Định dạng thời gian chỉ hiển thị giờ và phút
        sunrise_time = datetime.fromisoformat(sunrise_raw).strftime('%H:%M') if sunrise_raw else ''
        sunset_time = datetime.fromisoformat(sunset_raw).strftime('%H:%M') if sunset_raw else ''
    except Exception as e:
        print(f"Error in formatting sunrise/sunset times: {e}")
        sunrise_time = ''
        sunset_time = ''

    # Lấy ngày hiện tại với định dạng mong muốn
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Lấy dữ liệu từ hourly_data, kiểm tra sự tồn tại của các trường
    humidity = hourly_data.get('relative_humidity_2m', [''])[0] if 'relative_humidity_2m' in hourly_data else ''
    shower = hourly_data.get('showers', [''])[0] if 'showers' in hourly_data else ''
    precipitation = hourly_data.get('precipitation', [''])[0] if 'precipitation' in hourly_data else ''
    cloud_cover = hourly_data.get('cloudcover', [''])[0] if 'cloudcover' in hourly_data else ''

    # Lấy dữ liệu rain_sum từ daily_data
    rain_sum_today = daily_data.get('rain_sum', [''])[0] if 'rain_sum' in daily_data else ''

    return {
        'temperature': current_weather.get('temperature', ''),
        'weathercode': current_weather.get('weathercode', ''),
        'windspeed': current_weather.get('windspeed', ''),
        'is_day': current_weather.get('is_day', ''),
        'sunrise': sunrise_time,
        'sunset': sunset_time,
        'precipitation_probability': round(precipitation_probability_today, 2),  # Làm tròn giá trị xác suất mưa
        'today_date': today_date,
        'humidity': humidity,
        'showers': shower,
        'precipitation': precipitation,
        'cloud_cover': cloud_cover,
        'rain_sum': rain_sum_today  # Thêm rain_sum vào kết quả trả về
    }
