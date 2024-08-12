import requests

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "current_weather": "true",
        "daily": ["temperature_2m_max", "temperature_2m_min", "sunshine_duration", "precipitation_sum", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "sunrise", "sunset"],
        "timezone": "Asia/Bangkok",
        "past_days": 60  # Dữ liệu 60 ngày qua để huấn luyện mô hình
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    print(data)  # Kiểm tra dữ liệu trả về từ API
    
    # Kiểm tra nếu 'daily' có trong dữ liệu phản hồi
    if 'daily' not in data:
        raise KeyError("API response does not contain 'daily' data")

    return data
