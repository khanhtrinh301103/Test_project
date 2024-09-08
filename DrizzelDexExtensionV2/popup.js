document.addEventListener('DOMContentLoaded', function () {
    const locations = {
        'Ho Chi Minh': {'latitude': 10.8231, 'longitude': 106.6297},
        'Hanoi': {'latitude': 21.0285, 'longitude': 105.8542},
        'Da Nang': {'latitude': 16.0471, 'longitude': 108.2068},
        'Can Tho': {'latitude': 10.0452, 'longitude': 105.7469},
        'Nha Trang': {'latitude': 12.2388, 'longitude': 109.1967}
    };

    function fetchWeather(latitude, longitude) {
        const apiUrl = "https://api.open-meteo.com/v1/forecast";
        const params = new URLSearchParams({
            latitude: latitude,
            longitude: longitude,
            current_weather: true,
            timezone: "Asia/Bangkok",
            hourly: "relative_humidity_2m"
        });

        fetch(`${apiUrl}?${params}`)
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
                    console.log("No 'current_weather' data");
                }
            })
            .catch(error => console.log('Error fetching weather data:', error));
    }

    document.getElementById('location-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn không cho form gửi theo cách mặc định

        const formData = new FormData(this);
        const selectedLocation = formData.get('location'); // Lấy giá trị địa điểm từ form

        if (locations[selectedLocation]) {
            const { latitude, longitude } = locations[selectedLocation];

            // Fetch weather data from Open-Meteo API
            fetchWeather(latitude, longitude);

            // Fetch rain probability from Flask server
            fetch('http://127.0.0.1:5000', {
                method: 'POST',
                body: formData,
                mode: 'cors' 
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                // Xử lý phản hồi từ server
                var parser = new DOMParser();
                var doc = parser.parseFromString(data, 'text/html');
                var rainprobability = doc.querySelector('.rainprobability')?.innerText || 'N/A';

                document.getElementById('rainprobability').innerText = rainprobability;
            })
            .catch(error => {
                console.error('Error fetching rain probability:', error);
                document.getElementById('rainprobability').innerText = 'Rain Probability: Server has been closed';
            });
        } else {
            console.error('Selected location is not valid.');
            document.getElementById('rainprobability').innerText = 'Rain Probability: Error - Invalid location selected';
        }
    });
});