import requests

def get_current_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.8231,
        "longitude": 106.6297,
        "current_weather": True,
        "timezone": "Asia/Bangkok"
    }
    response = requests.get(url, params=params)
    data = response.json()
    current_weather = data.get('current_weather', {})
    temperature = current_weather.get('temperature', None)
    windspeed = current_weather.get('windspeed', None)
    return temperature, windspeed



def wind_Chill_Index(temperature, windspeed):
    if temperature < 10 and windspeed > 4.8:
        twc = 13.12 + 0.6215 * temperature - 11.37 * windspeed**0.16 + 0.3965 * temperature * windspeed**0.16
        return twc
    else:
        print(temperature)
        print(windspeed)
        return "Không đủ điều kiện tính chỉ số gió lạnh (Nhiệt độ phải dưới 10°C và tốc độ gió trên 4.8 km/h)."

# Sử dụng hàm để lấy dữ liệu thời tiết hiện tại
temperature, windspeed = get_current_weather()
result = wind_Chill_Index(temperature, windspeed)
print(result)
