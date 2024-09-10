import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from components.api import get_weather_data

nlp = spacy.load("en_core_web_sm")

# Tạo một dictionary để lưu tọa độ của các thành phố phổ biến
location_coordinates = {
    "washington": {"latitude": 38.8951, "longitude": -77.0364},
    "ho chi minh": {"latitude": 10.8231, "longitude": 106.6297},
    "hanoi": {"latitude": 21.0285, "longitude": 105.8542},
    "london": {"latitude": 51.5074, "longitude": -0.1278},
    # Thêm các thành phố khác theo nhu cầu
}

user_location_memory = None  # Lưu vị trí người dùng
user_weather_type_memory = None  # Lưu loại thời tiết người dùng

# Hàm để tìm vị trí gần đúng nhất dựa trên Fuzzy Matching
def find_closest_match(input_location, possible_locations):
    best_match = process.extractOne(input_location, possible_locations, scorer=fuzz.ratio)
    if best_match and best_match[1] > 70:  # Ngưỡng tương đồng 70%
        return best_match[0]
    return None

# Phân tích câu hỏi bằng mô hình NLP SpaCy và Fuzzy Matching
def analyze_question(user_input):
    global user_location_memory, user_weather_type_memory
    doc = nlp(user_input.lower())
    location = None
    weather_type = None

    # Xác định địa điểm từ câu hỏi và sử dụng fuzzy matching cho sai chính tả
    possible_locations = list(location_coordinates.keys())
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE là Geopolitical Entity (địa điểm)
            location = find_closest_match(ent.text, possible_locations)
            if location:
                user_location_memory = location  # Cập nhật vị trí vào bộ nhớ khi nhận diện được
                break

    # Nếu không tìm thấy địa điểm từ câu hỏi, dùng địa điểm trong bộ nhớ
    if not location and user_location_memory:
        location = user_location_memory

    # Dựa vào các từ khóa và mô hình phân tích, xác định loại thông tin thời tiết
    if "temperature" in user_input or "hot" in user_input:
        weather_type = "temperature"
    elif "rain" in user_input or "precipitation" in user_input:
        weather_type = "rain"
    elif "humidity" in user_input:
        weather_type = "humidity"
    elif "cloud" in user_input or "cloud cover" in user_input:
        weather_type = "cloudcover"
    elif "weather" in user_input:
        weather_type = "all"

    # Nếu loại thời tiết chưa được xác định, sử dụng từ bộ nhớ
    if not weather_type and user_weather_type_memory:
        weather_type = user_weather_type_memory

    # Ghi nhớ loại thời tiết nếu đã xác định được
    if weather_type:
        user_weather_type_memory = weather_type

    return location, weather_type

# Hàm xử lý và trả lời câu hỏi của người dùng
def get_chatbot_response(user_input):
    location, weather_type = analyze_question(user_input)

    if not location:
        return "Please specify the location you're asking about (e.g., Hanoi, London, Washington)."
    
    if not weather_type:
        return "Please specify what weather information you're asking for (e.g., temperature, rain, cloud cover)."

    coords = location_coordinates.get(location)
    
    # Gọi API để lấy dữ liệu thời tiết
    try:
        weather_data = get_weather_data(coords['latitude'], coords['longitude'])
    except KeyError as e:
        return f"Error fetching weather data: {e}"

    # Trả lời dựa trên loại thông tin yêu cầu
    if weather_type == "temperature":
        temp = weather_data['current_weather']['temperature']
        return f"The current temperature in {location.title()} is {temp}°C."
    elif weather_type == "rain":
        rain_probability = weather_data['daily']['precipitation_probability_max'][0]
        return f"The rain probability today in {location.title()} is {rain_probability}%."
    elif weather_type == "humidity":
        humidity = weather_data['hourly']['relative_humidity_2m'][0]
        return f"The current humidity in {location.title()} is {humidity}%."
    elif weather_type == "cloudcover":
        cloud_cover = weather_data['hourly']['cloudcover'][0]
        return f"The current cloud cover in {location.title()} is {cloud_cover}%."
    elif weather_type == "all":
        temp = weather_data['current_weather']['temperature']
        rain_probability = weather_data['daily']['precipitation_probability_max'][0]
        humidity = weather_data['hourly']['relative_humidity_2m'][0]
        cloud_cover = weather_data['hourly']['cloudcover'][0]
        return (f"The current weather in {location.title()} is as follows:\n"
                f"Temperature: {temp}°C\n"
                f"Rain Probability: {rain_probability}%\n"
                f"Humidity: {humidity}%\n"
                f"Cloud Cover: {cloud_cover}%")

    return "Sorry, I couldn't fetch the specific weather information you asked for."

# Hàm chính để bot xử lý câu hỏi từ người dùng
def process_user_message(user_input):
    return get_chatbot_response(user_input)
