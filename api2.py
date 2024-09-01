import requests

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "current_weather": True,
        "hourly": ["temperature_2m", "wind_speed_10m"],  # Danh sách tham số
        "daily": ["temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max"],  # Danh sách tham số
        "timezone": "Asia/Bangkok",
        "past_days": 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'current_weather' not in data:
        print("Không có dữ liệu 'current_weather'")
    if 'hourly' not in data:
        print("Không có dữ liệu 'hourly'")
    if 'daily' not in data:
        print("Không có dữ liệu 'daily'")

    return data

data = get_weather_data()

# In dữ liệu trả về để kiểm tra
print("Dữ liệu trả về từ API:")


def wind_chill_hourly_index(data):
    hourly_data = data.get("hourly", {})
    time_data = hourly_data.get("time", [])
    temperature_data = hourly_data.get("temperature_2m", [])
    windspeed_data = hourly_data.get("wind_speed_10m", [])
    twc_dict = {}

    if not time_data:
        print("Không có dữ liệu thời gian")
        return twc_dict  # Trả về từ điển rỗng nếu không có dữ liệu thời gian

    for i in range(len(time_data)):
        # In các giá trị để kiểm tra điều kiện
        print(f"Thời gian: {time_data[i]}, Nhiệt độ: {temperature_data[i]}, Tốc độ gió: {windspeed_data[i]}")
        
        # Kiểm tra điều kiện cho nhiệt độ và tốc độ gió
        if temperature_data[i] < 10 and windspeed_data[i] > 4.8:
            # Tính toán chỉ số lạnh gió (wind chill index)
            twc = (13.12 + 0.6215 * temperature_data[i] - 
                   11.37 * windspeed_data[i]**0.16 + 
                   0.3965 * temperature_data[i] * windspeed_data[i]**0.16)
            twc_dict[time_data[i]] = twc

    return twc_dict

twc_dict = wind_chill_hourly_index(data)
print(twc_dict)