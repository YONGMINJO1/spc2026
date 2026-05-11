users = [
    {"name": "김민수", "age": 25, "location": "서울", "car": "Hyundai Avante"},
    {"name": "이지훈", "age": 31, "location": "부산", "car": "Kia K5"},
    {"name": "박서연", "age": 22, "location": "인천", "car": "Tesla Model 3"},
    {"name": "문하은", "age": 28, "location": "대구", "car": "BMW 320i"},
    {"name": "김도윤", "age": 35, "location": "광주", "car": "Genesis G80"},
    {"name": "이예준", "age": 27, "location": "대전", "car": "Hyundai Sonata"},
    {"name": "박수빈", "age": 24, "location": "울산", "car": "Kia Sportage"},
    {"name": "문지우", "age": 30, "location": "수원", "car": "Audi A6"},
    {"name": "김유진", "age": 26, "location": "성남", "car": "Mercedes-Benz C-Class"},
    {"name": "이현우", "age": 33, "location": "고양", "car": "Tesla Model Y"}
]

print(users)
print("--"*30)

def find_user_and_print(name):
    for user in users:
        if user['name'] == name:
            print(user)

find_user_and_print("김")
find_user_and_print("문")
