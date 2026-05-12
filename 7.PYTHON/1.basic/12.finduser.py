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
    {"name": "이현우", "age": 33, "location": "고양", "car": "Tesla Model Y"},
]

print(users)
print("--" * 30)


def find_user_and_print(name):
    for user in users:
        # if user['name'] == name:
        if user["name"].startswith(name):
            print(user)


find_user_and_print("김")
find_user_and_print("문")

print("--" * 30)


def find_user_and_return(name):
    found = []  # 찾은 사용자를 담을 바구니 (리스트 변수)

    for user in users:
        if user["name"].startswith(name):
            found.append(user)

    return found


# found_users = find_user_and_return("김")
# found_users = find_user_and_return("오")
found_user = find_user_and_return("구")
print("찾은 사용자:", found_user)

print("-" * 30)


def find_users2(name=None, age=None):
    """이름 또는 나이를 입력받아 매칭되는 사람을 반환한다"""
    found = []

    for user in users:
        if name is not None and age is not None:
            if user["name"] == name and user["age"] == age:
                found.append(user)
        elif name is not None:
            if user["name"] == name:
                found.append(user)
        elif age is not None:
            if user["age"] == age:
                found.append(user)
    return found


print("-" * 30)


def find_users2_better(name=None, age=None, location=None):
    """이름 또는 나이를 받아 입력받아 매칭되는 사람을 반환한다."""
    found = []
    for user in users:
        # true or 비교문
        if (
            (name is None or user["name"] == name)
            and (age is None or user["age"] == age)
            and (location is None or user["location"] == location)
        ):
            found.append(user)
    return found


# print (find_users2_better("김민준"))
# print (find_users2_better("김민준"))
print(find_users2_better("김민준", 25, "서울"))
# print (find_users2_better(age=25))

print("-" * 30)

search_condition1 = {"name": "김민준"}
search_condition2 = {"name": "김민준", "age": 25}
search_condition3 = {"age": 25}
search_condition3 = {"min_age": 25}

# def find_users2_best(condition):
#     found = []
#     for user in users:
#         if user.get("name") == condition.get("name", "") and \
#         user.get("age") >= condition.get("min_age", 0) and \
#         user.get("location") == condition.get("location", ""):
#         found.append(user)
#     return found

# print(find_users2_best(search_condition1))
