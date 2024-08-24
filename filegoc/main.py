from api import get_weather_data
from chart import daily_temperature_chart

# Lấy dữ liệu thời tiết từ API
time_data, rain_sum_data, temperature_max_data = get_weather_data()

# Tạo ứng dụng Dash với biểu đồ
app = daily_temperature_chart(time_data, rain_sum_data, temperature_max_data)

# Chạy ứng dụng Dash
if __name__ == '__main__':
    app.run_server(debug=True)