import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from components.chatbotAPI import get_chatbot_weather_data
import json
import os

nlp = spacy.load("en_core_web_sm")

user_location_memory = None  # Lưu vị trí người dùng
user_weather_type_memory = None  # Lưu loại thời tiết người dùng
suggested_locations = None  # Lưu các gợi ý đã cung cấp cho người dùng
previous_weather_types = None  # Lưu từ khóa thời tiết của câu hỏi ban đầu

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

# Hàm để tìm vị trí gần đúng nhất dựa trên Fuzzy Matching và cung cấp gợi ý
def find_closest_match(input_location, possible_locations):
    print(f"Input location: {input_location}")  # Debug đầu vào fuzzy matching
    input_location = input_location.strip().lower()  # Chuẩn hóa chuỗi thành chữ thường và loại bỏ khoảng trắng
    possible_locations = [loc.strip().lower() for loc in possible_locations]  # Chuẩn hóa danh sách địa điểm
    matches = process.extract(input_location, possible_locations, scorer=fuzz.ratio, limit=5)
    
    # Nếu không có kết quả khớp nào có điểm trên 70%
    if not matches or matches[0][1] < 70:
        return None, matches  # Trả về danh sách gợi ý
    return matches[0][0], None  # Trả về địa danh khớp nhất và không có gợi ý

# Phân tích câu hỏi bằng mô hình NLP SpaCy và Fuzzy Matching
def analyze_question(user_input):
    global user_location_memory, user_weather_type_memory, suggested_locations, previous_weather_types
    doc = nlp(user_input.lower())
    locations = []  # Lưu tất cả các location
    weather_types = []
    suggestions = None

    # Tải danh sách địa điểm từ file JSON
    location_coordinates = load_location_data()
    possible_locations = list(location_coordinates.keys())

    # Xác định từ khoá thời tiết
    weather_keywords = {
        "temperature": ["temperature", "hot"],
        "rain": ["rain", "precipitation"],
        "humidity": ["humidity"],
        "cloudcover": ["cloud", "cloud cover"],
        "wind": ["wind"],
        "pressure": ["pressure"],
        "uv_index": ["uv", "uv index"],
        "sunrise": ["sunrise"],
        "sunset": ["sunset"],
        "all": ["weather"]
    }

    # Lặp qua các từ khóa thời tiết và thêm vào weather_types nếu có
    for weather_type, keywords in weather_keywords.items():
        for keyword in keywords:
            if keyword in user_input:
                weather_types.append(weather_type)

    # Nếu tìm thấy từ khóa thời tiết, lưu chúng lại
    if weather_types:
        previous_weather_types = weather_types

    # Loại bỏ các từ khóa thời tiết khỏi user_input để tìm địa danh
    for keyword in sum(weather_keywords.values(), []):  # Flatten các từ khóa
        user_input = user_input.replace(keyword, "").strip()

    # Loại bỏ các từ chung chung như "what is the weather in"
    user_input = user_input.replace("what is the weather in", "").strip()

    print(f"User input after removing weather keywords: {user_input}")  # Debug

    # Kiểm tra xem người dùng có chọn gợi ý từ danh sách trước đó không
    if suggested_locations:
        if user_input.strip().lower() in [loc.lower() for loc, _ in suggested_locations]:
            print(f"User selected a suggestion: {user_input}")
            return [user_input], previous_weather_types, None  # Trả về địa danh từ gợi ý đã chọn

    # Sử dụng fuzzy matching cho cả cụm từ địa danh
    fuzzy_location, suggestions = find_closest_match(user_input, possible_locations)
    if fuzzy_location:
        locations.append(fuzzy_location)
        user_location_memory = fuzzy_location  # Lưu vào bộ nhớ

    # Nếu không tìm thấy địa điểm, dùng bộ nhớ
    if not locations and user_location_memory:
        locations.append(user_location_memory)

    suggested_locations = suggestions  # Lưu lại danh sách gợi ý cho lần sau

    print(f"Final detected locations: {locations}, Weather types: {weather_types}")  # Debug final location and weather types

    return locations, weather_types, suggestions

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
def generate_weather_response(weather_data, location, weather_types):
    responses = []
    
    if "all" in weather_types or not weather_types:
        # Nếu người dùng hỏi chung chung về thời tiết ("weather"), trả về thông tin tổng quát
        temp = weather_data['current_weather']['temperature']
        rain_probability = weather_data['daily']['precipitation_probability_max'][0]
        humidity = weather_data['hourly']['relative_humidity_2m'][0]
        wind_speed = weather_data['current_weather']['windspeed']
        
        responses.append(f"The current weather in {location.title()} is as follows:")
        responses.append(f"- Temperature: {temp}°C")
        responses.append(f"- Rain Probability: {rain_probability}%")
        responses.append(f"- Humidity: {humidity}%")
        responses.append(f"- Wind Speed: {wind_speed} km/h")
        return "\n".join(responses)

    # Nếu không phải chỉ hỏi chung chung mà có các từ khóa thời tiết cụ thể
    for weather_type in weather_types:
        if weather_type == "temperature":
            temp = weather_data['current_weather']['temperature']
            responses.append(f"The current temperature in {location.title()} is {temp}°C.")
        elif weather_type == "rain":
            rain_probability = weather_data['daily']['precipitation_probability_max'][0]
            responses.append(f"The rain probability today in {location.title()} is {rain_probability}%.")
        elif weather_type == "humidity":
            humidity = weather_data['hourly']['relative_humidity_2m'][0]
            responses.append(f"The current humidity in {location.title()} is {humidity}%.")
        elif weather_type == "cloudcover":
            cloud_cover = weather_data['hourly']['cloudcover'][0]
            responses.append(f"The current cloud cover in {location.title()} is {cloud_cover}%.")
        elif weather_type == "wind":
            wind_speed = weather_data['current_weather']['windspeed']
            responses.append(f"The current wind speed in {location.title()} is {wind_speed} km/h.")
        elif weather_type == "pressure":
            pressure = weather_data['current_weather']['pressure_msl']
            responses.append(f"The current pressure in {location.title()} is {pressure} hPa.")
        elif weather_type == "uv_index":
            uv_index = weather_data['current_weather'].get('uv_index', 'No UV data available')
            responses.append(f"The UV index today in {location.title()} is {uv_index}.")
        elif weather_type == "sunrise":
            sunrise_time = weather_data['daily']['sunrise'][0]
            responses.append(f"The sunrise time today in {location.title()} is at {sunrise_time}.")
        elif weather_type == "sunset":
            sunset_time = weather_data['daily']['sunset'][0]
            responses.append(f"The sunset time today in {location.title()} is at {sunset_time}.")
    
    return " ".join(responses)

# Hàm xử lý và trả lời câu hỏi của người dùng
def get_chatbot_response(user_input):
    locations, weather_types, suggestions = analyze_question(user_input)

    # Nếu có gợi ý, trả về gợi ý cho người dùng
    if suggestions:
        suggestion_list = ", ".join([f"{loc} (score: {score})" for loc, score in suggestions])
        return f"Did you mean one of these locations? {suggestion_list}"

    responses = []
    for location in locations:
        coords = load_location_data().get(location)
        if coords:
            try:
                weather_data = get_chatbot_weather_data(coords['latitude'], coords['longitude'])
                responses.append(generate_weather_response(weather_data, location, weather_types))
            except KeyError as e:
                responses.append(f"Error fetching weather data for {location.title()}: {e}")
        else:
            responses.append(f"Sorry, I could not find the coordinates for {location.title()}.")

    return " ".join(responses)

# Hàm chính để bot xử lý câu hỏi từ người dùng
def process_user_message(user_input):
    return get_chatbot_response(user_input)
