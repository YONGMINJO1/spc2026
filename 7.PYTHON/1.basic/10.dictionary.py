students = {
    "민수": 87,
    "지훈": 92,
    "서연": 76,
    "하은": 100,
    "도윤": 64,
    "예준": 55,
    "수빈": 81,
    "지우": 73,
    "유진": 95,
    "현우": 68
}

print(students)

def get_a_student(students):
    a_students = []
    for name, score in students.items():
        if score >= 90:
            a_students.append(name)
    return a_students
    
print(get_a_student(students))