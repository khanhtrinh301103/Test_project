document.addEventListener('DOMContentLoaded', function () {
    const locations = {
        'Ho Chi Minh': {'latitude': 10.8231, 'longitude': 106.6297},
        'Hanoi': {'latitude': 21.0285, 'longitude': 105.8542},
        'Da Nang': {'latitude': 16.0471, 'longitude': 108.2068},
        'Can Tho': {'latitude': 10.0452, 'longitude': 105.7469},
        'Nha Trang': {'latitude': 12.2388, 'longitude': 109.1967}
    };

    const locationSelect = document.getElementById('location-select');

    function fetchWeather(latitude, longitude) {
        const apiUrl = "https://api.open-meteo.com/v1/forecast";
        const params = {
            latitude: latitude,
            longitude: longitude,
            current_weather: true,
            timezone: "Asia/Bangkok",
            hourly: "relative_humidity_2m" //lấy humidity do humidity ở current weather bị undefined
        };

        fetch(`${apiUrl}?latitude=${params.latitude}&longitude=${params.longitude}&current_weather=${params.current_weather}&timezone=${params.timezone}&hourly=${params.hourly}`)
            .then(response => response.json())
            .then(data => {
                if (data.current_weather) {
                    document.getElementById('temperature').textContent = `Temperature: ${data.current_weather.temperature}°C`;
                    document.getElementById('windspeed').textContent = `Windspeed: ${data.current_weather.windspeed} km/h`;
                    document.getElementById('weathercode').textContent = `Weather Code: ${data.current_weather.weathercode}`;
                    
                    const humidity = data.hourly.relative_humidity_2m[0];
                    document.getElementById('humidity').textContent = `Relative Humidity: ${humidity}%`;
                    
                    document.getElementById('daynight').textContent = `Day/Night: ${data.current_weather.is_day ? 'Day' : 'Night'}`;
                } else {
                    console.log("Không có dữ liệu 'current_weather'");
                }
            })
            .catch(error => console.log('Error fetching weather data:', error));
    }

    // Hồ chí Minh sẽ là mặc định
    fetchWeather(locations['Ho Chi Minh'].latitude, locations['Ho Chi Minh'].longitude);

    // thay đổi theo select người dùng
    locationSelect.addEventListener('change', function () {
        const selectedLocation = locationSelect.value;
        const { latitude, longitude } = locations[selectedLocation];
        fetchWeather(latitude, longitude);
    });
});
