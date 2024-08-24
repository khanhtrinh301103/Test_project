import requests

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "daily": 'rain_sum',
        "timezone": "Asia/Bangkok",
        "past_days": 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Kiểm tra dữ liệu trả về từ API
    print("Toàn bộ dữ liệu:")
    print(data)
    
    # Lấy phần 'time' từ dữ liệu
    time_data = data.get('daily', {}).get('time', [])
    
    print("\nDanh sách thời gian (time):")
    for time in time_data:
        print(time)

    return data

get_weather_data()
