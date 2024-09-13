import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from components.chatbotAPI import get_chatbot_weather_data
import json
import os

nlp = spacy.load("en_core_web_sm")

user_location_memory = None  # Lưu vị trí người dùng
user_weather_type_memory = None  # Lưu loại thời tiết người dùng

# Đường dẫn đến file JSON chứa tọa độ các địa điểm
location_file_path = os.path.join(os.path.dirname(__file__), '../data/location_coordinates.json')

# Đường dẫn đến file JSON chứa câu hỏi và câu trả lời
qa_file_path = os.path.join(os.path.dirname(__file__), '../data/conversation.json')

# Hàm để tải dữ liệu tọa độ từ JSON
def load_location_data():
    try:
        with open(location_file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

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
    weather_types = []

    # Tải danh sách địa điểm từ file JSON
    location_coordinates = load_location_data()

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

    # Dựa vào các từ khóa và mô hình phân tích, xác định nhiều loại thông tin thời tiết
    if "temperature" in user_input or "hot" in user_input:
        weather_types.append("temperature")
    if "rain" in user_input or "precipitation" in user_input:
        weather_types.append("rain")
    if "humidity" in user_input:
        weather_types.append("humidity")
    if "cloud" in user_input or "cloud cover" in user_input:
        weather_types.append("cloudcover")
    if "wind" in user_input:
        weather_types.append("wind")
    if "pressure" in user_input:
        weather_types.append("pressure")
    if "uv" in user_input or "uv index" in user_input:
        weather_types.append("uv_index")
    if "sunrise" in user_input:
        weather_types.append("sunrise")
    if "sunset" in user_input:
        weather_types.append("sunset")
    if "weather" in user_input and not weather_types:  # Nếu người dùng hỏi chung chung về thời tiết
        weather_types.append("all")

    return location, weather_types

# Hàm tìm câu hỏi trong file JSON
def find_question_in_json(user_input):
    try:
        with open(qa_file_path, "r") as file:
            data = json.load(file)
            for qa_pair in data:
                for question in qa_pair["questions"]:
                    if fuzz.ratio(user_input.lower(), question.lower()) > 70:  # Fuzzy matching
                        return qa_pair['weather_type']
    except FileNotFoundError:
        return None
    return None

# Hàm phụ để sinh câu trả lời cho từng loại thông tin
def generate_weather_response(weather_data, location, weather_type):
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
    elif weather_type == "wind":
        wind_speed = weather_data['current_weather']['windspeed']
        return f"The current wind speed in {location.title()} is {wind_speed} km/h."
    elif weather_type == "pressure":
        pressure = weather_data['current_weather']['pressure_msl']
        return f"The current pressure in {location.title()} is {pressure} hPa."
    elif weather_type == "uv_index":
        uv_index = weather_data['current_weather'].get('uv_index', 'No UV data available')
        return f"The UV index today in {location.title()} is {uv_index}."
    elif weather_type == "sunrise":
        sunrise_time = weather_data['daily']['sunrise'][0]
        return f"The sunrise time today in {location.title()} is at {sunrise_time}."
    elif weather_type == "sunset":
        sunset_time = weather_data['daily']['sunset'][0]
        return f"The sunset time today in {location.title()} is at {sunset_time}."
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

# Hàm xử lý và trả lời câu hỏi của người dùng
def get_chatbot_response(user_input):
    location, weather_types = analyze_question(user_input)

    # Nếu không tìm thấy thông tin thời tiết, tìm trong file JSON
    if not location or not weather_types:
        weather_type_from_json = find_question_in_json(user_input)
        if weather_type_from_json:
            weather_types = [weather_type_from_json]

    if not location:
        return "Please specify the location you're asking about (e.g., Hanoi, London, Washington)."
    
    if not weather_types:
        return "Please specify what weather information you're asking for (e.g., temperature, rain, cloud cover)."

    coords = load_location_data().get(location)  # Lấy tọa độ từ JSON

    if not coords:
        return f"Sorry, I could not find the coordinates for {location.title()}."

    # Gọi API mới từ chatbotAPI để lấy dữ liệu thời tiết
    try:
        weather_data = get_chatbot_weather_data(coords['latitude'], coords['longitude'])
    except KeyError as e:
        return f"Error fetching weather data: {e}"

    # Xử lý nhiều loại thông tin thời tiết
    responses = [generate_weather_response(weather_data, location, w_type) for w_type in weather_types]
    
    return " ".join(responses)

# Hàm chính để bot xử lý câu hỏi từ người dùng
def process_user_message(user_input):
    return get_chatbot_response(user_input)
